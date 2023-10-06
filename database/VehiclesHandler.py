from typing import List
from database import create_database_handler


class VehiclesHandler:
    """This class handles all database interactions related to the project vehicles."""

    TABLE_NAME: str = "Vehicles"
    COLUMN_ID: int = "id"
    COLUMN_CLASS: str = "class"
    COLUMN_PLATE: str = "plate"
    COLUMN_ROUTE: str = "route"
    COLUMN_PMDATE: str = "pmdate"  #Predicted Maintenance Date
    #COLUMN_NOT: str ="notification"

    def __init__(self) -> None:
        # Holds the database handler.
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
                "id": vehicle[0],
                "class": vehicle[1],
                "plate": vehicle[2],
                "route": vehicle[3],
                "pmdate": vehicle[4],
                #"notification":vehicle[5]
            }
            vehicles_information.append(vehicle_information)

        return vehicles_information