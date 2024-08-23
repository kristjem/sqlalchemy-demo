from keys import engine
from sqlalchemy import text
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

