from sqlalchemy import select, func, desc
from tables import Teacher, Subject, Group, Student, Grade
from connect_db import session


def select_test():
    stmt = (
        select(Teacher.TeacherID, Teacher.TeacherName).where(Teacher.TeacherName.like("%a%"))
    )
    result = session.execute(stmt)
    for teacher_id, teacher_name in result:
        print(f'Teacher ID: {teacher_id}\n'
              f'Teacher Name: {teacher_name}')


def select_01():
    stmt = (
        select(Grade.StudentID, func.avg(Grade.Grade).label('AverageGrade'))
        .group_by(Grade.StudentID)
        .order_by(desc('AverageGrade'))
        .limit(5)
    )
    result = session.execute(stmt)
    for student_id, average_grade in result:
        print(f'Student ID: {student_id}\n'
              f'Average Grade: {average_grade}')


def select_02():
    subject_id = 2
    stmt = (
        select(Grade.StudentID, func.avg(Grade.Grade).label('AverageGrade'))
        .filter(Grade.SubjectID == subject_id)
        .group_by(Grade.StudentID)
        .order_by(desc('AverageGrade'))
        .limit(1)
    )
    result = session.execute(stmt)
    for student_id, average_grade in result:
        print(f'Student ID: {student_id}\n'
              f'Average Grade in the Subject ID {subject_id}: {average_grade}')


def select_03():
    subject_id = 3
    stmt = (
        select(Student.GroupID, func.avg(Grade.Grade).label('AverageGrade'))
        .join(Grade, Student.StudentID == Grade.StudentID)
        .filter(Grade.SubjectID == subject_id)
        .group_by(Student.GroupID)
    )
    result = session.execute(stmt)
    for group_id, average_grade in result:
        print(f'Group ID: {group_id}\n'
              f'Average Grade: {average_grade}\n')


def select_04():
    stmt = (
        select(func.avg(Grade.Grade).label('AverageGrade'))
    )
    result = session.execute(stmt)
    for average_grade in result:
        print(f'Overall Average Grade: {average_grade[0]}')


def select_05():
    teacher_id = 2
    stmt = (
        select(Subject.SubjectName)
        .filter(Subject.TeacherID == teacher_id)
    )
    result = session.execute(stmt)
    if result:
        print(f'Courses taught by Teacher {teacher_id}:')
        for course_name, in result:
            print(course_name)
    else:
        print(f'Teacher with ID {teacher_id} not found or not teaching any courses.')


def select_06():
    group_id = 2
    stmt = (
        select(Student.StudentName)
        .filter(Student.GroupID == group_id)
    )
    result = session.execute(stmt)
    if result:
        print(f'Students in Group {group_id}:')
        for student_name, in result:
            print(student_name)
    else:
        print(f'Group with ID {group_id} not found or does not have any students.')


def select_07():
    subject_id = 1
    group_id = 1
    stmt = (
        select(Student.StudentName, Grade.Grade)
        .join(Grade, Student.StudentID == Grade.StudentID)
        .filter(Student.GroupID == group_id, Grade.SubjectID == subject_id)
    )
    result = session.execute(stmt)
    if result:
        print(f'Grades for students in Group {group_id} for Subject {subject_id}:')
        for student_name, grade in result:
            print(f'Student: {student_name}, Grade: {grade}')
    else:
        print(f'No grades found for students in Group {group_id} for Subject {subject_id}.')


def select_08():
    teacher_id = 1
    stmt = (
        select(func.avg(Grade.Grade).label('AverageGrade'))
        .join(Subject, Grade.SubjectID == Subject.SubjectID)
        .filter(Subject.TeacherID == teacher_id)
    )
    result = session.execute(stmt)
    for row in result:
        print(f'Average Grade given by Teacher {teacher_id}: {row[0]}')


def select_09():
    student_id = 2
    stmt = (
        select(Subject.SubjectName)
        .join(Grade, Subject.SubjectID == Grade.SubjectID)
        .filter(Grade.StudentID == student_id)
        .distinct()
    )
    result = session.execute(stmt)
    if result:
        print(f'Courses attended by Student {student_id}:')
        for course_name, in result:
            print(course_name)
    else:
        print(f'Student with ID {student_id} not found or not attending any courses.')


def select_10():
    student_id = 1
    teacher_id = 3
    stmt = (
        select(Subject.SubjectName)
        .join(Grade, Subject.SubjectID == Grade.SubjectID)
        .join(Teacher, Subject.TeacherID == Teacher.TeacherID)
        .filter(Grade.StudentID == student_id, Teacher.TeacherID == teacher_id)
        .distinct()
    )
    result = session.execute(stmt)
    if result:
        print(f'Courses attended by Student {student_id} taught by Teacher {teacher_id}:')
        for course_name, in result:
            print(course_name)
    else:
        print(f'Student with ID {student_id} or Teacher with ID {teacher_id} not found or no courses found.')


if __name__ == '__main__':
    # select_test()
    # select_01()
    # select_02()
    # select_03()
    # select_04()
    # select_05()
    # select_06()
    # select_07()
    # select_08()
    # select_09()
    # select_10()
    pass

