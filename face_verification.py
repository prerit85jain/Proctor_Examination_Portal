import cv2
import time
import requests
import os
from datetime import datetime


API_KEY = "pRWJ7BuSAPCmouo3B5XxSLcVsVH5h_kL"
API_SECRET = "1WHstlsEcu-tQ5_eXA0NbLn61gKyZXBL"


CHECK_INTERVAL = 30  
CONFIDENCE_THRESHOLD = 75 

def load_registered_token():
    """Load the registered face token from file"""
    try:
        with open("student_data/registered_students.txt", "r") as f:
            last_line = f.readlines()[-1].strip()
            return last_line.split(',')[1]
    except Exception as e:
        print(f"❌ Error loading registered token: {str(e)}")
        return None

def auto_capture_photo():
    """Capture photo from webcam with improved reliability"""
    try:
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not cap.isOpened():
            raise Exception("Webcam not accessible")
        
        print("\n🔵 Look at the camera for verification in...")
        for i in range(3, 0, -1):
            print(f"{i}...", end=' ', flush=True)
            time.sleep(1)
        
        ret, frame = cap.read()
        if not ret:
            raise Exception("Failed to capture image")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"current_face_{timestamp}.jpg"
        cv2.imwrite(filename, frame)
        print(f"\n✅ Verification photo captured: {filename}")
        return filename
        
    except Exception as e:
        print(f"\n❌ Capture error: {str(e)}")
        return None
    finally:
        if 'cap' in locals():
            cap.release()

def verify_face(registered_token, current_photo):
    """Compare current face with registered face"""
    try:
        response = requests.post(
            "https://api-us.faceplusplus.com/facepp/v3/compare",
            files={'image_file2': open(current_photo, 'rb')},
            data={
                'api_key': API_KEY,
                'api_secret': API_SECRET,
                'face_token1': registered_token
            },
            timeout=10
        )
        response.raise_for_status()
        result = response.json()
        
        if 'confidence' in result:
            confidence = result['confidence']
            if confidence > CONFIDENCE_THRESHOLD:
                print(f"✅ Verified (Confidence: {confidence:.2f}%)")
                return True
            else:
                print(f"❌ Verification Failed (Confidence: {confidence:.2f}%)")
                return False
        else:
            print("⚠️ No confidence score in response")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"⚠️ API Error: {str(e)}")
        return False
    except Exception as e:
        print(f"⚠️ Verification Error: {str(e)}")
        return False

def run_proctoring():
    """Main proctoring loop"""
    print("\n" + "="*50)
    print("EXAM PROCTORING SYSTEM".center(50))
    print("="*50 + "\n")
    
    registered_token = load_registered_token()
    if not registered_token:
        print("❌ No registered face token found. Run registration first!")
        return
    
    print("\n🔍 Starting exam proctoring...")
    print(f"⚙️ Settings: Checks every {CHECK_INTERVAL} seconds")
    print(f"⚙️ Confidence threshold: {CONFIDENCE_THRESHOLD}%")
    
    try:
        while True:
            print(f"\nNext verification in {CHECK_INTERVAL} seconds...")
            time.sleep(CHECK_INTERVAL)
            
            current_photo = auto_capture_photo()
            if not current_photo:
                continue
                
            if not verify_face(registered_token, current_photo):
                print("🚨 ALERT: Potential impersonation detected!")
                # Add additional alert actions here (email, log, etc.)
                break
                
    except KeyboardInterrupt:
        print("\n🛑 Proctoring stopped by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")

if __name__ == "__main__":
    os.makedirs("student_data", exist_ok=True)
    run_proctoring()