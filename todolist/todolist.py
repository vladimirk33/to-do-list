from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    # task = Column(String, default='default_value')
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def tasks():
    rows = session.query(Table).all()
    print("Today:")
    if not len(rows):
        print("Nothing to do!")
    else:
        for row in rows:
            print(f"{row.id}. {row.task}")


def add_task():
    task = input("\nEnter task\n")
    print("The task has been added!")
    new_row = Table(task=task,
                    deadline=datetime.today())
    session.add(new_row)
    session.commit()


def main():
    response = None
    while response != 0:
        print("1) Today's tasks\n2) Add task\n0) Exit")
        response = int(input())
        if response == 1:
            tasks()
        elif response == 2:
            add_task()
        elif response == 0:
            print("\nBye!")


if __name__ == "__main__":
    main()
