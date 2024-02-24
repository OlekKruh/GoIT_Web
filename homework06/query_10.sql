-- query_10.sql
SELECT DISTINCT sub.SubjectName
FROM Grades g
JOIN Subjects sub ON g.SubjectID = sub.SubjectID
JOIN Teachers t ON sub.TeacherID = t.TeacherID
JOIN Students s ON g.StudentID = s.StudentID
WHERE t.TeacherName = 'Dennis Sanders' AND s.StudentName = 'Richard Smith';
