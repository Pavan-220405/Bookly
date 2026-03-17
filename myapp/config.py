from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST : str 
    DB_PORT : str 
    DB_NAME : str 
    DATABASE_URL : str 


    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )
settings = Settings()



if __name__ == "__main__":
    print(settings.DATABASE_URL)
    print(settings.DB_NAME)