from pydantic import BaseSettings


class Settings(BaseSettings):
    
    TG_TOKEN: str

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()