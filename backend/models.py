"""
Data models for the contest management system
Using SQLModel for type hints + ORM
"""

from typing import Optional, List, Dict, Union
from sqlmodel import SQLModel, Field
from pydantic import field_validator
from sqlalchemy import Column, JSON

class ContestBase(SQLModel):
    """Base contest model with common fields"""
    class_level: str = Field(description="Class level (9, 10, 11, 12, or 'other')")
    year: int = Field(ge=2000, le=2100, description="Contest year")
    contest_name: str = Field(description="Name of the contest")
    contest_url: str = Field(description="URL to the contest")
    solutions: List[Dict[str, str]] = Field(
        default_factory=list,
        sa_column=Column(JSON),
        description="List of solutions with problem_name and solution_url"
    )

    @field_validator('class_level')
    @classmethod
    def validate_class_level(cls, v):
        # Accept both int and str, convert to string for storage
        # Convert int to str, keep string "other" as is
        if isinstance(v, int):
            v = str(v)
        elif isinstance(v, str) and v.isdigit():
            # Already a string number, validate it
            pass
        allowed = ["9", "10", "11", "12", "other"]
        if v not in allowed:
            raise ValueError(f'class_level must be one of {allowed}')
        return v

class Contest(ContestBase, table=True):
    """Contest model for database table"""
    __tablename__ = "contests"
    
    id: Optional[int] = Field(default=None, primary_key=True)

class ContestCreate(SQLModel):
    """Model for creating a new contest"""
    class_level: Union[int, str] = Field(description="Class level (9, 10, 11, 12, or 'other')")
    year: int = Field(ge=2000, le=2100, description="Contest year")
    contest_name: str = Field(description="Name of the contest")
    contest_url: str = Field(description="URL to the contest")
    solutions: List[Dict[str, str]] = Field(
        default_factory=list,
        sa_column=Column(JSON),
        description="List of solutions with problem_name and solution_url"
    )

    @field_validator('class_level')
    @classmethod
    def validate_class_level(cls, v):
        # Accept both int and str, convert to string for storage
        if isinstance(v, int):
            v = str(v)
        elif isinstance(v, str) and v.isdigit():
            pass
        allowed = ["9", "10", "11", "12", "other"]
        if v not in allowed:
            raise ValueError(f'class_level must be one of {allowed}')
        return v

class ContestUpdate(SQLModel):
    """Model for updating a contest"""
    class_level: Optional[Union[int, str]] = Field(default=None, description="Class level (9, 10, 11, 12, or 'other')")
    year: Optional[int] = Field(default=None, ge=2000, le=2100, description="Contest year")
    contest_name: Optional[str] = Field(default=None, description="Name of the contest")
    contest_url: Optional[str] = Field(default=None, description="URL to the contest")
    solutions: Optional[List[Dict[str, str]]] = Field(
        default=None,
        sa_column=Column(JSON),
        description="List of solutions with problem_name and solution_url"
    )

    @field_validator('class_level')
    @classmethod
    def validate_class_level(cls, v):
        if v is None:
            return v
        # Accept both int and str, convert to string for storage
        if isinstance(v, int):
            v = str(v)
        elif isinstance(v, str) and v.isdigit():
            pass
        allowed = ["9", "10", "11", "12", "other"]
        if v not in allowed:
            raise ValueError(f'class_level must be one of {allowed}')
        return v

class ContestRead(ContestBase):
    """Model for reading contest data (API response)"""
    id: int
