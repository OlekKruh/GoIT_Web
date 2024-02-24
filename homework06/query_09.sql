-- query_09.sql
SELECT DISTINCT sub.SubjectName
FROM Grades g
JOIN Subjects sub ON g.SubjectID = sub.SubjectID
JOIN Students s ON g.StudentID = s.StudentID
WHERE s.StudentName = 'Eric Bradley';
