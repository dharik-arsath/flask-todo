from sqlalchemy.orm import Session

from data_models.todo import Todo, CompletedTodo
from data_models.todo import get_engine

engine = get_engine()

with Session(engine) as session:
    t1 = Todo(
        title = "first_todo"
    )

    session.add(t1)
    session.commit()

with Session(engine) as session:
    todo = session.query(Todo).first()
    print(todo.title)
    c1 = CompletedTodo(
        todo = todo
    )

    session.add(c1)
    session.commit()




with Session(engine) as session:
    all_todos = session.query(Todo).all()

for todo in all_todos:
    print(todo.title)

with Session(engine) as session:
    all_todos_comp = session.query(CompletedTodo).all()

    for todo in all_todos_comp:
        print(todo.todo.title)