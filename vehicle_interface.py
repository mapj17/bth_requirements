from dataclasses import dataclass
from company_interface import SWRelease


@dataclass
class Response:
    result: bool
    message: str

class DesiresUpdateResponse(Response):
    pass

class UpdateSuccessfulResponse(Response):
    pass


class VehicleInterface:
    def __init__(self, hw_version: int, current_sw_version: int, desires_update: bool, groups: list):
        # To determine software compability
        self.hw_version = hw_version
        self.current_sw_version = current_sw_version
        self.response = None
        self.desires_update = desires_update
        self.groups = groups

    def is_compatible_with_release(self, release: SWRelease):
        return self.hw_version in release.compatible_hws

    # Only ask user if hw is compatible.
    def update_software(self, release: SWRelease):
        if (self.is_compatible_with_release(release) and
            self.current_sw_version != release.sw_version):
            if self.get_desires_update():
                self.current_sw_version = release.sw_version
                self.response = UpdateSuccessfulResponse(True, "SW update Successful")
            else:
                self.response = DesiresUpdateResponse(False, "Driver does not desire update")
        else:
            self.response = UpdateSuccessfulResponse(False, "SW version not compatible")

    def get_hw_version(self):
        return self.hw_version

    def get_desires_update(self):
        return self.desires_update

    def get_response(self):
        if self.response is None:
            raise Exception('No response available')
        response = self.response
        self.response = None
        return response
