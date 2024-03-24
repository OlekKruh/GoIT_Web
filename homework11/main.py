from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from homework11.src import schemas
from homework11.src.database.db import get_db
from homework11.src.crud.crud_contact import create_contact, get_contacts, get_contact, delete_contact, update_contact

app = FastAPI()


@app.post("/contacts/", response_model=schemas.Contact, status_code=status.HTTP_201_CREATED)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    return create_contact(db=db, contact=contact)


@app.get("/contacts/", response_model=List[schemas.Contact])
def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_contacts(db, skip=skip, limit=limit)


@app.get("/contacts/{contact_id}", response_model=schemas.Contact)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = get_contact(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


@app.put("/contacts/{contact_id}", response_model=schemas.Contact)
def update_contact(contact_id: int, contact: schemas.ContactUpdate, db: Session = Depends(get_db)):
    db_contact = update_contact(db, contact_id, contact)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


@app.delete("/contacts/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    delete_contact(db, contact_id)
    return {"detail": "Contact deleted"}
