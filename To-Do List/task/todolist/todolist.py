from sqlalchemy import create_engine,  Date,  Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta


Base = declarative_base()


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='Do great things')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

today = datetime.today()

def allq():
    return session.query(Task).order_by(Task.deadline).all()

def alltasks():
    print("All tasks:")
    num = 1
    rows = allq()
    for task in rows:
        if not task:
            print("Nothing to do!\n")
        else:
            print("{}. {}. {}".format(num, task.task, datetime.strftime(task.deadline, '%-d %b')))
        num += 1
    print("")

def weektasks():
    for d in range(7):
        next_day = today + timedelta(days=d)
        rows = session.query(Task).filter(Task.deadline == next_day.date()).order_by(Task.deadline).all()
        print(datetime.strftime(next_day, '%A %-d %b'))
        if not rows:
            print("Nothing to do!\n")
        else:
            tasks(rows)


def daytasks():
    rows = session.query(Task).filter(Task.deadline == today.date()).all()
    print("Today", datetime.strftime(today, '%-d %b'))
    tasks(rows)


def tasks(rows):
    num = 1
    if not rows:
        print("Nothing to do!")
    else:
        for task in rows:
            print("{}. {}".format(num, task.task))
            num += 1
    print("")


def new_task():
    newtask = input("Add new task: ")
    deadline = input("Enter a deadline: ")
    task = Task(task=newtask, deadline=datetime.strptime(deadline, '%Y-%m-%d'))
    session.add(task)
    session.commit()
    print("The task has been added!")


def missed_tasks():
    rows = session.query(Task).filter(Task.deadline < today.date()).order_by(Task.deadline).all()
    print("Missed tasks:")
    if rows:
        tasks(rows)
    else:
        print("All tasks have been completed!")


def delete_task():
    print("Choose the number of the task you want to delete:")
    alltasks()
    act = int(input(">"))
    if allq():
        session.delete(allq()[act-1])
        session.commit()
    else:
        print("Nothing to delete")

def menu():
    print("1) Today's tasks",
          "2) Week's tasks",
          "3) All tasks",
          "4) Missed tasks",
          "5) Add a task",
          "6) Delete a task",
          "0) Exit",
          sep='\n')



def main():
    act = ''
    while act != 0:
        menu()
        act = int(input(">"))
        print("")
        if act == 1:
            daytasks()
        elif act == 2:
            weektasks()
        elif act == 3:
            alltasks()
        elif act == 4:
            missed_tasks()
        elif act == 5:
            new_task()
        elif act == 6:
            delete_task()
        else:
            continue


if __name__ == "__main__":
    main()
    print("Bye")
