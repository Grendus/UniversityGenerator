import sqlite3
import os
import random

def createUniversity(name, classrange):
    currentFiles = listUniversities()
    #if the town already exists, append a number to the end and try again
    if name in currentFiles:
        i=1
        while ("%s(%i)"%(name,i)) in currentFiles:
            i+=1
        return createUniversity(name, classrange)
            
    try:
        conn = sqlite3.connect("universities/%s"%name)
        c = conn.cursor()
        c.execute("CREATE TABLE University_Data (name TEXT, num_dice INTEGER, max_dice INTEGER, current_week INTEGER)")
        c.execute("INSERT INTO University_Data VALUES (?,?,?,?)",(name, classrange[0], classrange[1], 0))
        conn.commit()
        conn.close()
        return True
    except:
        return False

def listUniversities():
    return os.listdir("%s/universities"%os.getcwd())

def getWeekCourses(name, week):
    pass

def getCurrentWeekCourses(name):
    pass

def generateCourse():
    return ["Lightning 1",1,1]

def generateWeek(name):
    conn = sqlite3.connect("universities/%s"%name)
    c = conn.cursor()

    #Retrieve the state of the store
    num_dice, max_dice = c.execute("SELECT num_dice, max_dice from University_Data").fetchone()
    currentWeekNumber = c.execute("SELECT current_week from University_Data").fetchone()[0]+1

    #Update the week and create a table for the next week.
    c.execute("UPDATE University_Data SET current_week=?",(currentWeekNumber))
    c.execute("CREATE TABLE Week%i (course_name TEXT, days_required INTEGER, days_left INTEGER, day INTEGER)"%currentWeekNumber)
    
    currently_running_courses = []

    #If there's a previously generated week, retrieve a list of all the courses. Otherwise the course list is a blank list.
    if currentWeekNumber>1:
        currently_running_courses = c.execute("SELECT course_name, days_required, days_left FROM  Week%i WHERE day=5"%(currentWeekNumber-1)).fetchall()
        
    #For each day of the week, remove complete courses and generate new ones if spaces still exist.
    for day_number in range(1,6):
        #Currently the list is holding yesterday's courses.
        #Reduce the days left of each course by 1, and then remove any that are complete
        currently_running_courses = map(lambda x: [x[0],x[1],x[2]-1], currently_running_courses)
        currently_running_courses = filter(lambda x: int(x[2])==0, currently_running_courses)

        #Generate a random number of courses to offer that day, based on the town's size
        num_courses = sum([random.randint(1,max_dice) for x in range(num_dice)])

        #If there are any course slots available after filling the available courses with the still running courses from yesterday, generate new courses
        for x in range(num_courses-len(currently_running_courses)):
            currently_running_courses.append(generateCourse())

        #Insert all courses into the database table.
        for x in currently_running_courses:
            c.execute("INSERT INTO Week%i values (?,?,?,?)"%currentWeekNumber,(x[0],x[1],x[2],day_number))

    conn.commit()
    conn.close()
