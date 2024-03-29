from dotenv import load_dotenv

from pydantic import BaseSettings


load_dotenv()


class Settings(BaseSettings):

    TG_TOKEN: str = "some_token"

    VK_TOKEN: str = "vk_token"
    VK_API_VERSION: str = "vk_api_version"

    VIBER_TOKEN: str = "viber_token"

    FB_MESSAGES_ENDPOINT: str = "https://fb_messages.endpoint/"
    FB_PROFILE_ENDPOINT: str = "https://fb_profile.endpoint/"
    FB_PAGE_TOKEN: str = "fb_page_token"

    MONGO_CONNECTION_URL: str
    REDIS_CONNECTION_URL: str

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
