"""
This module abstracts all database interactions related to the users.
"""

from enum import IntEnum, auto
from database import create_database_handler


class RegistrationStates(IntEnum):
    """This class contains the possible registration states."""

    ALREADY_REGISTERED = auto()
    SUCCESS = auto()
    NOT_REGISTERED = auto()


class UsersHandler:
    """This class abstracts all database interactions related to the users."""

    TABLE_NAME: str = "Users"
    COLUMN_ID: int = "id"
    COLUMN_COMP: str = "company"
    COLUMN_NAME: str = "name_surname"
    COLUMN_MAIL: str = "email"
    COLUMN_PASSWORD: str = "password"

    def __init__(self) -> None:
        self.db_handler = create_database_handler()

    def _where_on_column(self, column: str, name: str) -> str:
        return f"WHERE {column} = '{name}'"

    def get_emails(self) -> list[str]:
        """Return a list of registered emails.
        :returns: A list of registered emails.
        """
        return self.db_handler.get_columns_from_table(self.TABLE_NAME, self.COLUMN_MAIL)

    def register_user(self, user_info: dict[str, str]) -> RegistrationStates:
        """Register a new user. The user_info list must contain the following:
        [name_surname, company, email, password]
        :param user_info: A list containing the user information.
        :return: None
        """
        if not all(
            key in user_info for key in ["name_surname", "company", "email", "password"]
        ):
            raise ValueError(
                "The user_info dictionary must contain the following keys: "
                "name_surname, company, email, password"
            )

        user_already_registered = self.check_email(user_info["email"])
        if user_already_registered:
            return RegistrationStates.ALREADY_REGISTERED

        # Create a dictionary record to insert into the database.
        new_user_data = {
            self.COLUMN_NAME: user_info["name_surname"],
            self.COLUMN_COMP: user_info["company"],
            self.COLUMN_MAIL: user_info["email"],
            self.COLUMN_PASSWORD: user_info["password"],
        }

        # Insert the new user into the database.
        self.db_handler.insert_into_table(self.TABLE_NAME, new_user_data)

        # Check if the user is registered.
        user_registration_check = self.check_email(user_info["email"])
        if not user_registration_check:
            return RegistrationStates.NOT_REGISTERED
        return RegistrationStates.SUCCESS

    def check_email(self, email_to_check: str) -> bool:
        """Check if a user is registered.

        :param email_to_check: The email to check.
        :return: True if the user is registered, False otherwise.
        """
        return self.db_handler.check_value_exists(
            self.TABLE_NAME, self.COLUMN_MAIL, email_to_check
        )

    def get_password_hash(self, email: str) -> list[str]:
        """Get the password hash of a user.

        :param email: The email of the user.
        :return: The password hash of the user.
        """
        extra_condition = self._where_on_column(self.COLUMN_MAIL, email)
        passwords: list = self.db_handler.get_columns_from_table(
            self.TABLE_NAME, self.COLUMN_PASSWORD, extra_condition
        )
        return passwords[0][0]
