import unittest
import mock
from company_interface import *
from vehicle_interface import *
from intelliware import Intelliware

class TestIntelliware(unittest.TestCase):
    def setUp(self):
        available_release_1 = SWRelease(compatible_hws=[2], sw_version=5, price_per_unit=100)
        available_release_2 = SWRelease(compatible_hws=[2], sw_version=6, price_per_unit=150)
        available_releases = [available_release_1, available_release_2]
        company_interface = CompanyInterface(available_releases, [])

        connected_vehicles = []
        hw_version = 2
        sw_version = 4
        desires_update = True
        groups = [1, 2]
        connected_vehicles.append(VehicleInterface(hw_version, sw_version, desires_update, groups))
        connected_vehicles.append(VehicleInterface(hw_version, sw_version, desires_update, groups))
        groups = [1, 3]
        connected_vehicles.append(VehicleInterface(hw_version, sw_version, desires_update, groups))
        self.intelliware = Intelliware(company_interface, connected_vehicles)

    #Test software update is not initiated if either incompatible or declined.

    # REQ: It shall be system to update all vehicles in a group with the latest compatible release
    def test_update_with_latest_compatible_release_only_updates_vehicle_in_group(self):
        # arrange
        expected_sw_version = 6
        group_of_interest = 2
        for vehicle in self.intelliware.connected_vehicles:
            if group_of_interest in vehicle.groups:
                self.assertNotEqual(vehicle.current_sw_version, 6)

        # act
        self.intelliware.update_all_vehicles_in_group_with_latest_compatible_release(group_of_interest)

        # assert
        for vehicle in self.intelliware.connected_vehicles:
            if group_of_interest in vehicle.groups:
                self.assertEqual(vehicle.current_sw_version, 6)
        self.assertEqual(self.intelliware.company_interface.get_current_debt(), 2 * 150)

    def test_update_with_specific_release_only_updates_vehicle_in_group(self):
        # arrange
        release = self.intelliware.company_interface.available_releases[0]
        expected_sw_version = 6
        group_of_interest = 2
        for vehicle in self.intelliware.connected_vehicles:
            if group_of_interest in vehicle.groups:
                self.assertNotEqual(vehicle.current_sw_version, 5)

        # act
        self.intelliware.update_all_vehicles_in_group_with_specific_release(group_of_interest, release)

        # assert
        for vehicle in self.intelliware.connected_vehicles:
            if group_of_interest in vehicle.groups:
                self.assertEqual(vehicle.current_sw_version, 5)
        self.assertEqual(self.intelliware.company_interface.get_current_debt(), 2 * 100)

if __name__ == '__main__':
    unittest.main()
