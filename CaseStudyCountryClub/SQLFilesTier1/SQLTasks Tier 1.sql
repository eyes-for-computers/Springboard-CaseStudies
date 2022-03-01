/* Welcome to the SQL mini project. You will carry out this project partly in
the PHPMyAdmin interface, and partly in Jupyter via a Python connection.

This is Tier 1 of the case study, which means that there'll be more guidance for you about how to 
setup your local SQLite connection in PART 2 of the case study. 

The questions in the case study are exactly the same as with Tier 2. 

PART 1: PHPMyAdmin
You will complete questions 1-9 below in the PHPMyAdmin interface. 
Log in by pasting the following URL into your browser, and
using the following Username and Password:

URL: https://sql.springboard.com/
Username: student
Password: learn_sql@springboard

The data you need is in the "country_club" database. This database
contains 3 tables:
    i) the "Bookings" table,
    ii) the "Facilities" table, and
    iii) the "Members" table.

In this case study, you'll be asked a series of questions. You can
solve them using the platform, but for the final deliverable,
paste the code for each solution into this script, and upload it
to your GitHub.

Before starting with the questions, feel free to take your time,
exploring the data, and getting acquainted with the 3 tables. */


/* QUESTIONS 
/* Q1: Some of the facilities charge a fee to members, but some do not.
Write a SQL query to produce a list of the names of the facilities that do. */

ANSWER: 
SELECT name 
FROM Facilities 
WHERE membercost IS NOT 0




/* Q2: How many facilities do not charge a fee to members? */

Answer: 

SELECT COUNT(name) 
FROM Facilities 
WHERE membercost IS NOT 0 
#phpmyadmin calls for 'IS NOT' to use "!="

/* Q3: Write an SQL query to show a list of facilities that charge a fee to members,
where the fee is less than 20% of the facility's monthly maintenance cost.
Return the facid, facility name, member cost, and monthly maintenance of the
facilities in question. */

Answer: 
SELECT facid as face ,name,membercost,monthlymaintenance 
FROM Facilities 
WHERE membercost < (.2 * monthlymaintenance) AND membercost IS NOT 0 

/* Q4: Write an SQL query to retrieve the details of facilities with ID 1 and 5.
Try writing the query without using the OR operator. */

Answer:
SELECT * 
FROM Facilities 
WHERE facid = 1 
UNION ALL 
SELECT * FROM Facilities WHERE facid = 5;

/* Q5: Produce a list of facilities, with each labelled as
'cheap' or 'expensive', depending on if their monthly maintenance cost is
more than $100. Return the name and monthly maintenance of the facilities
in question. */

Answer:
SELECT name,monthlymaintenance, 
CASE 
WHEN (monthlymaintenance > 100) THEN "expensive" 
WHEN (monthlymaintenance < 100) THEN 'cheap' 
END AS Price FROM Facilities;

/* Q6: You'd like to get the first and last name of the last member(s)
who signed up. Try not to use the LIMIT clause for your solution. */

Answer:
SELECT firstname, surname
FROM Members
ORDER BY joindate DESC

/* Q7: Produce a list of all members who have used a tennis court.
Include in your output the name of the court, and the name of the member
formatted as a single column. Ensure no duplicate data, and order by
the member name. */

Answer:
SELECT CONCAT(firstname, ' ', surname) AS full_name, f.name AS facility
FROM Members AS m
LEFT JOIN Bookings AS b ON m.memid = b.memid
LEFT JOIN Facilities AS f ON b.facid = f.facid
WHERE f.name LIKE '%Tennis Court%'
GROUP BY full_name


/* Q8: Produce a list of bookings on the day of 2012-09-14 which
will cost the member (or guest) more than $30. Remember that guests have
different costs to members (the listed costs are per half-hour 'slot'), and
the guest user's ID is always 0. Include in your output the name of the
facility, the name of the member formatted as a single column, and the cost.
Order by descending cost, and do not use any subqueries. */

Answer:

SELECT f.name AS facility_name, CONCAT(m.firstname, ' ', m.surname) AS full_name,
CASE 
WHEN b.memid = 0
   THEN f.guestcost
   ELSE f.membercost
END AS cost
FROM Bookings AS b
INNER JOIN Members AS m ON b.memid = m.memid
INNER JOIN Facilities AS f ON b.facid = f.facid
WHERE b.starttime LIKE '2012-09-14%'
AND 
(CASE 
   WHEN b.memid =0
   THEN f.guestcost
   ELSE f.membercost
END) > 30
ORDER BY cost DESC;



/* Q9: This time, produce the same result as in Q8, but using a subquery. */

Answer:

SELECT name, full_name, cost
FROM 
(SELECT f.name, b.memid, CONCAT( m.firstname, ' ', m.surname ) AS full_name,
CASE 
   WHEN m.memid =0
   THEN f.guestcost
   ELSE f.membercost
END AS cost, b.starttime
FROM Bookings AS b
LEFT JOIN Facilities AS f ON f.facid = b.facid
LEFT JOIN Members AS m ON b.memid = m.memid
WHERE b.starttime LIKE '2012-09-14%'
) AS Main

WHERE cost > 30;

/* PART 2: SQLite
/* We now want you to jump over to a local instance of the database on your machine. 

Copy and paste the LocalSQLConnection.py script into an empty Jupyter notebook, and run it. 

Make sure that the SQLFiles folder containing thes files is in your working directory, and
that you haven't changed the name of the .db file from 'sqlite\db\pythonsqlite'.

You should see the output from the initial query 'SELECT * FROM FACILITIES'.

Complete the remaining tasks in the Jupyter interface. If you struggle, feel free to go back
to the PHPMyAdmin interface as and when you need to. 

You'll need to paste your query into value of the 'query1' variable and run the code block again to get an output.
 
QUESTIONS:
/* Q10: Produce a list of facilities with a total revenue less than 1000.
The output of facility name and total revenue, sorted by revenue. Remember
that there's a different cost for guests and members! */

Answer:

SELECT name, total revenue

SELECT f.name,
SUM(
CASE 
   WHEN m.memid = 0
   THEN f.guestcost
   WHEN m.memid <> 0
   THEN f.membercost
END ) AS Total_Revenue
FROM Facilities AS f
LEFT JOIN Bookings AS b ON f.facid = b.facid
LEFT JOIN Members AS m ON b.memid = m.memid
GROUP BY f.name
HAVING Total_Revenue < 1000
ORDER BY Total_Revenue;


/* Q11: Produce a report of members and who recommended them in alphabetic surname,firstname order */

Answer:

SELECT firstname, surname, (

SELECT CONCAT( firstname, ' ', surname )
FROM Members AS m
WHERE (

CASE WHEN memid = RecommenderId
THEN memid
ELSE NULL
END)
) AS recommended_by

FROM (

SELECT m1.memid, m1.firstname AS firstname, m1.surname AS surname, m1.recommendedby AS RecommenderID
FROM Members AS m1
INNER JOIN Members AS m2 ON m1.memid = m2.memid
ORDER BY m1.surname, m1.firstname
) AS Main;


/* Q12: Find the facilities with their usage by member, but not guests */

Answer:

SELECT f.name AS facility_name, COUNT( * ) AS facility_use, b.memid
FROM Facilities AS f
LEFT JOIN Bookings AS b ON f.facid = b.facid
WHERE b.memid !=0
GROUP BY b.memid
ORDER BY facility_use;


/* Q13: Find the facilities usage by month, but not guests */

Answer:

SELECT  EXTRACT(MONTH from starttime) AS Month, f.name AS facility_name, COUNT( * ) AS facility_use, b.memid
FROM Bookings AS b
LEFT JOIN Facilities AS f ON b.facid = f.facid
WHERE b.memid !=0
GROUP BY Month;


