"""
ORM models for the app/database
"""

from enum import Enum
from typing import List, Optional

from sqlalchemy.orm import joinedload
from sqlmodel import Field, Relationship, SQLModel, Session


PARENT_CHILD_SA_RELATIONSHIP_KWARGS = {
    "cascade": "all, delete, delete-orphan, save-update"
}
CHILD_PARENT_SA_RELATIONSHIP_KWARGS = {"cascade": "save-update, merge"}


class User(SQLModel, table=True):
    """SQLModel for "User" objects"""

    username: Optional[str] = Field(default="New User", primary_key=True)

    # Children
    routines: List["Routine"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs=PARENT_CHILD_SA_RELATIONSHIP_KWARGS,
    )
    programs: List["Program"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs=PARENT_CHILD_SA_RELATIONSHIP_KWARGS,
    )

    @classmethod
    def eagerly_get_user(cls, session: Session, username: str) -> Optional['User']:
        """Eagerly loads a user from the database (with all of their subsequent
        data) given a username. Returns None if no such username in DB."""
        return session.get(
            cls, username, options=[joinedload("*")], populate_existing=True)


class Program(SQLModel, table=True):
    """SQLModel for "Program" objects"""

    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)
    title: Optional[str] = Field(default="New Program")

    # Children
    routine_items: List["RoutineItem"] = Relationship(
        back_populates="program",
        sa_relationship_kwargs=PARENT_CHILD_SA_RELATIONSHIP_KWARGS,
    )
    # Parent
    user_username: Optional[int] = Field(default=None, foreign_key="user.username")
    user: Optional[User] = Relationship(
        back_populates="programs",
        sa_relationship_kwargs=CHILD_PARENT_SA_RELATIONSHIP_KWARGS,
    )

    def __str__(self):
        return self.title


class Routine(SQLModel, table=True):
    """SQLModel for "Routine" objects"""

    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)
    title: Optional[str] = Field(default="New Routine")
    target_duration: Optional[int] = Field(default=10)
    target_duration_enabled: bool = Field(default=False)

    # Children
    alarms: List["Alarm"] = Relationship(
        back_populates="routine",
        sa_relationship_kwargs=PARENT_CHILD_SA_RELATIONSHIP_KWARGS,
    )
    routine_items: List["RoutineItem"] = Relationship(
        back_populates="routine",
        sa_relationship_kwargs=PARENT_CHILD_SA_RELATIONSHIP_KWARGS,
    )
    # Parent
    user_username: Optional[int] = Field(default=None, foreign_key="user.username")
    user: Optional[User] = Relationship(
        back_populates="routines",
        sa_relationship_kwargs=CHILD_PARENT_SA_RELATIONSHIP_KWARGS,
    )


class PriorityLevel(str, Enum):
    "Enum for a RoutineItem's priority level"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class SoundFrequency(str, Enum):
    "Enum for a Alarm's sound frequency"
    CONSTANT = "constant"
    PERIODIC = "periodic"


class RoutineItem(SQLModel, table=True):
    """SQLModel for "RoutineItem" objects"""

    __tablename__ = "routine_item"

    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)
    order_index: int = Field(default=0)
    priority_level: PriorityLevel = Field(default=PriorityLevel.MEDIUM)
    is_reward: bool = Field(default=False)

    # Parents
    routine_id: Optional[int] = Field(default=None, foreign_key="routine.id")
    routine: Optional[Routine] = Relationship(
        back_populates="routine_items",
        sa_relationship_kwargs=CHILD_PARENT_SA_RELATIONSHIP_KWARGS,
    )
    program_id: Optional[int] = Field(default=None, foreign_key="program.id")
    program: Optional[Program] = Relationship(
        back_populates="routine_items",
        sa_relationship_kwargs=CHILD_PARENT_SA_RELATIONSHIP_KWARGS,
    )


class Alarm(SQLModel, table=True):
    """SQLModel for "Alarm" objects"""

    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)
    hour: int = Field(default=0)
    minute: int = Field(default=0)
    enabled: bool = Field(default=False)
    volume: float = Field(default=0.5)
    sound_frequency: SoundFrequency = Field(default=SoundFrequency.CONSTANT)

    # Parent
    routine_id: Optional[int] = Field(default=None, foreign_key="routine.id")
    routine: Optional[Routine] = Relationship(
        back_populates="alarms",
        sa_relationship_kwargs=CHILD_PARENT_SA_RELATIONSHIP_KWARGS,
    )

    def set_time(self, str_time: str):
        """Takes a string in the format "HH:MM" and sets the hour and minute"""
        self.hour, self.minute = str_time.split(":")

    def get_time(self) -> str:
        """Returns a string in the format "HH:MM" from the hour and minute"""
        return f"{self.hour}:{self.minute}"
