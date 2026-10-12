from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import Base, engine, get_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Library API",
    description="Simple API for managing books, readers and loans.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/authors", response_model=schemas.AuthorOut, status_code=status.HTTP_201_CREATED)
def create_author(payload: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db, payload)


@app.get("/authors", response_model=list[schemas.AuthorOut])
def list_authors(db: Session = Depends(get_db)):
    return crud.list_authors(db)


@app.post("/books", response_model=schemas.BookOut, status_code=status.HTTP_201_CREATED)
def create_book(payload: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db, payload)


@app.get("/books", response_model=list[schemas.BookOut])
def list_books(db: Session = Depends(get_db)):
    return crud.list_books(db)


@app.post("/readers", response_model=schemas.ReaderOut, status_code=status.HTTP_201_CREATED)
def create_reader(payload: schemas.ReaderCreate, db: Session = Depends(get_db)):
    return crud.create_reader(db, payload)


@app.get("/readers", response_model=list[schemas.ReaderOut])
def list_readers(db: Session = Depends(get_db)):
    return crud.list_readers(db)


@app.post("/loans", response_model=schemas.LoanOut, status_code=status.HTTP_201_CREATED)
def create_loan(payload: schemas.LoanCreate, db: Session = Depends(get_db)):
    return crud.create_loan(db, payload)


@app.get("/loans", response_model=list[schemas.LoanOut])
def list_loans(db: Session = Depends(get_db)):
    return crud.list_loans(db)


@app.post("/loans/{loan_id}/return", response_model=schemas.LoanOut)
def return_loan(loan_id: int, db: Session = Depends(get_db)):
    loan = crud.return_loan(db, loan_id)
    if loan is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Loan not found")
    return loan
