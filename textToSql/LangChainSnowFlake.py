from langchain.chains.openai_tools import create_extraction_chain_pydantic
from langchain_community.chat_message_histories.in_memory import ChatMessageHistory
from langchain_community.utilities.sql_database import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_core.prompts import FewShotChatMessagePromptTemplate, ChatPromptTemplate, PromptTemplate, \
    MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings
from langchain_core.pydantic_v1 import BaseModel, Field


class Table(BaseModel):
    """Table in SQL database."""

    name: str = Field(description="Name of table in SQL database.")


DEBUG = False


class LangChainSnowFlake(object):

    def __init__(self, account, user, password, database, schema, warehouse, role):
        self.chain = None
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
        # default
        self.database_chain = create_sql_query_chain(llm, db)
        self.execute_query = QuerySQLDataBaseTool(db=db)
        if DEBUG:
            print(self.database_chain.get_prompts()[0].pretty_print())

        prompt_with_history = ChatPromptTemplate.from_messages(
            [
                ("system",
                 """ Given an input question, first create a syntactically correct snowflake query to run, then look at the results of the query and return the answer. Unless the user specifies in his question a specific number of examples he wishes to obtain, always limit your query to at most 5 results. You can order the results by a relevant column to return the most interesting examples in the database.
Never query for all the columns from a specific table, only ask for a the few relevant columns given the question.
Pay attention to use only the column names that you can see in the schema description. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
Use the following format:
Question: Question here
SQLQuery: SQL Query to run
SQLResult: Result of the SQLQuery
Answer: Final answer here
Only use the following tables:
{table_info}
{top_k}
Question: {input}
"""),
                MessagesPlaceholder(variable_name="messages"),
                ("human", "{input}"),
            ]
        )
        self.history = ChatMessageHistory()
        self.generate_query = create_sql_query_chain(llm, db, prompt_with_history)
        self.rephrase_prompt(llm)

    def rephrase_prompt(self, llm):
        answer_prompt = PromptTemplate.from_template(
            """ 
            Given the following question, and raw data representing the answer, answer the user question in {language}. Treat None as empty or 0 depending on the context.

        Question: {question}
        SQL Result: {result}
        Answer: """
        )
        rephrase_answer = answer_prompt | llm | StrOutputParser()
        self.chain = (
                RunnablePassthrough.assign(query=self.generate_query).assign(
                    result=self.execute_query
                )
                | rephrase_answer
        )

    def to_sql(self, question_string):
        return self.database_chain.invoke({"question": question_string})

    def to_sql_and_run(self, question_string):
        results = self.chain.invoke(
            {"question": question_string, "language": "English", "messages": self.history.messages})
        self.history.add_user_message(question_string)
        self.history.add_ai_message(results)
        return results
