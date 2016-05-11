import cherrypy
import os
import os.path
from database import *
import requests
import datetime
from teacher import Teachers
from student import Students
import bottlenose
from bs4 import BeautifulSoup

class Admin(object):

    def __init__(self):
        self.teachers = Teachers()
        self.students = Students()
        
    @cherrypy.expose
    def index(self, school_name=""): 
        yield '''<html>
        <head>
            <link href="/static/css/style.css" rel="stylesheet">
            <title>Capstone Application</title>
          </head>
        '''
        yield '''<div 
            style="background-image:
                   url('http://www.rycorsoftware.com/SFimages/default-source/leaf-textbook-management-images/leaf-banner_tinypng.png?sfvrsn=2'); 
            width:100%; 
            height:100px; 
            background-position:center;">&nbsp;</div>'''
        yield '''<h1>Administrator Registration</h1> '''
        yield '''<h2>Please enter your school information</h2></br>'''
        yield '''
        <form action="admin_home">
        <div id="s">School Name: <input id="school_name" type="text" name="school_name" ></br>''' 
        yield'''</br></br>Type: <select name="school_type">
          <option value="College">College</option>
          <option value="University">University</option>
          <option value="High">High</option>
          <option value="Middle">Middle</option>
          <option value="Elementary" >Elementary</option>
          <option value="Other">Other</option>
        </select>'''
        yield '''</br>'''

        yield '''</br></br><div id = "b"><button id="login" type="submit" >Register</button></div></form>'''
        yield '''</br></br></br><form action = "reset"><button id="sel" type="submit" >RESET DATABASE</button></form></br>'''


    @cherrypy.expose
    def admin_home(self, school_name,school_type):
        yield '''<html>
        <head>
            <link href="/static/css/style.css" rel="stylesheet">
            <title>Capstone Application</title>
          </head>
        '''

        self.school_name = school_name
        self.school_type = school_type
        if(school_name != ""):
            exists = session.query(School.name).filter_by(name=school_name).scalar() 
            if (exists is None):             
                new_school = School(name=school_name, grade = school_type)
                session.add(new_school)
                session.commit()
        school_id = 0
        for school in session.query(School):
            if (school_name == school.name and school_type == school.grade):
                school_id = school.id
        yield '''<div 
            style="background-image:
                   url('http://www.rycorsoftware.com/SFimages/default-source/leaf-textbook-management-images/leaf-banner_tinypng.png?sfvrsn=2'); 
            width:100%; 
            height:100px; 
            background-position:center;">&nbsp;</div>'''
        
        yield '''<div id = "navigation_bar"><ul>
          <li><a href="/admin_home?school_name=%s&school_type=%s">Home</a></li>
          <li><a href="/admin_action?opt=%i&school_id=%s">View My Information</a></li>
          
          <li><a href="/teachers">Teacher Application</a></li>
          <li><a href="/students">Student Application</a></li>
          <li><a href="/">Logout</a></li>
          <li style="float:right"><a >%s %s</a></li>
        </ul></div>''' %(school_name, school_type, 4,school_id, school_name, school_type)
        yield '''<h1>Administrator Home</h1>'''
        yield '''
        <form action="admin_action">
        <div id="s">'''
        yield '''<label for="optout" >
        <input type="radio" name="opt" value="1" checked="checked"/>Enter Student List
        </label></br>
        <label for="optout">
        <input type="radio" name="opt" value="2"/>Enter Teacher List
        </label></br>
        <label for="optout">
        <input type="radio" name="opt" value="3"/>Enter Course List
        </label></br>
        
        '''
        yield '''<input type="hidden" name="school_id" value=%s />'''%school_id
        yield '''<button id="submit" type="submit" >Submit</button></form></div>'''
        
   
    @cherrypy.expose
    def admin_action(self, opt, school_id):
        yield '''<html>
        <head>
            <link href="/static/css/style.css" rel="stylesheet">
            <title>Capstone Application</title>
          </head>
        '''
        schl = session.query(School).get(int(school_id))
        school_name= schl.name
        school_type = schl.grade
        yield '''<div 
            style="background-image:
                   url('http://www.rycorsoftware.com/SFimages/default-source/leaf-textbook-management-images/leaf-banner_tinypng.png?sfvrsn=2'); 
            width:100%; 
            height:100px; 
            background-position:center;">&nbsp;</div>'''
        yield '''<div id = "navigation_bar"><ul>
          <li><a href="/admin_home?school_name=%s&school_type=%s">Home</a></li>
          <li><a href="/admin_action?opt=%i&school_id=%s">View My Information</a></li>
          
          <li><a href="/teachers">Teacher Application</a></li>
          <li><a href="/students">Student Application</a></li>
          <li><a href="/">Logout</a></li>
          <li style="float:right"><a >%s %s</a></li>
        </ul></div>''' %(school_name, school_type, 4,school_id, school_name, school_type)
        #enter list of students
        if opt =="1":
            yield '<body>'
            yield '''<h3>Edit or Add a Student Username</h3>'''
            yield '''<div id = "add">'''
            yield '<form action="entered">'
            yield 'Add Student Username:<br>'
            yield '<br><input type ="field", name="new_student" value><br><br>'
            yield '''<input type="hidden" name="school_id" value=%s />'''%school_id
            yield '<input type="submit" value="Add">'
            yield '</form>'
            yield '''</div>'''
            yield '<div id=user>'
            yield '''<form action = "edit">'''
            for person in session.query(Student):
                if (int(school_id)== person.school_id):
                    name = person.username
                    yield '''
                     <input type="checkbox" name="student" value="%s">%s
                    ''' % (name, name)
                    yield '<br>'
            yield '''<input type="hidden" name="school_id" value=%s />'''%school_id
            yield '''<br><input type="submit" value="Edit Selected"></form>'''
            yield '</div>'
            
            yield '</body>'
        # Enter list of teachers
        elif opt == "2":
            yield '''<h3>Edit or Add a Teacher Username</h3>'''
            yield '<body>'
            yield '''<div id = "add">'''
            yield '<form action="entered" >'
            yield 'Add Teacher Username:<br>'
            yield '<br><input type ="field", name="new_teacher" value><br><br>'
            yield '''<input type="hidden" name="school_id" value=%s />'''%school_id
            yield '<input type="submit" value="Add">'
            yield '</form></div>'
            yield '<div id=user>'
            yield '''<form action = "edit">'''
            for person in session.query(Teacher):
                if (int(school_id)== person.school_id):
                    name = person.username
                    yield '''
                     <input type="checkbox" name="teacher" value="%s">%s
                    ''' % (name, name)
                    yield '<br>'
            yield '''<input type="hidden" name="school_id" value=%s />'''%school_id
            yield '''<br><input type="submit" value="Edit Selected"></form>'''
            yield '</div>'
            
            yield '</body>'
        # Enter list of courses
        elif opt == "3":
            yield '''<h3>Edit or Add Courses</h3>'''
            yield '<body>'
            yield '''<div id = "add">'''
            yield '''<form action = "entered">'''
            yield 'Add Course:<br>'
            yield '<br><input type ="field" id = "c" name="new_course_subject" placeholder="Course Subject Code (ex: CSCI)" columns = 20>'
            yield '<input type ="field" id = "c" name="new_course_number" placeholder="Course Subject Number (ex: 381)"><br><br>'
            yield '''<input type="hidden" name="school_id" value=%s />'''%school_id
            yield '<input type="submit" value="Submit">'
            yield '</form></div>'
            yield '<div id = "user"><form action="edit">'
            for course in session.query(Courses):
                if (int(school_id)== course.school_id):
                    name = course.subject + " " + course.number
                    yield '''
                     <input type="checkbox" name="course" value="%s">%s
                    ''' % (name, name)
                    yield '<br>'
            yield '''<input type="hidden" name="school_id" value=%s />'''%school_id
            yield '''<br><input type="submit" value="Edit Selected"></form>'''
            yield '</div>'
            
            yield '</body>'
        elif opt == "4":
            schl = session.query(School).get(int(school_id))
            yield '''<div id = "marg"><h4>Information for %s<br></h4>'''% schl.name
            yield '<div id=list>'
            yield '''Student List:<br><br>'''
            for person in session.query(Student):
                if (int(school_id)== person.school_id):
                    name = person.username
                    yield '''
                    * %s<br>
                    ''' % (name)
            yield '</div>'
            yield '<div id=list>'
            yield '''Teacher List:<br><br>'''
            for person in session.query(Teacher):
                if (int(school_id)== person.school_id):
                    name = person.username
                    yield '''
                    * %s<br>
                    ''' % (name)
            yield '</div>'
            yield '<div id=list>'
            yield '''Course List:<br><br>'''
            for course in session.query(Courses):
                if (int(school_id)== course.school_id):
                    name = course.subject + " " + course.number
                    
                    yield '''
                    * %s<br>
                    ''' % (name)
            yield '</div>'
            yield '</div>'


    @cherrypy.expose
    def entered(self, **args):
        message = ""
        opt = 0
        school_id = args['school_id']
        if 'new_student' in args:
            new_name = args['new_student']

            if(new_name != ""):
                exists = session.query(Student.username).filter_by(username=new_name,school_id=int(school_id)).scalar() 
                if (exists is None):  
                                 
                    new_person = Student(username=new_name, school_id = int(school_id)) 
                    session.add(new_person)
                    session.commit()
                yield new_name
                message += new_name + ", "
                opt = 1
                # yield '<br>'
        if 'new_teacher' in args:
            new_name = args['new_teacher']
            if(new_name != ""):
                exists = session.query(Teacher.username).filter_by(username=new_name,school_id=int(school_id)).scalar() 
                if (exists is None):   
                    new_person = Teacher(username=new_name,school_id = int(school_id))
                    session.add(new_person)
                    session.commit()
                yield new_name
                message += new_name + ", "
                opt = 2
        occurs = 1
        if 'new_course_number' and 'new_course_subject' in args:
            new_course_number = args['new_course_number']
            new_course_subject = args['new_course_subject']
            if(new_course_number != "" and new_course_subject != ""):
                for course in session.query(Courses):
                    if (int(school_id) == course.school_id):
                        if (course.subject == new_course_subject):
                            if (course.number == new_course_number):
                                occurs = 0               
                           
                if occurs == 1:
                    new_course = Courses(subject=new_course_subject, number = new_course_number, school_id = int(school_id))
                    session.add(new_course)
                    session.commit()
                    message += new_course_subject + " " + new_course_number + ", "
                opt = 3
        if 'student_username' in args:
            student_username = args['student_username']
            student_id = args['student_id']
            if(student_username != ""):
                exists = session.query(Student.username).filter_by(username=student_username,school_id=int(school_id)).scalar() 
                if (exists is None):   
                    stud = session.query(Student).get(int(student_id))
                    stud.username = student_username
                    session.commit()
            opt = 1
        if 'teacher_username' in args:
            teacher_username = args['teacher_username']
            teacher_id = args['teacher_id']
            if(teacher_username != ""):
                exists = session.query(Teacher.username).filter_by(username=teacher_username,school_id=int(school_id)).scalar() 
                if (exists is None):   
                    teach = session.query(Teacher).get(int(teacher_id))
                    teach.username = teacher_username
                    session.commit()
            opt = 1
        if 'course_number' in args:
            course_number = args['course_number']
            course_id = args['course_id']
            crs = session.query(Courses).get(int(course_id))
            occurs = 1
            if (course_number != ""):
                for course in session.query(Courses):
                    if (int(school_id) == course.school_id):
                        if (course.number == course_number):
                            if (course.subject == crs.subject):
                                occurs = 0               
                           
                if occurs == 1:
                    crs.number = course_number
                    session.commit()
            opt = 3
        if 'course_subject' in args:
            course_subject = args['course_subject']
            course_id = args['course_id']
            crs = session.query(Courses).get(int(course_id))
            occurs = 1
            if (course_subject != ""):
                for course in session.query(Courses):
                    if (int(school_id) == course.school_id):
                        if (course.subject == course_subject):
                            if (course.number == crs.number):
                                occurs = 0               
                           
                if occurs == 1:
                    crs.subject = course_subject
                    session.commit()
            opt = 3


        message += "Entered"
        cherrypy.session['message'] = message
        raise cherrypy.HTTPRedirect('/admin_action?opt=%i&school_id=%s' % (opt,school_id))



    @cherrypy.expose
    def edit(self, **args):
        yield '''<html>
        <head>
            <link href="/static/css/style.css" rel="stylesheet">
            <title>Capstone Application</title>
          </head>
        '''
        school_id = args['school_id']
        sl = session.query(School).get(int(school_id))
        school_name = sl.name
        school_type = sl.grade
        yield '''<div 
            style="background-image:
                   url('http://www.rycorsoftware.com/SFimages/default-source/leaf-textbook-management-images/leaf-banner_tinypng.png?sfvrsn=2'); 
            width:100%; 
            height:100px; 
            background-position:center;">&nbsp;</div>'''
        
        yield '''<div id = "navigation_bar"><ul>
          <li><a href="/admin_home?school_name=%s&school_type=%s">Home</a></li>
          <li><a href="/admin_action?opt=%i&school_id=%s">View My Information</a></li>
          
          <li><a href="/teachers">Teacher Application</a></li>
          <li><a href="/students">Student Application</a></li>
          <li><a href="/">Logout</a></li>
          <li style="float:right"><a >%s %s</a></li>
        </ul></div>''' %(school_name, school_type, 4,school_id, school_name, school_type)
        if 'teacher' in args:
            person = args['teacher']
            for teach in session.query(Teacher):
                if (teach.username == person and teach.school_id == int(school_id)):
                    yield '''<h3>Edit Teacher Username</h3>'''
                    yield '''<div id = "ent">'''
                    yield '<form action="entered">'
                    yield '''
                     <input type="text" name="teacher_username" value="%s">
                    ''' % (teach.username)
                    yield '''<input type="hidden" name="teacher_id" value=%s />'''%teach.id
                    yield '''<input type="hidden" name="school_id" value=%s />'''%school_id
                    yield '<input type="submit" value="Change Username">'
                    yield '</form>'
                    yield '<br>'
        if 'student' in args:
            person = args['student']
            for student in session.query(Student):

                if (student.username == person and student.school_id == int(school_id)):
                    yield '''<h3>Edit Student Username</h3>'''
                    yield '''<div id = "ent">'''
                    yield '<form action="entered" >'
                    yield '''
                     <input type="text" name="student_username" value="%s">
                    ''' % (student.username)
                    yield '''<input type="hidden" name="student_id" value=%s />'''%student.id
                    yield '''<input type="hidden" name="school_id" value=%s />'''%school_id
                    yield '<input type="submit" value="Change Username">'
                    yield '</form>'
                    yield '<br>'
        if 'course' in args:
            course = args['course']
            c=(course.split())
            subject = c[0]
            number = c[1]
            for course in session.query(Courses):
                if(subject == course.subject and number == course.number and course.school_id == int(school_id)):
                    yield '''<h3>Edit Course Information</h3>'''
                    yield '''<div id = "et">'''
                    yield '<form action="entered" id = "ent">'
                    yield '''
                     <input type="text" name="course_subject" value="%s">
                    ''' % (course.subject)
                    yield '''<input type="hidden" name="course_id" value=%s />'''%course.id
                    yield '''<input type="hidden" name="school_id" value=%s />'''%school_id
                    yield '<input type="submit" value="Change Course Subject">'
                    yield '</form>'
                    yield '<form action="entered" id = "ent">'
                    yield '''
                     <input type="text" name="course_number" value="%s">
                    ''' % (course.number)
                    yield '''<input type="hidden" name="course_id" value=%s />'''%course.id
                    yield '''<input type="hidden" name="school_id" value=%s />'''%school_id
                    yield '<input type="submit" value="Change Course Number">'
                    yield '</form>'
                    yield '<br>'
        yield '''</div>'''



    @cherrypy.expose
    def reset(self):
        for row in session.query(Courses):
            session.delete(row)
        for row in session.query(Textbook):
            session.delete(row)
        for row in session.query(Teacher):
            session.delete(row)
        for row in session.query(Student):
            session.delete(row)
        for row in session.query(School):
            session.delete(row)
        session.commit()
        yield 'DATABASE RESET'
        cherrypy.session['message'] = "Database cleared"

if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }
    cherrypy.config.update({'server.socket_host': '127.0.0.1'})
    cherrypy.config.update({'server.socket_port': 5588})
    cherrypy.quickstart(Admin(), '/', conf)

