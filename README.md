# Capstone

Before Running:

Update IP Address in main function of student.py, admin.py, and teacher.py.
Update AWS credentials in teacher.py and student.py.
Update MySQL credentials in database.py

Run with:

python3 admin.py

Administration Application:
http://<ipaddress>:5588/
Student Application:
http://<ipadress>:5588/students/
Teacher Application:
http://<ipadress>:5588/teachers/

If port is blocked, use:

fuser -k 5588/tcp
