import pytest
from unittest.mock import MagicMock
from datetime import time
from app.services import StudentService, PresenceService
from app.models import Student, Presence

@pytest.fixture
def db_session():
    return MagicMock()

@pytest.fixture
def student_service(db_session):
    return StudentService(db_session)

@pytest.fixture
def presence_service(db_session):
    return PresenceService(db_session)

def test_add_student(student_service):
    student_service.student_repo.create = MagicMock(return_value=Student(id=1, name="John Doe"))
    student = student_service.add_student("John Doe")
    assert student.name == "John Doe"
    student_service.student_repo.create.assert_called_once()

def test_get_all_students(student_service):
    student_service.student_repo.get_all = MagicMock(return_value=[Student(id=1, name="John Doe")])
    students = student_service.get_all_students()
    assert len(students) == 1
    assert students[0].name == "John Doe"
    student_service.student_repo.get_all.assert_called_once()

def test_record_presence(presence_service):
    presence_service.student_repo.get_by_name = MagicMock(return_value=Student(id=1, name="John Doe"))
    presence_service.presence_repo.create = MagicMock(return_value=Presence(id=1, student_id=1, day=1, start_time=time(9, 0), end_time=time(10, 0), room="101"))

    presence = presence_service.record_presence("John Doe", 1, "19:00", "20:00", "101")

    assert presence.student_id == 1
    presence_service.student_repo.get_by_name.assert_called_once_with("John Doe")
    presence_service.presence_repo.create.assert_called_once()

def test_record_presence_student_not_exist(presence_service):
    presence_service.student_repo.get_by_name = MagicMock(return_value=None)
    with pytest.raises(ValueError, match="Student John Doe does not exist"):
        presence_service.record_presence("John Doe", 1, time(9, 0), time(10, 0), "101")

def test_generate_report(presence_service):
    presence_service.student_repo.get_all = MagicMock(return_value=[Student(id=1, name="John Doe")])
    presence_service.presence_repo.get_by_student = MagicMock(return_value=[
        Presence(id=1, student_id=1, day=1, start_time=time(9, 0), end_time=time(10, 0), room="101"),
        Presence(id=2, student_id=1, day=2, start_time=time(9, 0), end_time=time(10, 0), room="101")
    ])
    report = presence_service.generate_report()
    assert len(report) == 1
    assert report[0] == "John Doe: 120 minutes in 2 days"
    presence_service.student_repo.get_all.assert_called_once()
    presence_service.presence_repo.get_by_student.assert_called_once_with(1)
