from typing import List
from database import create_database_handler, DatabaseHandler


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
    
    def get_email(self, email: str) -> list[str]:
        # Receive the email of a user.
        extra_condition = self._where_on_column(self.COLUMN_NAME, name)
        return self.db_handler.get_columns_from_table(
            self.TABLE_NAME, self.COLUMN_MAIL, extra_condition
        )


    #def insert_user(self, name_surname: str, company: str, email: str, password: str) ->None:
    #    """Insert a user record into the 'Users' table."""
    #    insert_query = """
    #    INSERT INTO users (COLUMN_ID,COLUMN_NAME, COLUMN_COMP COLUMN_MAIL, COLUMN_PASSWORD)
    #    VALUES (1,%s, %s, %s, %s)
    #    """
    #    db_cursor.execute(insert_query, (name_surname, company, email, password))
    #    create_database_handler.commit()

