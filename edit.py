import cv2
import numpy as np
import csv
import socket

ESP_IP = '192.168.0.22'
ESP_PORT = 80

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to ESP8266
s.connect((ESP_IP, ESP_PORT))

frameWidth = 600
frameHeight = 400

url = "http://192.168.0.21/capture"

font = cv2.FONT_HERSHEY_COMPLEX

def empty(a):
    pass

cv2.namedWindow("Parameter")
cv2.resizeWindow("Parameter", 640, 240)
cv2.createTrackbar("Threshold1", "Parameter", 23, 255, empty)
cv2.createTrackbar("Threshold2", "Parameter", 22, 255, empty)

def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)

    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver

def sendCoordinates(coordinates):
    for point in coordinates:
        data = "{},{},".format(point[0], point[1])
        s.send(data.encode())

def getContours(img, imgContour):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    contour_points = []

    with open('testing_coordinate.csv', 'w') as fh:
        spamwriter = csv.writer(fh)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 1000:
                cv2.drawContours(imgContour, cnt, -1, (255, 0, 255), 7)
                moments = cv2.moments(cnt)
                centroid_x = int(moments["m10"] / moments["m00"])
                centroid_y = int(moments["m01"] / moments["m00"])

                rightmost = tuple(cnt[cnt[:, :, 0].argmax()][0])
                leftmost = tuple(cnt[cnt[:, :, 0].argmin()][0])
                second_rightmost = ((rightmost[0] + centroid_x) // 2, (rightmost[1] + centroid_y) // 2)
                second_leftmost = ((leftmost[0] + centroid_x) // 2, (leftmost[1] + centroid_y) // 2)
                #first_rightmost = ((rightmost[0] + second_rightmost[0]) // 2, (rightmost[1] + second_rightmost[1]) // 2)
                #first_leftmost = ((leftmost[0] + second_leftmost)[0] // 2, (leftmost[1] + second_leftmost[1]) // 2)
                #third_rightmost = ((second_rightmost[0] + centroid_x) // 2, (second_rightmost[1] + centroid_y) // 2)
                #third_leftmost = ((second_leftmost[0] + centroid_x) // 2, (second_leftmost[1] + centroid_y) // 2)

                cv2.putText(imgContour, str(rightmost), (rightmost[0], rightmost[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0))
                cv2.putText(imgContour, str(leftmost), (leftmost[0], leftmost[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0))
                cv2.putText(imgContour, str((centroid_x, centroid_y)), (centroid_x, centroid_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0))
                cv2.putText(imgContour, str(second_rightmost), (second_rightmost[0], second_rightmost[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0))
                cv2.putText(imgContour, str(second_leftmost), (second_leftmost[0], second_leftmost[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0))
                #cv2.putText(imgContour, str(first_rightmost), (first_rightmost[0], first_rightmost[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0))
                #cv2.putText(imgContour, str(first_leftmost), (first_leftmost[0], first_leftmost[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0))
                #cv2.putText(imgContour, str(third_rightmost), (third_rightmost[0], third_rightmost[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0))
                #cv2.putText(imgContour, str(third_leftmost), (third_leftmost[0], third_leftmost[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0))

                spamwriter.writerow(["Rightmost", rightmost[0], rightmost[1]])
                #spamwriter.writerow(["1st Rightmost", first_rightmost[0], first_rightmost[1]])
                spamwriter.writerow(["2nd Rightmost", second_rightmost[0], second_rightmost[1]])
                #spamwriter.writerow(["3rd Rightmost", third_rightmost[0], third_rightmost[1]])
                spamwriter.writerow(["Centroid", centroid_x, centroid_y])
                #spamwriter.writerow(["3rd Leftmost", third_leftmost[0], third_leftmost[1]])
                spamwriter.writerow(["2nd Leftmost", second_leftmost[0], second_leftmost[1]])
                #spamwriter.writerow(["1st Leftmost", first_leftmost[0], first_leftmost[1]])
                spamwriter.writerow(["Leftmost", leftmost[0], leftmost[1]])

                contour_points.append(rightmost)
                #contour_points.append(first_rightmost)
                contour_points.append(second_rightmost)
                #contour_points.append(third_rightmost)
                contour_points.append((centroid_x, centroid_y))
                #contour_points.append(third_leftmost)
                contour_points.append(second_leftmost)
                #contour_points.append(first_leftmost)
                contour_points.append(leftmost)

    sendCoordinates(contour_points)


cap = cv2.VideoCapture(url)

while True:
    ret, img = cap.read()

    if img is None:
        continue

    imgContour = img.copy()

    imgBlur = cv2.GaussianBlur(img, (7,7), 1)
    imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)

    threshold1 = cv2.getTrackbarPos("Threshold1", "Parameter")
    threshold2 = cv2.getTrackbarPos("Threshold2", "Parameter")

    imgCanny = cv2.Canny(imgGray, threshold1, threshold2)
    kernel = np.ones((5, 5))
    imgDil = cv2.dilate(imgCanny, kernel, iterations = 1)

    getContours(imgDil, imgContour)

    imgStack = stackImages(0.8,([img, imgGray, imgCanny],
                                [imgDil, imgContour, imgContour]))

    cv2.imshow("result", imgStack)
    if cv2.waitKey(1) & 0xFF == ord ('q'):
        break
