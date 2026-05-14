from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

# --- APPLICATION SETUP ---
app = Flask(__name__)
# For sessions: Encrypts login data so users stay logged in safely
app.secret_key = 'university_clinic_secret_key'
# For database: Connects the Python app to your specific MySQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:10121@localhost/clinic_db'
db = SQLAlchemy(app)

# --- DATABASE MODELS ---
# For Admin accounts: Structure for the 'users' table
class Admin(db.Model):
    __tablename__ = 'admins'
    admin_id = db.Column(db.Integer, primary_key=True)
    sr_code = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(255))

# For Student logins: Structure for the 'students' table
class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    sr_code = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

# --- REGISTRATION LOGIC ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get data from the HTML form
        pw = request.form.get('password')
        sr = request.form.get('sr_code')
        fname = request.form.get('fullname', '').strip().title()
        college = request.form.get('college')
        program = request.form.get('program')

        try:
            hashed_pw = generate_password_hash(pw)

            # Add to 'students' table (for logging in)
            db.session.execute(db.text(
                "INSERT INTO students (sr_code, password) VALUES (:sr, :pw)"),
                {'sr': sr, 'pw': hashed_pw})

            # Add to 'medical_records' table (for the profile dashboard)
            # This is the part that fixes the "Profile Error"
            year = request.form.get('year')
            blood = request.form.get('blood_type')

            db.session.execute(db.text(
                "INSERT INTO medical_records (sr_code, fullname, college, program, year_level, blood_type) VALUES (:sr, :n, :c, :p, :y, :b)"),
                {'sr': sr, 'n': fname, 'c': college, 'p': program, 'y': year, 'b': blood})
            # Save everything permanently
            db.session.commit()

            flash("Registration successful! You can now log in.", "success")
            return redirect(url_for('login'))

        except Exception as e:
            db.session.rollback() # If one fails, undo both to prevent "ghost" accounts
            print(f"Registration Crash: {e}")
            flash(f"Error: {e}", "error")

    return render_template('register.html')

# --- LOGIN LOGIC ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        input_pass = request.form.get('password')
        admin_user = request.form.get('admin_user')
        student_sr = request.form.get('sr_code')

        # Admin Login
        if admin_user:
            admin = Admin.query.filter_by(sr_code=admin_user).first()
            if not admin:
                flash("Admin account does not exist.", "error")
                return redirect(url_for('login'))
            if not check_password_hash(admin.password, input_pass):
                flash("Incorrect password.", "error")
                return redirect(url_for('login'))
            session['user_id'] = admin.admin_id
            session['role'] = 'admin'
            return redirect(url_for('admin_dashboard'))

        # Student Login
        if student_sr:
            student = Student.query.filter_by(sr_code=student_sr).first()
            if not student:
                flash("SR-Code does not exist.", "error")
                return redirect(url_for('login'))
            if not check_password_hash(student.password, input_pass):
                flash("Incorrect password.", "error")
                return redirect(url_for('login'))
            session['user_id'] = student.id
            session['user_sr'] = student.sr_code
            session['role'] = 'student'
            return redirect(url_for('student_dashboard'))

    return render_template('login.html')

# --- ADMIN DASHBOARD LOGIC ---
@app.route('/admin_dashboard')
def admin_dashboard():
    # Purpose: Shows student folders and records to the Admin
    if session.get('role') != 'admin':
        return redirect(url_for('login'))

    dept_name = request.args.get('dept_name')
    program_name = request.args.get('program_name')

    dept_map = {'COE': 'Engineering', 'CICS': 'CICS', 'CET': 'CET', 'CAFAD': 'CAFAD'}
    db_dept = dept_map.get(dept_name)

    all_programs = {
        'Engineering': [
            'Aerospace Engineering', 'Biomedical Engineering', 'Chemical Engineering',
            'Civil Engineering', 'Computer Engineering', 'Electrical Engineering',
            'Electronics Engineering', 'Food Engineering', 'Geodetic Engineering',
            'Industrial Engineering', 'Instrumentation and Control Engineering',
            'Mechanical Engineering', 'Mechatronics Engineering (MEXE)',
            'Naval Architecture and Marine Engineering (NAME)',
            'Petroleum Engineering', 'Sanitary Engineering'
        ],
        'CET': [
            'Automotive Engineering Technology', 'Civil Engineering Technology',
            'Computer Engineering Technology', 'Electrical Engineering Technology',
            'Electronics Engineering Technology', 'Mechanical Engineering Technology'
        ],
        'CICS': [
            'Information Technology', 'Computer Science'
        ],
        'CAFAD': [
            'Architecture', 'Fine Arts', 'Interior Design'
        ]
    }
    programs = all_programs.get(db_dept, [])
    students = []

    try:
        if program_name:
            res = db.session.execute(
                db.text("SELECT * FROM medical_records WHERE program=:p"),
                {'p': program_name}
            ).fetchall()

            # Safety: This loop must be indented inside the 'if program_name'
            for row in res:
                s = dict(row._mapping)
                b = s.get('birthdate')
                s['birthdate'] = b.strftime('%m/%d/%Y') if b and hasattr(b, 'strftime') else '---'
                s['fullname'] = s.get('fullname') or "Unnamed Student"
                s['blood_type'] = s.get('blood_type') or "N/A"
                s['allergies'] = s.get('allergies') or "None"
                students.append(s)

    except Exception as e:
        print(f"DEBUG ERROR: {e}")

    return render_template('admin.html',
                           dept_name=dept_name,
                           program_name=program_name,
                           programs=programs,
                           students=students)

# --- INDIVIDUAL RECORD VIEW ---
@app.route('/record/<sr_code>')
def manage_record(sr_code):
    # Purpose: Pulls up a single student record for editing
    res = db.session.execute(
        db.text("SELECT * FROM medical_records WHERE sr_code=:sr"),
        {'sr': sr_code}
    ).fetchone()

    if res:
        student_detail = dict(res._mapping)
        return render_template('admin.html', student_detail=student_detail)

    return redirect(url_for('admin_dashboard'))

# --- DATABASE UPDATE LOGIC ---
@app.route('/update_record/<sr_code>', methods=['POST'])
def update_record(sr_code):
    if session.get('role') != 'admin':
        return redirect(url_for('login'))

    # Get the current student's Dept and Program BEFORE updating
    # This allows us to redirect back to the correct list of names later
    info = db.session.execute(
        db.text("SELECT college, program FROM medical_records WHERE sr_code=:sr"),
        {'sr': sr_code}
    ).fetchone()

    # Determine where to send the admin back to
    rev_map = {'Engineering': 'COE', 'CICS': 'CICS', 'CET': 'CET', 'CAFAD': 'CAFAD'}
    target_dept = rev_map.get(info.college) if info else None
    target_prog = info.program if info else None

    # Collect the edited data from the form
    data = {
        'n': request.form.get('fullname'),
        'b': request.form.get('birthday'),
        'addr': request.form.get('address'),
        'cont': request.form.get('contact'),
        'bt': request.form.get('blood_type'),
        'a': request.form.get('allergies'),
        'h': request.form.get('history'),
        'sr': sr_code
    }

    try:
        # 3. Perform the update
        db.session.execute(db.text("""UPDATE medical_records
            SET fullname=:n, birthdate=:b, address=:addr, parent_contact=:cont,
                blood_type=:bt, allergies=:a, visit_history=:h
            WHERE sr_code=:sr"""), data)
        db.session.commit()
        flash("Record Updated successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash("Error during registration. SR-Code might already exist.", "error")

    # THE FIX: Redirect back to the specific list of names, not the main menu
    return redirect(url_for('admin_dashboard', dept_name=target_dept, program_name=target_prog))

# --- STUDENT DASHBOARD LOGIC ---
@app.route('/student_dashboard')
def student_dashboard():
    # Purpose: Shows a student their own medical profile
    if session.get('role') != 'student':
        return redirect(url_for('login'))

    sr = session.get('user_sr')

    try:
        record = db.session.execute(
            db.text("SELECT * FROM medical_records WHERE sr_code=:sr"),
            {'sr': sr}
        ).fetchone()

        if record:
            return render_template('student_dashboard.html',
                                   name=record.fullname,
                                   sr=sr,
                                   bday=record.birthdate.strftime('%m/%d/%Y') if record.birthdate else "---",
                                   addr=record.address,
                                   contact=record.parent_contact,
                                   blood=record.blood_type,
                                   year=record.year_level,
                                   allergies=record.allergies,
                                   log=record.visit_history)

        return "<h1>Profile Error</h1>Record not found."

    except Exception as e:
        print(f"Dashboard Error: {e}")
        return "An error occurred."

# --- LOGOUT LOGIC ---
@app.route('/logout')
def logout():
    # Purpose: Clears the session and logs the user out
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
