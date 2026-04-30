import dlib
import streamlit as st
import numpy as np
from PIL import Image
import face_recognition_models
from sklearn.svm import SVC
from src.database.db import get_all_students


@st.cache_resource
def load_dlib_models():
    """Load and cache dlib models."""
    face_detector = dlib.get_frontal_face_detector()
    
    # Load shape predictor and face recognition models using face_recognition_models paths
    shape_predictor = dlib.shape_predictor(face_recognition_models.pose_predictor_model_location())
    face_recognition_model = dlib.face_recognition_model_v1(face_recognition_models.face_recognition_model_location())
    
    return face_detector, shape_predictor, face_recognition_model

# Ye function face_pipeline.py mein hona chahiye
def train_classifier():
    """Clear the cached resource and re-train the model with new data."""
    try:
        st.cache_resource.clear() # Purana cached model delete karne ke liye
        model_data = get_trained_model() # Naya model train karne ke liye
        return bool(model_data)
    except Exception as e:
        print(f"Error during training: {e}")
        return False


def get_face_embeddings(image_np):
    """Detect faces and return 128D embeddings."""
    face_detector, shape_predictor, face_recognition_model = load_dlib_models()
    
    # Detect faces in the image
    faces = face_detector(image_np, 1)
    
    if len(faces) == 0:
        return []

    encodings = []
    for face in faces:
        # Get facial landmarks
        shape = shape_predictor(image_np, face)
        # num_jitters=1 helps in getting more stable embeddings
        face_descriptor = face_recognition_model.compute_face_descriptor(image_np, shape, num_jitters=1)
        encodings.append(np.array(face_descriptor))
        
    return encodings

def get_trained_model():
    """Train SVM classifier on student data from Database."""
    X, y = [], []
    student_db = get_all_students()

    if not student_db:
        return None
    
    for student in student_db:
        embedding = student.get('face_embedding')
        if embedding:
            # Convert stored list/string embedding back to numpy array
            X.append(np.array(embedding))
            y.append(student.get('student_id'))

    if len(X) == 0:
        return None
    
    unique_ids = sorted(list(set(y)))
    clf = None

    # SVM needs at least 2 distinct students
    if len(unique_ids) >= 2:
        try:
            clf = SVC(kernel="linear", probability=True, class_weight='balanced')
            clf.fit(X, y)
        except Exception as e:
            st.error(f"Training failed: {e}")
            return None
    
    return {'clf': clf, 'X': X, 'y': y, 'unique_ids': unique_ids}

def predict_attendance(class_image_np):
    """Match faces using SVM and Distance threshold."""
    encodings = get_face_embeddings(class_image_np)
    detected_students = {}
    model_data = get_trained_model()

    if not model_data or not encodings:
        return {}, [], len(encodings), "Model or faces not detected."

    clf = model_data['clf']
    X_train = model_data['X']
    y_train = model_data['y']
    all_student_ids = model_data['unique_ids']

    # Threshold for face verification (lower is stricter)
    resemblance_threshold = 0.6 

    for current_encoding in encodings:
        predicted_id = None

        # Case 1: Multi-class classification using SVM
        if clf is not None:
            predicted_id = int(clf.predict([current_encoding])[0])
        else:
            # Case 2: Single student in database
            predicted_id = int(all_student_ids[0])

        # Verification using Euclidean distance
        match_idx = y_train.index(predicted_id)
        trained_embedding = X_train[match_idx]
        
        # Calculate distance (L2 Norm)
        distance = np.linalg.norm(trained_embedding - current_encoding)

        if distance <= resemblance_threshold:
            detected_students[predicted_id] = True

    return detected_students, all_student_ids, len(encodings), "Success"