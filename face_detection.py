import cv2
import mediapipe as mp

# Setup MediaPipe Face Detection
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)

# Initialize webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    # Convert frame to RGB (MediaPipe works in RGB, OpenCV works in BGR)
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = face_detection.process(image)

    # Draw face detection on the frame
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.detections:
        # Check how many faces are detected
        if len(results.detections) > 1:
            print("⚠️ Multiple faces detected!")
        elif len(results.detections) == 1:
            print("✅ One face detected.")
        
        # Draw rectangles around the faces
        for detection in results.detections:
            mp_drawing.draw_detection(image, detection)
    else:
        print("❌ No face detected!")

    # Display the frame with detected faces
    cv2.imshow('Face Detection', image)

    # Break the loop on 'Esc' key press
    if cv2.waitKey(5) & 0xFF == 27:  # 27 is the ASCII code for 'Esc'
        break

# Release the webcam and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
