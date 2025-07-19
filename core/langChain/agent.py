from langchain.chat_models import ChatOpenAI
from langchain_experimental.sql import SQLDatabaseChain  # Ensure this is installed
from .db_langchain import get_langchain_db

def get_sql_agent(verbose=False):
    db = get_langchain_db()  # Get the SQL database connection
    llm = ChatOpenAI(temperature=0)  # Initialize the language model
    # Create an SQLDatabaseChain
    agent = SQLDatabaseChain.from_llm(llm=llm, db=db, verbose=verbose)  # Use 'db' instead of 'database'
    return agent

    