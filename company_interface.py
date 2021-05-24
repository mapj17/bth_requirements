from dataclasses import dataclass

@dataclass
class SWRelease:
    compatible_hws: list
    sw_version: int
    price_per_unit: int

    def is_compatible_with(self, hw_version):
        return hw_version in self.compatible_hws



@dataclass
class BillInfo:
    info: SWRelease
    num_updated_vehicles: int


class CompanyInterface:
    def __init__(self, available_releases: list, existing_bills: list):
        self.available_releases = available_releases
        self.existing_bills = existing_bills

    def get_latest_release(self):
        return self.available_releases[-1]

    def get_latest_release_for_hw(self, hw_version):
        for release in self.available_releases[::-1]:
            if release.is_compatible_with(hw_version):
                return release
        else:
            raise Exception("No available release for that hw")

    def publish_billables(self, bill_info):
        self.existing_bills.append(bill_info)

    def get_current_debt(self):
        return sum([x.num_updated_vehicles * x.info.price_per_unit for x in self.existing_bills])


