from typing import List
from database import create_database_handler


class ProjectManagersHandler:
    """This class handles all database interactions related to the project managers."""

    TABLE_NAME: str = "ProjectManagers"
    COLUMN_NAME: str = "name_surname"
    COLUMN_DESC: str = "description"
    COLUMN_IMG_LOC: str = "profile_img_location"
    COLUMN_LINK: str = "social_link"

    def __init__(self) -> None:
        # Holds the database handler.
        self.db_handler = create_database_handler()

    def _where_on_column(self, column: str, name: str) -> str:
        return f"WHERE {column} = '{name}'"

    def get_names(self) -> list[str]:
        # Receive the names of all project managers.
        return self.db_handler.get_columns_from_table(self.TABLE_NAME, self.COLUMN_NAME)

    def get_user_information(self, name: str) -> dict:
        # Receive the all other information of a project manager.
        desired_columns = (
            f"{self.COLUMN_DESC}, {self.COLUMN_IMG_LOC}, {self.COLUMN_LINK}"
        )
        extra_condition = self._where_on_column(self.COLUMN_NAME, name)
        return self.db_handler.get_columns_from_table(
            self.TABLE_NAME, desired_columns, extra_condition
        )

    def get_profile_image(self, name: str) -> bytes:
        # Receive the profile image of a project manager.
        extra_condition = self._where_on_column(self.COLUMN_NAME, name)
        return self.db_handler.get_columns_from_table(
            self.TABLE_NAME, self.COLUMN_IMG_LOC, extra_condition
        )

    def get_social_links(self, name: str) -> list[str]:
        # Receive the social links of a project manager.
        extra_condition = self._where_on_column(self.COLUMN_NAME, name)
        return self.db_handler.get_columns_from_table(
            self.TABLE_NAME, self.COLUMN_LINK, extra_condition
        )
