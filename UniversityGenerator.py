import ast
import sqlite3
import os

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
    conn = sqlite3.connect("universities/%s"%name)
    c = conn.cursor()
    c.execute("CREATE TABLE University_Data (name TEXT, min INTEGER, max INTEGER, current_week INTEGER)")
    c.execute("INSERT INTO University_Data VALUES (?,?,?,?)",(name, classrange[0], classrange[1], 1))
    conn.commit()
    conn.close()
    viewUniversity(name)
    
    
def viewUniversity(name=None):
    print "\n\n"
    if name == None:
        universities = os.listdir("%s/universities"%os.getcwd())
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
    conn = sqlite3.connect("universities/%s"%name)
    c = conn.cursor()
                

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
