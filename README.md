# College Attendance System - Setup Guide

## Prerequisites
- Python 3.7 or higher
- MongoDB installed and running locally

## Installation Steps

### 1. Install MongoDB
**Windows:**
- Download MongoDB Community Server from https://www.mongodb.com/try/download/community
- Install and start MongoDB service

**Mac:**
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

**Linux:**
```bash
sudo apt-get install mongodb
sudo systemctl start mongodb
```

### 2. Install Python Dependencies
Create a file named `requirements.txt` with the following content:
```
Flask==3.0.0
pymongo==4.6.0
```

Then install:
```bash
pip install -r requirements.txt
```

### 3. Project Structure
Create the following folder structure:
```
college_attendance/
├── app.py (main Flask application)
├── requirements.txt
└── templates/
    ├── login.html
    ├── admin_dashboard.html
    ├── mark_attendance.html
    ├── view_attendance.html
    └── student_dashboard.html
```

### 4. Run the Application
```bash
python app.py
```

The application will be available at: http://localhost:5000

## Default Login Credentials

### Admin/Faculty Access
- Username: `admin`
- Password: `admin123`

### Student Access
- Username: Student's Roll Number (e.g., `71222403001`)
- Password: Last 4 digits of Roll Number (e.g., `3001`)

## Features

### Admin Panel
1. **Mark Attendance**: Select department and year to mark attendance for students
2. **View Reports**: View attendance statistics and percentages for any class
3. **Bulk Operations**: Mark all present/absent with one click

### Student Panel
1. **Overall Attendance**: View total attendance percentage
2. **Subject-wise Breakdown**: See attendance for each subject
3. **Attendance History**: View recent attendance records
4. **Visual Statistics**: Color-coded stats (Green: ≥75%, Orange: 60-74%, Red: <60%)

## Database Collections

### students
Stores student information:
- roll_no (unique)
- name
- department
- year
- password

### attendance
Stores attendance records:
- roll_no
- name
- department
- year
- date
- subject
- status (present/absent)
- marked_by (faculty username)
- marked_at (timestamp)

### faculty
Stores faculty credentials:
- username
- password
- name
- department

## Adding More Students

To add students from other departments/years, modify the `init_students()` function in `app.py`:

```python
students = [
    {'roll_no': 'STUDENT_ID', 'name': 'STUDENT_NAME'},
    # Add more students...
]

for student in students:
    student['department'] = 'BE.AERO'  # Change department
    student['year'] = 1  # Change year
    student['password'] = student['roll_no'][-4:]
    students_collection.insert_one(student)
```

## Adding More Faculty

To add faculty members, insert into MongoDB:
```python
faculty_collection.insert_one({
    'username': 'faculty_username',
    'password': 'password',
    'name': 'Faculty Name',
    'department': 'Department'
})
```

## Security Considerations for Production

1. **Change Secret Key**: Update `app.secret_key` with a strong random key
2. **Hash Passwords**: Use `werkzeug.security` for password hashing
3. **MongoDB Authentication**: Enable MongoDB authentication
4. **HTTPS**: Use SSL/TLS in production
5. **Input Validation**: Add server-side validation for all inputs
6. **Session Timeout**: Implement session expiration
7. **Environment Variables**: Store credentials in environment variables

## Customization

### Departments
Edit the `departments` list in `admin_dashboard` route:
```python
departments = ['BE.CSE', 'BE.AERO', 'B.Tech AIDS', 'Add More...']
```

### Attendance Threshold
Modify the color-coding thresholds in HTML templates:
- Green (High): ≥ 75%
- Orange (Medium): 60-74%
- Red (Low): < 60%

## Troubleshooting

### MongoDB Connection Issues
- Ensure MongoDB is running: `mongod`
- Check connection string in app.py
- Verify MongoDB is listening on port 27017

### Template Not Found
- Ensure all HTML files are in the `templates/` folder
- Check file names match exactly (case-sensitive)

### Port Already in Use
Change the port in app.py:
```python
app.run(debug=True, port=5001)
```

## Future Enhancements

1. Export attendance to Excel/PDF
2. Email notifications for low attendance
3. Biometric integration
4. Mobile app
5. Parent portal access
6. Multi-semester support
7. Leave management system
8. Attendance analytics and charts

## Support

For issues or questions:
- Check MongoDB is running
- Verify all templates are in correct folder
- Check Python and package versions
- Review error logs in terminal

---

**Note**: This is a basic system for educational purposes. For production use, implement proper security measures, error handling, and data validation.