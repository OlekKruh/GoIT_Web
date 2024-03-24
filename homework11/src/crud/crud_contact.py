from datetime import datetime, timedelta
from sqlalchemy import or_, extract
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


def search_contacts(db: Session, query: str):
    return db.query(models.Contact).filter(
        or_(
            models.Contact.first_name.ilike(f"%{query}%"),
            models.Contact.last_name.ilike(f"%{query}%"),
            models.Contact.email.ilike(f"%{query}%")
        )
    ).all()


def get_upcoming_birthdays(db: Session):
    today = datetime.today()
    upcoming = today + timedelta(days=7)
    return db.query(models.Contact).filter(
        models.Contact.birth_date.isnot(None),
        extract('month', models.Contact.birth_date) >= today.month,
        extract('month', models.Contact.birth_date) <= upcoming.month,
        extract('day', models.Contact.birth_date) >= today.day,
        extract('day', models.Contact.birth_date) <= upcoming.day
    ).all()
