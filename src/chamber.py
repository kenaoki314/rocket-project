"""calculate c* value from values of Tc, gamma, and Mmol,
this is done by the equation c* = sqrt(R*T)/GammaFuntion
where R is the specific gas constant R = R_universal / M_mol 
M_mol is molecular weight 
T_c is the temperature at the chamber
Vandenkerckhove function(Gamma Function) represents compressibillity effect of gas as it accelerates to speed of sound at choke
Gamma function = sqrt(gamma)*[2/(gamma + 1))]exp((gamma+1)/2(gamma -1))
gamma is specific heat ratio c_p / c_v
c_p is specifc heat capacity at constant pressure 
c_v is specific heat capacity at constant volume
Supported propellant combinations:
    - lox_rp1  : LOX (90 K) / RP-1 (293 K), Pc = 3.45 MPa, shifting equilibrium
    - lox_lh2 : LOX (90K) / H(20K), Pc=3.45 MPa, shifting equilibrium. 
    - n2o_ethanol: N2O (293K) / C2H5OH Ethanol (293K) Pc = 3.45 Mpa, Shfitig equilibum 

Author Ken Aoki, 10:12PM 6/23/2026 """

import math
from thermochemistry import get_propellant_properties



def GammaFunc(gamma:float)-> float :
    """turns gamma into Vandenkerchove function
    gamma unitless
    gamma function uniltess """
    #gamma = 1.67 ####PLACE HOLDER FOR CALCULATED gamma VALUE FROM thermochemistry.py
    
    VDK_function = math.sqrt(gamma) * (2/(gamma +1))**((gamma+1)/(2*(gamma-1)))
    return  VDK_function


def Cstar(VDK_function:float, R: float, Tc:float) -> float: 
    """calculates C star as a function of Vandenkerchove function, Chamber Temperature, and R specific gas constant
    with R_specific = R_universal / M_mol
   returns: C* [m/s
    R J/kg*K
    Tc K]"""
    Vandenkerckhove = VDK_function 
    #R = 8.314/0.01118  # [ J / (mol*K) ] ###PLACE HOLDER FOR CALCULATED Mmol VALUE FROM thermochemistry.py
    #Tc = 3140.3 K
    Cstar = math.sqrt(R * Tc) / Vandenkerckhove
    return Cstar
if __name__ == '__main__':
    Propellant = 'n2o_ethanol'
    OF_ratio = 5.7
    props = get_propellant_properties(Propellant , OF_ratio)
    Tc = props['Tc']
    gamma = props['gamma']
    Mmol = props['Mmol']
    R_universal = 8.314
    R_specific = R_universal / Mmol
    gamma_func_result = GammaFunc(gamma)
    cstar_result = Cstar(gamma_func_result, R_specific, Tc)
    print(f'for {Propellant} with OF ratio {OF_ratio}, characteristic velocity c* is: {cstar_result} m/s')