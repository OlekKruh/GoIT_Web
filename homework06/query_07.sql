-- query_07.sql
SELECT s.StudentName, g.Grade
FROM Grades g
JOIN Students s ON g.StudentID = s.StudentID
JOIN Subjects sub ON g.SubjectID = sub.SubjectID
JOIN Groups grp ON s.GroupID = grp.GroupID
WHERE grp.GroupName = 'Omega' AND sub.SubjectName = 'Art';
