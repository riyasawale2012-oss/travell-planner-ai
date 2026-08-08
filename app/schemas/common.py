from pydantic import BaseModel
from typing import Optional, List, Generic, TypeVar

T = TypeVar("T")

class PaginationParams(BaseModel):
    page: int = 1
    per_page: int = 20

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    per_page: int
    total_pages: int

class MessageResponse(BaseModel):
    message: str
    success: bool = True

class ErrorResponse(BaseModel):
    detail: str
    status_code: int
    error_code: Optional[str] = None
