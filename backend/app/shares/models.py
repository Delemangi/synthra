import uuid

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..models import Base


class Share(Base):
    __tablename__ = "shares"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="shared_files")
    file_id = Column(UUID(as_uuid=True), ForeignKey("file.id"), nullable=False)
    file = relationship("File", back_populates="shared_with")
