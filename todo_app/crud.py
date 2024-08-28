from sqlalchemy.orm import Session
from sqlalchemy import exc
from models import Todo, User
from schemas import TodoCreate, TodoUpdate, UserCreate
from auth import get_password_hash
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# User CRUD operations
def get_user(db: Session, user_id: int):
    if user_id < 1:
        logger.warning("Invalid user ID")
        return None
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    email = email.strip()
    # Corrected to use proper filtering without bindparam
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        logger.warning(f"User with email {user.email} already exists")
        raise ValueError(f"User with email {user.email} already exists")
    
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, username=user.username, hashed_password=hashed_password)
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except exc.SQLAlchemyError as e:
        logger.error(f"Error creating user: {e}")
        db.rollback()  # Rollback to maintain database consistency
        raise e

# Todo CRUD operations
def get_todos(db: Session, skip: int = 0, limit: int = 100):
    try:
        return db.query(Todo).offset(skip).limit(limit).all()
    except exc.SQLAlchemyError as e:
        logger.error(f"Error retrieving todos: {e}")
        raise e

def create_todo(db: Session, todo: TodoCreate, user_id: int):
    if not todo.title or not todo.description:
        logger.warning("Todo title and description are required")
        raise ValueError("Todo title and description are required")
    
    if user_id < 1:
        logger.warning("Invalid user ID")
        raise ValueError("Invalid user ID")
    
    db_todo = Todo(**todo.dict(), owner_id=user_id)
    try:
        db.add(db_todo)
        db.commit()
        db.refresh(db_todo)
        return db_todo
    except exc.SQLAlchemyError as e:
        logger.error(f"Error creating todo: {e}")
        db.rollback()  # Rollback to maintain database consistency
        raise e

def update_todo(db: Session, todo_id: int, todo: TodoUpdate):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not db_todo:
        logger.warning(f"Todo with id {todo_id} does not exist")
        raise ValueError(f"Todo with id {todo_id} does not exist")
    
    for key, value in todo.dict().items():
        setattr(db_todo, key, value)
    try:
        db.commit()
        db.refresh(db_todo)
        return db_todo
    except exc.SQLAlchemyError as e:
        logger.error(f"Error updating todo: {e}")
        db.rollback()  # Rollback to maintain database consistency
        raise e

def delete_todo(db: Session, todo_id: int):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not db_todo:
        logger.warning(f"Todo with id {todo_id} does not exist")
        raise ValueError(f"Todo with id {todo_id} does not exist")
    
    try:
        db.delete(db_todo)
        db.commit()
        return db_todo
    except exc.SQLAlchemyError as e:
        logger.error(f"Error deleting todo: {e}")
        db.rollback()  # Rollback to maintain database consistency
        raise e
