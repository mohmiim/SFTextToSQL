import pickle
from operator import itemgetter

from langchain_community.utilities.sql_database import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ChatMessageHistory

DEBUG = False


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
        if DEBUG:
            print(db.dialect)
            print(db.get_usable_table_names())
            print(db.table_info)
        llm = ChatOpenAI(temperature=0, model_name='gpt-4')
        self.database_chain = create_sql_query_chain(llm, db)
        self.execute_query = QuerySQLDataBaseTool(db=db)

        ## answer rephrase
        answer_prompt = PromptTemplate.from_template(
            """ 
            Given the following question, and raw data representing the answer, answer the user question in {language}. Treat None as empty or 0 depending on the context.

        Question: {question}
        SQL Result: {result}
        Answer: """
        )
        rephrase_answer = answer_prompt | llm | StrOutputParser()
        self.chain = (
                RunnablePassthrough.assign(query=self.database_chain).assign(
                    result=self.execute_query
                )
                | rephrase_answer
        )

    def to_sql(self, question_string):
        return self.database_chain.invoke({"question": question_string})

    def to_sql_and_run(self, question_string):
        return self.chain.invoke({"question": question_string, "language": "English"})
