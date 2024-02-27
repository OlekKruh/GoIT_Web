-- query_04.sql
SELECT GroupID, AVG(Grade) AS AverageGrade FROM Grades
GROUP BY GroupID;