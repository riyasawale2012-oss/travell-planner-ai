from fastapi import Query
from typing import Optional

class Pagination:
    def __init__(self, page: int = Query(1, ge=1), per_page: int = Query(20, ge=1, le=100)):
        self.page = page
        self.per_page = per_page

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.per_page
