import cherrypy
import os
import os.path
from database import *
import requests
import datetime
import bottlenose
from bs4 import BeautifulSoup

AWSAccessKeyId="<my aws access key id>"
AWSSecretKey="<my aws secret key>"
Associate_id = "<my associate id>"
amazon = bottlenose.Amazon(AWSAccessKeyId, AWSSecretKey, Associate_id)

class Students(object):

    @cherrypy.expose
    def index(self, school_name="", username=""):
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
        yield '''<h1>Student Login</h1> '''
        yield '''
        <form action="student_home">
        <div id="s">School Name: <input id="school_name" type="text" name="school_name" value="%s"></br>''' % school_name 
        yield'''</br></br>Type:<select name="school_type">
        <option value="College">College</option>
        <option value="University">University</option>
        <option value="High">High</option>
        <option value="Middle">Middle</option>
        <option value="Elementary" >Elementary</option>
        <option value="Other">Other</option>
        </select>'''
        yield '''</br>'''
        yield '''</br>'''
        yield '''</br>'''
        yield '''Username: <input id="username" type="text" name="username" value="%s"></br>''' % username

        yield '''</br></br><button id="login" type="submit" >SUBMIT</button></div></form>'''

    @cherrypy.expose
    def student_home(self, school_name, school_type, username):
        yield '''<html>
        <head>
            <link href="/static/css/style.css" rel="stylesheet">
            <title>Capstone Application</title>
          </head>
        '''
        valid = 0
        school_id = 0
        self.school_name = school_name
        for school in session.query(School):
            if (school_name == school.name and school_type == school.grade):
                school_id = school.id
        schl = session.query(School).get(int(school_id))
        school_name = schl.name
        school_type = schl.grade
        yield '''<div 
            style="background-image:
                   url('http://www.rycorsoftware.com/SFimages/default-source/leaf-textbook-management-images/leaf-banner_tinypng.png?sfvrsn=2'); 
            width:100%; 
            height:100px; 
            background-position:center;">&nbsp;</div>'''
        yield '''<div id = "navigation_bar"><ul>
          <li><a href="/students/student_home?school_name=%s&school_type=%s&username=%s">Home</a></li>
          <li><a href="/students/student_action?opt=%i&username=%s&school_id=%s">View My Information</a></li>
          
          <li><a href="/students">Logout</a></li>
          <li style="float:right"><a >%s</a></li>
        </ul></div>''' %(school_name, school_type, username,5,username,school_id,username)
        for t in session.query(Student):
            if (t.username == username and t.school_id == int(school_id)):
                yield '''<h1>Student Home</h1>'''
                yield '''
                <form action="student_action" >
                <div id="s"></br>'''
                yield '''<label for="optout" >
                <input type="radio" name="opt" value="1" checked="checked"/>Update Personal Info
                </label></br>
                <label for="optout">
                <input type="radio" name="opt" value="2"/>Add My Courses
                </label></br>
                <label for="optout">
                <input type="radio" name="opt" value="3"/>View My Courses Information
                </label></br>
                <label for="optout">
                <input type="radio" name="opt" value="4"/>View Pricing Options (Provided by Amazon.com)
                </label></br>
                '''
                yield '''<input type="hidden" name="username" value=%s />'''%username
                yield '''<input type="hidden" name="school_id" value=%s />'''%school_id
                yield '''<button id="submit" type="submit" >Submit</button></div></form>'''
                valid = 1
        if (valid == 0):
            raise cherrypy.HTTPRedirect('/students/' )



    @cherrypy.expose
    def student_action(self, opt, username, school_id):
        yield '''<html>
        <head>
            <link href="/static/css/style.css" rel="stylesheet">
            <title>Capstone Application</title>
          </head>
        '''
        schl = session.query(School).get(int(school_id))
        school_name = schl.name
        school_type = schl.grade
        yield '''<div 
            style="background-image:
                   url('http://www.rycorsoftware.com/SFimages/default-source/leaf-textbook-management-images/leaf-banner_tinypng.png?sfvrsn=2'); 
            width:100%; 
            height:100px; 
            background-position:center;">&nbsp;</div>'''
        yield '''<div id = "navigation_bar"><ul>
          <li><a href="/students/student_home?school_name=%s&school_type=%s&username=%s">Home</a></li>
          <li><a href="/students/student_action?opt=%i&username=%s&school_id=%s">View My Information</a></li>
          
          <li><a href="/students">Logout</a></li>
          <li style="float:right"><a >%s</a></li>
        </ul></div>''' %(school_name, school_type, username,3,username,school_id,username)
        # enter personal info
        if opt =="1":
            yield '<body>'
            yield '''<h3>Edit My Personal Information</h3>'''
            yield '<div id="personal">'
            for person in session.query(Student):
                if (username == person.username and int(school_id)==person.school_id):
                    
                    
                    yield '''
                    <h5> Username: %s</h5>
                    ''' % (person.username)
                    yield '<form action="update">'
                    yield '''
                     <input type="text" name="first" value="%s">
                    ''' % (person.first)
                    yield '''<input type="hidden" name="username" value=%s />'''%username
                    yield '''<input type="hidden" name="school_id" value=%s />'''%school_id
                    yield '<input type="submit" value="Change First Name">'
                    yield '</form>'
                    yield '<br>'

                    yield '<form action="update">'
                    yield '''
                    <input type="text" name="last" value="%s">
                    ''' % (person.last)
                    yield '''<input type="hidden" name="username" value=%s />'''%username
                    yield '''<input type="hidden" name="school_id" value=%s />'''%school_id
                    yield '<input type="submit" value="Change Last Name">'
                    yield '''</form>'''
                    yield '<form action="update">'
                    yield '''
                    <br><input type="text" name="email" value="%s">
                    ''' % (person.email)
                    yield '''<input type="hidden" name="username" value=%s />'''%username
                    yield '''<input type="hidden" name="school_id" value=%s />'''%school_id
                    yield '<input type="submit" value="Change Email Address">'
                    
                    yield '</form>'
            yield '</div>'
            yield '</body>'
        # add courses for a student
        if opt == "2":
            yield '''<h3>Add My Courses</h3>'''
            yield '''<div id = "c"><form action = "entered">'''
            yield '<h5>Add Course:</h5>'
            yield '<br><input type ="field" name="new_course_subject" id = "c" placeholder="Course Subject Code (ex: CSCI)" columns = 20>'
            yield '<input type ="field" name="new_course_number" id = "c" placeholder="Course Subject Number (ex: 381)"><br><br>'
            yield '''<input type="hidden" name="username" value=%s />'''%username
            yield '''<input type="hidden" name="school_id" value=%s />'''%school_id
            yield '<input type="submit" value="Submit">'
            yield '</form>'
            
            
            for student in session.query(Student):
                if (student.username == username and student.school_id == int(school_id)):
                    if (student.courses is not None):
                        yield '''<div id = "courses">My Courses:<br><br>'''
                        yield '''<div style="height:120px;width:120px;border:1px solid #ccc;font:16px/26px Georgia, Garamond, Serif;overflow:auto;">'''
                        courses = student.courses
                        courselist =[x.strip() for x in courses.split(',')]
                        if (courselist[-1]==''):
                            del courselist[-1]
                        courselist = map(int, courselist)
                        for i in courselist:
                            for courses in session.query(Courses):
                                if (courses.school_id == int(school_id)):
                                    if (i == courses.id):                 
                                        yield ''' - %s %s <br>''' %(courses.subject, courses.number)
                        yield '''</div></div>'''
            yield '''<div  id = "courses">Courses for %s:<br><br>'''%(schl.name)
            yield '''<div style="height:120px;width:120px;border:1px solid #ccc;font:16px/26px Georgia, Garamond, Serif;overflow:auto;">'''
            for courses in session.query(Courses):
                    if (courses.school_id == int(school_id)):
                        yield '''  - %s %s</br>''' %(courses.subject,courses.number)
            yield '''</div></div>''' 
            yield '''</div>'''
            ############################################################
        
        #View courses
        if opt == "3":
            for student in session.query(Student):
                if (student.username == username and student.school_id == int(school_id)):
                    if (student.courses is None):
                        yield '''YOU ARE NOT SIGNED UP FOR ANY COURSES'''
                    if (student.courses is not None):
                        yield '''<h4>My Course/Textbook Information</h4>'''
                        courses = student.courses
                        courselist =[x.strip() for x in courses.split(',')]
                        if (courselist[-1]==''):
                            del courselist[-1]
                        courselist = map(int, courselist)
                        for i in courselist:
                            for courses in session.query(Courses):
                                if (int(i) == courses.id):
                                    yield '''<div id = "list"><br>%s %s'''%(courses.subject,courses.number)
                                    yield '<br><br>'
                                    if (courses.name is not None):
                                        yield '''%s<br>'''%(courses.name)
                                    if (courses.des is not None):
                                        yield '''<div style="height:80px;width:200px;border:1px solid #ccc;font:12px Georgia, Garamond, Serif;overflow:auto;">'''
                                        yield '''%s</div>'''% (courses.des)
                                    teacher_id = courses.teacher_id
                                    textbook_id = courses.textbook_id
                                    if (teacher_id is not None):
                                        for teacher in session.query(Teacher):
                                            if (teacher_id == teacher.id):
                                                yield '''Taught by: %s %s<br>'''% (teacher.first, teacher.last)
                                    if (textbook_id is not None):
                                        for text in session.query(Textbook):
                                            if (text.id == textbook_id):
                                                yield '''Textbook Information: <br>'''
                                                yield '''ISBN: %s  <br> Title: %s <br> Author: %s <br> Edition: %s <br><br>'''\
                                                    %(text.isbn, text.title, text.author, text.edition)
                                    yield '''</div>'''
        if opt == "4":
            

            for student in session.query(Student):
                if (student.username == username and int(school_id) == student.school_id):
                    yield '''<h3>Textbook Pricing Results Provided by Amazon.com</h3>'''
                    if (student.courses is not None):
                        courses = student.courses
                        courselist =[x.strip() for x in courses.split(',')]
                        if (courselist[-1]==''):
                            del courselist[-1]
                        courselist = map(int, courselist)
                        for i in courselist:
                            for courses in session.query(Courses):
                                if (i == courses.id):                 
                                    yield '''<div id ="list">%s %s <br>''' %(courses.subject, courses.number) 
                                    if (courses.textbook_id is not None):
                                        txt = session.query(Textbook).get(int(courses.textbook_id))
                                        isbn = txt.isbn
                                        isbn = isbn.replace("-","").replace(" ","")
                                        url = "http://www.amazon.com"
                                        yield '''%s<br>'''%isbn
                                        response = amazon.ItemLookup(ItemId=isbn, SearchIndex="Books", IdType="ISBN", ResponseGroup="Large",Operation="ItemLookup")
                                        soup = BeautifulSoup(response)
                                        if (soup.find('mediumimage') is not None):
                                            yield '''<br><img src = %s><br><br>'''%(soup.find('mediumimage').url.string)
                                        item_id = soup.find('itemid')
                                        if (item_id is not None):
                                            yield '''%s<br>'''% (item_id.string)
                                        #print(soup.findAll())
                                        title = soup.find('title')
                                        if(title is not None):
                                            yield '''<br>%s<br>'''% (title.string)
                                        price = soup.find('formattedprice')
                                        if (price is not None):
                                            yield '''<br>%s<br>'''% (price.string)
                                        cont = soup.find('content')
                                        if(cont is not None):
                                            yield '''<div style="height:120px;width:400px;border:1px solid #ccc;font:16px/26px Georgia, Garamond, Serif;overflow:auto;">'''
                                            yield '''%s</div>'''% (soup.find('content').string)
                                        detail_page = soup.find('detailpageurl')
                                        if (detail_page is not None):
                                            url = (soup.find('detailpageurl').string)
                                        yield '''<br><br><a href="%s">View it on Amazon.com</a><br><br><br><br></div>'''%url
        if opt == "5":
            for student in session.query(Student):
                if (username == student.username and int(school_id)==student.school_id):
                    yield '''<h3>Information for %s<br></h3>'''%(username)
                    yield '''<div id = "mid">'''
                    yield '''%s %s<br>%s<br><br>'''%(student.first,student.last,student.email)
                    if (student.courses is not None):
                        courses = student.courses
                        courselist =[x.strip() for x in courses.split(',')]
                        if (courselist[-1]==''):
                            del courselist[-1]
                        courselist = map(int, courselist)
                        for i in courselist:
                            for courses in session.query(Courses):
                                if (i == courses.id):    

                                    yield '''%s %s <br>%s<br><br>''' %(courses.subject, courses.number, courses.name) 
                                    yield '''<div id = "marg" style="height:80px;width:200px;border:1px solid #ccc;font:12px Georgia, Garamond, Serif;overflow:auto;">'''
                                    yield '''%s</div>'''% (courses.des)
                                    if (courses.textbook_id is not None):
                                        txt = session.query(Textbook).get(int(courses.textbook_id))
                                        yield '''<br>ISBN: %s<br>Title: %s<br>Author: %s<br>Edition: %s<br><br>'''%(txt.isbn, txt.title, txt.author, txt.edition)
                    yield '''</div>'''


    @cherrypy.expose
    def entered(self, **args):
        opt = 0
        course_list = ""
        username = args['username']
        school_id = args['school_id']
        if 'new_course_number' and 'new_course_subject' in args:
            new_course_number = args['new_course_number']
            new_course_subject = args['new_course_subject']
            if(new_course_number != "" and new_course_subject != ""):
                for course in session.query(Courses):
                    if (course.subject == new_course_subject and course.number == new_course_number and course.school_id == int(school_id)):
                        for student in session.query(Student):
                            if (student.username == username and student.school_id == int(school_id)):
                                if (student.courses is not None):
                                    course_list = student.courses
                                    course_list= course_list + ("%s,")%course.id
                                    student.courses = course_list
                                    session.commit()
                                elif (student.courses is None):
                                    course_list = ("%s,")% course.id
                                    student.courses = course_list
                                    session.commit()
                opt = 2
        raise cherrypy.HTTPRedirect('/students/student_action?opt=%i&username=%s&school_id=%s' % (opt,username,school_id))


    @cherrypy.expose
    def update(self, **args):
        school_id = args['school_id']
        username = args['username']
        opt = ""
        if 'first' in args:
            first = args['first']
            if(first != ""):
                for person in session.query(Student):
                    if (username == person.username and int(school_id)==person.school_id):
                        person.first = first
            opt = "1"
        if 'last' in args:
            last = args['last']
            if (last !=""):
                for person in session.query(Student):
                    if (username == person.username and int(school_id)==person.school_id):
                        person.last = last
            opt = "1"
        if 'email' in args:
            email = args['email']
            if(email != ""):
                for person in session.query(Student):
                    if (username == person.username and int(school_id)==person.school_id):
                        person.email = email
            opt = "1"
        session.commit()
        raise cherrypy.HTTPRedirect('/students/student_action?opt=%s&username=%s&school_id=%s'%(opt,username,school_id))


    
       
    





if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        
    }
    
    cherrypy.config.update({'server.socket_host': '127.0.0.1'})
    cherrypy.config.update({'server.socket_port': 5588})


    cherrypy.quickstart(Teach(), '/', conf)