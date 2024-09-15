import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Student, presence_factory
from app.repositories import StudentRepository, PresenceRepository

@pytest.fixture(scope='module')
def engine():
    return create_engine('sqlite:///:memory:')

@pytest.fixture(scope='module')
def Session(engine):
    return sessionmaker(bind=engine)

@pytest.fixture(scope='function')
def session(Session, engine):
    session = Session()
    Base.metadata.create_all(engine)
    yield session
    session.close()
    Base.metadata.drop_all(engine)

def test_create_student(session):
    student_repo = StudentRepository(session)
    new_student = Student(name="John Doe")
    created_student = student_repo.create(new_student)
    assert created_student.id is not None
    assert created_student.name == "John Doe"

def test_get_student_by_name(session):
    student_repo = StudentRepository(session)
    new_student = Student(name="Jane Doe")
    student_repo.create(new_student)
    retrieved_student = student_repo.get_by_name("Jane Doe")
    assert retrieved_student is not None
    assert retrieved_student.name == "Jane Doe"

def test_get_all_students(session):
    student_repo = StudentRepository(session)
    student_repo.create(Student(name="Student 1"))
    student_repo.create(Student(name="Student 2"))
    all_students = student_repo.get_all()
    assert len(all_students) == 2

def test_create_presence(session):
    presence_repo = PresenceRepository(session)
    new_presence = presence_factory(**get_presence_mock())
    created_presence = presence_repo.create(new_presence)
    assert created_presence.id is not None
    assert created_presence.student_id == 1

def test_get_presence_by_student(session):
    presence_repo = PresenceRepository(session)
    presence_repo.create(presence_factory(**get_presence_mock()))
    presence_repo.create(presence_factory(**get_presence_mock()))
    presences = presence_repo.get_by_student(1)
    assert len(presences) == 2

def get_presence_mock():
    return {
        "student_id": 1,
        "day": 1,
        "start_time": "08:00",
        "end_time": "09:00",
        "room": "test"
    }