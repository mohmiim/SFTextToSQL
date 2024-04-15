To run this program, you need to install the libraries in the `requirements.txt` file. You can do this by running the following command in the terminal:

### `pip install -r requirements.txt`

Also, the program expects these environment variables to be set:

- `OPENAI_API_KEY`: the API key for OpenAI
- `SF_ACCOUNT`: the account name for Snowflake
- `SF_USER`: the user name for Snowflake
- `SF_PASSWORD`: the password for Snowflake
- `SF_WH`: the warehouse name for Snowflake
- `SF_DB`: the database name for Snowflake
- `SF_SCHEMA`: the schema name for Snowflake
- `SF_ROLE`: the role name for Snowflake

The main file has a few questions to play with. The questions are based on Snowflake DB: SEC_FILINGS and Schema CYBERSYN, but you should be able to use whatever DB/Schemas you have access to.

Sample Question:

What are the top 10 measure descriptions by frequency?

Generated SQL:

```sql
SELECT measure_description, COUNT(*) AS frequency
FROM sec_report_attributes
GROUP BY measure_description
ORDER BY frequency DESC
LIMIT 10;
```

Output:

| Measure Description | Frequency   |
|---------------------|-------------|
| Ending balance      | 2,001,529   |
| Beginning balance   | 1,956,090   |
| Total               | 1,780,837   |
| Revenues            | 1,525,333   |
| Net income          | 1,367,210   |
| Revenue             | 1,281,254   |
| Net sales           | 1,189,114   |
| Balance             | 1,149,603   |
| Net loss            |   991,917   |
| Loans               |   869,803   |

