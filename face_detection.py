import cv2
import mediapipe as mp


mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)


cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = face_detection.process(image)

 
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.detections:
      
        if len(results.detections) > 1:
            print("⚠️ Multiple faces detected!")
        elif len(results.detections) == 1:
            print("✅ One face detected.")
        
      
        for detection in results.detections:
            mp_drawing.draw_detection(image, detection)
    else:
        print("❌ No face detected!")

    
    cv2.imshow('Face Detection', image)

   
    if cv2.waitKey(5) & 0xFF == 27:  
        break


cap.release()
cv2.destroyAllWindows()
