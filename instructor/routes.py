import base64
from functools import wraps
import cv2
from flask import Blueprint, flash, jsonify, render_template, request, redirect, session, url_for
from connection.controller import connection
import pyodbc
import numpy as np
from deepface import DeepFace


instructor = Blueprint('instructor', __name__, url_prefix='/instructor', template_folder='templates', static_folder='static')
sess = {
    'instructor_logged_in': False,
    'instructor_usertype': 'instructor'
}

@instructor.before_request
def make_session_permanent():
	session.permanent = True

def user_role_instructor(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if session['instructor_logged_in'] == True:           
			if session['instructor_usertype'] == 'instructor':
				return f(*args, **kwargs)
			else:
				flash('You do not have privilege to access this page!','danger')
				return redirect('index.main')
		else:
			flash('Unauthorized, Please login!','danger')
			return redirect(url_for('instructor.instructor_login'))
	return wrap

@instructor.route('/', methods=['GET', 'POST'])
def instructor_login():
    session['instructor_logged_in'] = False
    session['instructor_usertype'] = ''
    if request.method == 'POST':
        try:
            staff_reg_number = request.form.get('staff_reg_num')
            password = request.form.get('password')
            staff_image_data = request.form.get('staff_image')
            conn = connection()
            cur = conn.cursor()
            stored_proc = 'Exec spAuthStaff @staff_reg_number=?, @staff_password=?'
            param = staff_reg_number, password
            cur.execute(stored_proc, param)
            rows = cur.fetchone()
            cur.close()
            conn.commit()
            if rows:
                staff_db_image = rows.staff_image
                nparr1 = np.frombuffer(base64.b64decode(staff_image_data), np.uint8)
                nparr2 = np.frombuffer(base64.b64decode(staff_db_image), np.uint8)
                img1 = cv2.imdecode(nparr1, cv2.COLOR_BGR2GRAY)
                img2 = cv2.imdecode(nparr2, cv2.COLOR_BGR2GRAY)
                img_result = DeepFace.verify(img1, img2, enforce_detection=False)
                print(img_result)
                if img_result['verified'] == True:
                    sess['instructor_logged_in'] = True
                    sess['instructor_usertype'] = 'instructor'
                    session['instructor_logged_in'] = True
                    session['instructor_usertype'] = 'instructor'
                    sess['staff_id'] = rows.staff_id
                    session['staff_id'] = rows.staff_id
                    return redirect(url_for('instructor.landing'))
                else:
                    error = 'Either Image not Verified or  Your Details Are Invalid'
                    return render_template('instructor_login.html', error=error)
            else:
                error = 'Email not found. Are you sure you\'re registered?'
                return render_template('instructor_login.html', error=error)
        except (pyodbc.Error) as e:
            message = e
            return render_template('instructor_login.html', message=message)
    return render_template('instructor_login.html')

@instructor.route('/landing', methods=['GET', 'POST'])
def landing():
    if sess['instructor_logged_in'] == True and sess['instructor_usertype'] == 'instructor':
        return render_template('instructor_landing.html')
    return redirect(url_for('index.main'))

@instructor.route('/classes', methods=['GET', 'POST'])
def view_classes():
    if sess['instructor_logged_in'] == True and sess['instructor_usertype'] == 'instructor':
        staff_id = sess['staff_id']
        conn = connection()
        cur = conn.cursor()
        stored_proc = 'Exec getClassDetails @staff_id=?'
        param = staff_id
        cur.execute(stored_proc, param)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('assigned_classes.html', rows=rows)
    return redirect(url_for('index.main'))

@instructor.route('/attend-class', methods=['GET', 'POST'])
def attend_classes():
    if sess['instructor_logged_in'] == True and sess['instructor_usertype'] == 'instructor':
        staff_id = sess['staff_id']
        conn = connection()
        cur = conn.cursor()
        stored_proc = 'Exec getStaffClasses @staff_id=?'
        param = staff_id
        cur.execute(stored_proc, param)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('attend_class.html', rows=rows)
    return redirect(url_for('index.main'))

@instructor.route('/go-meet', methods=['GET', 'POST'])
def go_meet():
    class_id = request.form.get('class_id')
    meet_id = request.form.get('meetid')
    sess['class_id'] = class_id
    sess['meet_id'] = meet_id
    return redirect(url_for('video.meeting', uid=meet_id))

@instructor.route('/take-attendance', methods=['GET', 'POST'])
def take_attendance():
    if request.method == 'POST':
        staff_id = sess['staff_id']
        class_id = sess['class_id']
        conn = connection()
        cur = conn.cursor()
        stored_proc = 'Exec spCRUDStaff_Attendance @staff_attendance_id=?, @staff_id=?, @class_id=?, @StatementType=?'
        param = '1', staff_id, class_id, 'INSERT'
        cur.execute(stored_proc, param)
        cur.close()
        conn.commit()
        return jsonify({'message':'success'})
    return render_template('attend_class.html')


@instructor.route('/logout')
def logout():
      session.clear()
      return redirect(url_for('instructor.instructor_login'))