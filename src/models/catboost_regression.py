import pandas as pd
import numpy as np
import joblib
import optuna
from optuna.samplers import TPESampler
from optuna.pruners import MedianPruner

from catboost import CatBoostRegressor, Pool

from sklearn.model_selection import train_test_split, KFold
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

optuna.logging.set_verbosity(optuna.logging.WARNING)

# =====================================================
# LOAD DATA
# =====================================================

df = pd.read_csv("laptop_dataset_with_tiers.csv")

# =====================================================
# FEATURES / TARGET
# =====================================================

X = df.drop("Price (Rs)", axis=1)
y = np.log1p(df["Price (Rs)"])

# =====================================================
# CATEGORICAL FEATURES
# =====================================================

cat_features = [
    "Brand", "Processor", "Graphic Processor", "Processor Tier",
    "GPU Tier", "RAM Type", "SSD Type", "Wi-Fi Version",
    "Bluetooth Version", "Battery Type", "Category"
]

for col in cat_features:
    X[col] = X[col].astype(str)

# =====================================================
# TRAIN TEST SPLIT
# =====================================================

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =====================================================
# CAT FEATURE INDICES
# =====================================================

cat_feature_indices = [
    X_train.columns.get_loc(col) for col in cat_features
]

# =====================================================
# [S1 FIX] PRE-BUILD ALL FOLD POOLS ONCE
# Pool construction (Pandas → CatBoost internal format) is
# expensive. Previously done 5×100 = 500 times inside the
# objective. Now done exactly 5 times total, here.
# =====================================================

kf = KFold(n_splits=5, shuffle=True, random_state=42)
fold_data = []

print("Pre-building fold pools...")
for train_idx, valid_idx in kf.split(X_train):
    X_tr  = X_train.iloc[train_idx]
    X_val = X_train.iloc[valid_idx]
    y_tr  = y_train.iloc[train_idx]
    y_val = y_train.iloc[valid_idx]

    train_pool = Pool(X_tr, y_tr, cat_features=cat_feature_indices)
    valid_pool = Pool(X_val, y_val, cat_features=cat_feature_indices)

    fold_data.append((train_pool, valid_pool, y_val))

print("Fold pools ready.\n")

# =====================================================
# OPTUNA OBJECTIVE
# =====================================================

def objective(trial):

    params = {
        # ── Existing params (with fixes) ──────────────────────────────────
        "iterations"    : trial.suggest_int(  "iterations",    1000, 5000),
        "depth"         : trial.suggest_int(  "depth",         4, 10),          # [R4] was max 8
        "learning_rate" : trial.suggest_float("learning_rate", 0.01, 0.2, log=True),
        "l2_leaf_reg"   : trial.suggest_float("l2_leaf_reg",   1e-2, 20, log=True),  # [R3] log scale

        # ── New search parameters ──────────────────────────────────────────
        # [R2] These four together are some of the highest-impact regularisation
        # knobs CatBoost exposes and were completely absent before.
        "subsample"         : trial.suggest_float("subsample",         0.5, 1.0),
        "random_strength"   : trial.suggest_float("random_strength",   1e-9, 10, log=True),
        "min_data_in_leaf"  : trial.suggest_int(  "min_data_in_leaf",  1, 50),

        # ── Fixed accuracy improvements ────────────────────────────────────
        # [R1] max_ctr_complexity=1 banned ALL categorical combinations.
        # =2 lets CatBoost build statistics over pairs like Brand×GPU_Tier.
        # This is the single biggest accuracy change for a dataset with 11 cat features.
        "max_ctr_complexity": 2,

        # [R5] 64 is below the GPU default of 128 — coarser split candidates.
        "border_count"      : 128,

        # Required so `subsample` is respected on GPU (Poisson is GPU-only).
        "bootstrap_type"    : "Bernoulli",

        # [S4] Plain is explicitly faster on GPU; Ordered needs more memory + compute.
        "boosting_type"     : "Plain",

        # [R7] Align early stopping with the CV objective metric.
        "eval_metric"       : "RMSE",

        "loss_function"     : "RMSE",
        "random_seed"       : 42,
        "task_type"         : "GPU",
        "devices"           : "0",
        "verbose"           : False
    }

    scores = []

    for fold_idx, (train_pool, valid_pool, y_val) in enumerate(fold_data):

        model = CatBoostRegressor(**params)
        model.fit(
            train_pool,
            eval_set=valid_pool,
            early_stopping_rounds=50,   # [R6] was 30 — less aggressive
            verbose=False
        )

        pred  = model.predict(valid_pool)
        score = r2_score(y_val, pred)
        scores.append(score)

        # [S2] Report after every fold so MedianPruner can kill bad trials
        # before they waste time running all 5 folds.
        trial.report(np.mean(scores), fold_idx)
        if trial.should_prune():
            raise optuna.exceptions.TrialPruned()

    return np.mean(scores)

# =====================================================
# OPTUNA STUDY
# =====================================================

# [S3] multivariate=True: TPE learns that e.g. deep trees need
#      lower learning rates — better combos found per trial budget.
sampler = TPESampler(multivariate=True, seed=42)

# [S2] MedianPruner: after ≥10 completed trials exist, any new trial
#      whose score after fold K is below the median of other trials
#      at fold K gets killed immediately.
pruner = MedianPruner(
    n_startup_trials=10,   # Don't prune until 10 full baselines exist
    n_warmup_steps=2,      # Need ≥2 fold reports before pruning
    interval_steps=1
)

study = optuna.create_study(
    direction="maximize",
    sampler=sampler,
    pruner=pruner
)

study.optimize(
    objective,
    n_trials=100,
    n_jobs=1,
    show_progress_bar=True
)

# =====================================================
# [R8] DETERMINE OPTIMAL ITERATIONS FOR THE FINAL MODEL
#
# best_params["iterations"] includes early-stopping headroom.
# Without a validation set on the final fit the model would
# train into that headroom and overfit.
# Fix: re-run best config on each fold with early stopping,
# average the best_iteration_, and use that exact count.
# =====================================================

print("\nDetermining optimal iteration count for final model...")

FIXED_PARAMS = dict(
    border_count      = 128,
    max_ctr_complexity= 2,
    bootstrap_type    = "Bernoulli",
    boosting_type     = "Plain",
    eval_metric       = "RMSE",
    loss_function     = "RMSE",
    random_seed       = 42,
    task_type         = "GPU",
    devices           = "0",
    verbose           = False
)

best_iters = []
for train_pool, valid_pool, _ in fold_data:
    probe = CatBoostRegressor(**study.best_params, **FIXED_PARAMS)
    probe.fit(train_pool, eval_set=valid_pool, early_stopping_rounds=50, verbose=False)
    best_iters.append(probe.best_iteration_)

avg_best_iter = int(np.mean(best_iters))
print(f"Per-fold best iterations : {best_iters}")
print(f"Average best iteration   : {avg_best_iter}")

# =====================================================
# FINAL MODEL
# Overwrite iterations with the calibrated count.
# No early stopping needed — we already know the target.
# =====================================================

full_train_pool = Pool(X_train, y_train, cat_features=cat_feature_indices)

final_params = {**study.best_params, "iterations": avg_best_iter}

best_model = CatBoostRegressor(
    **final_params,
    **{k: v for k, v in FIXED_PARAMS.items() if k != "verbose"},
    verbose=100
)

best_model.fit(full_train_pool)

# =====================================================
# SAVE MODEL
# =====================================================

joblib.dump(best_model, "trained_models/regression/catboost.pkl")

# =====================================================
# PREDICTIONS
# =====================================================

pred_log = best_model.predict(X_test)
pred     = np.expm1(pred_log)
actual   = np.expm1(y_test)

# =====================================================
# METRICS
# =====================================================

mae  = mean_absolute_error(actual, pred)
rmse = np.sqrt(mean_squared_error(actual, pred))
r2   = r2_score(actual, pred)

# =====================================================
# RESULTS
# =====================================================

print("\n========== CATBOOST RESULTS ==========")

print("\nBest Parameters:")
print(study.best_params)

print(f"\nBest CV R²            : {study.best_value:.4f}")
print(f"Avg best iteration    : {avg_best_iter}")

pruned = len([t for t in study.trials if t.state == optuna.trial.TrialState.PRUNED])
print(f"Trials pruned early   : {pruned} / 100")

print(f"\nMAE  : {mae:,.2f}")
print(f"RMSE : {rmse:,.2f}")
print(f"R²   : {r2:.4f}")

print("\nSaved: catboost_model_gpu_claude.pkl")
