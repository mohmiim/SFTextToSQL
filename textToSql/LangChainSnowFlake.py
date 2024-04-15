import pickle

from langchain_community.utilities.sql_database import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_community.chat_models import ChatOpenAI


class LangChainSnowFlake(object):
    def __init__(self, account, user, password, database, schema, warehouse, role):
        self.snowflake_account = account
        self.username = user
        self.password = password
        self.database = database
        self.schema = schema
        self.warehouse = warehouse
        self.role = role
        snowflake_url = f"snowflake://{self.username}:{self.password}@{self.snowflake_account}/{self.database}/{self.schema}?warehouse={self.warehouse}&role={self.role}"
        db = SQLDatabase.from_uri(snowflake_url, sample_rows_in_table_info=1, view_support=True)
        llm = ChatOpenAI(temperature=0, model_name='gpt-4')
        self.database_chain = create_sql_query_chain(llm, db)

    def to_sql(self, question_string):
        return self.database_chain.invoke({"question": question_string})

