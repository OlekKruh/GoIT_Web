-- query_08.sql
SELECT AVG(Grade) AS AverageGrade
FROM Grades g
JOIN Subjects sub ON g.SubjectID = sub.SubjectID
JOIN Teachers t ON sub.TeacherID = t.TeacherID
WHERE t.TeacherName = 'Sarah Sanders' AND sub.SubjectName = 'Literature';
