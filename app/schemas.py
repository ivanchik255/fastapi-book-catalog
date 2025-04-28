from pydantic import BaseModel

class GenreBase(BaseModel):
    name: str

class GenreCreate(GenreBase):
    pass

class Genre(GenreBase):
    id: int

    class Config:
        orm_mode = True


class AuthorBase(BaseModel):
    name: str

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    id: int

    class Config:
        orm_mode = True


class BookBase(BaseModel):
    title: str
    description: str
    author_id: int
    genre_id: int

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    author: Author
    genre: Genre

    class Config:
        orm_mode = True

class UserBase(BaseModel):
       email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True
