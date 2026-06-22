"""
test_thermochemistry.py

Validates that get_combustion_properties() returns correct values for
LOX/RP-1 by comparing against the source CEA table at known O/F points.

Tolerance: exact match at table nodes (interpolation should be exact there).
"""

import pytest
from src.thermochemistry import get_combustion_properties


# Ground truth directly from your RPA sweep.
# List of tuples: (of_ratio, expected_Tc, expected_gamma, expected_Mmol)
LOX_RP1_TABLE = [
    (2.00, 3284.9177, 1.1827, 20.7375),
    (2.25, 3466.1841, 1.1761, 21.9373),
    (2.50, 3552.2443, 1.1816, 22.9241),
    (2.75, 3586.1270, 1.1877, 23.7541),
    (3.00, 3593.2163, 1.1908, 24.4723),
    (3.25, 3585.9737, 1.1911, 25.1068),
    (3.50, 3570.5588, 1.1896, 25.6748),
]


# pytest.mark.parametrize runs this test once per row in LOX_RP1_TABLE.
# The variable names on the left match the tuple positions on the right.
@pytest.mark.parametrize("of, Tc_ref, gamma_ref, Mmol_ref", LOX_RP1_TABLE)
def test_loxrp1_table_nodes(of, Tc_ref, gamma_ref, Mmol_ref):
    """At table nodes, interpolation must return exact CEA values."""
    props = get_combustion_properties(of_ratio=of, propellant="lox_rp1")

    # abs=0.01 means tolerance of 0.01 K on Tc — tight, as expected at a node
    assert props["Tc"]    == pytest.approx(Tc_ref,    abs=0.01),  f"Tc mismatch at O/F={of}"
    assert props["gamma"] == pytest.approx(gamma_ref, abs=0.0001), f"gamma mismatch at O/F={of}"
    assert props["Mmol"]  == pytest.approx(Mmol_ref,  abs=0.001),  f"Mmol mismatch at O/F={of}"


def test_extrapolation_blocked_low():
    """Query below O/F range must raise ValueError."""
    with pytest.raises(ValueError):
        get_combustion_properties(of_ratio=1.5, propellant="lox_rp1")


def test_extrapolation_blocked_high():
    """Query above O/F range must raise ValueError."""
    with pytest.raises(ValueError):
        get_combustion_properties(of_ratio=4.0, propellant="lox_rp1")