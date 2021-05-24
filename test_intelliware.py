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

    # REQ: Software is not updated in not compatible with hw.
    def test_only_updates_vehicle_in_group(self):
        # arrange

        # act
        self.intelliware.update_all_vehicles_in_group_with_latest_compatible_release(2)
        import pdb; pdb.set_trace()
        hej = 3


        # assert
        self.assertFalse(response.result)

if __name__ == '__main__':
    unittest.main()
