import unittest
import mock
from company_interface import *
from company_interface import *

class TestCompanyInterface(unittest.TestCase):
    def setUp(self):
        self.release_1 = SWRelease(compatible_hws=[1,2,3], sw_version=6, price_per_unit=150)
        self.release_2 = SWRelease(compatible_hws=[3, 4], sw_version=7, price_per_unit=250)
        self.company_interface = CompanyInterface(available_releases=[self.release_1, self.release_2],
                                                  existing_bills=[])


    # REQ: The system shall provide information any time a vehicle or a goup of vehicles are updated
    def test_updates_existing_bills_with_new_billables(self):
        # arrange
        new_bill = BillInfo(info=self.release_1, num_updated_vehicles=5)
        self.assertEqual(self.company_interface.existing_bills,[])

        # act
        self.company_interface.publish_billables(new_bill)

        # assert
        self.assertEqual(self.company_interface.existing_bills, [new_bill])

    # It shall be possible for the system to obtain the current debt from the company
    def test_get_current_debt(self):
        # arrange
        new_bill = BillInfo(info=self.release_1, num_updated_vehicles=5)
        self.company_interface.existing_bills = [new_bill]

        # act
        current_debt = self.company_interface.get_current_debt()

        # assert
        self.assertEqual(new_bill.info.price_per_unit * new_bill.num_updated_vehicles, current_debt)

    # There shall be an option for getting the latest release
    def test_get_latest_release(self):
        # arrange
        expected_latest_release = self.company_interface.available_releases[-1]

        # act
        actual_latest_release = self.company_interface.get_latest_release()

        # assert
        self.assertEqual(expected_latest_release, actual_latest_release)

    # There shall be an option for getting the latest release compatible with a given hw version.
    def test_get_latest_compatible_release(self):
        # arrange
        hw_version = 2
        expected_latest_compatible_release = self.release_1

        # act
        actual_latest_compatible_release = self.company_interface.get_latest_release_for_hw(hw_version)

        # assert
        self.assertEqual(expected_latest_compatible_release, actual_latest_compatible_release)




if __name__ == '__main__':
    unittest.main()
