import base64
import cv2
import numpy as np
from deepface import DeepFace
from datetime import timedelta
from functools import wraps
from flask import Blueprint, Response, flash, jsonify, redirect, render_template, request, session, url_for, Flask
from connection.controller import connection
import pyodbc

student = Blueprint('student', __name__, url_prefix='/student', template_folder='templates', static_folder='static')
sess = {
    'student_logged_in': False,
    'student_usertype': 'student'
}

@student.before_request
def make_session_permanent():
	session.permanent = True

def user_role_student(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if session['student_logged_in'] == True:           
			if session['student_usertype'] == 'student':
				return f(*args, **kwargs)
			else:
				flash('You do not have privilege to access this page!','danger')
				return redirect('index.main')
		else:
			flash('Unauthorized, Please login!','danger')
			return redirect(url_for('student.student_login'))
	return wrap

@student.route('/', methods=['GET', 'POST'])
def student_login():
    session['student_logged_in'] = False
    session['student_usertype'] = ''
    if request.method == 'POST':
        try:
            email = request.form.get('email')
            student_password = request.form.get('student_password')
            student_image_data = request.form.get('student_image')
            conn = connection()
            cur = conn.cursor()
            stored_proc = 'Exec spAuthStudent @email=?, @password=?'
            param = email, student_password
            cur.execute(stored_proc, param)
            rows = cur.fetchone()
            cur.close()
            conn.commit()
            if rows:
                student_db_image = rows.student_image
                nparr1 = np.frombuffer(base64.b64decode(student_image_data), np.uint8)
                nparr2 = np.frombuffer(base64.b64decode(student_db_image), np.uint8)
                image1 = cv2.imdecode(nparr1, cv2.COLOR_BGR2GRAY)
                image2 = cv2.imdecode(nparr2, cv2.COLOR_BGR2GRAY)
                img_result = DeepFace.verify(image1, image2, enforce_detection=False)
                print(img_result)
                if img_result["verified"] == True:
                    session['student_logged_in'] = True
                    session['student_usertype'] = 'student'
                    sess['student_logged_in'] = True
                    sess['student_usertype'] = 'student'
                    session['student_level'] = rows.level_id
                    sess['student_level'] = rows.level_id
                    session['student_id'] = rows.student_id
                    sess['student_id'] = rows.student_id
                    session['department_id'] = rows.department_id
                    sess['department_id'] = rows.department_id
                    flash('Login Successful', 'success')
                    return redirect(url_for('student.landing'))
                else:
                    error = 'Either Image not Verified or  Your Details Are Invalid'
                    return render_template('student_login.html', error=error)
            else:
                error = 'Email not found. Are you sure you\'re registered?'
                return render_template('student_login.html', error=error)
            return render_template('student_login.html')
        except (pyodbc.Error) as e:
            message = e
            return render_template('student_login.html', message=message)
    return render_template('student_login.html')


@student.route('/landing', methods=['GET', 'POST'])
def landing():
    if sess['student_logged_in'] == True and sess['student_usertype'] == 'student':
        return render_template('student_landing.html')
    return redirect(url_for('index.main'))


@student.route('/register-courses', methods=['GET', 'POST'])
def register_courses():
    if sess['student_logged_in'] == True and sess['student_usertype'] == 'student':
        level_id = sess['student_level']
        department_id = sess['department_id']
        conn = connection()
        cur = conn.cursor()
        stored_proc = 'Exec getCourses @level_id=?, @department_id=?'
        param = level_id, department_id
        cur.execute(stored_proc, param)
        rows = cur.fetchall()
        cur.close()
        conn.commit()
        print(rows)
        # conn = connection()
        # cur = conn.cursor()
        # stored_proc3 = 'Exec spCRUDCourse_Registration @course_registration_id=?, @course_id=?, @student_id=?, @StatementType=?'
        # param3 = '1', '', '', 'SELECT'
        # cur.execute(stored_proc3, param3)
        # data = cur.fetchall()
        # cur.close()
        # conn.commit()
        if request.method == 'POST':
            try:
                student_id = sess['student_id']
                course_id = request.form.get('course_id')
                print('collected the user data')
                conn2 = connection()
                cur2 = conn2.cursor()
                print('Established Connection')
                print(course_id, student_id)
                stored_proc2 = 'Exec spCRUDCourse_Registration @course_registration_id=?, @course_id=?, @student_id=?, @StatementType=?'
                param2 = '1', course_id, student_id, 'INSERT'
                cur2.execute(stored_proc2, param2)
                print(param2)
                cur2.close()
                conn2.commit()
                print('Stuffs are going alright. Procedure Complete')
                return redirect(url_for('student.landing'))
            except (pyodbc.Error) as e:
                message = e
                return render_template('register_courses.html', message=message)
        return render_template('register_courses.html', rows=rows)
    return redirect(url_for('index.main'))

@student.route('/registered-courses', methods=['GET', 'POST'])
def registered_courses():
    if sess['student_logged_in'] == True and sess['student_usertype'] == 'student':
        level_id = sess['student_level']
        department_id = sess['department_id']
        student_id = sess['student_id']

        conn = connection()
        cur = conn.cursor()
        stored_proc = 'Exec getRegisteredCourses @level_id=?, @department_id=?, @student_id=?'
        param = level_id, department_id, student_id
        cur.execute(stored_proc, param)
        rows = cur.fetchall()
        cur.close
        conn.commit()
        return render_template('registered_courses.html', rows=rows)
    return redirect(url_for('index.main'))

@student.route('/classes', methods=['GET', 'POST'])
def attend_classes():
    if sess['student_logged_in'] == True and sess['student_usertype'] == 'student':
        level_id = sess['student_level']
        department_id = sess['department_id']
        student_id = sess['student_id']
        conn = connection()
        cur = conn.cursor()
        stored_proc = 'Exec getStudentClasses @level_id=?, @department_id=?, @student_id=?'
        param = level_id, department_id, student_id
        cur.execute(stored_proc, param)
        rows = cur.fetchall()
        cur.close()
        conn.commit()
        return render_template('classes.html', rows=rows)
    return redirect(url_for('index.main'))

@student.route('/go_meet', methods=['GET', 'POST'])
def go_meet():
    classid=request.form.get("classid")
    meetid=request.form.get("meetid")
    course_registration_id = request.form.get('course_registration_id')
    session['course_registration_id'] = course_registration_id
    session['class_id'] = classid
    session['meet_id'] = meetid
    return redirect(url_for('video.meeting', uid=meetid))

@student.route('/take-attendance', methods=['GET', 'POST'])
def take_attendance():
    if request.method == 'POST':
        student_id = session['student_id']
        class_id = session['class_id']
        course_registration_id = session['course_registration_id']
        # class_id = 
        conn  = connection()
        cur = conn.cursor()
        stored_proc = 'Exec spCRUDStudent_Attendance @student_attendance_id=?, @student_id=?, @course_registration_id=?, @class_id=?, @StatementType=?'
        param = '1', student_id, course_registration_id, class_id, 'INSERT'
        cur.execute(stored_proc, param)
        cur.close()
        conn.commit()
        return jsonify({'message':'success'})
    return render_template('classes.html')

@student.route('/logout')
def logout():
      session.clear()
      return redirect(url_for('student.student_login'))