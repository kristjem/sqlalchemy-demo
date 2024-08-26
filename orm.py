from keys import engine
from orm_metadata import User, Address
from typing import List, Tuple
from sqlalchemy import text, select
from sqlalchemy.orm import Session

# About Session() and ORM vs Connection() and Core:
"""
As mentioned previously (see core.py), most of the patterns and examples from Core (core.py) apply to use with the ORM as well.
Core users can skip the ORM sections, but ORM users would best be familiar with these objects from both perspectives.

The fundamental transactional / database interactive object when using the ORM is called the Session. 
In modern SQLAlchemy, this object is used in a manner very similar to that of the Connection (Core), 
and in fact as the Session is used, it refers to a Connection internally which it uses to emit SQL.
"""


def select_x_y_where_y_greater_than_number(number):
    stmt = text("SELECT x, y FROM some_table WHERE y > :y ORDER BY x, y") # parameterized query :y
    with Session(engine) as session:
        result = session.execute(stmt, {"y": number})
        for row in result:
            print(f"x: {row.x}, y: {row.y}")

"""
The example above can be compared to the example in the preceding section in Sending Parameters 
- we directly replace the call to with engine.connect() as conn with with Session(engine) as session, 
and then make use of the Session.execute() method just like we do with the Connection.execute() method.

Also, like the Connection, the Session features “commit as you go” behavior using the Session.commit() method, 
illustrated below using a textual UPDATE statement to alter some of our data:
"""

def commit_as_you_go_session_example():
    with Session(engine) as session:
        result = session.execute(
            text("UPDATE some_table SET y=:y WHERE x=:x"),
            [{"x": 9, "y": 11}, {"x": 13, "y": 15}],
        )
        session.commit()

# Using SELECT Statements
"""
For both Core and ORM, the select() function generates a Select construct which is used for all SELECT queries. 
Passed to methods like Connection.execute() in Core and Session.execute() in ORM, a SELECT statement is emitted 
in the current transaction and the result rows available via the returned Result object.

When using the ORM, particularly with a select() construct that’s composed against ORM entities, we will want to 
execute it using the Session.execute() method on the Session; using this approach, we continue to get Row objects 
from the result, however these rows are now capable of including complete entities, such as instances of the '
User class, as individual elements within each row

Important difference between Core and ORM:
Row objects have only one element, which contain instances of the User class, as opposed to Core, where the
Row objects contain the actual data from the database.
"""

def select_users_from_User_where_name_is(name):
    # See orm_metadata.py for User class
    stmt = select(User).where(User.name == name)
    with Session(engine) as session:
        for row in session.execute(stmt):
            # The actual User object sits at row.User
            user_obj = row.User
            print(f'user: {user_obj}')
            print(f'user.fullname: {user_obj.fullname}')

select_users_from_User_where_name_is("spongebob")

def select_all_from_User() -> List[User]:
    stmt = select(User)
    with Session(engine) as session:
        return [row.User for row in session.execute(stmt)]

def example_use_of_select_all_from_User_then_do_something() -> List[User]:
    """Selects all User objects from the db and returns an altered copy of each User object, as a list."""
    user_objects = select_all_from_User()
    altered_users = map(lambda user: User(name=user.name, fullname=user.fullname + " ALTERED"), user_objects)
    print("Returning altered users:")
    for user in altered_users:
        print(f'Changed fullname to "{user.fullname}", for user {user.name}')
    return altered_users

def select_from_two_tables() -> List[Tuple[str, Address]]:
    """Returns a list of tuples containing User.name (str) and the corresponding Address object."""
    stmt = select(User.name, Address).where(User.id == Address.user_id).order_by(Address.id)
    with Session(engine) as session:
        return session.execute(stmt).all()  
        # .all() returns a list of all rows. Without it, we get a Result object.
        # if we in stead use .first() we get the first row as a Row object.

result_from_two_tables = select_from_two_tables()
print(f'\n{len(result_from_two_tables)} rows returned:\n')
for row in result_from_two_tables:
    print(row)

# TODO: Continue here: Selecting from Labeled SQL Expressions
# https://docs.sqlalchemy.org/en/20/tutorial/data_select.html