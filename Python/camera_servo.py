import cv2
import requests
import time

ESP32_IP = "192.168.4.1"

# Create a session and ignore Windows proxy settings
session = requests.Session()
session.trust_env = False

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Camera could not be opened")
    exit()

print("===================================")
print(" CAMERA → ESP32 → SERVO")
print("===================================")
print("Press Q to quit")

last_position = None
last_command_time = 0

def move_servo(angle, position):

    global last_command_time

    try:

        print(f"Sending: {position} -> {angle}°")

        response = session.get(
            f"http://{ESP32_IP}/servo",
            params={"angle": angle},
            timeout=2
        )

        print(
            f"ESP32 response: "
            f"{response.status_code} | {response.text}"
        )

        last_command_time = time.time()

    except Exception as e:

        print("ESP32 COMMAND ERROR:")
        print(e)


while True:

    ret, frame = camera.read()

    if not ret:
        print("Camera frame failed")
        break

    # Mirror camera
    frame = cv2.flip(frame, 1)

    height, width, _ = frame.shape

    # Convert to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Red object
    lower_red1 = (0, 120, 70)
    upper_red1 = (10, 255, 255)

    lower_red2 = (170, 120, 70)
    upper_red2 = (180, 255, 255)

    mask1 = cv2.inRange(
        hsv,
        lower_red1,
        upper_red1
    )

    mask2 = cv2.inRange(
        hsv,
        lower_red2,
        upper_red2
    )

    mask = mask1 + mask2

    # Find objects
    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    position = "NO OBJECT"

    if contours:

        largest = max(
            contours,
            key=cv2.contourArea
        )

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

            # Draw center
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
                angle = 30

            elif center_x < (2 * width // 3):

                position = "CENTER"
                angle = 90

            else:

                position = "RIGHT"
                angle = 150

            # Send only when position changes
            # Also wait 0.5 second between commands
            if (
                position != last_position
                and time.time() - last_command_time > 0.5
            ):

                move_servo(angle, position)

                last_position = position

    # Draw zone boundaries

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

    cv2.imshow(
        "AI Camera + ESP32 Servo",
        frame
    )

    # Q = quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


camera.release()
cv2.destroyAllWindows()

print("Camera stopped.")
