from random import randint, sample, choice
from datetime import datetime
from faker import Faker
from connect import create_connection, database

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


def prepare_data(teachers, groups, subjects, students, grades):
    for_teachers_id = [(teacher_id+1,) for teacher_id, _ in enumerate(teachers)]
    for_teachers = [(teacher, ) for teacher in teachers]

    for_groups_id = [(group_id+1,) for group_id, _ in enumerate(groups)]
    for_groups = [(group, ) for group in groups]

    for_subjects_id = [(subject_id+1,) for subject_id, _ in enumerate(subjects)]
    for_subjects = [(subject, choice(for_teachers_id)[0]) for subject in subjects]

    for_students_id = [(student_id+1,) for student_id, _ in enumerate(students)]
    for_students = [(student, choice(for_groups_id)[0]) for student in students]

    for_grades = [
        (
            choice(for_subjects_id)[0],
            choice(for_students_id)[0],
            grade,
            fake_data.date_between(start_date=datetime(2023, 10, 1),
                                   end_date=datetime.today()).strftime('%Y-%m-%d')
        ) for grade in grades
    ]

    return for_teachers, for_groups, for_subjects, for_students, for_grades


def seed(teachers_fin, groups_fin, subjects_fin, students_fin, grades_fin):
    with create_connection(database) as conn:
        cur = conn.cursor()

        try:
            sql_teachers = '''
            INSERT INTO teachers(TeacherName) VALUES(?)
            '''
            cur.executemany(sql_teachers, teachers_fin)

            sql_groups = '''
                INSERT INTO groups(GroupName) VALUES(?)
                '''
            cur.executemany(sql_groups, groups_fin)

            sql_subjects = '''
                INSERT INTO subjects(SubjectName, TeacherID) VALUES(?, ?)
                '''
            cur.executemany(sql_subjects, subjects_fin)

            sql_students = '''
                INSERT INTO students(StudentName, GroupID) VALUES(?, ?)
                '''
            cur.executemany(sql_students, students_fin)

            sql_grades = '''
                INSERT INTO grades(SubjectID, StudentID, Grade, GradeReceiveDate) 
                VALUES(?, ?, ?, ?)
                '''
            cur.executemany(sql_grades, grades_fin)

            conn.commit()
        except Exception as e:
            print(f"Error during seeding: {e}")


if __name__ == "__main__":
    teachers, groups, subjects, students, grades = generate_data()

    pre_teachers, pre_groups, pre_subjects, pre_students, pre_grades = prepare_data(
        teachers, groups, subjects, students, grades
    )

    seed(pre_teachers, pre_groups, pre_subjects, pre_students, pre_grades)
