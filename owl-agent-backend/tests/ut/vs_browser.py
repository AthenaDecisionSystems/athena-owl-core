"""
verify content of vector store as it is persisted in sqllite
"""
import sqlite3

def get_cursor():
    conn = sqlite3.connect("./tests/ut/chromadb/chroma.sqlite3")
    cursor = conn.cursor()
    return conn, cursor

def list_all_tables(cursor):
    # Execute the query to get the list of tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    # Fetch all the table names
    tables = cursor.fetchall()
    for table in tables:
        print(table[0])

def get_coll_table_schema(cursor, table_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    table_info = cursor.fetchall()

    # Print the table schema
    for column in table_info:
        cid, name, type, notnull, default_value, pk = column
        print(f"Column {cid}: '{name}' ({type}) {'NOT NULL' if notnull else 'NULL'} {'PRIMARY KEY' if pk else ''}")

def list_records_in_table(cursor,table_name):
    res = cursor.execute(f"SELECT * FROM {table_name}")
    r=res.fetchone()
    print(r)

conn, cursor = get_cursor()
get_coll_table_schema(cursor,"collections")
list_records_in_table(cursor,"collections")
get_coll_table_schema(cursor,"embedding_fulltext_search_data")
list_records_in_table(cursor,"embedding_fulltext_search_data")

get_coll_table_schema(cursor,"embedding_fulltext_search_content")
list_records_in_table(cursor,"embedding_fulltext_search_content")


get_coll_table_schema(cursor,"embedding_fulltext_search")
list_records_in_table(cursor,"embedding_fulltext_search")

get_coll_table_schema(cursor,"embeddings")
list_records_in_table(cursor,"embeddings")
# Close the database connection
conn.close()