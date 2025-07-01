from datetime import datetime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String
from sqlalchemy import func
from sqlalchemy import Enum as SQLEnum
from enum import Enum as PyEnum
from infra.db.base import Base


class StatusOrder(str, PyEnum):
    PENDING = "Pending"
    PROCESSING = "Processing"
    COMPLETED = "Completed"
    FAILED = "Failed"


class Order(Base):
    user_email: Mapped[str] = mapped_column(unique=True)
    item_name: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[StatusOrder] = mapped_column(SQLEnum(StatusOrder), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
