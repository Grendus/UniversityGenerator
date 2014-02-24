import ast
import sqlite3
import os
import controller

verbose = False

def createUniversity():
    print "\n\n"
    while True:
        name = raw_input("What would you like to call your university?\n")
        if name!='':
            break
    while True:
        classrange = ('','')
        try:
            classes = raw_input("How many courses per week does this university offer (input a die range, I.E. 1d4, 2d6, etc.):\n").split("d")
            classrange = (int(classes[0]), int(classes[1]))
        except ValueError:
            print "\nI'm sorry, I didn't quite catch that.\n"
        if classrange != ('',''):
            break
    if controller.createUniversity(name, classrange):
        viewUniversity(name)
    else:
        print "Error: unable to create town."
    
    
def viewUniversity(name=None):
    print "\n\n"
    if name == None:
        universities = controller.listUniversities()
        while name == None:
            print "Which university would you like to view?"
            for x in range(len(universities)):
                print "%i. %s"%(x+1,universities[x])
            choice = raw_input("Input the number of the university you want to view, or 'q' to return.\n")
            if choice == "q":
                return
            try:
                name = universities[int(choice)-1]
            except (TypeError, IndexError, ValueError):
                name == None
                print "\nI'm sorry, I didn't quite catch that\n"

    print "\n\nUniversity loaded successfully!\n\n\n\n\n"

    while True:
        choice=raw_input("Would you like to (v)iew the current weak, view a (p)revious week, generate the (n)ext week, or (r)eturn to the main menu?\n")
        try:
            if choice == "v":
                printWeek(controller.getCurrentWeekCourses(name, controller.currentWeek(name)))
            elif choice == "p":
                currentWeek = controller.currentWeek(name)
                week = int(raw_input("\n\nCurrent week is %i. Which week would you like to view?\n"%currentWeek))
                printWeek(controller.getWeekCourses(name, week))
            elif choice == "n":
                controller.generateWeek(name)
            elif choice == "r":
                return
            else:
                print "\nI'm sorry, I didn't quite catch that\n"
        except ValueError:
            print "\nOops, something unexpected happened. Please try again.\n\n"

def printWeek(week):
    pass

def deleteUniversity(name=None):
    pass

if __name__=="__main__":
    choice=""
    
    print "Welcome to the ELF University Generator\n"
    while True:
        choice = raw_input("Would you like to create a (n)ew university, (v)iew a university, (d)elete a university, or (q)uit?\n")
        if choice == "n":
            createUniversity()
        elif choice == "v":
            viewUniversity()
        elif choice == "q":
            break
        elif choice == "d":
            deleteUniversity()
        else:
            print "\nI'm sorry, I didn't quite catch that.\n"
