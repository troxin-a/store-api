from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    postgres_host: str
    postgres_port: int
    postgres_user: str
    postgres_password: str
    postgres_db: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def url(self):
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@"
            f"{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


class Settings(BaseSettings):
    db: DatabaseSettings = DatabaseSettings()

    title: str = "My project"
    version: str = "0.1.0"


settings = Settings()
