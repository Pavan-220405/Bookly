from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    JWT_SECRET_KEY : str
    JWT_ALGORITHM : str
    ACCESS_TOKEN_EXPIRY : int
    REFRESH_TOKEN_EXPIRY : int 
    DATABASE_URL : str 


    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )
settings = Settings()



if __name__ == "__main__":
    print(settings.DATABASE_URL)
    print(settings.DB_NAME)