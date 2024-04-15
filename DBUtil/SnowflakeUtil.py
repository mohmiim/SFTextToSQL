import snowflake.connector
import json


class SnowFlakeUtil:

    def __init__(self, account, user, password, database, schema):
        self.account = account
        self.user = user
        self.password = password
        self.database = database
        self.schema = schema
        self.connection = snowflake.connector.connect(
            user=self.user,
            password=self.password,
            account=self.account,
            database=self.database,
            schema=self.schema
        )
        self.cursor = self.connection.cursor()

    # close the connection
    def close(self):
        self.cursor.close()
        self.connection.close()

    # execute a query
    def execute_query(self, query):
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

