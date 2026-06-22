"""
thermochemistry.py

Provides combustion property lookups (Tc, gamma, Mmol) as a function of
O/F ratio by linear interpolation from tabulated NASA CEA data.



Supported propellant combinations:
    - lox_rp1  : LOX (90 K) / RP-1 (293 K), Pc = 3.45 MPa, shifting equilibrium
    - lox_lh2 : LOX (90K) / H(20K), Pc=3.45 MPa, shifting equilibrium. 
    - N2O_ethanol: N2O (293K) / C2H5OH Ethanol (293K) Pc = 3.45 Mpa, Shfitig equilibum 

Author : Ken Aoki 6/21/26
Project: LRE Sizing Tool — Phase 1 
"""

import numpy as np
import pandas as pd 
from pathlib import Path 

def get_propellant_properties(propellant:str, OF_query: float) -> dict:
    """Interpolates properties from CEA .csv file data 
    Arguments:
    propellant: str 
    OF_query: float 
    
    returns:
    Tc chamber temperature 
    gamma ratio of specific heats 
    Mmol molar mass
    raises key error if propellant stirng is not recognized
    fileNotFoundError if CSV is missing data
    ValueError if outside OF data range"""
    propellant_files = {
        'lox_rp1': 'cea_loxrp1.csv',
        'lox_lh2': 'cea_loxlh2.csv',
        'n2o_ethanol': 'cea_n2o_ethanol.csv'    
        }
    if propellant not in propellant_files: 
        raise KeyError(f"unknown proepllant'{propellant}'."
        f"Choose from: {list(propellant_files.keys())}")
    
    filename = propellant_files[propellant]
    filepath = Path(__file__).parent.parent/ 'data' / filename
    df = pd.read_csv(filepath)  
    OF = df['of_ratio'].to_numpy()
    Tc = df['Tc_K'].to_numpy()
    gamma = df['gamma'].to_numpy()
    Mmol = df['Mmol_kg_kmol'].to_numpy() / 1000.0 #converting kg/kmol to kg/mol
    if not (OF[0] <= OF_query <= OF[-1]):
        raise ValueError(
            f"OF_query={OF_query} is outside tabulated range "
            f"[{OF[0]}, {OF[-1]}] for propellant '{propellant}'"
        )
    Tc_value = np.interp(OF_query, OF, Tc)
    gamma_value = np.interp(OF_query, OF, gamma)
    Mmol_value = np.interp(OF_query, OF, Mmol)
    return {'Tc': Tc_value, 'gamma': gamma_value, 'Mmol': Mmol_value}
if __name__ == "__main__":
    propellant = 'n2o_ethanol'
    OF_ratio = 99
    result = get_propellant_properties(propellant, OF_ratio )
    print(f'For {propellant} with O/F ratio {OF_ratio}')
    print(f"Tc = {result['Tc']:.1f} K")
    print(f"gamma = {result['gamma']:.4f}")
    print(f"Mmol  = {result['Mmol']:.5f} kg/mol")