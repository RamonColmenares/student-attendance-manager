from unittest.mock import Mock
from app.commands import StudentCommand, PresenceCommand, CommandFactory
from datetime import time

def test_student_command():
    mock_student_service = Mock()
    student_command = StudentCommand(mock_student_service)
    student_name = "John Doe"

    student_command.execute(student_name)

    mock_student_service.add_student.assert_called_once_with(student_name)

def test_presence_command():
    mock_presence_service = Mock()
    presence_command = PresenceCommand(mock_presence_service)
    student_name = "John Doe"
    day = "1"
    start_time = time(9, 0)
    end_time = time(10, 0)
    room = "101"

    presence_command.execute(student_name, day, start_time, end_time, room)

    mock_presence_service.record_presence.assert_called_once_with(student_name, int(day), start_time, end_time, room)

def test_command_factory():
    mock_student_service = Mock()
    mock_presence_service = Mock()
    command_factory = CommandFactory(mock_student_service, mock_presence_service)

    student_command = command_factory.get_command('Student')
    presence_command = command_factory.get_command('Presence')
    invalid_command = command_factory.get_command('Invalid')

    assert isinstance(student_command, StudentCommand)
    assert isinstance(presence_command, PresenceCommand)
    assert invalid_command is None