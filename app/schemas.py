from datetime import date

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class AuthorCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)


class AuthorOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class BookCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    isbn: str = Field(min_length=10, max_length=32)
    total_copies: int = Field(default=1, ge=1)
    author_id: int


class BookOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    isbn: str
    total_copies: int
    available_copies: int
    author_id: int


class ReaderCreate(BaseModel):
    full_name: str = Field(min_length=1, max_length=255)
    email: EmailStr


class ReaderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    email: EmailStr
    active: bool


class LoanCreate(BaseModel):
    book_id: int
    reader_id: int
    days: int = Field(default=14, ge=1, le=90)


class LoanOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    book_id: int
    reader_id: int
    loan_date: date
    due_date: date
    returned_at: date | None
