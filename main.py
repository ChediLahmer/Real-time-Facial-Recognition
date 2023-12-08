import threading
import cv2
import face_recognition
def check_face(myframe):
    global face_match
    try:
        face_locations = face_recognition.face_locations(myframe)
        if len(face_locations) == 1:
            face_encoding = face_recognition.face_encodings(myframe, face_locations)[0]
            reference_encoding = face_recognition.face_encodings(reference_img)[0]
            face_match = face_recognition.compare_faces([reference_encoding], face_encoding)[0]
        else:
            face_match = False
    except Exception as e:
        print(f"Error: {str(e)}")
        face_match = False
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
counter = 0
face_match = False
image_path = 'me.png'
reference_img = face_recognition.load_image_file(image_path)
lock = threading.Lock()
while True:
    ret, frame = cap.read()
    if ret:
        if counter % 30 == 0:
            try:
                thread = threading.Thread(target=check_face, args=(frame.copy(),))
                thread.start()
            except Exception as e:
                print(f"Error starting thread: {str(e)}")
        counter += 1
        with lock:
            if face_match:
                cv2.putText(frame, "chedi", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
            else:
                cv2.putText(frame, "No Match !!", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
        cv2.imshow("Live", frame)
    key = cv2.waitKey(1)
    if key == ord("q"):
        break
cv2.destroyAllWindows()
cap.release()