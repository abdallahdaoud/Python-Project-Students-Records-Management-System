# Python Project – Students Records Management System
### Problem Overview:
In this project, the system will provide operations related to students record system like add a new
student record, update, search....  
### Where:  
• Year/semester represent the academic year and the current semester. For example: 2021-2022
represent the academic year, 1 represents first semester (2 for second semester, 3 for summer
semester)  
• Courses with grades: lists of course taken in the academic year/semester.
Each student must have separated file and the name of the file will be the student ID.
Scenario:  
• First the user must login to the system. Here there are two types of users: student and admin  
• Then, the program will print the available list of options which is based on the user type  
• The option available includes the following:  
o Admin options:
1. Add a new record file: here the program must ask to enter student ID. The
program must raise an error if the ID is not unique.
2. Add new semester with student course and grades: here the program must ask
to enter the required information (student ID, year/semester, courses and
grades). The system must raise an error if there is missing information or the
information in wrong format.
3. Update: here the system must ask for student ID and the name of the course to
be change and the new grade.
4. Student statistics: first the program must ask for student ID. The program will
print information such as number of taken hours, remaining courses (you need
to create a list/file that contains all ENCS and ENEE courses for computer
engineering program), average per semester, overall average
5. Global statistics: here the program must print information regarding all student
such as overall students average, average hours per semester, plot the
distribution of their grades (histogram).
6. Searching: here the system must retrieve the ID of the students that satisfy the
given criteria. Here you can search for the following: based on average, taken
hours. For example: retrieve the IDs that have an average grater/less/equal than
70.
o Students’ options:
1. Student statistics: here the program must print information such as number of
taken hours, remaining courses, average per semester, overall average.
2. Global statistics: here the program must print information regarding all student
such as overall average, average hours per semester, plot the distribution of
their grades
