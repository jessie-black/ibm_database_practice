## AFTER LOADING PROVIDED CSV DOCUMENT IN IBM DB2, CONNECTED TO DATABASE AND PERFORMED QUERIES BELOW TO 
## ANSWER QUESTIONS/PROMPTS (COMMENTED OUT HERE). LAST 2 LINES REQUIRED CONSULTING SOLUTIONS BUT OTHERS 
## WERE FINE.

# These libraries are pre-installed in SN Labs. If running in another environment please uncomment lines below to install them:
# !pip install --force-reinstall ibm_db==3.1.0 ibm_db_sa==0.3.3
# Ensure we don't load_ext with sqlalchemy>=1.4 (incompadible)
# !pip uninstall sqlalchemy==1.4 -y && pip install sqlalchemy==1.3.24
# !pip install ipython-sql

%load_ext sql

# Enter the connection string for your Db2 on Cloud database instance below
# %sql ibm_db_sa://my-username:my-password@my-hostname:my-port/my-db-name?security=SSL
%sql ibm_db_sa://

# type in your query to retrieve list of all tables in the database for your db2 schema (username)%
%sql SELECT tabschema, tabname, create_time FROM syscat.tables WHERE tabschema='QWW69437'

# type in your query to retrieve the number of columns in the SCHOOLS table
%sql select count(*) from SYSCAT.COLUMNS where TABNAME = 'SCHOOLS'

# type in your query to retrieve all column names in the SCHOOLS table along with their datatypes and length
%sql SELECT colname, typename, length FROM SYSCAT.COLUMNS WHERE TABNAME='SCHOOLS'

# How many elementary schools in data set?
%sql SELECT COUNT(*) FROM SCHOOLS WHERE "Elementary, Middle, or High School" = 'ES'

# What is the highest safety score?
%sql SELECT MAX(safety_score) FROM SCHOOLS

# Which schools have highest safety score?
%sql SELECT name_of_school, safety_score from SCHOOLS WHERE safety_score =99

# What are the top 10 schools with the highest "Average Student Attendance"?
%sql SELECT name_of_school, average_student_attendance FROM SCHOOLS ORDER BY average_student_attendance desc nulls last limit 10

#Retrieve the list of 5 Schools with the lowest Average Student Attendance sorted in ascending order based on attendance
%sql SELECT name_of_school, average_student_attendance FROM SCHOOLS ORDER BY average_student_attendance asc nulls last limit 5

# Now remove the '%' sign from the above result set for Average Student Attendance column
%sql SELECT name_of_school, REPLACE(average_student_attendance,'%','') as avg_attendance FROM SCHOOLS ORDER BY average_student_attendance asc nulls last limit 5

# Get the total College Enrollment for each Community Area
%sql SELECT community_area_name, SUM(college_enrollment) from SCHOOLS GROUP BY community_area_name ORDER BY community_area_name

# Get the 5 Community Areas with the least total College Enrollment sorted in ascending order
%sql SELECT community_area_name, SUM(college_enrollment) from SCHOOLS GROUP BY community_area_name ORDER BY SUM(college_enrollment) ASC LIMIT 5

# List 5 schools with lowest safety score.
%sql SELECT name_of_school, safety_score FROM SCHOOLS ORDER BY safety_score asc LIMIT 5

# Get the hardship index for the community area which has College Enrollment of 4368
# (Needed to check solution for this -- it refers to a column in a table from a previous lab)
%%sql 
select hardship_index 
   from chicago_socioeconomic_data CD, schools CPS 
   where CD.ca = CPS.community_area_number 
      and college_enrollment = 4368
#Get the hardship index for the community area which has the school with the highest enrollment.
# (NEEDED TO CHECK SOLUTION FOR THIS)
%sql select ca, community_area_name, hardship_index from chicago_socioeconomic_data \
   where ca in \
   ( select community_area_number from schools order by college_enrollment desc limit 1 )
