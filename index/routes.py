from flask import Blueprint, flash, render_template, request, session
from conn import CRUDFunction
import bluescan

index = Blueprint('index', __name__, url_prefix='', template_folder='templates', static_folder='index/static')
sess = {}

@index.route('/')
def main():
    session.clear()
    session['student_logged_in'] = False
    session['student_usertype'] = ''
    sess['student_logged_in'] = False
    sess['student'] = ''
    session['admin_logged_in'] = False
    session['admin_usertype'] = ''
    sess['admin_logged_in'] = False
    sess['admin_usertype'] = ''
    session['instructor_logged_in'] = False
    session['instructor_usertype'] = ''
    sess['instructor_logged_in'] = False
    sess['instructor_usertype'] = ''
    return render_template('index.html')