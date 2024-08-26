from keys import engine
from core_metadata import user_table, address_table
from sqlalchemy import text
from sqlalchemy import insert, select, bindparam
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
    """
    This is a very simple example, without using metadata objects, but raw SQL.
    See the example in metadata_core.py for 'reflecting' the table from the database, 
    making a metadata object of the 'some_table' table, which is then usable in exactly 
    the same way as a Table that we declare explicitly
    """
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

def show_all_tables_in_database(engine=engine):
    with engine.connect() as conn:
        # Print all MySQL tables in the database:
        result = conn.execute(text("SHOW TABLES"))
        print(result.all())

# show_all_tables_in_database()
def insert_into_user_table(name:str, fullname:str):
    """
    This uses the metadata object `user_table` from core_metadata.py as opoosed to raw SQL.<br> 
    See: https://docs.sqlalchemy.org/en/20/tutorial/data_insert.html"""
    stmt = insert(user_table).values(name=name, fullname=fullname)
    # print(stmt)

    with engine.connect() as conn:
        conn.execute(stmt)
        conn.commit()

def insert_many_into_user_table(data:List[Dict[str, str]]):
    """
    This uses the metadata object `user_table` from core_metadata.py as opoosed to raw SQL.<br> 
    See: https://docs.sqlalchemy.org/en/20/tutorial/data_insert.html"""
    stmt = insert(user_table)
    # print(stmt)

    with engine.connect() as conn:
        # statement, parameters
        conn.execute(stmt, data) # see list_of_dicts_containing_users below
        conn.commit()

"""
The execution above features “executemany” form first illustrated at Sending Multiple Parameters (link below), however unlike 
when using the text() construct, we didn't have to spell out any SQL. By passing a dictionary OR list of dictionaries 
to the Connection.execute() method in conjunction with the Insert construct, the Connection ensures that the column 
names which are passed will be expressed in the VALUES clause of the Insert construct automatically.

https://docs.sqlalchemy.org/en/20/tutorial/dbapi_transactions.html#tutorial-multiple-parameters
"""

list_of_dicts_containing_users = [
    {"name": "ed", "fullname": "Ed Jones"},
    {"name": "wendy", "fullname": "Wendy Williams"},
    {"name": "mary", "fullname": "Mary Contrary"},
    {"name": "fred", "fullname": "Fred Flintstone"},
    {"name": "sandy", "fullname": "Sandy Cheeks"},
    {"name": "patrick", "fullname": "Patrick Star"},
]



def insert_into_address_table():
    """
    The scalar_subq is supposed to return a single user_id for each username. However, if there are 
    multiple users with the same username, the subquery will return multiple rows, causing an error.
    I have no constraint on the username column in the user_table, so this is possible. Adding the
    .limit(1) method to the subquery will make sure that only one row is returned for each username.
    """

    scalar_subq = (
        select(user_table.c.id)
        .where((user_table.c.name == bindparam("username")))
        .limit(1) # Makes sure only one row pr. username is returned
        .scalar_subquery()
    )

    with engine.connect() as conn:
        result = conn.execute(
            insert(address_table).values(user_id=scalar_subq),
            [
                {
                    "username": "spongebob",
                    "email_address": "spongebob@sqlalchemy.org",
                },
                {"username": "sandy", "email_address": "sandy@sqlalchemy.org"},
                {"username": "sandy", "email_address": "sandy@squirrelpower.org"},
            ],
        )
        conn.commit()


def delete_data_from_user_account_table_where_user_id_is(user_id:int):
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM user_account WHERE id = :user_id"), {"user_id": user_id})
        conn.commit()



def show_users_and_addresses_in_database():
    users_res = select_all_from_table("user_account")
    for row in users_res:
        print(f'user_account: {row}')

    adress_res = select_all_from_table("address")
    for row in adress_res:
        print(f'address: {row}')

# show_all_tables_in_database()
# show_users_and_addresses_in_database()

# for row in select_all_from_table("user_account"):
#     print(f'user_account: {row}')

# for row in select_all_from_table("address"):
#     print(f'address: {row}')

# Using SELECT Statements
"""
For both Core and ORM, the select() function generates a Select construct which is used for all SELECT queries. 
Passed to methods like Connection.execute() in Core and Session.execute() in ORM, a SELECT statement is emitted 
in the current transaction and the result rows available via the returned Result object.

Important difference between Core and ORM:
Row objects have only one element, which contain instances of the User class, as opposed to Core, where the
Row objects contain the actual data from the database.
"""
def select_all_from_user_table_where_name_is(name:str):
    stmt = select(user_table).where(user_table.c.name == name)
    with engine.connect() as conn:
        for row in conn.execute(stmt):
            print(row)

def select_spesified_columns_from_user_table_where_name_is(name:str):
    """
    Multiple columns may be specified for a select() by using a tuple of strings representing the column names
    ### Example:
    Note: this must be used if the column names contian spaces or special characters.<br>
    `select(user_table.c["name", "fullname"])`<br>
    in stead of <br>
    `select(user_table.c.name, user_table.c.fullname)`<br>
    """
    stmt = select(user_table.c["name", "fullname"]).where(user_table.c.name == name)
    with engine.connect() as conn:
        for row in conn.execute(stmt, {"name": name}):
            print(row)

select_spesified_columns_from_user_table_where_name_is("spongebob")