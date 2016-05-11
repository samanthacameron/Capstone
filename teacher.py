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

class Teachers(object):
   
    @cherrypy.expose
    def index(self, school_name="" , username = ""):
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
        yield '''<h1>Teacher Login</h1> '''
        yield '''
        <form action="teacher_home">
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

        yield '''</br></br><div id = "b"><button id="login" type="submit" >SUBMIT</button></div></form>'''

    @cherrypy.expose
    def teacher_home(self, school_name, school_type, username):
        yield '''<html>
        <head>
            <link href="/static/css/style.css" rel="stylesheet">
            <title>Capstone Application</title>
          </head>
        '''
        school_id = 0
        valid = 0
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
          <li><a href="/teachers/teacher_home?school_name=%s&school_type=%s&username=%s">Home</a></li>
          <li><a href="/teachers/teacher_action?opt=%i&username=%s&school_id=%s">View My Information</a></li>
          
          <li><a href="/teachers">Logout</a></li>
          <li style="float:right"><a >%s</a></li>
        </ul></div>''' %(school_name, school_type, username,7,username,school_id,username)
        for t in session.query(Teacher):
            if (t.username == username and t.school_id == int(school_id)):
                yield '''<h1>Teacher Home</h1>'''
                yield '''
                <form action="teacher_action" >
                <div id="s"></br>'''
                yield '''<label for="optout" >
                <input type="radio" name="opt" value="1" checked="checked"/>Enter My Personal Information
                </label></br>
                <label for="optout">
                <input type="radio" name="opt" value="2"/>Add My Courses
                </label></br>
                <label for="optout">
                <input type="radio" name="opt" value="3"/>Edit My Course Information
                </label></br>
                <label for="optout">
                <input type="radio" name="opt" value="4"/>Edit Textbook Information
                </label></br>
                <label for="optout">
                <input type="radio" name="opt" value="5"/>View Textbook Pricing (Provided by Amazon.com)
                </label></br>'''
                yield '''<input type="hidden" name="username" value=%s />'''%username
                yield '''<input type="hidden" name="school_id" value=%s />'''%school_id
                yield '''<button id="submit" type="submit" >Submit</button></div></form>'''
                valid = 1
        if (valid == 0):
            raise cherrypy.HTTPRedirect('/teachers/' )

    @cherrypy.expose
    def teacher_action(self, opt, username, school_id):
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
          <li><a href="/teachers/teacher_home?school_name=%s&school_type=%s&username=%s">Home</a></li>
          <li><a href="/teachers/teacher_action?opt=%i&username=%s&school_id=%s">View My Information</a></li>
          
          <li><a href="/teachers">Logout</a></li>
          <li style="float:right"><a >%s</a></li>
        </ul></div>''' %(school_name, school_type, username,7,username,school_id,username)
        # enter personal info
        if opt =="1":
            yield '<body>'
            yield '''<h3>Edit My Personal Information</h3>'''
            yield '<div id="personal">'
            for person in session.query(Teacher):
                if (username == person.username and person.school_id == int(school_id)):
                    yield '''
                    <h5> Username : %s</h5>
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
        # add courses for a teacher
        schl = session.query(School).get(int(school_id))
        school_name = schl.name
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
            
            
            for teacher in session.query(Teacher):
                if (teacher.username == username and teacher.school_id == int(school_id)):
                    if (teacher.courses is not None):
                        yield '''<div id = "courses">My Courses:<br><br>'''
                        yield '''<div style="height:120px;width:120px;border:1px solid #ccc;font:16px/26px Georgia, Garamond, Serif;overflow:auto;">'''
                        courses = teacher.courses
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

            
        #edit teacher's course information
        if opt == "3":
            for teacher in session.query(Teacher):
                if (teacher.username == username and teacher.school_id == int(school_id)):
                    if (teacher.courses is None):
                        yield '''YOU ARE NOT SIGNED UP FOR ANY COURSES'''
                    if (teacher.courses is not None):
                        yield '''<h4>Edit My Course Information</h4>'''
                        courses = teacher.courses
                        courselist =[x.strip() for x in courses.split(',')]
                        if (courselist[-1]==''):
                            del courselist[-1]
                        courselist = map(int, courselist)

                        for i in courselist:
                            for courses in session.query(Courses):
                                if (i == courses.id):
                                    yield '''<div id = "list">'''
                                    yield '''%s %s'''%(courses.subject,courses.number)
                                    yield '<br><br><br>'
                                    yield '<form action="update">'
                                    yield '''
                                     <input type="text" name="subject" value="%s">
                                    ''' % (courses.subject)
                                    yield '''<input type="hidden" name="course_id" value=%s />'''%courses.id
                                    yield '''<input type="hidden" name="username" value=%s />'''%username
                                    yield '''<input type="hidden" name="school_id" value=%s />'''%school_id
                                    yield '<input type="submit" value="Change Subject">'
                                    yield '</form>'
                                    
                                    yield '<form action="update">'
                                    yield '''
                                     <input type="text" name="number" value="%s">
                                    ''' % (courses.number)
                                    yield '''<input type="hidden" name="course_id" value=%s />'''%courses.id
                                    yield '''<input type="hidden" name="username" value=%s />'''%username
                                    yield '''<input type="hidden" name="school_id" value=%s />'''%school_id
                                    yield '<input type="submit" value="Change Number">'
                                    yield '</form>'
                                    yield '<form action="update">'
                                    yield '''
                                    <input type="text" name="name" value="%s">
                                    ''' % (courses.name)
                                    yield '''<input type="hidden" name="course_id" value=%s />'''%courses.id
                                    yield '''<input type="hidden" name="username" value=%s />'''%username
                                    yield '''<input type="hidden" name="school_id" value=%s />'''%school_id
                                    yield '<input type="submit" value="Change Name">'
                                    yield '</form>'
                                    yield '<form action="update">'
                                    yield '''
                                    <input type="text" id = "des" name="des" value="%s">
                                    ''' % (courses.des)
                                    yield '''<input type="hidden" name="course_id" value=%s />'''%courses.id
                                    yield '''<input type="hidden" name="username" value=%s />'''%username
                                    yield '''<input type="hidden" name="school_id" value=%s />'''%school_id
                                    yield '<input type="submit" value="Change Description">'
                                    yield '</form>'
                                    yield '''<br>'''
                                    yield '''</div>'''
        if opt == "4":
            for teacher in session.query(Teacher):
                if (teacher.username == username and teacher.school_id == int(school_id)):
                    if (teacher.courses is None):
                        yield '''YOU ARE NOT SIGNED UP FOR ANY COURSES'''
                    if (teacher.courses is not None):
                        yield '''<h4>Edit Textbook Information</h4>'''
                        courses = teacher.courses
                        courselist =[x.strip() for x in courses.split(',')]
                        if (courselist[-1]==''):
                            del courselist[-1]
                        courselist = map(int, courselist)

                        
                        for i in courselist:
                            for courses in session.query(Courses):
                                if (i == courses.id):
                                    yield '''<div id = "list">'''
                                    yield '''%s %s %s<br><br>'''%(courses.subject,courses.number,courses.name)
                                    textbook_id = courses.textbook_id
                                    if (textbook_id is not None):
                                        yield '''<form action = "edit_text">'''
                                        for text in session.query(Textbook):
                                            if (textbook_id == text.id):
                                                yield '''ISBN: %s  <br> Title: %s <br> Author: %s <br> Edition: %s <br><br>'''\
                                                    %(text.isbn, text.title, text.author, text.edition)
                                                yield '''<input type="hidden" name="text_id" value=%s />'''%text.id

                                                
                                        yield '''<input type="hidden" name="username" value=%s />'''%username 
                                        yield '''<input type="hidden" name="course_id" value=%s />'''%courses.id 
                                        yield '''<input type="hidden" name="school_id" value=%s />'''%school_id    
                                        yield '''<button id="login" type="submit">EDIT</button></form>'''
                                        yield '''</div>'''

                                    elif(textbook_id is None):
                                        # yield '''<div id = "list">'''
                                        # yield '''%s %s %s<br><br>'''%(courses.subject,courses.number,courses.name)
                                        yield '<form action="entered" >'
                                        yield '''<br><br>'''
                                        yield 'Add Textbook ISBN (Required):'
                                        yield '<input type ="field", name="new_isbn" ><br><br>'
                                        yield 'Title: <input type ="field", name="author" >'
                                        yield ' Author: <input type ="field", name="title" >'
                                        yield ' Edition: <input type ="field", name="edition" >'
                                        yield '''<input type="hidden" name="course_id" value=%s />'''%courses.id
                                        yield '''<input type="hidden" name="username" value=%s />'''%username
                                        yield '''<input type="hidden" name="school_id" value=%s />'''%school_id
                                        yield '<br><br><input type="submit" value="Submit">'
                                        yield '</form>'
                                        yield '''</div>'''
        if opt == "7":
            for teacher in session.query(Teacher):
                if (username == teacher.username and int(school_id)==teacher.school_id):
                    yield '''<h3>Information for %s<br></h3>'''%(username)
                    yield '''<div id = "mid">'''
                    yield '''%s %s<br>%s<br><br>'''%(teacher.first,teacher.last,teacher.email)
                    if (teacher.courses is not None):
                        courses = teacher.courses
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


        if opt == "5":
            
            for teacher in session.query(Teacher):
                if (teacher.username == username and int(school_id) == teacher.school_id):
                    yield '''<h4>Textbook Pricing Results Provided by Amazon.com</h4>'''
                    if (teacher.courses is not None):
                        courses = teacher.courses
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
                        if (course.teacher_id is None):###### if a teacher is not already teaching the course 
                            for teacher in session.query(Teacher):
                                if (teacher.username == username):
                                    course.teacher_id = teacher.id
                                    if (teacher.courses is not None):
                                        course_list = teacher.courses
                                        course_list= course_list + ("%s,")%course.id
                                        teacher.courses = course_list
                                        session.commit()
                                    elif (teacher.courses is None):
                                        course_list = ("%s,")% course.id
                                        teacher.courses = course_list
                                        session.commit()
                     
                opt = 2
        if 'new_isbn' in args:
            new_isbn = args['new_isbn']
            course_id = args['course_id']
            title = args['title'] 
            author = args['author']
            edition = args['edition']
            isbn = new_isbn.replace("-","").replace(" ","")
            response = amazon.ItemLookup(ItemId=isbn, SearchIndex="Books", IdType="ISBN", ResponseGroup="Large",Operation="ItemLookup")
            soup = BeautifulSoup(response)
            #auto populate
            if title == "":
                title = soup.find('title')
                if(title is not None):
                    title = str(title.string)

            if author == "":
                author = soup.find('author')
                if (author is not None):
                    author = str(author.string)
            if edition == "":
                edition = soup.find('edition')
                if (edition is not None):
                    edition = str(edition.string)

            
            if (new_isbn != ""):
                new_text = Textbook(isbn=new_isbn,title = title, author=author, edition = edition,school_id = school_id) 
                session.add(new_text)
                session.commit()
            for txt in session.query(Textbook):
                if(txt.isbn == new_isbn):                    
                    session.query(Courses).filter_by(id=course_id).update({"textbook_id": txt.id})
                    session.commit()
            opt = 4



        raise cherrypy.HTTPRedirect('/teachers/teacher_action?opt=%i&username=%s&school_id=%s' % (opt,username,school_id))


    @cherrypy.expose
    def edit_text(self, text_id,username,course_id, school_id):
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
          <li><a href="/teachers/teacher_home?school_name=%s&school_type=%s&username=%s">Home</a></li>
          <li><a href="/teachers/teacher_action?opt=%i&username=%s&school_id=%s">View My Information</a></li>
          
          <li><a href="/teachers">Logout</a></li>
          <li style="float:right"><a >%s</a></li>
        </ul></div>''' %(school_name, school_type, username,7,username,school_id,username)
        text_id = int(text_id)
        course_id = int(course_id)
        course = session.query(Courses).get(course_id)
        text = session.query(Textbook).get(text_id)
        yield '''<h4>Editing Textbook Information for %s %s, %s </h4>'''%(course.subject, course.number, course.name)
        yield '<div id = "t"><form action="change_text">'
        yield '''
         ISBN (required): <input type="text" id = "t" name="isbn" value="%s">
        ''' % (text.isbn)
        yield '''<input type="hidden" name="text_id" value=%s />'''%text.id
        yield '''<input type="hidden" name="username" value=%s />'''%username
        yield '''<input type="hidden" name="school_id" value=%s />'''%school_id
        yield '''<input type="hidden" name="course_id" value=%s />'''%course_id
        yield '<input type="submit" value="Change">'
        yield '''<br>'''
        yield '''</form>'''
        yield '<form action="change_text">'
        yield '''
         Title: <input type="text" id = "t" name="title" value="%s">
        ''' % (text.title)
        yield '''<input type="hidden" name="text_id" value=%s />'''%text.id
        yield '''<input type="hidden" name="username" value=%s />'''%username
        yield '''<input type="hidden" name="school_id" value=%s />'''%school_id
        yield '''<input type="hidden" name="course_id" value=%s />'''%course_id
        yield '<input type="submit" value="Change">'
        yield '''<br>'''
        yield '''</form>'''
        yield '<form action="change_text">'
        yield '''
         Author: <input type="text" id = "t" name="author" value="%s">
        ''' % (text.author)
        yield '''<input type="hidden" name="text_id" value=%s />'''%text.id
        yield '''<input type="hidden" name="username" value=%s />'''%username
        yield '''<input type="hidden" name="school_id" value=%s />'''%school_id
        yield '''<input type="hidden" name="course_id" value=%s />'''%course_id
        yield '<input type="submit" value="Change">'
        yield '''<br>'''
        yield '''</form>'''
        yield '<form action="change_text">'
        yield '''
         Edition: <input type="text" id = "t" name="edition" value="%s">
        ''' % (text.edition)
        yield '''<input type="hidden" name="text_id" value=%s />'''%text.id
        yield '''<input type="hidden" name="username" value=%s />'''%username
        yield '''<input type="hidden" name="school_id" value=%s />'''%school_id
        yield '''<input type="hidden" name="course_id" value=%s />'''%course_id
        yield '<input type="submit" value="Change">'
        yield '''<br>'''
        yield '''</form></div>'''

    @cherrypy.expose
    def change_text(self, **args):
        text_id = args['text_id']
        username = args['username']
        school_id = args['school_id']
        course_id = args['course_id']
        text_id = int(text_id)
        
        txt = session.query(Textbook).get(text_id)
        if 'isbn' in args:
            isbn = args['isbn']
            if(isbn != ""):
                txt.isbn = isbn
        if 'author' in args:
            author = args['author']
            if(author != ""):
                txt.author = author
        if 'title' in args:
            title = args['title']
            if(title != ""):
                txt.title = title
        if 'edition' in args:
            edition = args['edition']
            if(edition != ""):
                txt.edition = edition
        session.commit()
        raise cherrypy.HTTPRedirect('/teachers/teacher_action?opt=4&username=%s&school_id=%s'%(username,school_id))

    @cherrypy.expose
    def update(self, **args):
        school_id = args['school_id']
        username = args['username']
        opt = ""
        if 'first' in args:
            first = args['first']
            if(first != ""):
                for person in session.query(Teacher):
                    if (username == person.username and int(school_id) == person.school_id):
                        person.first = first
            opt = "1"
        if 'last' in args:
            last = args['last']
            if (last !=""):
                for person in session.query(Teacher):
                    if (username == person.username and int(school_id) == person.school_id):
                        person.last = last
            opt = "1"
        if 'email' in args:
            email = args['email']
            if(email != ""):
                for person in session.query(Teacher):
                    if (username == person.username and int(school_id) == person.school_id):
                        person.email = email
            opt = "1"
        if 'subject' in args:
            subject = args['subject']
            course_id = args['course_id']
            if (subject != "" and course_id != ""):
                course_id = int(course_id)
                for courses in session.query(Courses):
                    if (course_id == courses.id and courses.school_id == int(school_id)):
                        courses.subject = subject
            opt = "3"
        if 'number' in args:
            number = args['number']
            course_id = args['course_id']
            if (number!= "" and course_id != ""):
                course_id = int(course_id)
                for courses in session.query(Courses):
                    if (course_id == courses.id):
                        courses.number = number
            opt = "3"
        if 'name' in args:
            name = args['name']
            course_id = args['course_id']
            if (name != "" and course_id != ""):
                course_id = int(course_id)
                for courses in session.query(Courses):
                    if (course_id == courses.id and courses.school_id == int(school_id)):
                        courses.name = name
            opt = "3"
        if 'des' in args:
            des = args['des']
            course_id = args['course_id']
            if (des != "" and course_id != ""):
                course_id = int(course_id)
                for courses in session.query(Courses):
                    if (course_id == courses.id and courses.school_id == int(school_id)):
                        courses.des = des
            opt = "3"
        if 'isbn' in args:
            isbn = args['isbn']
            text_id = args['text_id']
            if (isbn != "" and text_id != ""):
                text_id = int(text_id)
                for txt in session.query(Textbook):
                    if (txt.id == text_id and txt.school_id == int(school_id)):
                        txt.isbn = isbn
            opt = "4"
        session.commit()
        raise cherrypy.HTTPRedirect('/teachers/teacher_action?opt=%s&username=%s&school_id=%s'%(opt,username,school_id))


    
if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        
    }
    
    cherrypy.config.update({'server.socket_host': '127.0.0.1'})
    cherrypy.config.update({'server.socket_port': 5588})


    cherrypy.quickstart(Teachers(), '/', conf)