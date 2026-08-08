from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from typing import Optional
import json
from app.database.session import get_db
from app.auth.dependencies import get_current_user
from app.schemas.journal import TravelJournalCreate, TravelJournalUpdate, TravelJournalResponse
from app.models.journal import TravelJournal
from app.models.user import User

router = APIRouter()

def _serialize_journal(journal: TravelJournal) -> TravelJournalResponse:
    photos_list = []
    if journal.photos:
        try:
            photos_list = json.loads(journal.photos)
        except Exception:
            photos_list = [journal.photos]
    return TravelJournalResponse(
        journal_id=journal.journal_id,
        user_id=journal.user_id,
        trip_id=journal.trip_id,
        title=journal.title,
        content=journal.content,
        photos=photos_list,
        mood=journal.mood,
        rating=journal.rating,
        location=journal.location,
        created_at=journal.created_at,
    )

@router.post("", response_model=TravelJournalResponse, status_code=201)
async def create_journal(journal_data: TravelJournalCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    data = journal_data.model_dump()
    if "photos" in data and isinstance(data["photos"], list):
        data["photos"] = json.dumps(data["photos"])
    journal = TravelJournal(user_id=current_user.user_id, **data)
    db.add(journal)
    await db.commit()
    await db.refresh(journal)
    return _serialize_journal(journal)

@router.get("")
async def list_journals(
    trip_id: Optional[int] = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(TravelJournal).where(TravelJournal.user_id == current_user.user_id)
    if trip_id:
        query = query.where(TravelJournal.trip_id == trip_id)
    count_result = await db.execute(select(func.count()).select_from(query.subquery()))
    total = count_result.scalar()
    query = query.order_by(TravelJournal.created_at.desc()).offset((page - 1) * per_page).limit(per_page)
    result = await db.execute(query)
    journals = result.scalars().all()
    serialized = [_serialize_journal(j) for j in journals]
    return {"journals": serialized, "total": total, "page": page, "per_page": per_page}

@router.get("/{journal_id}", response_model=TravelJournalResponse)
async def get_journal(journal_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TravelJournal).where(and_(TravelJournal.journal_id == journal_id, TravelJournal.user_id == current_user.user_id)))
    journal = result.scalar_one_or_none()
    if not journal:
        raise HTTPException(status_code=404, detail="Journal not found")
    return _serialize_journal(journal)

@router.put("/{journal_id}", response_model=TravelJournalResponse)
async def update_journal(journal_id: int, data: TravelJournalUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TravelJournal).where(and_(TravelJournal.journal_id == journal_id, TravelJournal.user_id == current_user.user_id)))
    journal = result.scalar_one_or_none()
    if not journal:
        raise HTTPException(status_code=404, detail="Journal not found")
    update_data = data.model_dump(exclude_unset=True)
    if "photos" in update_data and isinstance(update_data["photos"], list):
        update_data["photos"] = json.dumps(update_data["photos"])
    for field, value in update_data.items():
        setattr(journal, field, value)
    await db.commit()
    await db.refresh(journal)
    return _serialize_journal(journal)

@router.delete("/{journal_id}")
async def delete_journal(journal_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TravelJournal).where(and_(TravelJournal.journal_id == journal_id, TravelJournal.user_id == current_user.user_id)))
    journal = result.scalar_one_or_none()
    if not journal:
        raise HTTPException(status_code=404, detail="Journal not found")
    await db.delete(journal)
    await db.commit()
    return {"message": "Journal deleted successfully"}
