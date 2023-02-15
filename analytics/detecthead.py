import cv2

cap = cv2.VideoCapture('swing-5.mp4')

object_detection = cv2.createBackgroundSubtractorMOG2(
    history=100, varThreshold=40)

while True:
    ret, frame = cap.read()
    height, width, _ = frame.shape
    roi = frame[0:height, 250:1000]

    if not ret:
        break

    mask = object_detection.apply(roi)

    _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(
        mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 25:
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 2)
    # show the contour in the frame and update the text

    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)
    cv2.imshow('roi', roi)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
