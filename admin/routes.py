from functools import wraps
from flask import Blueprint, flash, jsonify, redirect, render_template, request, session, url_for
from conn import CRUDFunction
from connection.controller import connection
import pyodbc
import base64

admin = Blueprint('admin', __name__, url_prefix='/admin', template_folder='templates', static_folder='static')
sess = {
    'admin_logged_in': False,
    'admin_usertype': ''
}

@admin.before_request
def make_session_permanent():
	session.permanent = True

def user_role_admin(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if session['admin_logged_in'] == True:           
			if session['admin_usertype'] == 'admin':
				return f(*args, **kwargs)
			else:
				flash('You do not have privilege to access this page!','danger')
				return redirect(url_for('index.main'))
		else:
			flash('Unauthorized, Please login!','danger')
			return redirect(url_for('index.main'))
	return wrap

@admin.route('/', methods=['GET', 'POST'])
def index():
    session['admin_logged_in'] = False
    session['admin_usertype'] = ''
    if request.method == 'POST':
        try:
            admin_username = request.form.get('username')
            admin_password = request.form.get('password')

            conn = connection()
            cur = conn.cursor()
            proc = 'Exec spReadAdmins @admin_username=?, @admin_password=?, @statement_type=?'
            param = admin_username, admin_password, "SELECT"
            cur.execute(proc, param)
            rows = cur.fetchone()
            cur.close()
            conn.commit()
            if rows:
                session['admin_logged_in'] = True
                session['admin_usertype'] = 'admin'
                sess['admin_logged_in'] = True
                sess['admin_usertype'] = 'admin'
                return redirect(url_for('admin.dashboard'))
            else:
                return render_template('admin_login.html')
        except (pyodbc.Error) as e:
            message = e
            return render_template('admin_login.html', message=message)
    return render_template('admin_login.html')

@admin.route('/dashboard',  methods=['GET','POST'])
def dashboard():
    if sess['admin_logged_in'] == True and sess['admin_usertype'] == 'admin':
        return render_template('admin_dashboard.html')
    return redirect(url_for('index.main'))

@admin.route('/add-faculty', methods=['GET','POST'])
def add_faculty():
    if sess['admin_logged_in'] == True and sess['admin_usertype'] == 'admin':
        if request.method=='POST':
            try:
                faculty_name=request.form.get("faculty_name")
                faculty_code=request.form.get("faculty_code")
                faculty_description=request.form.get("faculty_description")
                con=connection()
                cur=con.cursor()
                stored_proc="Exec spCRUDFaculty @faculty_id=?, @faculty_name=?, @faculty_code=?,@faculty_Description=?,@StatementType=?"
                param="1",faculty_name, faculty_code, faculty_description, "INSERT"
                cur.execute(stored_proc, param)
                cur.close()
                con.commit()
                flash("Registration successful.")
                session['admin_logged_in'] = True
                session['admin_usertype'] = 'admin'
                return redirect(url_for('admin.dashboard'))
            except (pyodbc.Error) as e:
                message=e
                return render_template('add_faculty.html', message=message)
        return render_template('add_faculty.html')
    return redirect(url_for('index.main'))

@admin.route('/add-department', methods=['GET', 'POST'])
def add_department():
    if sess['admin_logged_in'] == True and sess['admin_usertype'] == 'admin':
        if request.method == 'POST':
            try:
                dept_name = request.form.get('department_name')
                dept_code = request.form.get('department_code')
                dept_description = request.form.get('department_description')
                faculty_id = request.form.get('faculty_id')

                conn = connection()
                cur = conn.cursor()
                stored_proc = 'EXEC spCRUDDepartment @department_id=?, @department_name=?, @department_code=?, @department_description=?, @faculty_id=?, @StatementType=?'
                param = '1', dept_name, dept_code, dept_description, faculty_id, "INSERT"
                cur.execute(stored_proc, param)
                cur.close()
                conn.commit()
                session['admin_logged_in'] = True
                session['admin_usertype'] = 'admin'
                return redirect(url_for('admin.dashboard'))
            except (pyodbc.Error) as e:
                message = e
                return render_template('add_department.html', message=message)
        conn = connection()
        cur = conn.cursor()
        stored_proc = 'Exec spCRUDFaculty @faculty_id=?, @faculty_code=?, @faculty_name=?, @faculty_description=?, @StatementType=?'
        param = "1",'','','',"SELECT" #to allow the procedure to run without issues
        cur.execute(stored_proc, param)
        rows = cur.fetchall()
        cur.close()
        conn.commit()
        return render_template('add_department.html', rows = rows)
    return redirect(url_for('index.main'))

@admin.route('/add-student', methods=['GET', 'POST'])
def add_student():
    if sess['admin_logged_in'] == True and sess['admin_usertype'] == 'admin':
        if request.method == 'POST':
            try:
                student_name = request.form.get('student_name')
                matric_num = request.form.get('matric_num')
                tel_num = request.form.get('tel_num')
                email = request.form.get('email')
                dept_id = request.form.get('department_id')
                student_image_data = request.form.get('student_image')
                level = request.form.get('level_id')
                print('Message still working fine')
                conn = connection()
                cur = conn.cursor()
                print('Message, Connection Successful')
                stored_proc = 'Exec spCRUDStudent @student_id=?, @student_name=?, @matric_num=?, @tel_num=?, @email=?, @department_id=?, @student_image=?, @level_id=?, @StatementType=?'
                param = '1', student_name, matric_num, tel_num, email, dept_id, student_image_data, level, "INSERT"
                cur.execute(stored_proc, param)
                print('This also completed successfully')
                cur.close()
                conn.commit()
                session['admin_logged_in'] = True
                session['admin_usertype'] = 'admin'
                print("This session statement is after the function to add students", session)
                return redirect(url_for('admin.dashboard'))
            except (pyodbc.Error) as e:
                message = e
                return render_template('add_student.html', message=message)
        return render_template('add_student.html')
    return redirect(url_for('index.main'))

@admin.route('/add-staff', methods=['GET', 'POST'])
def add_staff():
    if sess['admin_logged_in'] == True and sess['admin_usertype'] == 'admin':
        if request.method == 'POST':
            try:
                staff_name = request.form.get('staff_name')
                staff_reg_num = request.form.get('staff_reg_num')
                tel_num = request.form.get('tel_num')
                email = request.form.get('email')
                dept_id = request.form.get('department_id')
                staff_image_data = request.form.get('staff_image')
                print('Message, still working fine`')
                conn = connection()
                cur = conn.cursor()
                stored_proc = 'Exec spCRUDStaff @staff_id=?, @staff_name=?, @staff_reg_number=?, @tel_num=?, @email=?, @department_id=?, @staff_image=?, @StatementType=?'
                param = '1', staff_name, staff_reg_num, tel_num, email, dept_id, staff_image_data, "INSERT"
                cur.execute(stored_proc, param)
                cur.close()
                conn.commit()
                session['admin_logged_in'] = True
                session['admin_usertype'] = 'admin'
                return redirect(url_for('admin.dashboard'))
            except (pyodbc.Error) as e:
                message = e
                return render_template('add_staff.html', message=message)
        return render_template('add_staff.html')
    return redirect(url_for('index.main'))

@admin.route('/add-level', methods=['GET', 'POST'])
def add_level():
    if sess['admin_logged_in'] == True and sess['admin_usertype'] == 'admin':
        if request.method == 'POST':
            try:
                level = request.form.get('level_name')
                conn = connection()
                cur = conn.cursor()
                stored_proc = 'Exec spCRUDLevel @level_id=?, @level_name=?, @StatementType=?'
                param = '1', level, 'INSERT'
                cur.execute(stored_proc, param)
                cur.close()
                conn.commit()
                session['admin_logged_in'] = True
                session['admin_usertype'] = 'admin'
                return redirect(url_for('admin.dashboard'))
            except (pyodbc.Error) as e:
                message = e
                return render_template('add_level.html', message=message)
        return render_template('add_level.html')
    return redirect(url_for('index.main'))

@admin.route('/add-sessions', methods=['GET', 'POST'])
def add_session():
    if sess['admin_logged_in'] == True and sess['admin_usertype'] == 'admin':
        if request.method == 'POST':
            try:
                session_start = request.form.get('session_start')
                session_end = request.form.get('session_end')

                conn = connection()
                cur = conn.cursor()
                stored_proc = 'Exec spCRUDSession @session_id=?, @session_start=?, @session_end=?, @StatementType=?'
                param = '1', session_start, session_end, 'INSERT'
                cur.execute(stored_proc, param)
                cur.close()
                conn.commit()
                session['admin_logged_in'] = True
                session['admin_usertype'] = 'admin'
                return redirect(url_for('admin.dashboard'))
            except (pyodbc.Error) as e:
                message = e
                return render_template('add_session.html', message=message)
        return render_template('add_session.html')
    return redirect(url_for('index.main'))

@admin.route('/add-semester', methods=['GET', 'POST'])
def add_semester():
    if sess['admin_logged_in'] == True and sess['admin_usertype'] == 'admin':
        if request.method == 'POST':
            try:
                semester_start = request.form.get('semester_start')
                semester_end = request.form.get('semester_end')
                session_id = request.form.get('session_id')

                conn = connection()
                cur = conn.cursor()
                stored_proc = 'Exec spCRUDSemester @semester_id=?, @semester_start=?, @semester_end=?, @session_id=?, @StatementType=?'
                param = '1', semester_start, semester_end, session_id, 'INSERT'
                cur.execute(stored_proc, param)
                cur.close()
                conn.commit()
                session['admin_logged_in'] = True
                session['admin_usertype'] = 'admin'
                return redirect(url_for('admin.dashboard'))
            except (pyodbc.Error) as e:
                message = e
                return render_template('add_semester.html', message=message)
        return render_template('add_semester.html')
    return redirect(url_for('index.main'))

@admin.route('/add-courses', methods=['GET', 'POST'])
def add_courses():
    if sess['admin_logged_in'] == True and sess['admin_usertype'] == 'admin':
        if request.method == 'POST':
            try:
                course_name = request.form.get('course_name')
                course_code = request.form.get('course_code')
                dept_id = request.form.get('department_id')
                level_id = request.form.get('level_id')
                semester_id = request.form.get('semester_id')
                staff_id = request.form.get('staff_id')

                conn = connection()
                cur = conn.cursor()
                stored_proc = 'Exec spCRUDCourses @course_id=?, @course_name=?, @department_id=?, @level_id=?, @semester_id=?, @course_code=?, @staff_id=?, @StatementType=?'
                param = '1', course_name, dept_id, level_id, semester_id, course_code, staff_id, 'INSERT'
                cur.execute(stored_proc, param)
                cur.close()
                conn.commit()

                session['admin_logged_in'] = True
                session['admin_usertype'] = 'admin'
                return redirect(url_for('admin.dashboard'))

            except (pyodbc.Error) as e:
                message = e
                return render_template('add_courses.html', message=message)
        return render_template('add_courses.html')
    return redirect(url_for('index.main'))

@admin.route('/add-classes', methods=['GET', 'POST'])
def add_classes():
    if sess['admin_logged_in'] == True and sess['admin_usertype'] == 'admin':
        if request.method == 'POST':
            try:
                class_date = request.form.get('class_date')
                class_start = request.form.get('class_start')
                class_end = request.form.get('class_end')
                course_id = request.form.get('course_id')

                conn = connection()
                cur = conn.cursor()
                stored_proc = 'Exec spCRUDClasses @class_id=?, @class_date=?, @class_in=?, @class_out=?, @course_id=?, @StatementType=?'
                param = '1', class_date, class_start, class_end, course_id, 'INSERT'
                cur.execute(stored_proc, param)
                cur.close()
                conn.commit()

                session['admin_logged_in'] = True
                session['admin_usertype'] = 'admin'
                return redirect(url_for('admin.dashboard'))
            except (pyodbc.Error) as e:
                message = e
                return render_template('add_classes.html', message=message)
        return render_template('add_classes.html')
    return redirect(url_for('index.main'))

@admin.route('/add-programme', methods=['GET', 'POST'])
def add_programme():
    if sess['admin_logged_in'] == True and sess['admin_usertype'] == 'admin':
        if request.method == 'POST':
            try:
                programme_name = request.form.get('programme_name')
                programme_duration = request.form.get('programme_duration')
                dept_id = request.form.get('department_id')

                conn = connection()
                cur = conn.cursor()
                stored_proc = 'Exec spCRUDProgramme @programme_id=?, @programme_name=?, @programme_duration=?, @department_id=?, @StatementType=?'
                param = '1', programme_name, programme_duration, dept_id, 'INSERT'
                cur.execute(stored_proc, param)
                cur.close()
                conn.commit()

                session['admin_logged_in'] = True
                session['admin_usertype'] = 'admin'
                return redirect(url_for('admin.dashboard'))
            except (pyodbc.Error) as e:
                message = e
                return render_template('add_programme.html', message=message)
        return render_template('add_programme.html')
    return redirect(url_for('index.main'))

@admin.route('/manage-faculty', methods=['GET', 'POST'])
def manage_faculty():
    if sess['admin_logged_in'] == True and sess['admin_usertype'] == 'admin':
        conn = connection()
        cur = conn.cursor()
        stored_proc = 'Exec spCRUDFaculty @faculty_id=?, @faculty_code=?, @faculty_name=?, @faculty_description=?, @StatementType=?'
        param = "1",'','','',"SELECT" #to allow the procedure to run without issues
        cur.execute(stored_proc, param)
        rows = cur.fetchall()
        cur.close()
        conn.commit()
        return render_template('manage_faculty.html', rows=rows)
    return redirect(url_for('index.main'))

@admin.route('/manage-department', methods=['GET', 'POST'])
def manage_department():
    if sess['admin_logged_in'] == True and sess['admin_usertype'] == 'admin':
        conn = connection()
        cur = conn.cursor()
        stored_proc = 'Exec spCRUDDepartment @department_id=?, @department_name=?, @department_code=?, @department_description=?, @faculty_id=?, @StatementType=?'
        param = '1', '', '', '', '', 'SELECT'
        cur.execute(stored_proc, param)
        rows = cur.fetchall()
        cur.close()
        conn.commit()
        return render_template('manage_department.html', rows=rows)
    return redirect(url_for('index.main'))

@admin.route('/manage-programme', methods=['GET', 'POST'])
def manage_programme():
    if sess['admin_logged_in'] == True and sess['admin_usertype'] == 'admin':
        conn = connection()
        cur = conn.cursor()
        stored_proc = 'Exec spCRUDProgramme @programme_id=?, @programme_name=?, @programme_duration=?, @department_id=?, @StatementType=?'
        param = '1', '', '', '', 'SELECT'
        cur.execute(stored_proc, param)
        rows = cur.fetchall()
        cur.close()
        conn.commit()
        return render_template('manage_programme.html', rows=rows)
    return redirect(url_for('index.main'))

@admin.route('/manage-level', methods=['GET', 'POST'])
def manage_level():
    if sess['admin_logged_in'] == True and sess['admin_usertype'] == 'admin':
        conn = connection()
        cur = conn.cursor()
        stored_proc = 'Exec spCRUDLevel @level_id=?, @level_name=?, @StatementType=?'
        param = '1', '', 'SELECT'
        cur.execute(stored_proc, param)
        rows = cur.fetchall()
        cur.close()
        conn.commit()
        return render_template('manage_level.html', rows=rows)
    return redirect(url_for('index.main'))

@admin.route('/manage-session', methods=['GET', 'POST'])
def manage_session():
    if sess['admin_logged_in'] == True and sess['admin_usertype'] == 'admin':
        conn = connection()
        cur = conn.cursor()
        stored_proc = 'Exec spCRUDSession @session_id=?, @session_start=?, @session_end=?, @StatementType=?'
        param = '1', '', '', 'SELECT'
        cur.execute(stored_proc, param)
        rows = cur.fetchall()
        cur.close()
        conn.commit()
        return render_template('manage_session.html', rows=rows)
    return redirect(url_for('index.main'))

@admin.route('/manage-semester', methods=['GET', 'POST'])
def manage_semester():
    if sess['admin_logged_in'] == True and sess['admin_usertype'] == 'admin':
        conn = connection()
        cur = conn.cursor()
        stored_proc = 'Exec spCRUDSemester @semester_id=?, @semester_start=?, @semester_end=?, @session_id=?, @StatementType=?'
        param = '1', '', '', '', 'SELECT'
        cur.execute(stored_proc, param)
        rows = cur.fetchall()
        cur.close()
        conn.commit()
        return render_template('manage_semester.html', rows=rows)
    return redirect(url_for('index.main'))

@admin.route('/manage-courses', methods=['GET', 'POST'])
def manage_courses():
    if sess['admin_logged_in'] == True and sess['admin_usertype'] == 'admin':
        conn = connection()
        cur = conn.cursor()
        stored_proc = 'Exec spCRUDCourses @course_id=?, @course_name=?, @department_id=?, @level_id=?, @semester_id=?, @course_code=?, @staff_id=?, @StatementType=?'
        param = '1', '', '', '', '', '', '', 'SELECT'
        cur.execute(stored_proc, param)
        rows = cur.fetchall()
        cur.close()
        conn.commit()
        return render_template('manage_courses.html', rows=rows)
    return redirect(url_for('index.main'))

@admin.route('/manage-classes', methods=['GET', 'POST'])
def manage_classes():
    if sess['admin_logged_in'] == True and sess['admin_usertype'] == 'admin':
        conn = connection()
        cur = conn.cursor()
        stored_proc = 'Exec spCRUDClasses @class_id=?, @class_date=?, @class_in=?, @class_out=?, @course_id=?, @StatementType=?'
        param = '1', '', '', '', '', 'SELECT'
        cur.execute(stored_proc, param)
        rows = cur.fetchall()
        cur.close()
        conn.commit()
        return render_template('manage_classes.html', rows=rows)
    return redirect(url_for('index.main'))



# @admin.route('/delete-faculty', methods=['GET', 'POST'])
# def delete_faculty():
#     if request.method == 'POST':
#         try:
#             faculty_id = request.form.get('faculty_id')
#             stored_proc = 'Exec spDeleteFaculty @faculty_id=?'
#             param = faculty_id
#             conn = connection()
#             cur = conn.cursor()
#             cur.execute(stored_proc, param)
#             cur.close()
#             conn.commit()
#             return redirect(url_for('admin.dashboard'))
#         except (pyodbc.Error) as e:
#             message = e
#             return render_template('manage_faculty.html', message=message)
#     return render_template('manage_faculty.html')
            