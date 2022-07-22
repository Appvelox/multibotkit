from pydantic import BaseSettings


class Settings(BaseSettings):

    TG_TOKEN: str = "tg_token"

    VK_TOKEN: str = "vk_token"
    VK_API_VERSION: str = "vk_api_version"

    VIBER_TOKEN: str = "viber_token"

    FB_MESSAGES_ENDPOINT: str = "https://fb_messages.endpoint/"
    FB_PROFILE_ENDPOINT: str = "https://fb_profile.endpoint/"
    FB_PAGE_TOKEN: str = "fb_page_token"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
