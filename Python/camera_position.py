import cv2

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Camera could not be opened")
    exit()

print("Camera started")
print("Move a RED object in front of the camera")
print("Press Q to quit")

while True:

    ret, frame = camera.read()

    if not ret:
        print("Failed to read camera")
        break

    # Mirror the camera
    frame = cv2.flip(frame, 1)

    height, width, _ = frame.shape

    # Convert image to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Red color ranges
    lower_red1 = (0, 120, 70)
    upper_red1 = (10, 255, 255)

    lower_red2 = (170, 120, 70)
    upper_red2 = (180, 255, 255)

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    mask = mask1 + mask2

    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    position = "NO OBJECT"

    if contours:

        largest = max(contours, key=cv2.contourArea)

        area = cv2.contourArea(largest)

        if area > 1000:

            x, y, w, h = cv2.boundingRect(largest)

            center_x = x + w // 2
            center_y = y + h // 2

            # Draw bounding box
            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

            # Draw object center
            cv2.circle(
                frame,
                (center_x, center_y),
                6,
                (255, 0, 0),
                -1
            )

            # Determine position
            if center_x < width // 3:

                position = "LEFT"

            elif center_x < (2 * width // 3):

                position = "CENTER"

            else:

                position = "RIGHT"

    # Draw dividing lines
    cv2.line(
        frame,
        (width // 3, 0),
        (width // 3, height),
        (255, 255, 255),
        2
    )

    cv2.line(
        frame,
        (2 * width // 3, 0),
        (2 * width // 3, height),
        (255, 255, 255),
        2
    )

    # Display position
    cv2.putText(
        frame,
        position,
        (30, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.2,
        (0, 255, 0),
        3
    )

    cv2.imshow("Camera Position Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
