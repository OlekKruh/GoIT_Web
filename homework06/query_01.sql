-- query_01.sql
SELECT StudentID, AVG(Grade) AS AverageGrade
FROM Grades
GROUP BY StudentID
ORDER BY AverageGrade DESC
LIMIT 5;
