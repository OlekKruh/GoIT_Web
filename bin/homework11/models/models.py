from sqlalchemy import Column, Integer, String, Date, Table, MetaData

metadata = MetaData()

contacts = Table(
    "contacts",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("first_name", String, nullable=False),
    Column("last_name", String, nullable=False),
    Column("email", String, nullable=False, unique=True, index=True),
    Column("phone_number", String, nullable=False),
    Column("birth_date", Date, nullable=False),
    Column("additional_info", String, nullable=True),
)
