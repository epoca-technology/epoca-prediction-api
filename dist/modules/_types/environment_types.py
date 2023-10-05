from typing import TypedDict




# Environment Variables
class IEnvironment(TypedDict):
    production: bool 
    test_mode: bool 
    debug_mode: bool 
    restore_mode: bool 
    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    FLASK_SECRET_KEY: str
    PORT: int