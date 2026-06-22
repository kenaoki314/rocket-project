"""
thermochemistry.py

Provides combustion property lookups (Tc, gamma, Mmol) as a function of
O/F ratio by linear interpolation from tabulated NASA CEA data.

No chemical equilibrium solver is implemented. All thermochemistry comes
from pre-computed CEA outputs stored in data/. This is a hard constraint.

Supported propellant combinations:
    - lox_rp1  : LOX (90 K) / RP-1 (293 K), Pc = 3.45 MPa, shifting eq.

Author : Ken Aoki
Project: LRE Sizing Tool — Phase 1
"""

# --- Imports ---
# numpy: numerical arrays and interpolation
# pathlib: cross-platform file path handling (better than raw strings)
import numpy as np
from pathlib import Path


# --- Constants ---
# Path to the data directory, relative to this file's location.
# __file__ is a Python built-in that holds the path to the current script.
# .parent gives you the directory containing it (src/).
# Then we go up one level (.parent again) to reach the project root,
# then down into data/.
DATA_DIR = Path(__file__).parent.parent / "data"


def load_cea_table(propellant: str) -> dict:
    """
    Load a CEA data table from CSV and return it as a dictionary of arrays.

    Parameters
    ----------
    propellant : str
        Propellant key. Currently supported: 'lox_rp1'

    Returns
    -------
    dict with keys:
        'of'    : np.ndarray — O/F ratio values (dimensionless)
        'Tc'    : np.ndarray — Chamber temperature (K)
        'gamma' : np.ndarray — Specific heat ratio (dimensionless)
        'Mmol'  : np.ndarray — Mean molecular weight (kg/kmol)

    Raises
    ------
    ValueError if propellant string is not recognized.
    FileNotFoundError if the CSV does not exist at the expected path.
    """

    # Map propellant name to filename
    # This dict maps string keys to filenames.
    # Syntax: {key: value, key: value}
    file_map = {
        "lox_rp1": "cea_loxrp1.csv",
    }

    # Check that the propellant is in our map
    # 'in' tests dictionary key membership
    if propellant not in file_map:
        raise ValueError(
            f"Unknown propellant '{propellant}'. "
            f"Supported options: {list(file_map.keys())}"
        )

    csv_path = DATA_DIR / file_map[propellant]

    # np.genfromtxt reads CSV into a structured numpy array.
    # delimiter=',' tells it columns are comma-separated.
    # names=True reads the first row as column names.
    # dtype=None lets numpy infer float vs int automatically.
    # encoding=None avoids byte-string issues on Windows.
    raw = np.genfromtxt(csv_path, delimiter=",", names=True, dtype=None, encoding=None)

    # raw is a structured array. Access columns by name.
    # We convert to plain float64 arrays for use with np.interp.
    return {
        "of":    raw["of_ratio"].astype(float),
        "Tc":    raw["Tc_K"].astype(float),
        "gamma": raw["gamma"].astype(float),
        "Mmol":  raw["Mmol_kg_kmol"].astype(float),
    }


def get_combustion_properties(of_ratio: float, propellant: str = "lox_rp1") -> dict:
    """
    Return interpolated combustion properties at a given O/F ratio.

    Physics
    -------
    Linear interpolation between adjacent CEA table entries:

        f(x) = f(x0) + (x - x0) * [f(x1) - f(x0)] / (x1 - x0)

    where x is the query O/F ratio and x0, x1 are the bracketing table points.

    This is valid only within the tabulated O/F range. Extrapolation outside
    that range is blocked and will raise a ValueError.

    Parameters
    ----------
    of_ratio : float
        Oxidizer-to-fuel mass ratio (dimensionless)
    propellant : str
        Propellant combination key. Default: 'lox_rp1'

    Returns
    -------
    dict with keys:
        'Tc'    : float — Adiabatic flame temperature (K)
        'gamma' : float — Specific heat ratio (dimensionless)
        'Mmol'  : float — Mean molecular weight of combustion products (kg/kmol)
        'of'    : float — O/F ratio used for lookup (echo back for traceability)

    Raises
    ------
    ValueError if of_ratio is outside the tabulated range.
    """

    table = load_cea_table(propellant)

    of_min = table["of"].min()
    of_max = table["of"].max()

    # Block extrapolation — we do not trust the model outside calibrated range
    if of_ratio < of_min or of_ratio > of_max:
        raise ValueError(
            f"O/F ratio {of_ratio} is outside tabulated range "
            f"[{of_min}, {of_max}] for propellant '{propellant}'. "
            "Extrapolation is not permitted."
        )

    # np.interp(x, xp, fp) performs linear interpolation.
    # x  : the query point (our of_ratio)
    # xp : the known x values (table O/F column) — must be increasing
    # fp : the known y values (table Tc, gamma, or Mmol column)
    Tc    = float(np.interp(of_ratio, table["of"], table["Tc"]))
    gamma = float(np.interp(of_ratio, table["of"], table["gamma"]))
    Mmol  = float(np.interp(of_ratio, table["of"], table["Mmol"]))

    return {
        "Tc":    Tc,
        "gamma": gamma,
        "Mmol":  Mmol,
        "of":    of_ratio,
    }