import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Student, student_factory, presence_factory
import datetime

@pytest.fixture(scope='module')
def engine():
    return create_engine('sqlite:///:memory:')

@pytest.fixture(scope='module')
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

@pytest.fixture(scope='function')
def db_session(engine, tables):
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()

    yield session

    session.close()
    transaction.rollback()
    connection.close()

def test_student_factory_valid_data(db_session):
    student_data = {
        "name": "John Doe"
    }
    student = student_factory(**student_data)
    db_session.add(student)
    db_session.commit()

    assert student.id is not None
    assert student.name == "John Doe"

def test_student_factory_invalid_data():
    student_data = {
        "name": None
    }
    with pytest.raises(ValueError):
        student_factory(**student_data)

def test_presence_factory_valid_data(db_session):
    student = Student(name="Jane Doe")
    db_session.add(student)
    db_session.commit()

    presence_data = {
        "student_id": student.id,
        "day": 1,
        "start_time": "09:00",
        "end_time": "10:00",
        "room": "101"
    }
    presence = presence_factory(**presence_data)
    db_session.add(presence)
    db_session.commit()

    assert presence.id is not None
    assert presence.student_id == student.id
    assert presence.day == 1
    assert presence.start_time == datetime.time(9, 0)
    assert presence.end_time == datetime.time(10, 0)
    assert presence.room == "101"

def test_presence_factory_invalid_data():
    presence_data = {
        "student_id": None,
        "day": 1,
        "start_time": datetime.time(9, 0),
        "end_time": datetime.time(10, 0),
        "room": "101"
    }
    with pytest.raises(ValueError):
        presence_factory(**presence_data)