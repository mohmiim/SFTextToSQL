# This is a sample Python script.
import sys

from DBUtil.SnowflakeUtil import SnowFlakeUtil
from textToSql.LangChainSnowFlake import LangChainSnowFlake
import os

# Q = "How many companies are there in the dataset? Use the fully qualified table name"
# Q = "How many companies are there in the dataset?"
# Q = "What are the top 10 measure descriptions by frequency?"
# Q = "What are the distinct statements in the report attributes?"
# Q = "What are the top 10 measures in the Income Statement?"
# Q = "What are the top 10 measures in the Balance Sheet?"
# Q = "What are the top 10 measures in the Cover Page? Use the measure description"
# Q = "What are the distinct metadata types for Net sales for Apple?"
Q = "What annual measures are available from the 'NIKE INC' Income Statement?"
# Q = "What's the distinct metadata in Alphabet's Income Statement?"
# Q = "What are the annual 'Revenues' by 'BusinessSegments' for Alphabet?"
# Q = "What are the quarterly revenues by business segment for Alphabet?"
# Q = "What income statement metrics are available for Tesla?"
# Q = "What are the quarterly 'Automotive sales' and 'Automotive leasing' for Tesla?"
# Q = "What are the most frequent balance sheet measures for SIC description 'NATIONAL COMMERCIAL BANKS'?"
# Q = "How many airline companies are there?"
# Q = "What's the most recent number of Chipotle restaurants?"
# Q = "How many Chipotle restaurants are there currently?"
# Q = "What metrics are available for Apple?"
# Q = "What were Apple's total revenues each quarter?"

ACCOUNT = os.environ['SF_ACCOUNT']
USERNAME = os.environ['SF_USER']
PASSWORD = os.environ['SF_PASSWORD']
DB = os.environ['SF_DB']
SCHEMA = os.environ['SF_SCHEMA']
WH = os.environ['SF_WH']
ROLE = os.environ['SF_ROLE']

snowFL = SnowFlakeUtil(ACCOUNT, USERNAME, PASSWORD, DB, SCHEMA)
snowFlkSQL = LangChainSnowFlake(ACCOUNT, USERNAME, PASSWORD, DB, SCHEMA, WH, ROLE)
sql = snowFlkSQL.to_sql_and_run(Q)
#sql = snowFlkSQL.to_sql(Q)
print(sql)
#print(snowFL.execute_query(sql))

snowFL.close()
