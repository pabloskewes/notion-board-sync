from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # Notion API
    notion_api_key: str = Field(..., env="NOTION_API_KEY")
    notion_database_id: str = Field(..., env="NOTION_DATABASE_ID")

    # Slack API
    slack_bot_token: str = Field(..., env="SLACK_BOT_TOKEN")
    slack_channel_id: str = Field(..., env="SLACK_CHANNEL_ID")

    # Logging
    log_level: str = Field("INFO", env="LOG_LEVEL")

    class Config:
        env_file = ".env"


settings = Settings()

if __name__ == "__main__":
    print("Notion API Key:", settings.notion_api_key)
    print("Notion Database ID:", settings.notion_database_id)
    print("Slack Bot Token:", settings.slack_bot_token)
    print("Slack Channel ID:", settings.slack_channel_id)
    print("Log Level:", settings.log_level)
