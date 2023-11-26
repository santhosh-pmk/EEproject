import cv2
import numpy as np
import socket
my_socket=socket.socket()
port=5055
ip="192.168.43.99"
my_socket.connect((ip,port))
# Replace 'your_ip_address' with the actual IP address of your webcam
url = 'http://192.168.43.103:81/stream'
abscount=0
fireval=0
# Load YOLO
net = cv2.dnn.readNet('yolov3.weights', 'yolov3.cfg')
layer_names = net.getUnconnectedOutLayersNames()

# Create a VideoCapture object to capture video from the webcam
cap = cv2.VideoCapture(url)

# Resize parameters
new_width = 640
new_height = 480

# Frame processing parameters
confidence_threshold = 0.5
nms_threshold = 0.4

# Skip processing every N frames
frame_counter = 0
skip_frames = 5

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Increment frame counter
    frame_counter += 1

    # Skip processing if not enough frames have passed
    if frame_counter % skip_frames != 0:
        continue

    # Reset frame counter
    frame_counter = 0

    if not ret:
        print("Error reading frame")
        break

    # Resize the frame
    frame = cv2.resize(frame, (new_width, new_height))

    # Detect objects using YOLO
    blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    detections = net.forward(layer_names)

    # Filter out only humans (class 0 in COCO dataset)
    for detection in detections:
        for obj in detection:
            scores = obj[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > confidence_threshold and class_id == 0:
                print("Person present")
                if(fireval==0):
                    fireval=1
                    my_socket.send("1".encode())
                abscount=0
                break
        else:
            continue
        break
    else:
        abscount+=1
        if(abscount>=10 and fireval==1):
            fireval=0
            my_socket.send("0".encode())
        print("Person not present")

    # Display the frame
    cv2.imshow('Frame', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture and close the OpenCV window
cap.release()
cv2.destroyAllWindows()