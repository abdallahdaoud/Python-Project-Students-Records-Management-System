###########################################################################
###########################################################################
############# id='0002244' for admin mode (like password) #################
###########################################################################
###########################################################################

import re
import os
import matplotlib.pyplot as plt

def userInput(regex):
    answer = input("Enter the input: ")
    while (not re.match(regex, answer)):
        answer = input("Enter the input: ")
    return answer

class Student:
    Tuple = ("ENCS2340", "ENEE2307", "ENCS2110", "ENCS2380", "ENEE2304",
             "ENEE2312", "ENCS2380", "ENCS3130", "ENCS3310", "ENCS4110",
             "ENCS2360", "ENEE3309", "ENCS3320", "ENCS3330", "ENCS3340",
             "ENCS4370", "ENEE2103", "ENEE4113", "ENCS4130", "ENCS3210",
             "ENCS4310", "ENCS4320", "ENCS4380", "ENCS4330", "ENCS5140",
             "ENCS5200", "ENCS5150", "ENCS5300")
    stdsAve = {}
    stdcount = 0
    SemAvgHours = {}  # keeps track of average hours per semester                               #calcAllSemAvgHours
    SemSumHours = {}  # keeps track of how many hours of all student put into this semester     #setStdInfo
    SemTakers = {}  ###keeps tack of how many student in semester                               #setStdInfo
    sems = []  # keeps track of all semesters registered in the system                          #setStdInfo

    def __init__(self, id):
        self.id = str(id)  # student ID number
        self.stdSems = {}  # records grade per course in semesters
        self.courses = {}  # records all grade per course
        self.semAve = {}  # records average grade
        self.semHours = {}  # records the number of hours taken each semester
        self.takenHours = 0  # records taken hours
        self.average = 0  # Overall average grade
        self.remainingCourses = []  # Remaining Courses

        Student.stdcount = Student.stdcount + 1  # count

        if (self.id in os.listdir("all")):
            self.readFromFile()  # get data from file

    def readFromFile(self):
        file = open("all/" + str(self.id), 'r')
        file.readline()  # this is to skip first line
        line = file.readline()
        while (line != '\n') and (line != ''):
            # process Whole Semesters
            sem = (str.split(line, ';')[0])[:-1]
            self.addNewSem(sem)
            strings = str.split(str.split(line, ';')[1], ',')
            # process th courses in one semester
            for s in strings:
                course = str.split(s, ' ')[1]
                grade = str.split(s, ' ')[2]
                self.addOrEditCourse(sem, course, grade)
            line = file.readline()

    def addNewSem(self, sem):
        self.stdSems[sem] = {}

    def addOrEditCourse(self, sem, course, grade):
        self.stdSems[sem][course] = int(grade)

    def avePerSem(self, sem):
        sum = 0
        for course in self.stdSems[sem].keys():
            sum += self.stdSems[sem][course]
        print(sum / len(self.stdSems[sem]))

    def overallAve(self):
        sum = 0
        courseNum = 0
        for sem in self.stdSems.keys():
            for course in self.stdSems[sem].keys():
                sum += self.stdSems[sem][course]
                courseNum += 1
        print(sum / courseNum)

    def writToFile(self):
        record = open("all/" + self.id, "w")
        record.write("Year\Semester ; Courses with grades\n")
        for sem in self.stdSems.keys():
            line = sem + " ;"
            for course in self.stdSems[sem].keys():
                line += " " + course + " " + str(self.stdSems[sem][course]) + ","
            line = line[:-1]
            record.write(line + '\n')
        record.close()

    def isRecordedSemester(self, sem):
        return sem in self.stdSems

    def isInSemester(self, sem, course): # cheack if the course in the semester
        return course in self.stdSems[sem]

    def setStdInfo(self):  # this function will fill out all the student information of a particular student
        self.takenHours = 0  # reset in case of added semesters, we reset this variable each time
        gradevalue = 0
        totalGrades = 0  # this is to keep count track of weighted grades(course grade* course hours)
        # process Whole Semesters
        for sem in self.stdSems:
            sumhours = 0
            gradevalue = 0
            # process the courses in one semester
            for course in self.stdSems[sem]:
                self.courses[course] = self.stdSems[sem][course]
                sumhours += int(course[5])
                gradevalue += int(course[5]) * self.stdSems[sem][course]

            self.semHours[sem] = sumhours
            self.semAve[sem] = gradevalue / sumhours

            if not (sem in Student.SemTakers):
                Student.SemTakers[sem] = 0
            Student.SemTakers[sem] += 1
            if not (sem in Student.SemSumHours):
                Student.SemSumHours[sem] = 0
            Student.SemSumHours[sem] += sumhours
            totalGrades += gradevalue
            self.takenHours += sumhours
        self.average = totalGrades / self.takenHours

    def calcAllSemAvgHours():  # this calculates the average hours per each semester
        for sem in Student.SemTakers:
            Student.SemAvgHours[sem] = Student.SemSumHours[sem] / Student.SemTakers[sem]

    def setRemainingCourses(self): 
        for course in Student.Tuple:
            if not (course in self.courses):
                self.remainingCourses.append(course)

def getID(): #read id from user
    print('Student ID')
    studentID = userInput("^\d{7}$")
    return studentID

# Admin 1)
def addNewRecord():
    studentID = getID()
    if (studentID in os.listdir("all")):
        print(studentID + " isn't unique")
        return 1
    student = Student(studentID)
    addSemester(student)
    student.writToFile()


def getSemester(): #read semester from user
    print('The year of the semester for example (enter 2019 for 2019-2020)')
    year = userInput('^\d{4}$')
    year += "-" + str(int(year) + 1)
    print('First semester (1) second semester (2), summer semester (3)')
    semster = userInput('^[1-3]$')
    sem = year + "/" + semster
    return sem


# Admin 2)
def addSemester(student): 
    answer = 'y'
    while (answer == 'y') or (answer == 'Y'):
        sem = getSemester()
        if (student.isRecordedSemester(sem)):
            print("This semester was recorded")
        else:
            student.addNewSem(sem)
            updateStudentInformation(student, sem)

        print("Did you want to add any semester for "
              + student.id + " [y/n] (yes/no)")
        answer = userInput("[YyNn]")


# Admin 3)
def updateStudentInformation(student, sem):
    answer = 'y'
    while (answer == 'y') or (answer == 'Y'):
        print("[a/c] (Add course / change course grade) for "
              + student.id + " in " + sem)
        answer = userInput("[AaCc]")
        print("Course name")
        course = userInput('^[a-zA-Z]+\d+$')

        if ((answer == 'C') or (answer == 'c')) and (not student.isInSemester(sem, course)):
            print(student.id + " not have " + course + " course in " + sem + " to change")
        else:
            print("Enter course grade (like 90 without %)")
            grade = userInput('^\d{1,3}$')
            student.addOrEditCourse(sem, course, grade)

        print("Did you want to add more course or change for "
              + student.id + " in " + sem + " [y/n] (yes/no)")
        answer = userInput("[YyNn]")


def AllStdAvg(students):  # takes in a list of all students
    sum = 0
    for stu in students:
        # first we calculate the overall student average
        sum += stu.average 
    return sum/Student.stdcount


def calcAllHours(Tuple):  # calculat all houers needed
    sum = 0
    for s in Tuple:
        sum += int(s[5])
    return sum


def printGlobalAdmin():
    students = []
    Averages = []
    for id in os.listdir("all"):
        stu = Student(id)
        stu.setStdInfo()
        Averages.append(stu.average)
        students.append(stu)
    print("All students average grade: " + str(AllStdAvg(students)))
    Student.calcAllSemAvgHours()
    print("Average hours per semester : " + str(Student.SemAvgHours))
    print("Close figure to continue!!") 
    plt.figure("Admin Mode Graph")
    plt.hist(Averages, bins=20)
    plt.xlabel("Average Grades")
    plt.ylabel("Number of students")
    plt.grid()
    plt.title("Histogram for Admin mode")
    plt.show()

def printGlobalStudent():
    students = []
    Averages = []
    IDs=[]
    for id in os.listdir("all"):
        stu = Student(id)
        stu.setStdInfo()
        Averages.append(stu.average)
        IDs.append(stu.id)
        students.append(stu)
    print("All students average grade: " + str(AllStdAvg(students)))
    Student.calcAllSemAvgHours() 
    print("Average hours per semester : " + str(Student.SemAvgHours))
    print("Close figure to continue!!") 
    plt.figure("Student Mode Graph")
    plt.plot(IDs,Averages) 
    plt.xlabel("Student IDs")
    plt.ylabel("Student Averages")
    plt.grid()
    plt.title("graph for student mode")
    plt.show()


# Student 1)
def studentStatistics(studentID):
    stu = Student(studentID)
    stu.setStdInfo()
    stu.setRemainingCourses()
    print("Taken hours: " + str(stu.takenHours))
    print("Remaining hours " + str(calcAllHours(Student.Tuple) - stu.takenHours))
    print("Remaining courses: " + str(stu.remainingCourses))
    print("Overall average: " + str(stu.average))

    print("Did you want to see any semester average for "
          + stu.id + " [y/n] (yes/no)")
    answer = userInput("[YyNn]")
    while (answer == 'y') or (answer == 'Y'):
        sem = getSemester()
        if not (stu.isRecordedSemester(sem)):
            print("This semester wasn't recorded")
        else:
            print(sem + " semester average: " + str(stu.semAve[sem]))
        print("Did you want to see any semester average for "
              + stu.id + " [y/n] (yes/no)")
        answer = userInput("[YyNn]")


# Admin 4)
# the same as studentStatis() but ask about student ID
def studentStatisticsForAdmin():
    studentID = getID()
    if not (studentID in os.listdir("all")):
        print(studentID + " wasn't recorded")
        return 1
    studentStatistics(studentID)

# Admin 5)
def globalStatisticsWithHistogram():
    ################   histogram   #################
    printGlobalAdmin()

# Admin 6)
def searching():
    print("please enter parameter you want to search by, eg (<80)")
    parameter = userInput("[><=][6-9][0-9]")                #since all our records contain courses that are passed, all grades are 60+
    op = parameter[0]
    threshold = int(parameter[1:])
    students = {}
    for id in os.listdir("all"):
        stu = Student(id)
        stu.setStdInfo()
        if (op == '>'):
            if (stu.average > threshold):
                students[id] = stu.average
        elif (op == '='):
            if (stu.average == threshold):
                students[id] = stu.average
        else:
            if (stu.average < threshold):
                students[id] = stu.average
    if (students):
        print("students with Average " + op + " " + str(threshold))
        print(students)
    else:
        print("no students in searched parameter")


# Student 2)
def globalStatisticsWithGraph():
    ################   Graph   #################
    printGlobalStudent()


print("User ID")
id = userInput("^\d{7}$")
# id='0002244' for admin (like password)
while (True):
    Student.stdcount=0 
    if(id == '0002244'):
        print("\n Admin Mode")
        print("------------")
        print("1) Add a new record")
        print("2) Add new semester")
        print("3) Update student information")
        print("4) Student statistics")
        print("5) Global statistics")
        print("6) Searching")
        choice = int(userInput("^[1-6]$"))
        if (choice == 1):
            addNewRecord()
        elif (choice == 2):
            studentID = getID()
            if (not studentID in os.listdir("all")):
                print(studentID + " isn't recorded")
            else:
                stu = Student(studentID)
                addSemester(stu)
                stu.writToFile()
        elif (choice == 3):
            studentID = getID()
            if (not studentID in os.listdir("all")):
                print(studentID + " isn't recorded")
            else:
                stu = Student(studentID)
                sem = getSemester()
                if (stu.isRecordedSemester(sem)):
                    updateStudentInformation(stu, sem)
                    stu.writToFile()
                else:
                    print("This semester wasn't recorded")

        elif (choice == 4):
            studentStatisticsForAdmin()
        elif (choice == 5):
            globalStatisticsWithHistogram()
        elif (choice == 6):
            searching()
        print("exit ? [y,n]")
        answer = userInput("^[YyNn]$")
        if ( answer == 'Y' or answer == 'y'):
            print("Thank you for using our program!")
            exit()
    else:
        if not (id in os.listdir("all")):
            print(id + " wasn't recorded")
            exit()
        else:
            print("\n Student Mode")
            print("--------------")
            print("1) Student statistics")
            print("2) Global statistics")
            choice = int(userInput("[1-2]"))
            if (choice == 1):
                studentStatistics(id)
            elif (choice == 2):
                globalStatisticsWithGraph()
            print("exit ? [y,n]")
            answer = userInput("^[YyNn]$")
            if (answer == 'Y' or answer == 'y'):
                print("Thank you for using our program!")
                exit()


