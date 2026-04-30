import streamlit as st
from src.database.config import supabase
import bcrypt


# --- Password Utilities ---
def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()

def check_pass(pwd, hashed):
    return bcrypt.checkpw(pwd.encode(), hashed.encode())

# --- Teacher Logic ---
def check_teacher_exists(username):
    response = supabase.table('teachers').select('username').eq('username', username).execute()
    return len(response.data) > 0

def create_teacher(username, password, name):
    data = { 'username': username, 'password': hash_pass(password), "name": name }
    response = supabase.table('teachers').insert(data).execute() 
    return response.data

def teacher_login(username, password):
    response = supabase.table('teachers').select('*').eq('username', username).execute()
    if response.data:
        teacher = response.data[0]
        if check_pass(password, teacher['password']):
            return teacher
    return None #"Invalid credentials" # None ki jagah consistent return rakhein

# --- Student Logic ---
def get_all_students():
    response = supabase.table('students').select('*').execute()
    return response.data

def create_student(new_name, face_embedding=None, voice_embedding=None):
    data = {'name': new_name, 'face_embedding': face_embedding, 'voice_embedding': voice_embedding}
    response = supabase.table('students').insert(data).execute()
    return response.data

# --- Subject Logic ---
def create_subject(subject_code, name, section, teacher_id):
    # Dhyan dein: Dictionary ki keys wahi honi chahiye jo database table columns hain
    data = {
        "subject_code": subject_code, 
        "name": name,  # Agar DB mein column 'name' hai, toh yahan 'name' likhein
        "section": section, 
        "teacher_id": teacher_id
    }
    try:
        response = supabase.table("subjects").insert(data).execute()
        return response.data
    except Exception as e:
        st.error(f"Database Error: {e}")
        return None
# def create_subject(subject_code, name, section, teacher_id):
#     data = {"subject_code": subject_code, "name": name, "section": section, "teacher_id": teacher_id}
#     response = supabase.table("subjects").insert(data).execute()
#     return response.data

def get_teacher_subjects(teacher_id):
    # Fixed: Query string aur keys ka dhyan rakhein
    response = supabase.table('subjects').select("*, subject_students(count), attendance_logs(timestamp)").eq("teacher_id", teacher_id).execute()
    subjects = response.data

    for sub in subjects:
        # 1. Students Count Fix: Supabase count list return karta hai [{'count': 5}]
        student_data = sub.get("subject_students", [])
        sub["total_students"] = student_data[0].get('count', 0) if student_data else 0
        
        # 2. Attendance Fix: Unique classes count karne ke liye
        attendance = sub.get("attendance_logs", []) # Yahan aapne 'attendance_log' likha tha (s miss tha)
        unique_sessions = len(set(log['timestamp'] for log in attendance))
        sub['total_classes'] = unique_sessions

        # 3. Cleaning: Taaki extra data UI mein na jaye
        sub.pop('subject_students', None)
        sub.pop('attendance_logs', None)

    return subjects


def enroll_student_to_subject(student_id, subject_id):
    data = {'student_id': student_id, "subject_id": subject_id}
    response = supabase.table('subject_students').insert(data).execute()
    return response.data

def unenroll_student_to_subject(student_id, subject_id):
    response = supabase.table('subject_students').delete().eq('student_id', student_id).eq('subject_id', subject_id).execute()
    return response.data

def get_student_subjects(student_id):
    response = supabase.table('subject_students').select('*, subjects(*)').eq('student_id', student_id).execute()
    return response.data


def get_student_attendance(student_id):
    response = supabase.table('attendance_logs').select('*, subjects(*)').eq('student_id', student_id).execute()
    return response.data

def create_attendance(logs):
    response = supabase.table('attendance_logs').insert(logs).execute()
    return response

def get_attendance_for_teacher(teacher_id):
    response = supabase.table('attendance_logs').select('*, subjects!inner(*)').eq('subjects.teacher_id', teacher_id).execute()
    return response.data