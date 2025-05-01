import cv2
import time
import requests
import os
from datetime import datetime

API_KEY = "pRWJ7BuSAPCmouo3B5XxSLcVsVH5h_kL"
API_SECRET = "1WHstlsEcu-tQ5_eXA0NbLn61gKyZXBL"

os.makedirs("student_data", exist_ok=True)

def auto_capture_photo(student_id):
    """Capture photo from webcam with improved error handling"""
    try:
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) 
        if not cap.isOpened():
            raise Exception("Webcam not found or accessible")
        
        print("\n🔵 Get ready for photo capture in 3 seconds...")
        for i in range(3, 0, -1):
            print(f"{i}...", end=' ', flush=True)
            time.sleep(1)
        
        ret, frame = cap.read()
        if not ret:
            raise Exception("Failed to capture image")
        
     
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"student_data/{student_id}_{timestamp}.jpg"
        cv2.imwrite(filename, frame)
        print(f"\n✅ Photo saved as {filename}")
        return filename
        
    except Exception as e:
        print(f"\n❌ Error during capture: {str(e)}")
        return None
    finally:
        if 'cap' in locals():
            cap.release()

def get_face_token(photo_path):
    """Get face token with better error handling and retries"""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(f"\nAttempt {attempt+1} to detect face...")
            response = requests.post(
                "https://api-us.faceplusplus.com/facepp/v3/detect",
                files={'image_file': open(photo_path, 'rb')},
                data={
                    'api_key': API_KEY,
                    'api_secret': API_SECRET,
                    'return_landmark': 0
                },
                timeout=10
            )
            response.raise_for_status()
            result = response.json()
            
            if 'faces' in result and result['faces']:
                face_token = result['faces'][0]['face_token']
                print(f"✅ Face Token: {face_token}")
                return face_token
            else:
                print("❌ No face detected in the image")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"⚠️ API Error: {str(e)}")
            if attempt == max_retries - 1:
                return None
            time.sleep(2)

def save_student_data(student_id, face_token):
    """Save student data to a file"""
    with open("student_data/registered_students.txt", "a") as f:
        f.write(f"{student_id},{face_token}\n")
    print(f"Student data saved for ID: {student_id}")

def main():
    print("\n" + "="*50)
    print("STUDENT REGISTRATION SYSTEM".center(50))
    print("="*50 + "\n")
    
    student_id = input("Enter Student ID: ").strip()
    if not student_id:
        print("❌ Student ID cannot be empty!")
        return
    
    photo_path = auto_capture_photo(student_id)
    if not photo_path:
        return
    
    face_token = get_face_token(photo_path)
    if face_token:
        save_student_data(student_id, face_token)
        print("\n🎉 Registration Successful! 🎉")
    else:
        print("\n⚠️ Registration Failed. Please try again with better lighting.")

if __name__ == "__main__":
    main()