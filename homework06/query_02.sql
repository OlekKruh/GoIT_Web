-- query_02.sql
SELECT StudentID, AVG(Grade) AS AverageGrade FROM Grades
WHERE SubjectID = 1
GROUP BY StudentID
ORDER BY AverageGrade DESC
LIMIT 1;
