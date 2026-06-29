"""Author Ken Aoki 6/27 
performance of the rocket engine
Will calculate the thrust, and Isp
Thrust is the amount of force that the rocket engine will produce 
Isp is specific impulse and it is a measure of how efficient the rocket engine is 
"""
import math 
import scipy.constants as const 
from src.thermochemistry import get_propellant_properties
from src.nozzle import mach_from_area_ratio, exit_conditions, thrust_coefficient, throat_area, exit_area
def thrust (mdot: float, v_exit: float, Pe: float, Pa: float, Ae: float) -> float: 
    """calculates the thrust provided by the rocket engine,
    the thrust provided by rocket engine comes from 2 things: 
    the momentum of the gas exiting the nozzle 
    the pressure difference at exit plane acting over area Ae
    F_momentum = mdot * velocity 
    F_pressure = (Pe - Pa)Ae 
    
    Args: 
    mdot: mass flow rate [kg/s]
    v_exit: velocity of gas exiting nozzle [m/s]
    Pe: pressure at nozzle exit [Pa]
    Pa: ambient pressure of atmosphere [Pa]
    Ae: area of exit [m^2]
    returns: 
    thrust [N]"""
    F_momentum = mdot * v_exit
    F_pressure = (Pe - Pa) * Ae 
    Force_thrust = F_momentum + F_pressure 
    return Force_thrust 

def specific_impulse (Force_thrust:float, mdot: float) -> float: 
    """calculates the specific impulse which measures the efficeincy of the rocket engine 
    specific impulse has units of seconds 
    it measures how many seconds a rocket engine can produce 1 N of thrust for consuming 1 N of propellant
    Isp = Force_thrust / (g0 * mdot)
    Arugs:
    Force_thrust [N]
    g0 gravity @ sea level [m/s^2]
    mdot mass flow rate [kg/s]"""
    g0 = 9.80665
    Isp = Force_thrust / (g0 * mdot)
    return Isp 

def compute_isp(propellant: str, OF:float, Pc:float, epsilon:float, Pa:float, mdot:float) -> float: 
    """calculates the isp as a function of only the Oxidiser and Fuel ratio OF
    props = get_propellant_properties
    """
    props = get_propellant_properties(propellant, OF)
    Tc = props['Tc']
    gamma = props['gamma']
    Mmol = props['Mmol']
    R_specific = 8.314 / Mmol 
    Me = mach_from_area_ratio(epsilon, gamma)
    Pe,Te,Ve = exit_conditions(Pc, Tc, gamma, Me, Mmol)
    Cf = thrust_coefficient(gamma, Pe, Pc, Pa , epsilon) 
    At = throat_area(1000, Cf, Pc)   # F_target = 1000 N
    Ae = exit_area(epsilon, At)
    F = thrust(mdot,Ve,Pe,Pa,Ae)
    Isp = specific_impulse(F,mdot)
    return Isp 

print(compute_isp('lox_rp1', 2.75, 3.45e6, 10, 101325, 10))