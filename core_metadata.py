from keys import engine
from typing import List
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String, ForeignKey


# Working with Database Metadata - SQL Expression Language
"""
READ: https://docs.sqlalchemy.org/en/20/tutorial/metadata.html

The central element of both SQLAlchemy Core and ORM is the "SQL Expression Language" which allows for fluent, 
composable construction of SQL queries. The foundation for these queries are Python objects that represent 
database concepts like tables and columns. These objects are known collectively as database metadata.

The most common foundational objects for database metadata in SQLAlchemy are known as:
* MetaData
* Table
* Column

To start using the SQLAlchemy Expression Language, we will want to have Table objects constructed that 
represent all of the database tables we are interested in working with. The Table is constructed programmatically, 
either directly by using the Table constructor, or indirectly by using ORM Mapped classes, optionally 
load some or all table information from an existing database (called reflection).

Whichever kind of approach is used, we always start out with a collection that will be where we place our 
tables known as:
* the MetaData object.
Once we have a MetaData object, we can declare some Table objects.

Having a single MetaData object for an entire application is the most common case, 
represented as a module-level variable in a single place in an application, often in a “models” or “dbschema” type of package.
MetaData is a container object that holds information about tables and their associated columns, etc.
* This is a simplifyed structure of a MetaData object:
MetaData:
    -> Table A
        ---> Column
        ---> Column
    -> Table B
        ---> Column
        ---> Column
    ...
"""

metadata_obj = MetaData()

user_table = Table(
    "user_account",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("fullname", String(255)),
)

"""
With the above example, when we wish to write code that refers to the user_account table in the database, 
we will use the user_table Python variable to refer to it. Columns are accessed as attributes of the Table object,
using "c" as a namespace for "column": user_table.c.id, user_table.c.name, etc. 

* Example of how to get the column headers:
>>> user_table.c.keys()
['id', 'name', 'fullname']

* Example of getting primary_key info:
>>> user_table.primary_key
PrimaryKeyConstraint(Column('id', Integer(), table=<user_account>, primary_key=True, nullable=False))
"""

# Declaring Simple Constraints: ForeignKeyConstraint
"""
A ForeignKeyConstraint that involves only a single column on the target table is typically declared using a 
column-level shorthand notation via the ForeignKey object. Below we declare a second table address that will 
have a foreign key constraint referring to the user table.

    *Tip:
    When using the ForeignKey object within a Column definition, we can omit the datatype for that Column; 
    it is automatically inferred from that of the related column, in the above example the Integer datatype 
    of the user_account.id column.
"""

address_table = Table(
    "address",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("user_account.id"), nullable=False),
    Column("email_address", String(255), nullable=False),
)

# Not nullable constraint
"""
The table above also features a another kind of constraint, which in SQL is the “NOT NULL” constraint, 
indicated above using the Column.nullable parameter.
"""

# Example of getting all tables and their columns from the metadata object:
"""
>>> print(metadata_obj.tables)
FacadeDict(
	{'user_account': 
		Table(
			'user_account', MetaData(), 
				Column('id', Integer(), table=<user_account>, primary_key=True, nullable=False), 
				Column('name', String(length=30), table=<user_account>), 
				Column('fullname', String(), table=<user_account>), schema=None), 
	'address': 
		Table(
			'address', MetaData(), 
				Column('id', Integer(), table=<address>, primary_key=True, nullable=False), 
				Column('user_id', Integer(), ForeignKey('user_account.id'), table=<address>, nullable=False), 			
				Column('email_address', String(), table=<address>, nullable=False), schema=None)
	}
)
"""

# Create all tables in the metadata object, in our database (engine):
"""
We'll invoking the MetaData.create_all() method on our MetaData, sending it the Engine that refers to the target database:
"""
def create_all_tables_in_database(engine):
    metadata_obj.create_all(engine)

def drop_all_metadata_tables_from_db(engine=engine):
   """Any tables in the engine database that are NOT in the metadata object will not be affected"""
   metadata_obj.drop_all(engine)


# Reflecting Database Objects
"""
How to generate Table objects automatically from an existing database (called "table reflection" in SQLAlchemy).

* Tip: 
    There is no requirement that reflection must be used in order to use SQLAlchemy with a pre-existing database. 
    It is entirely typical that the SQLAlchemy application declares all metadata explicitly in Python, such that 
    its structure corresponds to that the existing database. The metadata structure also need not include tables, 
    columns, or other constraints and constructs in the pre-existing database that are not needed for the local 
    application to function.
* Read more: https://docs.sqlalchemy.org/en/20/core/reflection.html
* To do it the ORM way, see https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-declarative-reflected
"""
some_table = Table("some_table", metadata_obj, autoload_with=engine)

"""
The 'some_table' object now contains the information about the Column objects present in the table, 
and the object is usable in exactly the same way as a Table that we declared explicitly:

>>> some_table
Table('some_table', MetaData(),
    Column('x', INTEGER(), table=<some_table>),
    Column('y', INTEGER(), table=<some_table>),
    schema=None)

>>> print(some_table.c.keys())
['x', 'y']
"""


