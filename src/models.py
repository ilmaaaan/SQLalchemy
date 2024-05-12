from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, text 
from database import Base, str_200
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
from typing import Optional, Annotated
import datetime




class WorkersOrm(Base):
    __tablename__ = "workers"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]= mapped_column()

    resumes: Mapped[list["ResumesOrm"]] = relationship(
        back_populates="worker",#Задает связь с таблицей WorkerOrm
    )
    resumes_parttime: Mapped[list["ResumesOrm"]] = relationship(
        back_populates="worker",
        primaryjoin="and_(WorkersOrm.id == ResumesOrm.worker_id, ResumesOrm.workload == 'parttime')", #Задаем условия для вывода резюме только с parttime
        order_by="ResumesOrm.id.desc()", #Сортировка резюме по убыванию индекса
    )


class WorkloadOrm(enum.Enum):
    parttime = "parttime"
    fulltime = "fulltime"

class ResumesOrm(Base):
    __tablename__ = "resumes"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str_200]
    compensation: Mapped[int | None]
    workload: Mapped[WorkloadOrm]
    worker_id: Mapped[int] = mapped_column(ForeignKey(WorkersOrm.id, ondelete='CASCADE'))
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())")) 
    updated_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"),
                                                          onupdate=datetime.datetime.now()) 
    worker: Mapped["WorkersOrm"] = relationship(
        back_populates="resumes",
    )

    vacancies_replied: Mapped[list["VacanciesOrm"]] = relationship(
        back_populates="resumes_replied",
        secondary="vacancies_replies",
    )

class VacanciesOrm(Base):
    __tablename__ = "vacancies"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    compensation: Mapped[Optional[int]]

    resumes_replied: Mapped[list["ResumesOrm"]] = relationship(
        back_populates="vacancies_replied",
        secondary="vacancies_replies", #Показывает посредника связи таблиц resumes и vacancies_replies
    )


class VacanciesRepliesOrm(Base):
    __tablename__= "vacancies_replies"

    resume_id: Mapped[int] = mapped_column(
        ForeignKey("resumes.id", ondelete="CASCADE"),
        primary_key=True,
    )
    vacancy_id: Mapped[int] = mapped_column(
        ForeignKey("vacancies.id", ondelete="CASCADE"),
        primary_key=True,
    )
    cover_letter: Mapped[Optional[str]] #Сопроводительное письмо

metadata_obj = MetaData()

workers_table = Table(
    "workers",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("username", String)
 )


