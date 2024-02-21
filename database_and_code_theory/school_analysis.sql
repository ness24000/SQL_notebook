-- TO MENTION
-- ORDER OF CODE IS CRUCIAL

-- QUERIES WITHOUT CONDITION

SELECT * 
FROM client;

SELECT client_name, industry
FROM client;

-- INTRODUCING CONDITIONS

SELECT *
FROM course
WHERE language = 'ENG'
ORDER BY level;

-- ORDERING

SELECT *
FROM course
WHERE language = 'ENG'
ORDER BY client;

SELECT *
FROM course
WHERE language = 'ENG'
ORDER BY start_date DESC;

SELECT first_name
FROM teacher
WHERE language_2 = 'ENG'
ORDER BY first_name;

    --HIERARCHICAL ORDERING 
SELECT *
FROM course
WHERE language = 'ENG'
ORDER BY start_date, level;

-- AND, OR, NOT and IN
SELECT * 
FROM course
WHERE language = 'ENG' AND course_length_weeks = 10;

SELECT * 
FROM course
WHERE language = 'ENG' OR course_length_weeks = 10;

SELECT language
FROM course
WHERE NOT language = 'ENG';

SELECT *
FROM course
WHERE language in ('ENG','FRA','RUS') AND course_length_weeks < 40
ORDER BY level;

-- COMPARISON OPERATORS
SELECT first_name, last_name, phone_no
FROM teacher
WHERE dob < '1990-01-01';

SELECT language
FROM course
WHERE language != 'ENG';

-- BETWEEN OPERATOR
SELECT *
FROM teacher
WHERE dob BETWEEN '1990-01-01' AND '1999-12-31'
ORDER BY dob;

-- LIKE OPERATOR AND WILDCARDS
SELECT course_name, level
FROM course
WHERE course_name LIKE '%interm%';

-- IS NULL OPERATOR
SELECT *
FROM teacher 
WHERE language_2 IS NULL;

SELECT *
FROM teacher 
WHERE language_2 IS NOT NULL;

-- AGREGATE FUNCTIONS 
SELECT AVG(course_length_weeks)
FROM course;

SELECT client, AVG(course_length_weeks)
FROM course
GROUP BY client;

SELECT language, COUNT(language)
FROM course
GROUP BY language;

SELECT participant_id, COUNT(participant_id)
FROM takes_course
GROUP BY participant_id
ORDER BY COUNT(participant_id) DESC;

-- NESTED QUERIES 
SELECT *
FROM teacher
WHERE dob > 
    (SELECT AVG(dob)
    FROM teacher);

SELECT course_name
FROM course 
WHERE teacher = (
    SELECT teacher_id
    FROM teacher 
    WHERE first_name = 'Niamh' AND last_name = 'Murphy');

-- INNER JOIN 

SELECT participant.first_name, participant.last_name
FROM participant
JOIN client ON participant.client = client.client_id
WHERE client.industry = 'NGO';

SELECT course.course_name, client.address
FROM client
JOIN course
ON course.client = client.client_id
WHERE course.in_school = FALSE;


SELECT course.course_id, course.course_name, course.in_school, 
client.address
FROM client
JOIN course
ON course.client = client.client_id
WHERE course.in_school = FALSE AND course.teacher = 
    (SELECT teacher_id
    FROM teacher
    WHERE first_name LIKE 'Stef%' AND last_name = 'Martin');


-- All participants in class taught by Niamh Murphy
-- Handling n-to-m relationships in a join

SELECT course.course_name
FROM course
JOIN takes_course ON takes_course.course_id = course.course_id
JOIN participant ON participant.participant_id = takes_course.participant_id
WHERE participant.client = (
    SELECT client_id
    FROM client
    WHERE industry = 'NGO');



-- Outter joins
-- Only useful if some data missing so add new table
CREATE TABLE industry_prospects(
    industry TEXT PRIMARY KEY,
    outlook TEX);

INSERT INTO industry_prospects VALUES
('Retail', 'Good'),
('Hospitality', 'Poor'),
('Logistics', 'Terrible'),
('Tourism', 'Great'),
('Events', 'Good');

-- INNER, LEFT AND RIGHT JOIN

SELECT client.client_id, client.industry, industry_prospects.industry, industry_prospects.outlook
FROM client
JOIN industry_prospects ON client.industry = industry_prospects.industry;

SELECT client.client_id, client.industry, industry_prospects.industry, industry_prospects.outlook
FROM client
LEFT JOIN industry_prospects ON client.industry = industry_prospects.industry;

UPDATE industry_prospects
SET outlook = NULL 
WHERE industry in ('Retail', 'Hospitality')

UPDATE industry_prospects
SET outlook = 'Constant'
WHERE outlook IS NULL;


SELECT * FROM teacher;

SELECT * FROM course;