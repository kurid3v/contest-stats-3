"""
Contest CRUD routes
Handles all contest management operations
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from database import get_session
from models import Contest, ContestCreate, ContestUpdate, ContestRead
from .auth import verify_token

router = APIRouter(prefix="/contests", tags=["contests"])

@router.get("", response_model=List[ContestRead])
async def get_all_contests(session: Session = Depends(get_session)):
    """
    Get all contests
    Returns all contests ordered by year (descending) and contest_name
    """
    statement = select(Contest).order_by(Contest.year.desc(), Contest.contest_name)
    contests = session.exec(statement).all()
    return contests

@router.get("/{contest_id}", response_model=ContestRead)
async def get_contest(contest_id: int, session: Session = Depends(get_session)):
    """
    Get a specific contest by ID
    """
    contest = session.get(Contest, contest_id)
    if not contest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contest with id {contest_id} not found",
        )
    return contest

@router.post("", response_model=ContestRead, status_code=status.HTTP_201_CREATED)
async def create_contest(
    contest: ContestCreate,
    session: Session = Depends(get_session),
    _token: str = Depends(verify_token),
):
    """
    Create a new contest
    """
    db_contest = Contest.model_validate(contest)
    session.add(db_contest)
    session.commit()
    session.refresh(db_contest)
    return db_contest

@router.put("/{contest_id}", response_model=ContestRead)
async def update_contest(
    contest_id: int,
    contest_update: ContestUpdate,
    session: Session = Depends(get_session),
    _token: str = Depends(verify_token),
):
    """
    Update an existing contest
    """
    db_contest = session.get(Contest, contest_id)
    if not db_contest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contest with id {contest_id} not found",
        )
    
    # Update fields
    contest_data = contest_update.model_dump(exclude_unset=True)
    for field, value in contest_data.items():
        setattr(db_contest, field, value)
    
    session.add(db_contest)
    session.commit()
    session.refresh(db_contest)
    return db_contest

@router.delete("/{contest_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contest(
    contest_id: int,
    session: Session = Depends(get_session),
    _token: str = Depends(verify_token),
):
    """
    Delete a contest by ID
    """
    db_contest = session.get(Contest, contest_id)
    if not db_contest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contest with id {contest_id} not found",
        )
    
    session.delete(db_contest)
    session.commit()
    return None

@router.get("/class/{class_level}", response_model=List[ContestRead])
async def get_contests_by_class(
    class_level: str,
    session: Session = Depends(get_session),
):
    """
    Get all contests for a specific class level (9, 10, 11, 12, or 'other')
    """
    allowed_levels = ["9", "10", "11", "12", "other"]
    # Convert to string if it's a number
    class_level_str = str(class_level) if class_level.isdigit() else class_level
    if class_level_str not in allowed_levels:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Class level must be one of {allowed_levels}",
        )
    
    # class_level is stored as string in database
    statement = select(Contest).where(Contest.class_level == class_level_str).order_by(Contest.year.desc(), Contest.contest_name)
    contests = session.exec(statement).all()
    return contests

@router.get("/year/{year}", response_model=List[ContestRead])
async def get_contests_by_year(
    year: int,
    session: Session = Depends(get_session),
):
    """
    Get all contests for a specific year
    """
    statement = select(Contest).where(Contest.year == year).order_by(Contest.class_level, Contest.contest_name)
    contests = session.exec(statement).all()
    return contests
