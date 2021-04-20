import pytest
import calculator

#Dummy variables

def test_total_force():
    assert calculator.total_force(5, 7) == 5.9565

def test_velocity():
    assert calculator.velocity(11,13) == 22.7165

def test_radius():
    assert calculator.radius(1,2,3,5,8,13) == 35.16766563026828

def test_centripetal_force():
    assert calculator.centripetal_force(17,19) == 15.210526315789474

def test_is_derailed():
    assert calculator.is_derailed(calculator.DERAIL_THRESHOLD) == False
    assert calculator.is_derailed(-calculator.DERAIL_THRESHOLD) == False
    assert calculator.is_derailed(calculator.DERAIL_THRESHOLD+1) == True
    assert calculator.is_derailed(-calculator.DERAIL_THRESHOLD - 0.000001)
