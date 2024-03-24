from fastapi import FastAPI
from homework11.src.routes import contacts

app = FastAPI()

app.include_router(contacts.router, prefix='/api')

