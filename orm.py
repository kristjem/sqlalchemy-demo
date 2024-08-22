from keys import engine
from sqlalchemy import text
from sqlalchemy.orm import Session

# About Session() and ORM vs Connection() and Core:
"""
As mentioned previously (see core.py), most of the patterns and examples from Core (core.py) apply to use with the ORM as well.
The fundamental transactional / database interactive object when using the ORM is called the Session. 
In modern SQLAlchemy, this object is used in a manner very similar to that of the Connection (Core), 
and in fact as the Session is used, it refers to a Connection internally which it uses to emit SQL.
"""

stmt = text("SELECT x, y FROM some_table WHERE y > :y ORDER BY x, y")
with Session(engine) as session:
    result = session.execute(stmt, {"y": 6})
    for row in result:
        print(f"x: {row.x}, y: {row.y}")