from sqlite3 import Error

from connect import create_connection, database


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        conn.commit()
    except Error as e:
        print(e)


if __name__ == '__main__':
    Students_table = """
    CREATE TABLE IF NOT EXISTS Students (
     StudentID INTEGER PRIMARY KEY,
     StudentName VARCHAR(50),
     GroupID INT,
     FOREIGN KEY (GroupID) REFERENCES Groups(GroupID)
    );
    """

    Groups_table = """
    CREATE TABLE IF NOT EXISTS Groups (
     GroupID INTEGER PRIMARY KEY,
     GroupName VARCHAR(50)
    );
    """

    Teachers_table = """
    CREATE TABLE IF NOT EXISTS Teachers (
     TeacherID INTEGER PRIMARY KEY,
     TeacherName VARCHAR(50)
    );
    """

    Subjects_table = """
    CREATE TABLE IF NOT EXISTS Subjects (
     SubjectID INTEGER PRIMARY KEY,
     SubjectName VARCHAR(100),
     TeacherID INT,
     FOREIGN KEY (TeacherID) REFERENCES Teachers(TeacherID)
    );
    """

    Grades_table = """
    CREATE TABLE IF NOT EXISTS Grades (
     GradeID INTEGER PRIMARY KEY,
     SubjectID INT,
     StudentID INT,
     Grade INT,
     GradeReceiveDate DATE,
     FOREIGN KEY (StudentID) REFERENCES Students(StudentID),
     FOREIGN KEY (SubjectID) REFERENCES Subjects(SubjectID)
    );
    """

    with create_connection(database) as conn:
        if conn is not None:
            create_table(conn, Students_table)
            create_table(conn, Groups_table)
            create_table(conn, Teachers_table)
            create_table(conn, Subjects_table)
            create_table(conn, Grades_table)
        else:
            print("Error! cannot create the database connection.")
