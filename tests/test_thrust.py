"""test the thrust and specific impulse calculations"""

import pytest
import math 
from src.performance import thrust, specific_impulse, compute_isp



def test_Force_thrust():
    result = thrust(10, 3000,50000,101325,0.5)
    assert result == pytest.approx(4337.5, rel=0.02)
def test_Isp():
    result = specific_impulse(4337.5,10)
    assert result ==pytest.approx(44.23, rel=0.02)

def test_compute_isp_loxrp1():
    result = compute_isp('lox_rp1', 2.75, 3.45e6, 10, 101325, 10)
    assert result > 250
    assert result < 400

    print(compute_isp('lox_rp1', 2.75, 3.45e6, 10, 101325, 10))