from sqlalchemy.orm import Session
from homework11.src import schemas
from homework11.src.database import models


def get_contact(db: Session, contact_id: int):
    return db.query(models.Contact).filter(models.Contact.id == contact_id).first()


def get_contacts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Contact).offset(skip).limit(limit).all()


def create_contact(db: Session, contact: schemas.ContactCreate):
    db_contact = models.Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def update_contact(db: Session, contact_id: int, contact: schemas.ContactUpdate):
    db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if db_contact:
        update_data = contact.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_contact, key, value)
        db.commit()
        return db_contact
    return None


def delete_contact(db: Session, contact_id: int):
    db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if db_contact:
        db.delete(db_contact)
        db.commit()
        return True
    return False
