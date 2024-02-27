from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///zd07.db")
Session = sessionmaker(bind=engine)
session = Session()
