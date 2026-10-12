from datetime import date, timedelta

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models, schemas


def create_author(db: Session, payload: schemas.AuthorCreate) -> models.Author:
    author = models.Author(name=payload.name)
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


def list_authors(db: Session) -> list[models.Author]:
    return list(db.scalars(select(models.Author).order_by(models.Author.name)))


def create_book(db: Session, payload: schemas.BookCreate) -> models.Book:
    author = db.get(models.Author, payload.author_id)
    if author is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Author not found")

    if db.scalar(select(models.Book).where(models.Book.isbn == payload.isbn)):
        raise HTTPException(status.HTTP_409_CONFLICT, "ISBN already exists")

    book = models.Book(
        title=payload.title,
        isbn=payload.isbn,
        total_copies=payload.total_copies,
        available_copies=payload.total_copies,
        author_id=payload.author_id,
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def list_books(db: Session) -> list[models.Book]:
    return list(db.scalars(select(models.Book).order_by(models.Book.title)))


def create_reader(db: Session, payload: schemas.ReaderCreate) -> models.Reader:
    if db.scalar(select(models.Reader).where(models.Reader.email == payload.email)):
        raise HTTPException(status.HTTP_409_CONFLICT, "Email already exists")

    reader = models.Reader(full_name=payload.full_name, email=payload.email)
    db.add(reader)
    db.commit()
    db.refresh(reader)
    return reader


def list_readers(db: Session) -> list[models.Reader]:
    return list(db.scalars(select(models.Reader).order_by(models.Reader.full_name)))


def create_loan(db: Session, payload: schemas.LoanCreate) -> models.Loan:
    book = db.get(models.Book, payload.book_id)
    if book is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Book not found")

    reader = db.get(models.Reader, payload.reader_id)
    if reader is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Reader not found")

    if not reader.active:
        raise HTTPException(status.HTTP_409_CONFLICT, "Reader is inactive")

    if book.available_copies < 1:
        raise HTTPException(status.HTTP_409_CONFLICT, "No copies available")

    book.available_copies -= 1
    loan = models.Loan(
        book_id=book.id,
        reader_id=reader.id,
        loan_date=date.today(),
        due_date=date.today() + timedelta(days=payload.days),
    )
    db.add(loan)
    db.commit()
    db.refresh(loan)
    return loan


def return_loan(db: Session, loan_id: int) -> models.Loan:
    loan = db.get(models.Loan, loan_id)
    if loan is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Loan not found")

    if loan.returned_at is not None:
        raise HTTPException(status.HTTP_409_CONFLICT, "Loan already returned")

    loan.returned_at = date.today()
    loan.book.available_copies += 1
    db.commit()
    db.refresh(loan)
    return loan


def list_loans(db: Session) -> list[models.Loan]:
    return list(db.scalars(select(models.Loan).order_by(models.Loan.id.desc())))
