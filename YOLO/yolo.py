# -*- coding: utf-8 -*-
"""Untitled

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-dw03DZhbjMuxIrKTS9barpqeZWVXM6u

# ***Image Classification Model using YOLO (You Only Look Once)***

<table class="tfo-notebook-buttons" align="left">
  <td>
    <a target="_blank" href="https://pjreddie.com/darknet/yolo/"><img src="https://pjreddie.com/media/image/yologo_2.png" alt="Yolo" width="80" height="40" />View on Yolo site</a>
  </td>
  <td>
    <a target="_blank" href="https://colab.research.google.com/drive/1-dw03DZhbjMuxIrKTS9barpqeZWVXM6u#scrollTo=u4nN351_Dd1Y"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" />Run in Google Colab</a>
  </td>
  <td>
    <a target="_blank" href="https://github.com/tensorflow/hub/blob/master/examples/colab/object_detection.ipynb"><img src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" />View source on GitHub</a>
  </td>
  <td>
    <a href="https://pjreddie.com/media/files/yolov3.weights"><img src="https://www.tensorflow.org/images/download_logo_32px.png" />Download Yolo Weights</a>
  </td>
</table>
"""

!git clone https://github.com/pjreddie/darknet

cd darknet

!make

!wget https://pjreddie.com/media/files/yolov3.weights

!./darknet detect cfg/yolov3.cfg yolov3.weights data/dog.jpg

!./darknet detector test cfg/coco.data cfg/yolov3.cfg yolov3.weights data/dog.jpg

# !wget https://pjreddie.com/media/files/yolov3-tiny.weights

import numpy as np
import cv2

confidenceThreshold = 0.5
NMSThreshold = 0.3

modelConfiguration = '/content/darknet/cfg/yolov3.cfg'
modelWeights = '/content/darknet/yolov3.weights'
inputimage = '/content/darknet/data/dog.jpg'
labelsPath = '/content/darknet/data/coco.names'

labels = open(labelsPath).read().strip().split('\n')
labels

np.random.seed(10)
COLORS = np.random.randint(0, 255, size=(len(labels), 3), dtype="uint8")

net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
image = cv2.imread(inputimage)
(H, W) = image.shape[:2]

layerName = net.getLayerNames()
layerName = [layerName[i[0] - 1] for i in net.getUnconnectedOutLayers()]

blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB = True, crop = False)
net.setInput(blob)
layersOutputs = net.forward(layerName)

boxes = []
confidences = []
classIDs = []

for output in layersOutputs:
    for detection in output:
        scores = detection[5:]
        classID = np.argmax(scores)
        confidence = scores[classID]
        if confidence > confidenceThreshold:
            box = detection[0:4] * np.array([W, H, W, H])
            (centerX, centerY,  width, height) = box.astype('int')
            x = int(centerX - (width/2))
            y = int(centerY - (height/2))

            boxes.append([x, y, int(width), int(height)])
            confidences.append(float(confidence))
            classIDs.append(classID)

detectionNMS = cv2.dnn.NMSBoxes(boxes, confidences, confidenceThreshold, NMSThreshold)
if(len(detectionNMS) > 0):
    for i in detectionNMS.flatten():
        (x, y) = (boxes[i][0], boxes[i][1])
        (w, h) = (boxes[i][2], boxes[i][3])
        
        detected = labels[classIDs[i]]
        print(detected)
        
        color = [int(c) for c in COLORS[classIDs[i]]]
        cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
        text = '{}: {:.4f}'.format(labels[classIDs[i]], confidences[i])
        cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

cv2.imshow('Image', image)
cv2.waitKey(0)