from sqlalchemy import text
from keys import engine

# About the 'text()' construct:
"""
...textual SQL is the exception rather than the rule in day-to-day SQLAlchemy use, but it's always available
"""

def create_some_table():
    with engine.connect() as conn:
        conn.execute(text("CREATE TABLE IF NOT EXISTS some_table (x int, y int)"))
        conn.commit()

def insert_into_some_table(x:int, y:int):
    with engine.connect() as conn:
        conn.execute(text(f"INSERT INTO some_table (x, y) VALUES ({x}, {y})"))
        conn.commit()

def select_all_from_table(table:str) -> list:
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT * FROM {table}"))
        return result.all()

res = select_all_from_table("some_table")
print(res)




