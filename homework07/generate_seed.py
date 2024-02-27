from datetime import datetime
from connect_db import session
from tables import Teacher, Subject, Group, Student, Grade
from faker import Faker
from random import randint, sample, choice

fake_data = Faker()

SUBJECT_NAMES = ["Mathematics", "Physics", "Chemistry", "Biology", "History", "Literature", "Programming", "Art"]
STUDENTS_QUANTITY = randint(30, 50)
SUBJECTS_QUANTITY = randint(5, 8)
TEACHERS_QUANTITY = randint(3, 5)
GROUP_NAMES = ["Alpha", "Brawo", "Omega"]
GROUPS_QUANTITY = 3
GREADS_QUANTITY = randint(10, 20)


def generate_data():
    gen_teachers = [fake_data.name() for _ in range(TEACHERS_QUANTITY)]
    gen_groups = sample(GROUP_NAMES, GROUPS_QUANTITY)
    gen_subjects = sample(SUBJECT_NAMES, SUBJECTS_QUANTITY)
    gen_students = [fake_data.name() for _ in range(STUDENTS_QUANTITY)]
    gen_grades = [randint(2, 5) for _ in range(SUBJECTS_QUANTITY * STUDENTS_QUANTITY * GREADS_QUANTITY)]

    return gen_teachers, gen_groups, gen_subjects, gen_students, gen_grades


if __name__ == '__main__':
    teachers, groups, subjects, students, grades = generate_data()
    student_id = 0

    for teacher_name in teachers:
        teacher = Teacher(TeacherName=teacher_name)
        session.add(teacher)

    for group_name in groups:
        group = Group(GroupName=group_name)
        session.add(group)

    for subject_name in subjects:
        random_teacher_id = fake_data.random_int(min=1, max=TEACHERS_QUANTITY)
        subject = Subject(SubjectName=subject_name, TeacherID=random_teacher_id)
        session.add(subject)

    for student_name in students:
        student_id += 1
        random_group_id = fake_data.random_int(min=1, max=GROUPS_QUANTITY)
        subject = Student(StudentName=student_name, GroupID=random_group_id)
        session.add(subject)

        for _ in range(GREADS_QUANTITY):
            random_subject_id = fake_data.random_int(min=1, max=SUBJECTS_QUANTITY)
            random_datetime = fake_data.date_between(start_date=datetime(2023, 10, 1),
                                                     end_date=datetime.today())
            grade_add = Grade(SubjectID=random_subject_id, StudentID=student_id, Grade=randint(2, 5),
                              GradeReceiveDate=random_datetime)
            session.add(grade_add)

session.commit()
