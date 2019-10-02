from sqlalchemy import Table, Column, String, Integer

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Vacancy(Base):
    __tablename__ = 'vacancy'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    spider = Column(String, nullable=True)
    name = Column(String, nullable=True)
    salary = Column(String, nullable=True)
    employer_name = Column(String, nullable=True)
    vacancy_link = Column(String, nullable=True)

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.spider = kwargs.get('spider')
        self.salary = kwargs.get('salary')
        self.employer_name = kwargs.get('employer_name')
        self.vacancy_link = kwargs.get('vacancy_link')
