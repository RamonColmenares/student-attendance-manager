"""This module contains the SQLAlchemy models for the database."""
from __future__ import annotations
import datetime
from typing import Any, List
from sqlalchemy import Integer, String, ForeignKey, Time
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .db import Base
from .schemas import PresenceSchema, StudentSchema
from marshmallow.exceptions import ValidationError


class Student(Base):
    __tablename__ = 'students'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)

    presences: Mapped[List[Presence]] = relationship("Presence", back_populates="student")


class Presence(Base):
    __tablename__ = 'presences'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    day: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[datetime.time] = mapped_column(Time)
    end_time: Mapped[datetime.time] = mapped_column(Time)
    room: Mapped[str] = mapped_column(String)

    student: Mapped[Student] = relationship("Student", back_populates="presences")


def presence_factory(**kwargs: Any) -> Presence:
    """"
    Factory function for creating a Presence object.

    Args:
        **kwargs (Any): The attributes of the Presence object.

    Returns:
        Presence: The created Presence object.
    """
    schema = PresenceSchema()
    try:
        validated_data = schema.load(kwargs)
    except ValidationError as err:
        raise ValueError(f"Invalid data: {err.messages}")

    presence = Presence(**validated_data)
    return presence

def student_factory(**kwargs: Any) -> Student:
    """
    Factory function for creating a Student object.

    Args:
        **kwargs (Any): The attributes of the Student object.

    Returns:
        Student: The created Student object.
    """
    schema = StudentSchema()
    try:
        validated_data = schema.load(kwargs)
    except ValidationError as err:
        raise ValueError(f"Invalid data: {err.messages}")

    student = Student(**validated_data)
    return student
