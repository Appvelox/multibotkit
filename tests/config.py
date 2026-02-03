from dotenv import load_dotenv
from pydantic import ConfigDict
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    model_config = ConfigDict(case_sensitive=True)

    TG_TOKEN: str = "some_token"

    VK_TOKEN: str = "vk_token"
    VK_API_VERSION: str = "vk_api_version"

    VIBER_TOKEN: str = "viber_token"

    FB_MESSAGES_ENDPOINT: str = "https://fb_messages.endpoint/"
    FB_PROFILE_ENDPOINT: str = "https://fb_profile.endpoint/"
    FB_PAGE_TOKEN: str = "fb_page_token"

    YANDEX_MESSENGER_TOKEN: str = "test_token"

    MONGO_CONNECTION_URL: str = "mongodb://localhost:27017/"
    REDIS_CONNECTION_URL: str = "redis://localhost/0"


settings = Settings()
