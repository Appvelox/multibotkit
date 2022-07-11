from pydantic import BaseSettings


class Settings(BaseSettings):
    
    TG_TOKEN: str = ""

    VK_TOKEN: str = ""
    VK_API_VERSION: str = ""

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()