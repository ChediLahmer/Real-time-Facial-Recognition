# Project Documentation:

# **Face Recognition System**

## **Overview**

This project implements a simple face recognition system using the OpenCV and face_recognition libraries in Python. The system captures video frames from a webcam, detects faces in each frame, and compares the detected face with a reference face to determine if there is a match.

## **Dependencies**

- Python 3.x
- OpenCV (**`cv2`**) library
- face_recognition library

Install the required libraries using the following commands:

```bash
pip install opencv-python
pip install face-recognition
```

## **Code Explanation**

### **Imports**

```python
pythonCopy code
import threading
import cv2
import face_recognition
```

- The **`threading`** module is used for running face recognition in a separate thread.
- **`cv2`** is the OpenCV library for computer vision.
- **`face_recognition`** is a face recognition library that uses dlib.

### **Face Recognition Function**

```python
pythonCopy code
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

```

- The **`check_face`** function takes a frame (**`myframe`**) as input and performs face recognition on it.
- It detects face locations in the frame using **`face_recognition.face_locations`**.
- If exactly one face is detected, it extracts the face encoding and compares it with the reference face encoding.
- The result of the comparison is stored in the global variable **`face_match`**.

### **Video Capture Setup**

```python
pythonCopy code
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

```

- The project captures video from the default camera (index 0).
- The frame dimensions are set to 640x480 pixels.

### **Initialization**

```python
pythonCopy code
counter = 0
face_match = False
image_path = 'me.png'
reference_img = face_recognition.load_image_file(image_path)
lock = threading.Lock()

```

- **`counter`** is used to control the frequency of face recognition (every 30 frames in this case).
- **`face_match`** is a global variable indicating whether a face match is found.
- **`image_path`** is the file path to the reference image for face recognition.
- The reference image is loaded using **`face_recognition.load_image_file`**.
- **`lock`** is a threading lock to synchronize access to the **`face_match`** variable.

### **Main Loop**

```python
pythonCopy code
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

```

- The main loop captures frames from the webcam using **`cap.read()`**.
- Every 30 frames, a new thread is started to perform face recognition using the **`check_face`** function.
- The result of face recognition is displayed on the frame using OpenCV functions.
- The loop continues until the user presses the 'q' key.

### **Cleanup**

```python
pythonCopy code
cv2.destroyAllWindows()
cap.release()

```

- Closes all OpenCV windows and releases the video capture object.

## **Usage**

1. Ensure that Python and the required libraries are installed.
2. Set the correct camera index in **`cv2.VideoCapture(0)`**.
3. Provide the path to the reference image in the **`image_path`** variable.
4. Run the script and observe the live video feed with face recognition results.

## **Note**

- Ensure that the **`dlib`** library is installed, as it is a dependency of **`face_recognition`**.
- The performance of the face recognition system may vary based on the quality of the reference image and environmental conditions.

## **References**

- [OpenCV Documentation](https://docs.opencv.org/)
- [face_recognition Documentation](https://github.com/ageitgey/face_recognition)