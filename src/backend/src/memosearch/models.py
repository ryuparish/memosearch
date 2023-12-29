from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String
from .extensions import db
from dataclasses import dataclass


# Define Models and create tables
@dataclass
class Link(db.Model):
    __tablename__ = "links"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    link: Mapped[str] = mapped_column(String)
    about: Mapped[str] = mapped_column(String)
    date: Mapped[str] = mapped_column(String)
    site_name: Mapped[str] = mapped_column(String)
    related_activity: Mapped[str] = mapped_column(String)
    view: Mapped[str] = mapped_column(String)

    # This method is for printing.
    # It will show "<Student [firstname]>" as the type.
    def __repr__(self):
        return f"<Link id:{self.id}, site_name: {self.site_name}>"


@dataclass
class Screenshot(db.Model):
    __tablename__ = "screenshots"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    about: Mapped[str] = mapped_column(String)
    date: Mapped[str] = mapped_column(String)
    caption: Mapped[str] = mapped_column(String)
    text_in_image: Mapped[str] = mapped_column(String)
    path: Mapped[str] = mapped_column(String)
    related_activity: Mapped[str] = mapped_column(String)
    view: Mapped[str] = mapped_column(String)

    def __repr__(self):
        return f"<Screenshot id:{self.id}, caption: {self.caption}>"


@dataclass
class Note(db.Model):
    __tablename__ = "notes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String)
    about: Mapped[str] = mapped_column(String)
    date: Mapped[str] = mapped_column(String)
    related_activity: Mapped[str] = mapped_column(String)
    view: Mapped[str] = mapped_column(String)

    def __repr__(self):
        return f"<Screenshot id:{self.id}, about: {self.about}>"
