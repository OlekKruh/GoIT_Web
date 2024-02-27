from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Teacher(Base):
    __tablename__ = 'Teachers'
    TeacherID = Column(Integer, primary_key=True)
    TeacherName = Column(String(200), nullable=False)


class Group(Base):
    __tablename__ = 'Groups'
    GroupID = Column(Integer, primary_key=True)
    GroupName = Column(String(200), nullable=False)


class Subject(Base):
    __tablename__ = 'Subjects'
    SubjectID = Column(Integer, primary_key=True)
    SubjectName = Column(String(200), nullable=False)
    TeacherID = Column(Integer, ForeignKey('Teachers.TeacherID'))


class Student(Base):
    __tablename__ = 'Students'
    StudentID = Column(Integer, primary_key=True)
    StudentName = Column(String(200), nullable=False)
    GroupID = Column(Integer, ForeignKey('Groups.GroupID'))


class Grade(Base):
    __tablename__ = 'Grades'
    GradeID = Column(Integer, primary_key=True)
    SubjectID = Column(Integer, ForeignKey('Subjects.SubjectID'))
    StudentID = Column(Integer, ForeignKey('Students.StudentID'))
    Grade = Column(Integer)
    GradeReceiveDate = Column(DateTime)
