from keys import engine
from sqlalchemy import text
from typing import List, Dict

# About the Enging and Connection:
"""
The purpose of the Engine is to connect to the database by providing a Connection object. 
When working with the Core directly, the Connection object is how all interaction with the database is done. 
Because the Connection creates an open resource against the database, we want to limit our use of this object 
to a specific context. The best way to do that is with a Python context manager, also known as the with statement.
"""

# About the 'text()' construct:
"""
...textual SQL is the exception rather than the rule in day-to-day SQLAlchemy use, but it's always available

However, when using textual SQL, a Python literal value, even non-strings like integers or dates, 
should never be stringified into SQL string directly; a parameter should always be used 
(see example below: `select_all_from_some_table_where_x_is()` in core.py). This is most 
famously known as how to avoid SQL injection attacks when the data is untrusted. However it also allows 
the SQLAlchemy dialects and/or DBAPI to correctly handle the incoming input for the backend. Outside of 
plain textual SQL use cases, SQLAlchemy’s Core Expression API otherwise ensures that Python literal values 
are passed as bound parameters where appropriate.
"""

def create_some_table():
    with engine.connect() as conn:
        conn.execute(text("CREATE TABLE IF NOT EXISTS some_table (x int, y int)"))
        conn.commit()

# "commit as you go"
def insert_into_some_table_commit_as_you_go(x:int, y:int):
    """Please see: insert_into_some_table_begin_once()
    The code below is only committed to the database after conn.commit() is called!"""
    with engine.connect() as conn:
        conn.execute(text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
                     {"x": x, "y": y}, # This is a parameterized query, its purpose is to prevent SQL injection
                     )
        conn.commit()

# "begin once"
def insert_into_some_table_begin_once(x:int, y:int):
    """This is prefered over "comit as you go" because:
    - its shorter and more readable.
    - it shows up front that the operation is a transaction.
    - no need to call conn.commit()
    """
    with engine.begin() as conn:
        conn.execute(
            text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
            {"x": x, "y": y}
        )


def select_all_from_table(table:str) -> list:
    """
    The object returned is called <b>Result</b> and represents an iterable object of result rows.<br>
    
    Result has lots of methods for fetching and transforming rows, such as the 
    Result.all() method, which returns a list of all Row objects. It also implements 
    the Python iterator interface so that we can iterate over 
    the collection of <b>Row</b> objects directly.<br>

    The Row objects themselves are intended to act like Python named tuples, there are 
    a variety of ways to access rows. 
    ### Example:
    Assuming: `result = conn.execute(text("select x, y from some_table"))`

    `for x, y in result:`
    or <br>
    `for row in result:
    x = row[0]`
    or <br>
    `for row in result:
    y = row.y`<br>
    <i>For immutable results, use the result.mappings()</i>
    """

    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT * FROM {table}"))
        return result.all()

def select_all_from_some_table_where_x_is(parameter:int) -> list:
    """Using the `some_table` table. Demonstrating parameterized queries"""
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM some_table WHERE x = :x"), 
                              {"x": parameter})
        return result.all()

def execute_many_inserts_using_a_list_of_dictionaries():
    """Inserting many rows at once using a list of dictionaries<br>
    The below operation is equivalent to running the given INSERT statement 
    once for each parameter set (each dictionary in `data`), except that the operation will be optimized 
    for better performance across many rows.<br>
    
    A key behavioral difference between “execute” and “executemany” is that 
    the latter doesn’t support returning of result rows (with some exaceptions).
    """
    data = [{"x": 95, "y": 45}, {"x": 74, "y": 34}]
    with engine.connect() as conn:
        conn.execute(text("INSERT INTO some_table (x, y) VALUES (:x, :y)"), data)
        conn.commit()

execute_many_inserts_using_a_list_of_dictionaries()
# print(select_all_from_some_table_where_x_is(10))


res = select_all_from_table("some_table")
for row in res:
    print(f"x: {row.x}  y: {row.y}")


