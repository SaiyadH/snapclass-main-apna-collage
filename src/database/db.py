# from src.database.config import supabase
# import bcrypt



# def hash_pass(pwd):
#     return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()

# def check_pass(pwd, hashed):
#     return bcrypt.checkpw(pwd.encode(), hashed.encode())

# def check_teacher_exists(username):
#     # Supabase query to check if teacher exists
#     response = supabase.table('teacher').select('username').eq('username', username).execute()
#     return len(response.data) > 0


# def create_teacher(username, password, name):

#     data = { 'username': username, 'password': hash_pass(password), "name": name }
#     response = supabase.table('teacher').insert(data).execute() 
#     return response.data

# def teacher_login(username, password):
#     response = supabase.table('teacher').select('*').eq('username', username).execute()
#     # if len(response.data) == 0:
#     #     return False, "Teacher not found"
    
#     # teacher = response.data[0]
#     # if bcrypt.checkpw(password.encode(), teacher['password'].encode()):
#     #     return True, teacher
#     # else:
#     #     return False, "Incorrect password"  
#     if response.data:
#         teacher = response.data[0]
#         if check_pass(password, teacher['password']):
#             return True, teacher
#         # else:
#         #     return False, "Incorrect password"
#     return None
    

# def get_all_students():
#     response = supabase.table('students').select('*').execute()
#     return response.data

# def create_student(new_name, face_embedding=None, voice_embedding = None):
#     data = {'name':new_name, 'face_embedding':face_embedding, 'voice_embedding':voice_embedding}
#     response = supabase.table('students').insert(data).execute()
#     return response.data


# def create_subject(subject_code, name, section, teacher_id):
#     data = {"subject_code":subject_code, "name":name, "section":section, "teacher_id":teacher_id}
#     response = supabase.table("subjects").insert(data).execute()
#     return response.data


# def get_teacher_subjects(teacher_id):
#     response = supabase.table('subjects').select("*, subject_students(count), attendance_logs(timestamp)").eq("teacher_id", teacher_id).execute()
#     subjects = response.data


#     for sub in subjects:
#         sub["total_student"] = sub.get("subject_student", [{}])[0].get('count', 0) if sub.get('subject_students') else 0
#         attendance = sub.get("attendance_log", [])
#         unique_session = len(set(log['timestamp'] for log in attendance))
#         sub['total_classes'] = unique_session

#         sub.pop('subject_student', None)
#         sub.pop('attendance_logs', None)

#     return subjects

from src.database.config import supabase
import bcrypt

# --- Password Utilities ---
def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()

def check_pass(pwd, hashed):
    return bcrypt.checkpw(pwd.encode(), hashed.encode())

# --- Teacher Logic ---
def check_teacher_exists(username):
    response = supabase.table('teacher').select('username').eq('username', username).execute()
    return len(response.data) > 0

def create_teacher(username, password, name):
    data = { 'username': username, 'password': hash_pass(password), "name": name }
    response = supabase.table('teacher').insert(data).execute() 
    return response.data

def teacher_login(username, password):
    response = supabase.table('teacher').select('*').eq('username', username).execute()
    if response.data:
        teacher = response.data[0]
        if check_pass(password, teacher['password']):
            return True, teacher
    return False, "Invalid credentials" # None ki jagah consistent return rakhein

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
    data = {"subject_code": subject_code, "name": name, "section": section, "teacher_id": teacher_id}
    response = supabase.table("subjects").insert(data).execute()
    return response.data

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