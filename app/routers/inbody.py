from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.deps import get_current_user_id
from app.models.inbody import InBodyRecord
from app.schemas.inbody import InBodyCreate, InBodyUpdate, InBodyResponse

router = APIRouter()


@router.get("/", response_model=list[InBodyResponse])
async def list_records(
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(InBodyRecord)
        .where(InBodyRecord.user_id == user_id)
        .order_by(InBodyRecord.measured_at.desc())
    )
    return result.scalars().all()


@router.post("/", response_model=InBodyResponse, status_code=status.HTTP_201_CREATED)
async def create_record(
    data: InBodyCreate,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    record = InBodyRecord(**data.model_dump(), user_id=user_id)
    db.add(record)
    await db.commit()
    await db.refresh(record)
    return record


@router.get("/{record_id}", response_model=InBodyResponse)
async def get_record(
    record_id: int,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(InBodyRecord).where(InBodyRecord.id == record_id, InBodyRecord.user_id == user_id)
    )
    record = result.scalar_one_or_none()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
    return record


@router.put("/{record_id}", response_model=InBodyResponse)
async def update_record(
    record_id: int,
    data: InBodyUpdate,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(InBodyRecord).where(InBodyRecord.id == record_id, InBodyRecord.user_id == user_id)
    )
    record = result.scalar_one_or_none()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(record, field, value)

    await db.commit()
    await db.refresh(record)
    return record


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_record(
    record_id: int,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(InBodyRecord).where(InBodyRecord.id == record_id, InBodyRecord.user_id == user_id)
    )
    record = result.scalar_one_or_none()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")

    await db.delete(record)
    await db.commit()
