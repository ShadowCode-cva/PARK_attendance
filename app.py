from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime
from functools import wraps
import os
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex()

# MongoDB Connection
client = MongoClient('mongodb+srv://cvasolves:TaFWgraTc7EC4vCl@ramacluster.hy9ebnm.mongodb.net/')
db = client['college_attendance']
students_collection = db['students']
attendance_collection = db['attendance']
attendance_sessions_collection = db['attendance_sessions']
faculty_collection = db['faculty']

# Initialize default faculty account if not exists
def init_faculty():
    if faculty_collection.count_documents({}) == 0:
        faculty_collection.insert_one({
            'username': 'admin',
            'password': 'admin123',
            'name': 'Administrator',
            'department': 'CSE'
        })

# Initialize CSE 2nd year students with gender
def init_students():
    if students_collection.count_documents({'department': 'BE.CSE', 'year': 2}) == 0:
        students = [
            {'roll_no': '71222403001', 'name': 'AATHI HARI KRISHNAN M', 'gender': 'Male'},
            {'roll_no': '71222403002', 'name': 'ABHRO KANTH S', 'gender': 'Male'},
            {'roll_no': '71222403003', 'name': 'ABIRAMI G', 'gender': 'Female'},
            {'roll_no': '71222403004', 'name': 'ADAIKALASAMY V', 'gender': 'Male'},
            {'roll_no': '71222403005', 'name': 'ADHIMOOLAM A', 'gender': 'Male'},
            {'roll_no': '71222403006', 'name': 'AKALYA E', 'gender': 'Female'},
            {'roll_no': '71222403007', 'name': 'AKASH P', 'gender': 'Male'},
            {'roll_no': '71222403008', 'name': 'ARAVINDH P', 'gender': 'Male'},
            {'roll_no': '71222403009', 'name': 'ARULKUMAR K', 'gender': 'Male'},
            {'roll_no': '71222403010', 'name': 'ASHIKA S M', 'gender': 'Female'},
            {'roll_no': '71222403011', 'name': 'BALAKRISHNAN S', 'gender': 'Male'},
            {'roll_no': '71222403012', 'name': 'BAVYA M', 'gender': 'Female'},
            {'roll_no': '71222403013', 'name': 'BHARATH R', 'gender': 'Male'},
            {'roll_no': '71222403014', 'name': 'CASTRO JENIFER S', 'gender': 'Female'},
            {'roll_no': '71222403015', 'name': 'DHANALAKSHMI B', 'gender': 'Female'},
            {'roll_no': '71222403016', 'name': 'DHANUSH P', 'gender': 'Male'},
            {'roll_no': '71222403017', 'name': 'DHARANI P', 'gender': 'Female'},
            {'roll_no': '71222403018', 'name': 'DINESHKARAN N', 'gender': 'Male'},
            {'roll_no': '71222403019', 'name': 'GANESH M', 'gender': 'Male'},
            {'roll_no': '71222403020', 'name': 'HARIHARAN R', 'gender': 'Male'},
            {'roll_no': '71222403021', 'name': 'HARISH V', 'gender': 'Male'},
            {'roll_no': '71222403022', 'name': 'JAIARAVINDHAN C M', 'gender': 'Male'},
            {'roll_no': '71222403023', 'name': 'KALAIARASAN N', 'gender': 'Male'},
            {'roll_no': '71222403024', 'name': 'KATHIR MANIKANDAN P', 'gender': 'Male'},
            {'roll_no': '71222403025', 'name': 'KEERTHIKA S', 'gender': 'Female'},
            {'roll_no': '71222403026', 'name': 'KISHORE KANNAN B', 'gender': 'Male'},
            {'roll_no': '71222403027', 'name': 'KISHORE P', 'gender': 'Male'},
            {'roll_no': '71222403028', 'name': 'KISHORE S', 'gender': 'Male'},
            {'roll_no': '71222403029', 'name': 'KISHORE SELVAKUMAR', 'gender': 'Male'},
            {'roll_no': '71222403030', 'name': 'KRISHNA PRAKASH A', 'gender': 'Male'},
            {'roll_no': '71222403031', 'name': 'MAHA RAKESH K', 'gender': 'Male'},
            {'roll_no': '71222403032', 'name': 'MAHALAKSHMI G', 'gender': 'Female'},
            {'roll_no': '71222403034', 'name': 'MOHANRAJ T', 'gender': 'Male'},
            {'roll_no': '71222403035', 'name': 'MUGILAN M', 'gender': 'Male'},
            {'roll_no': '71222403036', 'name': 'NADHIYA N', 'gender': 'Female'},
            {'roll_no': '71222403037', 'name': 'NAGOOR SHEIK MYDEEN P', 'gender': 'Male'},
            {'roll_no': '71222403038', 'name': 'NAVANEETHA NAGARAJAN L', 'gender': 'Male'},
            {'roll_no': '71222403039', 'name': 'NAVIN B', 'gender': 'Male'},
            {'roll_no': '71222403040', 'name': 'POOPATHI C', 'gender': 'Female'},
            {'roll_no': '71222403041', 'name': 'RASHIYA S', 'gender': 'Female'},
            {'roll_no': '71222403042', 'name': 'RATHAN KUMAR V P', 'gender': 'Male'},
            {'roll_no': '71222403043', 'name': 'RATHNA NITHI M', 'gender': 'Male'},
            {'roll_no': '71222403044', 'name': 'RITHANYA M', 'gender': 'Female'},
            {'roll_no': '71222403045', 'name': 'SAKTHIVEL A', 'gender': 'Male'},
            {'roll_no': '71222403046', 'name': 'SANJU B', 'gender': 'Male'},
            {'roll_no': '71222403047', 'name': 'SANTHOSH R', 'gender': 'Male'},
            {'roll_no': '71222403048', 'name': 'SARATHI V', 'gender': 'Male'},
            {'roll_no': '71222403049', 'name': 'SATHISH A', 'gender': 'Male'},
            {'roll_no': '71222403050', 'name': 'SATHISHKUMAR M', 'gender': 'Male'},
            {'roll_no': '71222403052', 'name': 'SHIYAM G', 'gender': 'Male'},
            {'roll_no': '71222403053', 'name': 'SIVA K', 'gender': 'Male'},
            {'roll_no': '71222403054', 'name': 'SIVARAJAN S', 'gender': 'Male'},
            {'roll_no': '71222403055', 'name': 'SUDHAHAR S', 'gender': 'Male'},
            {'roll_no': '71222403056', 'name': 'SUREKA K', 'gender': 'Female'},
            {'roll_no': '71222403057', 'name': 'SUSMITHA V', 'gender': 'Female'},
            {'roll_no': '71222403059', 'name': 'THAMARAISELVAN M', 'gender': 'Male'},
            {'roll_no': '71222403060', 'name': 'VELUTHAI ESWARI T', 'gender': 'Female'},
            {'roll_no': '71222403061', 'name': 'VISHAL K', 'gender': 'Male'},
            {'roll_no': '71222403063', 'name': 'YOGESWARAN N', 'gender': 'Male'}
        ]
        
        for student in students:
            student['department'] = 'BE.CSE'
            student['year'] = 2
            student['password'] = student['roll_no'][-4:]
            students_collection.insert_one(student)

init_faculty()
init_students()

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_type' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_type' not in session or session['user_type'] != 'admin':
            flash('Admin access required', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_type = request.form['user_type']
        
        if user_type == 'admin':
            faculty = faculty_collection.find_one({'username': username, 'password': password})
            if faculty:
                session['user_type'] = 'admin'
                session['username'] = username
                session['name'] = faculty['name']
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Invalid credentials', 'error')
        else:
            student = students_collection.find_one({'roll_no': username, 'password': password})
            if student:
                session['user_type'] = 'student'
                session['roll_no'] = username
                session['name'] = student['name']
                session['department'] = student['department']
                session['year'] = student['year']
                return redirect(url_for('student_dashboard'))
            else:
                flash('Invalid credentials', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    departments = ['BE.CSE', 'BE.AERO', 'B.Tech AIDS']
    years = [1, 2, 3, 4]
    return render_template('admin_dashboard.html', departments=departments, years=years)

@app.route('/admin/mark_attendance', methods=['GET', 'POST'])
@admin_required
def mark_attendance():
    if request.method == 'POST':
        department = request.form['department']
        year = int(request.form['year'])
        date = request.form['date']
        subject = request.form['subject']
        
        students = list(students_collection.find({'department': department, 'year': year}))
        
        # Calculate summary
        total_students = len(students)
        total_present = 0
        total_absent = 0
        boys_present = 0
        boys_absent = 0
        girls_present = 0
        girls_absent = 0
        
        attendance_records = []
        
        for student in students:
            roll_no = student['roll_no']
            status = request.form.get(f'attendance_{roll_no}', 'absent')
            gender = student.get('gender', 'Unknown')
            
            # Count statistics
            if status == 'present':
                total_present += 1
                if gender == 'Male':
                    boys_present += 1
                elif gender == 'Female':
                    girls_present += 1
            else:
                total_absent += 1
                if gender == 'Male':
                    boys_absent += 1
                elif gender == 'Female':
                    girls_absent += 1
            
            # Store individual attendance
            attendance_record = {
                'roll_no': roll_no,
                'name': student['name'],
                'gender': gender,
                'department': department,
                'year': year,
                'date': date,
                'subject': subject,
                'status': status,
                'marked_by': session['username'],
                'marked_by_name': session['name'],
                'marked_at': datetime.now()
            }
            attendance_collection.insert_one(attendance_record)
            attendance_records.append(attendance_record)
        
        # Store attendance session summary
        session_summary = {
            'department': department,
            'year': year,
            'date': date,
            'subject': subject,
            'total_students': total_students,
            'total_present': total_present,
            'total_absent': total_absent,
            'boys_present': boys_present,
            'boys_absent': boys_absent,
            'girls_present': girls_present,
            'girls_absent': girls_absent,
            'marked_by': session['username'],
            'marked_by_name': session['name'],
            'marked_at': datetime.now(),
            'attendance_records': [r['roll_no'] for r in attendance_records]
        }
        attendance_sessions_collection.insert_one(session_summary)
        
        # Store summary in session for display
        session['last_attendance_summary'] = session_summary
        session['last_attendance_summary']['_id'] = str(session_summary['_id'])
        
        return redirect(url_for('attendance_summary'))
    
    department = request.args.get('department')
    year = request.args.get('year', type=int)
    
    if department and year:
        students = list(students_collection.find({'department': department, 'year': year}))
        return render_template('mark_attendance.html', students=students, department=department, year=year)
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/attendance_summary')
@admin_required
def attendance_summary():
    summary = session.get('last_attendance_summary')
    if not summary:
        flash('No attendance summary available', 'error')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('attendance_summary.html', summary=summary)

@app.route('/admin/view_attendance')
@admin_required
def view_attendance():
    department = request.args.get('department')
    year = request.args.get('year', type=int)
    
    if department and year:
        students = list(students_collection.find({'department': department, 'year': year}))
        
        for student in students:
            total = attendance_collection.count_documents({'roll_no': student['roll_no']})
            present = attendance_collection.count_documents({'roll_no': student['roll_no'], 'status': 'present'})
            student['total_classes'] = total
            student['present'] = present
            student['percentage'] = round((present / total * 100), 2) if total > 0 else 0
        
        return render_template('view_attendance.html', students=students, department=department, year=year)
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/attendance_history')
@admin_required
def attendance_history():
    # Get recent attendance sessions
    sessions = list(attendance_sessions_collection.find().sort('marked_at', -1).limit(50))
    
    for sess in sessions:
        sess['marked_at_formatted'] = sess['marked_at'].strftime('%Y-%m-%d %I:%M %p')
    
    return render_template('attendance_history.html', sessions=sessions)

@app.route('/student/dashboard')
@login_required
def student_dashboard():
    if session['user_type'] != 'student':
        return redirect(url_for('admin_dashboard'))
    
    roll_no = session['roll_no']
    
    total = attendance_collection.count_documents({'roll_no': roll_no})
    present = attendance_collection.count_documents({'roll_no': roll_no, 'status': 'present'})
    absent = total - present
    percentage = round((present / total * 100), 2) if total > 0 else 0
    
    attendance_records = list(attendance_collection.find({'roll_no': roll_no}).sort('date', -1).limit(20))
    
    # Format marked_at timestamp
    for record in attendance_records:
        if 'marked_at' in record:
            record['marked_at_formatted'] = record['marked_at'].strftime('%Y-%m-%d %I:%M %p')
    
    subject_wise = {}
    for record in attendance_collection.find({'roll_no': roll_no}):
        subject = record['subject']
        if subject not in subject_wise:
            subject_wise[subject] = {'total': 0, 'present': 0}
        subject_wise[subject]['total'] += 1
        if record['status'] == 'present':
            subject_wise[subject]['present'] += 1
    
    for subject in subject_wise:
        total_sub = subject_wise[subject]['total']
        present_sub = subject_wise[subject]['present']
        subject_wise[subject]['percentage'] = round((present_sub / total_sub * 100), 2) if total_sub > 0 else 0
    
    return render_template('student_dashboard.html', 
                         total=total, 
                         present=present, 
                         absent=absent, 
                         percentage=percentage,
                         attendance_records=attendance_records,
                         subject_wise=subject_wise)

if __name__ == '__main__':
    app.run(debug=True)