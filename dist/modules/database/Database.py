from typing import Any, Optional, Tuple, List
from psycopg2 import connect
from psycopg2.extras import RealDictCursor, Json
from psycopg2.extensions import new_type, DECIMAL, register_type, register_adapter
from modules._types import ITableNames
from modules.environment.Environment import ENV








## Table Names ##



# Name Retriever
def _get_table_name(table_name: str) -> str:
    """Retrieves a table name based on the test mode value provided by the environment.
    If test_mode is enabled, it will attach the test_ string. F.e test_$TABLE_NAME

    Args:
        table_name (str)
            The name of the table.

    Returns:
        str
    """
    if ENV["test_mode"]:
        return f"test_{table_name}"
    else:
        return table_name






# Table Names Dictionary
# This dictionary contains the table names based on the mode the API is running.
TN: ITableNames = {TN: _get_table_name(TN) for TN in (
    "api_errors", 
    "epochs"
)}










## Cursors ## 



# Dict Cursor - Used to retrieve data in a dictionary format that can be accessed
# by column name
DICT_CURSOR: RealDictCursor = RealDictCursor










## Data Adapters ##



# DECIMAL
# Psycopg converts decimal / numeric database types into Python Decimal objects. 
# This adapter convers these values into floats.
DEC2FLOAT = new_type(
    DECIMAL.values,
    "DEC2FLOAT",
    lambda value, curs: float(value) if value is not None else None)
register_type(DEC2FLOAT)




# JSON
# Registers the Json Adapter
register_adapter(dict, Json)







## Database Connection ##




# Connection
# Establishes a connection to the Database based on the environment variables.
CONNECTION: Any = connect(
    host=ENV["POSTGRES_HOST"],
    user=ENV["POSTGRES_USER"],
    password=ENV["POSTGRES_PASSWORD"],
    database=ENV["POSTGRES_DB"],
    port="5432"
)







# Database Cursor
# Initializes a Cursor that is ready to interact with the Database.
#CURSOR: Any = CONNECTION.cursor(cursor_factory=DICT_CURSOR)








# Read Query
# Performs a read database query and returns the results.
def read_query(text: str, values: Optional[Tuple[Any]] = None) -> List[Any]:
    """Executes a read query and returns whatever is returned by the DB Driver.
    
    Args:
        text: str
            The query to be executed.
        values: Optional[Tuple[Any]]
            The tuple of values to be used for the query substitutions.

    Returns:
        List[Any]
    """
    # Init the records
    records: List[Any] = []

    # Handle the case accordingly
    if values:
        with CONNECTION.cursor(name="db_cursor", cursor_factory=DICT_CURSOR) as curs:
            curs.execute(text, values)
            records = curs.fetchall()
    else:
        with CONNECTION.cursor(name="db_cursor", cursor_factory=DICT_CURSOR) as curs:
            curs.execute(text)
            records = curs.fetchall()
    
    # Return the Execution Response
    return records






# Write Query
# Performs a write query on the database.
def write_query(text: str, values: Optional[Tuple[Any]] = None) -> None:
    """Executes a write query as well as commiting the changes. If an error is 
    raised, it will rollback the query.

    Args:
        text: str
            The query to be executed.
        values: Optional[Tuple[Any]]
            The tuple of values to be used for the query substitutions.
    """
    try:
        # Handle the case accordingly
        if values:
            with CONNECTION.cursor(cursor_factory=DICT_CURSOR) as curs:
                curs.execute(text, values)
        else:
            with CONNECTION.cursor(cursor_factory=DICT_CURSOR) as curs:
                curs.execute(text)
        
        # Commit the write action
        CONNECTION.commit()

    # In the case of an error, roll back the execution and re-raise it
    except Exception as e:
        CONNECTION.rollback()
        raise e