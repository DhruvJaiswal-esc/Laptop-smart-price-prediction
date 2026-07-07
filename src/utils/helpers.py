import numpy as np


# =====================================================
# LOG TRANSFORM HELPERS
# =====================================================

def log_transform(values):

    return np.log1p(values)


def inverse_log_transform(values):

    return np.expm1(values)


# =====================================================
# FEATURE ENGINEERING HELPERS
# =====================================================

def create_cpu_gpu_combo(
    cpu_tier,
    gpu_tier
):

    return (
        str(cpu_tier)
        + "_"
        + str(gpu_tier)
    )


# =====================================================
# DISPLAY HELPERS
# =====================================================

def print_separator():

    print(
        "\n" + "=" * 50 + "\n"
    )


def print_heading(title):

    print_separator()

    print(title.upper())

    print_separator()