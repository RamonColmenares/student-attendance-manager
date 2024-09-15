""" This module contains the repositories for the Student and Presence models. """
from .models import Student, Presence
from sqlalchemy.orm import Session
from typing import Optional

class StudentRepository:
    """
    Repository for managing Student entities in the database.

    This class provides methods to create, retrieve, and query Student records.

    Attributes:
        db (Session): The database session used for database operations.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_by_name(self, name: str) -> Optional[Student]:
        """
        Retrieve a student by their name.

        Args:
            name (str): The name of the student to retrieve.

        Returns:
            Optional[Student]: The Student object if found, None otherwise.
        """
        return self.db.query(Student).filter(Student.name == name).first()

    def create(self, student: Student) -> Student:
        """
        Create a new student record in the database.

        Args:
            student (Student): The Student object to be created.

        Returns:
            Student: The created Student object with updated database information.
        """
        self.db.add(student)
        self.db.commit()
        self.db.refresh(student)
        return student

    def get_all(self) -> list[Student]:
        """
        Retrieve all students from the database.

        Returns:
            list[Student]: A list of all Student objects in the database.
        """
        return self.db.query(Student).all()

class PresenceRepository:
    """
    Repository for managing Presence entities in the database.

    This class provides methods to create and retrieve Presence records.

    Attributes:
        db (Session): The database session used for database operations.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(self, presence: Presence) -> Presence:
        """
        Create a new presence record in the database.

        Args:
            presence (Presence): The Presence object to be created.

        Returns:
            Presence: The created Presence object with updated database information.
        """
        self.db.add(presence)
        self.db.commit()
        self.db.refresh(presence)
        return presence

    def get_by_student(self, student_id: int) -> list[Presence]:
        """
        Retrieve all presence records for a specific student.

        Args:
            student_id (int): The ID of the student whose presence records are to be retrieved.

        Returns:
            list[Presence]: A list of Presence objects associated with the given student ID.
        """
        return self.db.query(Presence).filter(Presence.student_id == student_id).all()
