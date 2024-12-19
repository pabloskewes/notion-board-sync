from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Notion API
    NOTION_API_KEY: str
    NOTION_DATABASE_ID: str

    # Slack API
    SLACK_BOT_TOKEN: str
    SLACK_CHANNEL_ID: str

    # Logging
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"


settings = Settings()

if __name__ == "__main__":
    print("Notion API Key:", settings.NOTION_API_KEY)
    print("Notion Database ID:", settings.NOTION_DATABASE_ID)
    print("Slack Bot Token:", settings.SLACK_BOT_TOKEN)
    print("Slack Channel ID:", settings.SLACK_CHANNEL_ID)
    print("Log Level:", settings.LOG_LEVEL)
