import cv2
from imutils.video import WebcamVideoStream
import face_recognition

import numpy as np
import argparse
import sys
from math import pow, sqrt

labels = [line.strip() for line in open("class_labels.txt")]

# Generate random bounding box bounding_box_color for each label
bounding_box_color = np.random.uniform(0, 255, size=(len(labels), 3))


# Load model
print("\nLoading model...\n")
network = cv2.dnn.readNetFromCaffe("SSD_MobileNet_prototxt.txt", "SSD_MobileNet.caffemodel")

print("\nStreaming video using device...\n")

class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.

        self.stream = WebcamVideoStream(src=0).start()

    def __del__(self):
        self.stream.stop()

    def get_frame(self):

        frame = self.stream.read()

        (h, w) = frame.shape[:2]

        # Resize the frame to suite the model requirements. Resize the frame to 300X300 pixels
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)

        # network = cv2.dnn.readNetFromCaffe("SSD_MobileNet_prototxt.txt", "SSD_MobileNet.caffemodel")
        network.setInput(blob)
        detections = network.forward()

        pos_dict = dict()
        coordinates = dict()

        # Focal length
        F = 615

        for i in range(detections.shape[2]):

            confidence = detections[0, 0, i, 2]

            if confidence > 0.2:

                class_id = int(detections[0, 0, i, 1])

                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype('int')

                # Filtering only persons detected in the frame. Class Id of 'person' is 15
                if class_id == 15.00:

                    # Draw bounding box for the object
                    cv2.rectangle(frame, (startX, startY), (endX, endY), bounding_box_color[class_id], 2)

                    label = "{}: {:.2f}%".format(labels[class_id], confidence * 100)
                    print("{}".format(label))


                    coordinates[i] = (startX, startY, endX, endY)

                    # Mid point of bounding box
                    x_mid = round((startX+endX)/2,4)
                    y_mid = round((startY+endY)/2,4)

                    height = round(endY-startY,4)

                    # Distance from camera based on triangle similarity
                    distance = (165 * F)/height
                    print("Distance(cm):{dist}\n".format(dist=distance))

                    # Mid-point of bounding boxes (in cm) based on triangle similarity technique
                    x_mid_cm = (x_mid * distance) / F
                    y_mid_cm = (y_mid * distance) / F
                    pos_dict[i] = (x_mid_cm,y_mid_cm,distance)

        # Distance between every object detected in a frame
        close_objects = set()
        for i in pos_dict.keys():
            for j in pos_dict.keys():
                if i < j:
                    dist = sqrt(pow(pos_dict[i][0]-pos_dict[j][0],2) + pow(pos_dict[i][1]-pos_dict[j][1],2) + pow(pos_dict[i][2]-pos_dict[j][2],2))

                    # Check if distance less than 2 metres or 200 centimetres
                    if dist < 200:
                        close_objects.add(i)
                        close_objects.add(j)

        for i in pos_dict.keys():
            if i in close_objects:
                COLOR = np.array([0,0,255])
                (startX, startY, endX, endY) = coordinates[i]
                cv2.rectangle(frame, (startX, startY), (endX, endY), (0,0,255), 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                # Convert cms to feet
                cv2.putText(frame, 'Depth: {i} ft'.format(i=round(pos_dict[i][2]/30.48,4)), (startX, y),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
                
                
                
            else:
                COLOR = np.array([0,255,0])
                (startX, startY, endX, endY) = coordinates[i]
                cv2.rectangle(frame, (startX, startY), (endX, endY), (0,255,0), 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
    # Convert cms to feet
                cv2.putText(frame, 'Depth: {i} ft'.format(i=round(pos_dict[i][2]/30.48,4)), (startX, y),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
                

        ret, jpeg = cv2.imencode('.jpg', frame)
        data = []
        data.append(jpeg.tobytes())
        # data.append(name)
        return data