-- query_06.sql
SELECT StudentName
FROM Students
WHERE GroupID = (SELECT GroupID FROM Groups WHERE GroupName = 'Brawo');
