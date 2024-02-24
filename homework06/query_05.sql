-- query_05.sql
SELECT SubjectName
FROM Subjects
WHERE TeacherID = (SELECT TeacherID FROM Teachers WHERE TeacherName = 'Amy Bell');
