"""This module contains the services that interact with the repositories to perform business logic."""

from sqlalchemy.orm import Session
from .repositories import StudentRepository
from .models import Student, presence_factory, student_factory
from .repositories import PresenceRepository
from datetime import time


class StudentService:
    """
    Service class for managing student-related operations.
    """

    def __init__(self, db: Session):
        self.db = db
        self.student_repo = StudentRepository(db)

    def add_student(self, name: str) -> Student:
        """
        Add a new student to the database.

        Args:
            name (str): The name of the student.

        Returns:
            Student: The newly created student object.
        """
        student = student_factory(name=name)
        return self.student_repo.create(student)

    def get_all_students(self) -> list[Student]:
        """
        Retrieve all students from the database.

        Returns:
            list[Student]: A list of all student objects.
        """
        return self.student_repo.get_all()


class PresenceService:
    """
    Service class for managing student presence records and generating reports.
    """

    def __init__(self, db: Session):
        self.db = db
        self.presence_repo = PresenceRepository(db)
        self.student_repo = StudentRepository(db)

    def record_presence(
        self, name: str, day: int, start_time: time, end_time: time, room: str
    ):
        """
        Record a student's presence.

        Args:
            name (str): The name of the student.
            day (int): The day of presence.
            start_time (time): The start time of presence.
            end_time (time): The end time of presence.
            room (str): The room where the student was present.

        Returns:
            Presence: The newly created presence record.

        Raises:
            ValueError: If the student does not exist.
        """
        student = self.student_repo.get_by_name(name)

        if not student:
            raise ValueError(f"Student {name} does not exist")

        presence_data = {
            "student_id": student.id,
            "day": day,
            "start_time": start_time,
            "end_time": end_time,
            "room": room,
        }

        presence = presence_factory(**presence_data)

        return self.presence_repo.create(presence)

    def generate_report(self) -> list[str]:
        """
        Generate a report of student presence.

        Returns:
            list[str]: A list of formatted strings representing each student's presence report, sorted by total minutes in descending order.
        """
        students = self.student_repo.get_all()
        report = [self._generate_student_report(student) for student in students]
        sorted_report = sorted(report, key=lambda x: x[1], reverse=True)
        return [self._format_report_entry(entry) for entry in sorted_report]

    def _generate_student_report(self, student: Student) -> tuple[str, int, int]:
        """
        Generate a report for a single student.

        Args:
            student (Student): The student object.

        Returns:
            tuple[str, int, int]: A tuple containing the student's name, total minutes present, and number of days attended.
        """
        presences = self.presence_repo.get_by_student(student.id)
        total_minutes = 0
        days_attended = set()

        for presence in presences:
            duration = self._calculate_duration(presence.start_time, presence.end_time)
            if duration >= 5:
                total_minutes += duration
                days_attended.add(presence.day)

        return (student.name, total_minutes, len(days_attended))

    def _calculate_duration(self, start_time: time, end_time: time) -> int:
        """
        Calculate the duration between two times in minutes.

        Args:
            start_time (time): The start time.
            end_time (time): The end time.

        Returns:
            int: The duration in minutes.
        """
        start_minutes = start_time.hour * 60 + start_time.minute
        end_minutes = end_time.hour * 60 + end_time.minute
        return end_minutes - start_minutes

    def _format_report_entry(self, entry: tuple) -> str:
        """
        Format a single report entry.

        Args:
            entry (tuple): A tuple containing (student_name, total_minutes, days_attended).

        Returns:
            str: A formatted string representing the report entry.
        """
        student_name, total_minutes, days = entry
        day_str = "day" if days == 1 else "days"
        time_str = f"{total_minutes} minutes"
        days_str = f" in {days} {day_str}" if days > 0 else ""
        return f"{student_name}: {time_str}{days_str}"
