"""
This module handles all database interactions related to the project vehicles.
"""

from database import create_database_handler
from .UsersHandler import RegistrationStates


class VehiclesHandler:
    """This class handles all database interactions related to the project vehicles."""

    TABLE_NAME: str = "Vehicles"
    COLUMN_ID: int = "id"  # Data ID
    COLUMN_DEVICEID: str = "device_id"  # Device ID
    COLUMN_CLASS: str = "class"  # Vehicle Type
    COLUMN_PLATE: str = "plate"  # Plate Number
    COLUMN_ROUTE: str = "route"  # Route Number
    COLUMN_LASTDATE: str = "last_date"  # Last Maintenance Date
    COLUMN_PMDATE: str = "pmdate"  # Predicted Maintenance Date
    COLUMN_BATTERY: str = "battery"  # Battery Percentage
    COLUMN_GPS_LAT: str = "gps_lat"  # GPS Latitude
    COLUMN_GPS_LON: str = "gps_lon"  # GPS Longitude


    def __init__(self) -> None:
        self.db_handler = create_database_handler()

    def get_all_information(self) -> dict:
        """Return a list of vehicles information where
        each element is a dictionary.

        :return: A dictionary of vehicles information.
        """
        # Receive the all information of all vehicles.
        vehicles = self.db_handler.get_columns_from_table(self.TABLE_NAME, "*")
        # Since the information is list of tuples, we need to convert it to a
        # list of dictionaries.
        vehicles_information = []
        for vehicle in vehicles:
            vehicle_information = {
                "vid": vehicle[1],
                "class": vehicle[2],
                "plate": vehicle[3],
                "route": vehicle[4],
                "pmdate": vehicle[6],
                "battery": vehicle[7],
                "gps_latitude": vehicle[8],
                "gps_longitude": vehicle[9],
            }
            vehicles_information.append(vehicle_information)

        return vehicles_information

    def register_device(self, device_info: dict[str, str]) -> RegistrationStates:
        """Register a new device. The device_info keys must be the following:
        [device_id, class, plate, last_date]

        :param device_info: A dict containing the device information.
        :return: RegistrationStates
        """
        # Check if the dictionary contains the required keys.
        if not all(
            key in device_info for key in ["device_id", "class", "plate", "route", "last_date"]
        ):
            raise ValueError(
                "The device_info dictionary must contain the following keys: "
                "device_id, class, plate, route, last_date"

            )

        # Check if the device is registered.
        device_already_registered = self.check_device_id(device_info["device_id"])
        if device_already_registered:
            return RegistrationStates.ALREADY_REGISTERED

        # Create a dictionary record to insert into the database.
        device_data_record = {
            self.COLUMN_DEVICEID: device_info["device_name"],
            self.COLUMN_CLASS: device_info["class"],
            self.COLUMN_PLATE: device_info["plate"],
            self.COLUMN_ROUTE: device_info["route"],
            self.COLUMN_LASTDATE: device_info["last_date"],
            self.COLUMN_BATTERY: 0,
            self.COLUMN_GPS_LAT: 0,
            self.COLUMN_GPS_LON: 0,
            self.COLUMN_PMDATE: "None",
        }

        # Insert the new device into the database.
        self.db_handler.insert_into_table(self.TABLE_NAME, device_data_record)

        # Check if the device is registered.
        device_registration_check = self.check_device_id(device_info["device_id"])
        if not device_registration_check:
            return RegistrationStates.NOT_REGISTERED
        return RegistrationStates.SUCCESS

    def check_device_id(self, device_id_to_check: str) -> bool:
        """Check if a device is registered.

        :param device_id_to_check: The device ID to check.
        :return: True if the device is registered, False otherwise.
        """
        return self.db_handler.check_value_exists(
            self.TABLE_NAME, self.COLUMN_DEVICEID, device_id_to_check
        )
