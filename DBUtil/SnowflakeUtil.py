import snowflake.connector
import json


class SnowFlakeUtil:

    table_description = "Table Name: {table_name} \nTable Description: {table_description}\n"

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

    # get the schema
    def get_schema(self):
        self.cursor.execute("SHOW SCHEMAS")
        self.schema = self.cursor.fetchall()
        return self.schema

    # get the views
    def get_views(self):
        self.cursor.execute(f"SHOW VIEWS")
        views = self.cursor.fetchall()
        return views

    def get_schema_description(self):
        schema_str = ""
        schema = self.get_schema()
        views = self.get_views()
        for view in views:
            schema_str += self.table_description.format(table_name=view[1], table_description=view[6])
        return schema_str


