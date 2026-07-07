from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report
)


def evaluate_classification(
    y_true,
    y_pred
):

    metrics = {

        "Accuracy":
        round(
            accuracy_score(
                y_true,
                y_pred
            ),
            4
        ),

        "Precision":
        round(
            precision_score(
                y_true,
                y_pred,
                average="weighted"
            ),
            4
        ),

        "Recall":
        round(
            recall_score(
                y_true,
                y_pred,
                average="weighted"
            ),
            4
        ),

        "F1":
        round(
            f1_score(
                y_true,
                y_pred,
                average="weighted"
            ),
            4
        )
    }

    return metrics


def print_report(
    y_true,
    y_pred
):

    print(
        classification_report(
            y_true,
            y_pred
        )
    )