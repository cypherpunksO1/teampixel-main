from datetime import datetime
from sqlalchemy import UUID, DateTime, ForeignKey, String, func, Enum, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.config.templates import DEFAULT_AVATAR

from core.models import Base
from src.users.consts import Role
from src.portals.models import Department
from src.courses.models import UserCourse, UserTest


class User(Base):
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    patronymic: Mapped[str] = mapped_column(String, nullable=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[bytes] = mapped_column(String)
    birth_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True
    )
    avatar: Mapped[str] = mapped_column(String, default=DEFAULT_AVATAR)
    role: Mapped[Role] = mapped_column(Enum(Role), default=Role.WORKER.value)
    is_dismissed: Mapped[bool] = mapped_column(Boolean, default=False)

    department_id: Mapped[UUID] = mapped_column(ForeignKey("portals_department.id"), nullable=True)
    portal_id: Mapped[UUID] = mapped_column(ForeignKey("portals_portal.id"), nullable=True)

    courses: Mapped[list["UserCourse"]] = relationship("UserCourse", lazy="selectin")
    tests: Mapped[list["UserTest"]] = relationship("UserTest", lazy="selectin")
    portal: Mapped["Portal"] = relationship(
        "Portal", lazy="selectin", foreign_keys="User.portal_id"
    )
    department: Mapped["Department"] = relationship("Department", lazy="selectin")
    
    
    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.patronymic}, '\
                f'департамент «{self.department}», '\
                f'портал «{self.portal}»'


class Review(Base):
    text: Mapped[str] = mapped_column(Text)
