import numpy as np
import cv2

(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

# set up tracker
tracking_types = ["BOOSTING", "MIL", "KCF", "TLD",
                  "MEDIANFLOW", "GOTURN", "MOSSE", "CSRT"]
tracker_type = tracking_types[7]

if int(minor_ver) < 3:
    tracker = cv2.Tracker_create(tracker_type)
else:
    if tracker_type == 'BOOSTING':
        tracker = cv2.TrackerBoosting_create()
    if tracker_type == 'MIL':
        tracker = cv2.TrackerMIL_create()
    if tracker_type == 'KCF':
        tracker = cv2.TrackerKCF_create()
    if tracker_type == 'TLD':
        tracker = cv2.TrackerTLD_create()
    if tracker_type == 'MEDIANFLOW':
        tracker = cv2.TrackerMedianFlow_create()
    if tracker_type == 'GOTURN':
        tracker = cv2.TrackerGOTURN_create()
    if tracker_type == "MOSSE":
        tracker = cv2.TrackerMOSSE_create()
    if tracker_type == "CSRT":
        tracker = cv2.TrackerCSRT_create()


WIDTH = 1280
HEIGHT = 560

# Read video
video = cv2.VideoCapture("swing-5.mp4")

# start = (0, 0)
# end = (1280, 560)

lower_hsv = np.array([0, 230, 0])
upper_hsv = np.array([179, 255, 255])

ok, frame = video.read()
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, lower_hsv, upper_hsv)

bbox = cv2.selectROI("Frame", frame, False)
ok = tracker.init(frame, bbox)


# Check if video opened successfully
if (video.isOpened() == False):
    print("Error opening video stream or file")

while(video.isOpened()):

    ret, frame = video.read()
    if not ret:
        break

    timer = cv2.getTickCount()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
    ok, bbox = tracker.update(frame)

    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

    if ok:
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        x = int(p1[1] - p1[0])
        y = int(p2[1] - p2[0])
        cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
    else:
        cv2.putText(frame, "Tracking failure detected", (100, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

    cv2.putText(frame, tracker_type + " Tracker", (100, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)

    cv2.putText(frame, "FPS : " + str(int(fps)), (100, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)

    # print out the position of the bbox
    print(f"x: {x}, y: {y}")

    cv2.imshow("Tracking", frame)

    # if ret == True:
    #     # frame = cv2.line(frame, start, end, (0, 0, 0), 2)

    # mask = cv2.inRange(hsv, lower_hsv, upper_hsv)

    #     cv2.imshow('Frame', frame)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

    # else:
    #     break

video.release()

cv2.destroyAllWindows()
