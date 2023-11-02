"""
This module provides a abstraction layer for Project Managers table.
"""

from database import create_database_handler


class ProjectManagersHandler:
    """This class handles all database interactions related to the project managers."""

    TABLE_NAME: str = "ProjectManagers"
    COLUMN_NAME: str = "name_surname"
    COLUMN_DESC: str = "description"
    COLUMN_IMG_LOC: str = "profile_img_location"
    COLUMN_LINK: str = "social_link"

    def __init__(self) -> None:
        self.db_handler = create_database_handler()

    def _where_on_column(self, column: str, name: str) -> str:
        return f"WHERE {column} = '{name}'"

    def get_names(self) -> list[str]:
        """Return a list of project manager names.
        
        :returns: A list of project manager names.
        """
        return self.db_handler.get_columns_from_table(self.TABLE_NAME, self.COLUMN_NAME)

    def get_user_information(self, name: str) -> dict:
        """Return a dictionary of project manager information.
        
        :param name: The name of the project manager.
        :returns: A dictionary of project manager information.
        """
        desired_columns = (
            f"{self.COLUMN_DESC}, {self.COLUMN_IMG_LOC}, {self.COLUMN_LINK}"
        )
        extra_condition = self._where_on_column(self.COLUMN_NAME, name)
        return self.db_handler.get_columns_from_table(
            self.TABLE_NAME, desired_columns, extra_condition
        )

    def get_profile_image(self, name: str) -> str:
        """Return the profile image location of a project manager.

        :param name: The name of the project manager.
        :returns: The profile image location of a project manager.
        """
        extra_condition = self._where_on_column(self.COLUMN_NAME, name)
        return self.db_handler.get_columns_from_table(
            self.TABLE_NAME, self.COLUMN_IMG_LOC, extra_condition
        )

    def get_social_links(self, name: str) -> list[str]:
        """Return the social links of a project manager.

        :param name: The name of the project manager.
        :returns: The social links of a project manager.
        """
        extra_condition = self._where_on_column(self.COLUMN_NAME, name)
        return self.db_handler.get_columns_from_table(
            self.TABLE_NAME, self.COLUMN_LINK, extra_condition
        )

    def get_all_information(self) -> dict:
        """Return a list of people information where
        each element is a dictionary.

        :return: A dictionary of people information.
        """
        people = self.db_handler.get_columns_from_table(self.TABLE_NAME, "*")
        # Since the information is list of tuples, we need to convert it to a
        # list of dictionaries.
        people_information = []
        for person in people:
            person_information = {
                "name_surname": person[0],
                "profile_img_location": person[1],
                "description": person[2],
                "social_link": person[3],
            }
            people_information.append(person_information)
            people_information.sort(key=lambda x: x["name_surname"])

        return people_information
