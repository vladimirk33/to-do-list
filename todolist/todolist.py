from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker

from datetime import datetime, timedelta

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def today_tasks():
    today = datetime.today()
    rows = session.query(Table).filter(Table.deadline == today.date()).all()
    print(f"\nToday {today.day} {today.strftime('%b')}:")
    if not len(rows):
        print("Nothing to do!\n")
    else:
        for i in range(len(rows)):
            print(f"{i + 1}. {rows[i].task}")
        print()


def week_tasks():
    WEEKDAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
                "Saturday", "Sunday")
    today = datetime.today()
    print()
    for day_number in range(7):
        day = today + timedelta(days=day_number)
        print(f"{WEEKDAYS[day.weekday()]} {day.day} {day.strftime('%b')}:")
        rows = session.query(Table).filter(Table.deadline == day.date()).all()
        if not len(rows):
            print("Nothing to do!\n")
        else:
            for i in range(len(rows)):
                print(f"{i + 1}. {rows[i].task}")
            print()



def all_tasks():
    rows = session.query(Table).order_by(Table.deadline).all()
    print("\nAll tasks:")
    if not len(rows):
        print("Nothing to do!\n")
    else:
        for i in range(len(rows)):
            print(f"{i + 1}. {rows[i].task}. {rows[i].deadline.day} "
                  + f"{rows[i].deadline.strftime('%b')}")
        print()


def _get_correct_row(task):
    while True:
        try:
            deadline = [int(s) for s in input("Enter deadline\n").split("-")]
            new_row = Table(task=task,
                            deadline=datetime(deadline[0], deadline[1], deadline[2]))
            break
        except (ValueError, IndexError):
            print("\nPrint correct date (YYYY-MM-DD)\n")
    return new_row


def add_task():
    task = input("\nEnter task\n")
    new_row = _get_correct_row(task)
    session.add(new_row)
    session.commit()
    print("The task has been added!\n")


def menu():
    response = None
    while response != 0:
        print("1) Today's tasks\n2) Week's tasks\n3) All tasks")
        print("4) Add task\n0) Exit")
        try:
            response = int(input())
        except ValueError:
            print("Choose an item from the menu (0-4)\n")
        if response == 1:
            today_tasks()
        elif response == 2:
            week_tasks()
        elif response == 3:
            all_tasks()
        elif response == 4:
            add_task()
        elif response == 0:
            print("\nBye!")


def main():
    menu()


if __name__ == "__main__":
    main()
