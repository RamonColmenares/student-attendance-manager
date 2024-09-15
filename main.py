import sys
from app import init_db, SessionLocal
from app.services import StudentService
from app.services import PresenceService
from app.commands import CommandFactory
from sqlalchemy import text
from app.logger_config import logger

def truncate_tables(db):
    db.execute(text("PRAGMA foreign_keys = OFF;"))
    db.execute(text("DELETE FROM students;"))
    db.execute(text("DELETE FROM presences;"))
    db.execute(text("PRAGMA foreign_keys = ON;"))
    db.commit()

def main(input_file):
    init_db()
    db = SessionLocal()

    truncate_tables(db)

    student_service = StudentService(db)
    presence_service = PresenceService(db)
    command_factory = CommandFactory(student_service, presence_service)

    with open(input_file, 'r') as file:
        for line in file:
            parts = line.strip().split()
            command_name = parts[0]
            command = command_factory.get_command(command_name)

            if command:
                try:
                    command.execute(*parts[1:])
                except Exception as e:
                    logger.error(f"Skipping command due to error: {e}")

    report = presence_service.generate_report()

    for line in report:
        print(line)

if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
    main(input_file)
