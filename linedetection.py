import cv2
import numpy as np
import matplotlib.pyplot as plt

def imshowPLT(image):
    plt.imshow(image)
    plt.show()

def imshowCV(image):
    cv2.imshow("Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def drawLines(image, lines, color=[0, 0, 255], thickness = 3):
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(image, (x1, y1), (x2, y2), color, thickness=10)

def findAverageLines(image, lines):
    imgCopy= image.copy()
    leftLines = []
    leftWeights = []
    rightLines = []
    rightWeights = []

    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:

                if x1 == x2:
                    pass
                else:
                    k = (y2 - y1) / (x2 - x1)
                    c = y1 - k * x1
                    length = np.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)
                    if k < 0:
                        leftLines.append((k, c))
                        leftWeights.append((length))
                    else:
                        rightLines.append((k, c))
                        rightWeights.append((length))

        left_lane = np.dot(leftWeights, leftLines) / np.sum(leftWeights) if len(leftWeights) > 0 else None
        right_lane = np.dot(rightWeights, rightLines) / np.sum(rightWeights) if len(rightWeights) > 0 else None

        for slope, intercept in [left_lane, right_lane]:

            height = image.shape[0]

            y1 = int(height)

            y2 = int(0.65 * height)

            x1 = int((y1-intercept)/slope)
            x2 = int((y2-intercept)/slope)

            drawLines(imgCopy, np.array([[[x1, y1, x2, y2]]]), color=[0, 0, 255], thickness=10)

        return cv2.addWeighted(image, 0.1, imgCopy, 0.95, 0.)

def getROI(image, vertices):

    mask = np.zeros_like(image)
    if len(image.shape) > 2:
        channel_count = image.shape[2]
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255

    cv2.fillPoly(mask, vertices, ignore_mask_color)

    maskedImage = cv2.bitwise_and(image, mask)
    return maskedImage


def getVertices(image):
    height = image.shape[0]
    width = image.shape[1]

    bottom_left = [width * 0.15, height]
    top_left = [width * 0.45, height * 0.6]
    bottom_right = [width * 0.95, height]
    top_right = [width * 0.55, height * 0.6]

    polyCoordinates = np.array([[bottom_left, top_left, top_right, bottom_right]], dtype=np.int32)
    return polyCoordinates


def filterWhiteYellow(image):
    hslImage = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)

    lowerWhite = np.uint8([0, 200, 0])
    upperWhite = np.uint8([255, 255, 255])
    whiteMask = cv2.inRange(hslImage, lowerWhite, upperWhite)

    lowerYellow = np.uint8([20, 0, 100])
    upperYellow = np.uint8([50, 255, 255])
    yellowMask = cv2.inRange(hslImage, lowerYellow, upperYellow)

    mask = cv2.bitwise_or(whiteMask, yellowMask)
    
    masked = cv2.bitwise_and(image, image, mask = mask)
    return masked


def processImage(image):
    imgMasked = filterWhiteYellow(image)
    vertices = getVertices(imgMasked)
    roiImage = getROI(imgMasked, vertices)

    grayImage = cv2.cvtColor(roiImage, cv2.COLOR_BGR2GRAY)
    gaussianImage = cv2.GaussianBlur(grayImage, (11, 11), 0)
    cannyImage = cv2.Canny(gaussianImage, threshold1=50, threshold2=150)

    houghLines = cv2.HoughLinesP(cannyImage, rho=1, theta=np.pi/180, threshold=20, minLineLength=20, maxLineGap=300)

    lineImage = np.zeros((image.shape[0], image.shape[1],3), dtype=np.uint8)

    lineImage = findAverageLines(lineImage, houghLines)

    output = cv2.addWeighted(lineImage, 1, image, 1, 0.)

    return imgMasked, grayImage, cannyImage, roiImage, output






