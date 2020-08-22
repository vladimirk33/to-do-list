from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker

from datetime import datetime, timedelta

# create todo.db file
engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    """Create DB Table."""
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        """Print task column."""
        return self.task


# create DB session
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def print_tasks(rows):
    """Print tasks in {i. Task. Day Month} format."""
    for i in range(len(rows)):
        print(f"{i + 1}. {rows[i].task}. {rows[i].deadline.day} "
              + f"{rows[i].deadline.strftime('%b')}")


def today_tasks():
    """Print today's tasks."""
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
    """Print week's tasks."""
    # weekdays tuple for .weekday method
    WEEKDAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
                "Saturday", "Sunday")
    today = datetime.today()
    print()
    for day_number in range(7):
        day: datetime = today + timedelta(days=day_number)
        print(f"{WEEKDAYS[day.weekday()]} {day.day} {day.strftime('%b')}:")
        rows = session.query(Table).filter(Table.deadline == day.date()).all()
        if not len(rows):
            print("Nothing to do!\n")
        else:
            for i in range(len(rows)):
                print(f"{i + 1}. {rows[i].task}")
            print()


def all_tasks():
    """Print all tasks."""
    rows = session.query(Table).order_by(Table.deadline).all()
    print("\nAll tasks:")
    if not len(rows):
        print("Nothing to do!\n")
    else:
        print_tasks(rows)
        print()


def missed_tasks():
    """Print missed tasks."""
    today = datetime.today()
    rows = session.query(Table).filter(Table.deadline < today.date()).all()
    print("\nMissed tasks:")
    if not len(rows):
        print("Nothing is missed!\n")
    else:
        print_tasks(rows)
        print()


def _get_correct_row(task):
    """Return correct row for add_task function."""
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
    """Add task to DB."""
    task = input("\nEnter task\n")
    new_row = _get_correct_row(task)
    session.add(new_row)
    session.commit()
    print("The task has been added!\n")


def delete_task():
    """Delete task from DB."""
    rows = session.query(Table).order_by(Table.deadline).all()
    print("\nChoose the number of the task you want to delete:")
    if not len(rows):
        print("Nothing to delete!\n")
    else:
        print_tasks(rows)
        while True:
            try:
                delete_number = int(input())
                if delete_number:
                    session.delete(rows[delete_number - 1])
                    break
                else:
                    print("Print correct number")
            except (ValueError, IndexError):
                print("Print correct number")
        session.commit()
        print("The task has been deleted!\n")


def menu():
    """Menu with modes."""
    menu_list = ["1) Today's tasks", "2) Week's tasks", "3) All tasks",
                 "4) Missed tasks", "5) Add task", "6) Delete task", "0) Exit"]
    response = None
    while response != 0:
        for menu_item in menu_list:
            print(menu_item)
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
            missed_tasks()
        elif response == 5:
            add_task()
        elif response == 6:
            delete_task()
        elif response == 0:
            print("\nBye!")


def main():
    """Starter."""
    menu()


if __name__ == "__main__":
    main()
