from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from ..crud import crud_contact
from ..database.db import get_db
from ..schemas import ContactCreate, ContactUpdate, Contact
from ..repository import contacts as contacts_repository

router = APIRouter()


@router.post("/", response_model=Contact)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    return contacts_repository.create_contact(db=db, contact=contact)


@router.get("/", response_model=List[Contact])
def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contacts = contacts_repository.get_contacts(db, skip=skip, limit=limit)
    return contacts


@router.get("/{contact_id}", response_model=Contact)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = contacts_repository.get_contact(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


@router.put("/{contact_id}", response_model=Contact)
def update_contact(contact_id: int, contact: ContactUpdate, db: Session = Depends(get_db)):
    return contacts_repository.update_contact(db=db, contact_id=contact_id, contact=contact)


@router.delete("/{contact_id}", response_model=Contact)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    return contacts_repository.delete_contact(db=db, contact_id=contact_id)


@router.get("/search/")
def search(query: str, db: Session = Depends(get_db)):
    contacts = crud_contact.search_contacts(db, query=query)
    return contacts


@router.get("/upcoming-birthdays/")
def upcoming_birthdays(db: Session = Depends(get_db)):
    contacts = crud_contact.get_upcoming_birthdays(db)
    return contacts
