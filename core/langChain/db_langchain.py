from langchain.sql_database import SQLDatabase

from app.config import config  # استورد الإعدادات لديك (أو BaseConfig مباشرة)

def get_langchain_db() -> SQLDatabase:
    """
    ينشئ اتصال LangChain مع PostgreSQL باستخدام نفس URI الموجود لديك
    """
    return SQLDatabase.from_uri(config.SQLALCHEMY_DATABASE_URL)
