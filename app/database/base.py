from sqlalchemy.orm import declarative_base, declared_attr
import re

class CustomBase:
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return re.sub(r'(?<!^)(?=[A-Z])', '_', cls.__name__).lower() + "s"
    __table_args__ = {"extend_existing": True}

Base = declarative_base(cls=CustomBase)
