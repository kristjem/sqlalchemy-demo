from keys import engine
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase

from typing import List
from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

def opening_notes_long_read() -> None:
    # Note from Copilot:
    """
    When using an object-oriented programming (OOP) style, it is generally preferred to use the ORM (Object-Relational Mapping) 
    part of SQLAlchemy. The ORM provides a more intuitive and Pythonic way to interact with the database by mapping database 
    tables to Python classes. This allows you to work with database records as if they were regular Python objects, making the 
    code more readable and maintainable.

    Here are some reasons why using the ORM is preferred in an OOP context:

    Encapsulation: The ORM allows you to encapsulate database logic within classes, making it easier to manage and reuse code.
    Abstraction: It abstracts away the SQL queries, allowing you to interact with the database using Python objects and methods.
    Type Safety: The ORM can provide type safety and better integration with static analysis tools like Mypy.
    Declarative Syntax: The declarative syntax of the ORM is more concise and aligns well with OOP principles.
    Relationships: The ORM makes it easier to define and work with relationships between tables using class attributes.
    """

    # PLEASE ALSO SEE core_metadata.py FOR COMPARISSON
    """
    Another way to make Table objects?

    The preceding examples illustrated direct use of the Table object, which underlies how SQLAlchemy ultimately 
    refers to database tables when constructing SQL expressions. The SQLAlchemy ORM provides for a facade around 
    the Table declaration process referred towards as "Declarative Table". 

    The Declarative Table process accomplishes the same goal as we had in the previous section (see core_metadata.py), 
    that of building Table objects, but also within that process gives us something else called an ORM mapped class, 
    or just “mapped class”. 

    The mapped class is the most common foundational unit of SQL when using the ORM, and in modern SQLAlchemy can also 
    be used quite effectively with Core-centric use as well.

    Some benefits of using Declarative Table include:
        * A more succinct ("kortfattet") and Pythonic style of setting up column definitions, 
        * where Python types may be used to represent SQL types to be used in the database

        * The resulting mapped class can be used to form SQL expressions that in many cases maintain 
        * PEP 484 typing information that's picked up by static analysis tools such as Mypy and IDE type checkers

        * Allows declaration of table metadata and the ORM mapped class used in persistence / object loading operations all at once.

    This section will illustrate the same Table metadata of the previous section(s) (see core_metadata.py) being constructed using 
    * Declarative Table.

    When using the ORM, the process by which we declare Table metadata is usually combined with the process of declaring 
    mapped classes. The mapped class is any Python class we'd like to create, which will then have attributes on it that 
    will be linked to the columns in a database table. While there are a few varieties of how this is achieved, the most 
    common style is known as declarative, and allows us to declare our user-defined classes and Table metadata at once.
    """

    # Establishing a Declarative Base
    """
    When using the ORM, the MetaData collection remains present, however it itself is associated with an ORM-only 
    construct commonly referred towards as the Declarative Base. The most expedient way to acquire a new 
    Declarative Base is to create a new class that subclasses the SQLAlchemy DeclarativeBase class:
    

    class Base(DeclarativeBase):
        pass

    
    Above, the Base class is what we'll call the Declarative Base. When we make new classes that are subclasses of Base, 
    combined with appropriate class-level directives, they will each be established as a new ORM mapped class at class 
    creation time, each one typically (but not exclusively) referring to a particular Table object.

    The Declarative Base refers to a MetaData collection that is created for us automatically, assuming we didn't provide 
    one from the outside. This MetaData collection is accessible via the DeclarativeBase.metadata class-level attribute. 
    As we create new mapped classes, they each will reference a Table within this MetaData collection:

    >>> Base.metadata
    MetaData()
    """

"""
* About DeclarativeBase:
The class Base(DeclarativeBase) acts as a foundational class for all ORM-mapped classes in SQLAlchemy, 
providing them with essential metadata and functionality for database interactions. Your custom classes 
inherit from Base, automatically gaining the capabilities needed to interact with the database.
"""
class Base(DeclarativeBase):
    pass


# Declaring Mapped Classes¶
"""
With the Base class established, we can now define ORM mapped classes for the user_account and address 
tables in terms of the two new classes:
* User 
* Address
We illustrate below the most modern form of Declarative, which is driven from PEP 484 type annotations 
using a special type Mapped, which indicates attributes to be mapped as particular types:
"""

class User(Base):
    """
    ### Example / break down:
    `name: Mapped[str] = mapped_column(String(30))`
    <br><br>
        * `name` is the name of the attribute in the class.<br>
        * `Mapped[str]` is a type hint that indicates the type of the attribute.<br>
        * `mapped_column(String(30))` is a SQLAlchemy function that sets the column property in the database table.<br>
    """
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]] = mapped_column(String(255))
    addresses: Mapped[List["Address"]] = relationship(back_populates="user")
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str] = mapped_column(String(255))
    user_id = mapped_column(ForeignKey("user_account.id"))
    user: Mapped[User] = relationship(back_populates="addresses")
    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"
    
def create_all_tables_in_database(engine):
    Base.metadata.create_all(engine)

