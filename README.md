# LRE_Sizing_Tool





thermochemistry.py
gets cea data and interpolates Temperature, gamma, and Mmol 

chamber.py 
calculate c* value (Tc, gamma, Mmol) -> c* [m/s]
calculate the chamber dimensions (c*, mdot, Pc, L*) -> volume, L, D [m^3, m, m]

nozzle.py
calculate the throat area (F, Pc, Cf) -> At [m^2]
calculate the exit area (At, area_ratio) -> Ae [m^2]
calculate the exit conditions (Pc, gamma, Me) -> Ve, Pe, Te

performace.py
calculate the thrust  (mdot, Ve, Pe, Pa, Ae) → F 
calculate the Isp (F, mdot) → Isp
