"""
This module tests the creation and plots of motor curves.
"""
from helpers.types import MotorOperationPoint, MotorEfficiencyPoint
from components.motor_curves import MechanicalMaxPowerVsRPMCurves, MechanicalPowerEfficiencyCurves
from simulation.plot import plot_power_curve_and_efficiency

def test_motor_curves():
    min_rpms = 800.0
    max_rpms = 5_000.0
    power_max = 2_200.0
    min_effi = 0.15
    min_rpm_point = MotorOperationPoint(power=1_800.0,
                                        rpm=min_rpms)
    peak_rpm_point = MotorOperationPoint(power=power_max,
                                        rpm=2_200.0)
    max_rpm_point = MotorOperationPoint(power=2_000.0,
                                        rpm=max_rpms)
    ice_power_func = MechanicalMaxPowerVsRPMCurves.ice(min_rpm=min_rpm_point,
                                                       max_rpm=max_rpm_point,
                                                       peak_rpm=peak_rpm_point)
    max_eff_point = MotorEfficiencyPoint(power=1_950.0,
                                         rpm=2_000.0,
                                         efficiency=0.35)
    ice_eff_func = MechanicalPowerEfficiencyCurves.gaussian(max_eff=max_eff_point,
                                                            min_eff=min_effi,
                                                            falloff_rpm=0.0000001,
                                                            falloff_power=0.0000002,
                                                            max_power_vs_rpm=ice_power_func,
                                                            min_rpm=min_rpms,
                                                            max_rpm=max_rpms)
    plot_power_curve_and_efficiency(min_rpm=min_rpms,
                                    max_rpm=max_rpms,
                                    num_points=300,
                                    power_max=power_max,
                                    power_func=ice_power_func,
                                    eff_func=ice_eff_func)

    min_effi = 0.70
    em_power_func = MechanicalMaxPowerVsRPMCurves.em(base_rpm=1_000.0,
                                                     max_rpm=5_000.0,
                                                     max_power=2_200.0)
    max_eff_point = MotorEfficiencyPoint(power=1750.0,
                                        rpm=2_000.0,
                                        efficiency=0.95)
    em_eff_func = MechanicalPowerEfficiencyCurves.gaussian(max_eff=max_eff_point,
                                                           min_eff=min_effi,
                                                           falloff_rpm=0.0000001,
                                                           falloff_power=0.0000002,
                                                           max_power_vs_rpm=em_power_func,
                                                           min_rpm=0.0,
                                                           max_rpm=5_000.0)
    plot_power_curve_and_efficiency(min_rpm=0.0,
                                    max_rpm=5_000.0,
                                    num_points=300,
                                    power_max=2_200.0,
                                    power_func=em_power_func,
                                    eff_func=em_eff_func)

if __name__ == "__main__":
    test_motor_curves()
