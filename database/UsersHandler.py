from typing import List
from database import create_database_handler


class UsersHandler:
    """This class handles all database interactions related to the users."""

    TABLE_NAME: str = "Users"
    COLUMN_ID: int = "id"
    COLUMN_COMP: str = "company" 
    COLUMN_NAME: str = "name"
    COLUMN_MAIL: str = "email"
    COLUMN_PASSWORD: str = "password"

     
    def __init__(self) -> None:
        # Holds the database handler.
        self.db_handler = create_database_handler()
    
    def _where_on_column(self, column: str, name: str) -> str:
        return f"WHERE {column} = '{name}'"
    
    def get_emails(self, email: str) -> list[str]:
        # Receive the emails of a user.
        return self.db_handler.get_columns_from_table(
            self.TABLE_NAME, self.COLUMN_MAIL
        )

    def insert_user(self, user_info: list) ->None:
        # Insert the new user.
        user_data = {
        'COLUMN_NAME': user_info[0],
        'COLUMN_COMP': user_info[1],
        'COLUMN_MAIL': user_info[2],
        'COLUMN_PASSWORD': user_info[3]
        }
        veri=create_database_handler()
        veri.insert_into_table(self.TABLE_NAME,user_data)

    def check_email(self,email_to_check:str) -> bool:
        # Check e-mail if exist
        return self.db_handler.check_value_exists(
            self.TABLE_NAME, "COLUMN_MAIL", email_to_check
            )
