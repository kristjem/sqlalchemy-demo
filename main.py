from sqlalchemy import text
from keys import engine

# with engine.connect() as conn:
#     #conn.execute(text("CREATE TABLE some_table (x int, y int)"))
#     conn.execute(
#         text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
#         [{"x": 9, "y": 9}, {"x": 10, "y": 10}],
#     )
#     conn.commit()

with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM some_table"))
    print(result.all())

    