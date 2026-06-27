"""calculator to calculate the value of the throat area as a function of the force, pressure, and thrust coeeficient 

this will implement isentropic flow relatinos and solve mach area equation numerically
then it will calculate the value of the throar area as a function of the force, pressure, and the thrust coefficent 
then it will calculate the exit area A_e from area ratio by Pe/Pc or exit mach 
then output nozzle geometry and then calcualte exit velocity


Isp: specific impulse [s]
mdot: mass flow rate [kg/s]
g0: gravitational acceleration at sea level [m/s^2]
F: thrust [N]
C_f: thurst coefficient [none]
gamma: heat capacity ratio [none]
M: Mach number 

exhaust velocity c = Isp *g0 = F / mdot [m/s]
Throat area At = F / (C_f * P_c) [m^2]

Diverging bell curve:
A / A_t = 1/M * [(2+(gamma-1)M^2) / (gamma + 1)]^((gamma+1)/2(gamma-1))

P_exit = P_c * (1+ (gamma -1)/2 * M_exit^2)^(-gamma / (gamma -1))
T_exit = T_c * (1+(gamma-1)/2 * M_exit^2)^-1
V_exit
""" 
import math
from scipy.optimize import brentq


def mach_from_area_ratio(epsilon:float, gamma: float)-> float: 
    """return exit mach number for a given area ratio
    solve mach area equation using bentq
    A/A* = (1/M) * [(2 + (gamma-1)*M^2) / (gamma+1)]^((gamma+1) / 2(gamma-1))
    args: 
    epsilon: area ratio A/A* unitlless
    gamma: specific heat ratio unitles
    returns: 
    Me: exit mach number 
   """
    def f(M):
        rhs = (1/M) * ((2+ (gamma-1) * M**2) / (gamma + 1))**((gamma+1) / (2*(gamma-1)))
        return epsilon - rhs
    Me = brentq(f,1.0, 10.0)
    return Me

def temperature_exit(gamma: float, Tc: float, M: float) -> float: 
    """Governing equation:
    Te = Tc * (1 + (gamma-1)/2 * M^2)^-1

    Args:
    Tc:    chamber temperature [K]
    gamma: ratio of specific heats [-]
    M:     exit Mach number [-]
    Returns:
    Te: exit temperature [K]
    """
    Te = Tc * (1 + (gamma - 1)/2 * M**2)**-1
    return Te

def pressure_exit(gamma: float, Pc: float, M: float) -> float: 
    """calcualte the pressure at the exit as a function of the pressure in the chamber, gamma ratio, and the mach number
    Pe = Pc * (1 + (gamma -1)/2 * M**2)**((gamma * -1)/(gamma - 1)) 
    Args: 
    Pc: chamber prssure [Pa]
    gamma: specific heat ratio 
    M: exit mach number
    returns: exit pressure [Pa]"""
    
    
    Pe = Pc * (1 + (gamma -1)/2 * M**2)**((gamma * -1)/(gamma - 1))
    return Pe 


def velocity_exit(Me: float, gamma: float, R_specific: float, Te) -> float: 
    """calculate the velocity of propellant as it exits nozzle,
    a_exit = sqrt(gamma * R_specifc * Te)
    V_exit = M_exit * a_exit
    Args: 
    M: exit mach number 
    Rsp: specific idea gas constant 
    Te: temperature of gas at exit [K]
    gamma: specific heat ratio 
    returns
    Ve: velocity at exit """
    a_exit = math.sqrt(gamma * R_specific * Te)
    Ve = Me * a_exit 
    return Ve 

def exit_conditions(Pc: float, Tc: float, gamma: float, Me: float, Mmol:float) -> tuple: 
    """returns exit conditions of pressure, temperature, and velocity
    args: 
    Pc: chamber prssure Pa]
    Tc: chamber temperature [K]
    gamma: specific heat ratio 
    Me: exit mach number 
    Mmol: molar mass kg/mol
    Returns:
    Pe: exit pressure [Pa]
    Te: exit temperature [K]
    Ve: exit velocity [m/s] """
    R_specific = 8.314 / Mmol
    Te = temperature_exit(gamma, Tc, Me)
    Pe = pressure_exit(gamma, Pc, Me)
    Ve = velocity_exit(Me, gamma, R_specific, Te)
    return Pe, Te, Ve
def exit_area(epsilon:float, At:float )-> float: 
    """exit area is equal to epsilon * throat area 
    args: 
    epsilon unitless
    throat area [m^2]
    returns: 
    exit area [m^2]"""
    A_exit = epsilon * At 
    return A_exit 
def thrust_coefficient(gamma: float, Pe: float, Pc: float, Pa:float , epsilon: float) -> float:
    """thrust coefficeint determines how efficient a rocket engine expands gas 
    to solve by normalizeation of the momentum thrust and pressure thrust 
    Cf = Cf = sqrt(2gamma^2/(gamma-1) * (2/(gamma+1))^((gamma+1)/(gamma-1)) * [1-(Pe/Pc)^((gamma-1)/gamma)]) + (Pe-Pa)/Pc * epsilon
    args: 
    gamma: specific heat ratio
    epsilon: Area ratio Ae/At 
    Pe: pressure at exit [Pa]
    Pc: pressure in chamber [Pa]
    Pa: ambient pressure [Pa] at sea level = 1 atm, in vaccum = 0
    returns
    Cf: thrust coefficient"""
    momentum_thrust = math.sqrt(2*gamma**2/(gamma-1) * (2/(gamma+1))**((gamma+1)/(gamma-1)) * (1 - (Pe/Pc)**((gamma-1)/gamma)))
    pressure_thrust = (Pe - Pa)/Pc * epsilon
    Cf = momentum_thrust + pressure_thrust
    return Cf 
def throat_area(thrust: float ,Cf: float, Pc: float) -> float: 
    """calculate the throat area from the equation At = F / (Cf * Pc)
    args
    F: thrust [N]
    Cf: thrust coefficient
    Pc: pressure at chamber [Pa]
    returns
    At: throat area [m^2]"""
    At = thrust /(Pc * Cf)
    return At 

def nozzle_geometry(At: float, Ac: float, Ae: float,theta_conv: float = 30, theta_div: float = 15) -> dict:
    """calculatrs the Lengths of the convering section, divering section, radius of throat, radius of the exit,and radius of the chamber 
    Args: 
    At: area of throat [m^2]
    Ac: area of chamber [m^2]
    Ae: area of exit [m^2]
    theta_conv: angle between wall and orthogonal line to center of area of chamber on inlet side of throat [deg]
    theta_div: angle between wall and orthognal line to center of area of exit on exitr side of throat [deg] 
    Returns: 
    Ldiv,
    Lconv
    Rt 
    Re
    Rc"""
    Rt = math.sqrt( At / math.pi) 
    Re = math.sqrt( Ae / math.pi)  
    Rc = math.sqrt( Ac / math.pi)
    L_div = (Re - Rt) / math.tan(math.radians(theta_div)) 
    L_conv = (Rc - Rt) / math.tan(math.radians(theta_conv)) 
    return {'L_div': L_div, 'L_conv': L_conv, 'Rt': Rt, 'Re': Re, 'Rc': Rc } 

