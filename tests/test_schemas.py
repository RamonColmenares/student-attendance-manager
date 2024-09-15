import pytest
from marshmallow import ValidationError
from datetime import time
from app.schemas import StudentSchema, PresenceSchema

def test_student_schema_valid():
    schema = StudentSchema()
    data = {"name": "John Doe"}
    result = schema.load(data)
    assert result["name"] == "John Doe"

def test_student_schema_invalid():
    schema = StudentSchema()
    data = {}
    with pytest.raises(ValidationError) as excinfo:
        schema.load(data)
    assert "name" in excinfo.value.messages

def test_presence_schema_valid():
    schema = PresenceSchema()
    data = {
        "student_id": 1,
        "day": 3,
        "start_time": "09:00",
        "end_time": "10:00",
        "room": "101"
    }
    result = schema.load(data)
    assert result["day"] == 3
    assert result["start_time"] == time(9, 0)
    assert result["end_time"] == time(10, 0)
    assert result["room"] == "101"

def test_presence_schema_invalid_day():
    schema = PresenceSchema()
    data = {
        "student_name": "John Doe",
        "day": 8,
        "start_time": time(9, 0),
        "end_time": time(10, 0),
        "room": "101"
    }
    with pytest.raises(ValidationError) as excinfo:
        schema.load(data)
    assert "day" in excinfo.value.messages

def test_presence_schema_invalid_time_order():
    schema = PresenceSchema()
    data = {
        "student_name": "John Doe",
        "day": 3,
        "start_time": time(10, 0),
        "end_time": time(9, 0),
        "room": "101"
    }
    with pytest.raises(ValidationError) as excinfo:
        schema.load(data)
    assert "end_time" in excinfo.value.messages