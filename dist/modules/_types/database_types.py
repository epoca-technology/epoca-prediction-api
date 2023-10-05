from typing import TypedDict




# Table Names
# A dict containing the actual names of the database tables based
# on the mode the API is running in.
class ITableNames(TypedDict):
    api_errors: str
    epochs: str