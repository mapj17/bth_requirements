from vehicle_interface import *
from company_interface import *
from collections import defaultdict
class Intelliware:
    def __init__(self, company_interface: CompanyInterface, connected_vehicles: list):
        self.company_interface = company_interface
        self.connected_vehicles = connected_vehicles

    # Update all vehicles in group
    # Update all vechicles
    def update_all_vehicles_in_group_with_latest_compatible_release(self, group_id: int, update_all_groups: bool=False):
        updated_vehicle_count = defaultdict(int)
        sw_releases = {}
        for vehicle in self.connected_vehicles:
            if group_id in vehicle.groups or update_all_groups:
                compatible_release = \
                    self.company_interface.get_latest_release_for_hw(vehicle.hw_version)
                vehicle.update_software(compatible_release)
                if vehicle.response.result:
                    if compatible_release.sw_version not in sw_releases.keys():
                        sw_releases[compatible_release.sw_version] = compatible_release
                        updated_vehicle_count[compatible_release.sw_version]+=1
        for sw_release in sw_releases.values():
            self.company_interface.publish_billables(BillInfo(sw_release,
                                                     updated_vehicle_count[sw_release.sw_version]))

    def update_all_vehicles_in_group_with_specific_release(self, group_id: int, release: SWRelease, update_all_groups: bool=False):
        num_updated_vehicles = 0
        for vehicle in self.connected_vehicles:
            if group_id in vehicle.groups or update_all_groups:
                vehicle.update_software(compatible_release)
                if vehicle.response.result:
                    num_updated_vehicles+=1
        self.company_interface.publish_billables(release, num_updated_vehicles)

