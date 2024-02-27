-- query_03.sql
SELECT g.GroupID, AVG(Grade) AS AverageGrade FROM Grades AS g
JOIN Subjects AS s ON g.SubjectID = s.SubjectID
WHERE s.SubjectName = 'Art'
GROUP BY g.GroupID;
