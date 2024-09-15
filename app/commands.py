""" Module for command classes. """
from typing import Optional
from app.services import StudentService
from app.services import PresenceService
from datetime import time

class Command:
    """
    Abstract base class for commands.
    """
    def execute(self, *args):
        """
        Execute the command.

        Args:
            *args: Variable length argument list.

        Raises:
            NotImplementedError: If the subclass does not implement this method.
        """
        raise NotImplementedError

class StudentCommand(Command):
    """
    Command for adding a student.
    """
    def __init__(self, student_service: StudentService):
        """
        Initialize the StudentCommand.

        Args:
            student_service (StudentService): The service to handle student-related operations.
        """
        self.student_service = student_service

    def execute(self, name: str) -> None:
        """
        Execute the command to add a student.

        Args:
            name (str): The name of the student to add.
        """
        self.student_service.add_student(name)

class PresenceCommand(Command):
    """
    Command for recording student presence.
    """
    def __init__(self, presence_service: PresenceService):
        """
        Initialize the PresenceCommand.

        Args:
            presence_service (PresenceService): The service to handle presence-related operations.
        """
        self.presence_service = presence_service

    def execute(self, name: str, day: str, start_time: time, end_time: time, room: str) -> None:
        """
        Execute the command to record student presence.

        Args:
            name (str): The name of the student.
            day (str): The day of presence (will be converted to int).
            start_time (str): The start time of presence.
            end_time (str): The end time of presence.
            room (str): The room where the student was present.
        """
        self.presence_service.record_presence(name, int(day), start_time, end_time, room)

class CommandFactory:
    """
    Factory class for creating command objects.
    """
    def __init__(self, student_service: StudentService, presence_service: PresenceService):
        """
        Initialize the CommandFactory.

        Args:
            student_service (StudentService): The service to handle student-related operations.
            presence_service (PresenceService): The service to handle presence-related operations.
        """
        self.commands = {
            'Student': StudentCommand(student_service),
            'Presence': PresenceCommand(presence_service)
        }

    def get_command(self, command_name: str) -> Optional[Command]:
        """
        Get a command object based on the command name.

        Args:
            command_name (str): The name of the command to retrieve.

        Returns:
            Optional[Command]: The command object if found, None otherwise.
        """
        return self.commands.get(command_name)
