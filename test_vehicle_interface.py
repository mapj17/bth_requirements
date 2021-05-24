import unittest
import mock
from company_interface import *
from vehicle_interface import *

class TestVehicleInterface(unittest.TestCase):
    def setUp(self):
        hw_version = 2
        sw_version = 4
        desires_update = True
        self.vehicle_interface = VehicleInterface(hw_version,
                                                  sw_version,
                                                  desires_update)

    #Test software update is not initiated if either incompatible or declined.

    # REQ: Software is not updated in not compatible with hw.
    def test_does_not_update_with_non_compatible_sw(self):
        # arrange
        non_compatible_release = SWRelease(compatible_hws=[1,3,4], sw_version=5, price_per_unit=100)

        # act
        self.vehicle_interface.update_software(non_compatible_release)
        response = self.vehicle_interface.get_response()

        # assert
        self.assertFalse(response.result)

    # REQ: Can update software
    # REQ: Acknowledge program of success
    def test_update_sw_version_with_compatible_sw(self):
        # arrange
        compatible_release = SWRelease(compatible_hws=[1,2,4], sw_version=5, price_per_unit=100)
        self.assertNotEqual(compatible_release.sw_version,
                            self.vehicle_interface.current_sw_version)

        # act
        self.vehicle_interface.update_software(compatible_release)
        response = self.vehicle_interface.get_response()

        # assert
        self.assertTrue(response.result)
        self.assertEqual(compatible_release.sw_version,
                         self.vehicle_interface.current_sw_version)


    def test_does_not_update_sw_version_with_compatible_sw_against_desire(self):
        # arrange
        compatible_release = SWRelease(compatible_hws=[1,2,4], sw_version=5, price_per_unit=150)
        self.vehicle_interface.desires_update = False
        self.assertNotEqual(compatible_release.sw_version,
                            self.vehicle_interface.current_sw_version)

        # act
        self.vehicle_interface.update_software(compatible_release)
        response = self.vehicle_interface.get_response()

        # assert
        self.assertFalse(response.result)
        self.assertNotEqual(compatible_release.sw_version,
                         self.vehicle_interface.current_sw_version)

    # REQ: Driver is not prompted if there is incompatible hardware
    def test_driver_not_prompted_if_incompatible_hw (self):
        incompatible_release = SWRelease(compatible_hws=[1,4], sw_version=5, price_per_unit=60)
        with mock.patch.object(VehicleInterface,
                               'get_desires_update',
                               wraps=self.vehicle_interface.get_desires_update) as interface_mock:
            self.vehicle_interface.update_software(incompatible_release)
            self.assertEqual(0, interface_mock.call_count)

    def test_driver_prompted_before_update_if_incompatible_hw (self):
        compatible_release = SWRelease(compatible_hws=[1,2], sw_version=5, price_per_unit=100)
        self.assertNotEqual(compatible_release.sw_version,
                            self.vehicle_interface.current_sw_version)
        with mock.patch.object(VehicleInterface,
                               'get_desires_update',
                               wraps=self.vehicle_interface.get_desires_update) as interface_mock:
            self.vehicle_interface.update_software(compatible_release)
            self.assertEqual(1, interface_mock.call_count)

        self.assertEqual(compatible_release.sw_version,
                            self.vehicle_interface.current_sw_version)


if __name__ == '__main__':
    unittest.main()
