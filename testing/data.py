import pandas as pd

# =====================================================
# LOAD DATASET
# =====================================================

df = pd.read_csv("laptop_dataset_with_tiers.csv")

# =====================================================
# PROCESSOR SEGMENT
# =====================================================

def get_processor_segment(cpu):

    cpu = str(cpu).upper()

    priority_order = [
        "HX",
        "HQ",
        "HK",
        "HS",
        "U",
        "P",
        "H",
        "G7",
        "G4",
        "G1",
        "G"
    ]

    for segment in priority_order:
        if segment in cpu:
            return segment

    return "Other"

# =====================================================
# GPU BRAND
# =====================================================

def get_gpu_brand(gpu):

    gpu = str(gpu).upper()

    # NVIDIA
    if any(x in gpu for x in [
        "RTX",
        "GTX",
        "MX",
        "QUADRO",
        "NVIDIA"
    ]):
        return "NVIDIA"

    # AMD
    if any(x in gpu for x in [
        "RADEON",
        "VEGA",
        "RX "
    ]):
        return "AMD"

    # Intel
    if any(x in gpu for x in [
        "IRIS",
        "UHD",
        "HD GRAPHICS",
        "INTEL ARC"
    ]):
        return "Intel"

    # Apple
    if "APPLE" in gpu:
        return "Apple"

    # Qualcomm
    if any(x in gpu for x in [
        "ADRENO",
        "SNAPDRAGON"
    ]):
        return "Qualcomm"

    # ARM
    if "MALI" in gpu:
        return "ARM"

    return "Other"

# =====================================================
# ADD NEW FEATURES
# =====================================================

df["Processor Segment"] = df["Processor"].apply(
    get_processor_segment
)

df["GPU Brand"] = df["Graphic Processor"].apply(
    get_gpu_brand
)

# =====================================================
# SAVE
# =====================================================

output_file = "laptop_dataset_enhanced.csv"

df.to_csv(
    output_file,
    index=False
)
df["CPU_GPU_Combo"] = (
    df["Processor Tier"].astype(str)
    + "_"
    + df["GPU Tier"].astype(str)
)

print("\n========== PROCESSOR SEGMENTS ==========")
print(df["Processor Segment"].value_counts())

print("\n========== GPU BRANDS ==========")
print(df["GPU Brand"].value_counts())

print(f"\nSaved as: {output_file}")