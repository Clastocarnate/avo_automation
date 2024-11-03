import cv2
import numpy as np

# Initialize counters
accepted_count = 0
rejected_count = 0
calculation_started = False

# Function to do nothing, used as a placeholder for the trackbar callbacks
def nothing(x):
    pass

# Function to handle mouse events
def mouse_click(event, x, y, flags, param):
    global calculation_started
    # Check if the left mouse button was clicked and if it is within the "Start" button region
    if event == cv2.EVENT_LBUTTONDOWN:
        if 10 <= x <= 110 and 10 <= y <= 60:  # Coordinates for the button area
            calculation_started = True

# Initialize webcam
cap = cv2.VideoCapture(0)

# Set the desired frame rate (fps)
fps = 3
frame_delay = int(1000 / fps)  # Delay in milliseconds for 3 fps (333ms)

# Create a window named 'HSV Adjuster'
cv2.namedWindow('HSV Adjuster')
cv2.setMouseCallback('HSV Adjuster', mouse_click)  # Set mouse callback

# Create trackbars for adjusting HSV values
cv2.createTrackbar('Hue Min', 'HSV Adjuster', 0, 179, nothing)
cv2.createTrackbar('Hue Max', 'HSV Adjuster', 179, 179, nothing)
cv2.createTrackbar('Sat Min', 'HSV Adjuster', 0, 255, nothing)
cv2.createTrackbar('Sat Max', 'HSV Adjuster', 255, 255, nothing)
cv2.createTrackbar('Val Min', 'HSV Adjuster', 0, 255, nothing)
cv2.createTrackbar('Val Max', 'HSV Adjuster', 255, 255, nothing)

while True:
    # Capture frame from webcam
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Ensure the frame width is greater than 600 pixels for cropping
    if frame.shape[1] > 600:
        # Crop the frame to keep only the part starting from column 800 onwards
        frame_cropped = frame[:, 800:]
    else:
        print("Frame width is less than 600 pixels, cannot crop.")
        frame_cropped = frame

    # Convert the cropped part of the frame to HSV
    hsv = cv2.cvtColor(frame_cropped, cv2.COLOR_BGR2HSV)

    # Get current positions of all trackbars
    h_min = cv2.getTrackbarPos('Hue Min', 'HSV Adjuster')
    h_max = 180
    s_min = cv2.getTrackbarPos('Sat Min', 'HSV Adjuster')
    s_max = 255
    v_min = cv2.getTrackbarPos('Val Min', 'HSV Adjuster')
    v_max = 255

    # Define lower and upper HSV range
    lower_hsv = np.array([h_min, s_min, v_min])
    upper_hsv = np.array([h_max, s_max, v_max])

    # Threshold the HSV image to get only the desired colors
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)

    # Apply the mask to get the result
    result = cv2.bitwise_and(frame_cropped, frame_cropped, mask=mask)

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw contours and bounding boxes along with the area
    for cnt in contours:
        # Calculate the area of the contour
        area = cv2.contourArea(cnt)
        if area > 5000 and area < 30000:  # Adjust this threshold as needed
            # Draw contours
            cv2.drawContours(result, [cnt], -1, (0, 255, 0), 2)

            # Calculate the bounding box around the contour
            x, y, w, h = cv2.boundingRect(cnt)
            # Draw the bounding box
            cv2.rectangle(frame_cropped, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # Display the area inside or next to the bounding box
            cv2.putText(frame_cropped, f"Area: {int(area)}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

            # Start calculation once the button is pressed
            if calculation_started:
                # Check if the detected area is within the acceptable range (11000 to 20000)
                if 12000 <= area <= 20000:
                    accepted_count += 1
                else:
                    rejected_count += 1

    # Draw the "Start" button
    cv2.rectangle(frame_cropped, (10, 10), (110, 60), (0, 255, 0), -1)
    cv2.putText(frame_cropped, "START", (20, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    # Display the accepted and rejected counts
    cv2.putText(frame_cropped, f"Accepted: {accepted_count}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.putText(frame_cropped, f"Rejected: {rejected_count}", (10, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    # Display the result
    cv2.imshow('HSV Adjuster', frame_cropped)

    # Exit the loop when 'q' is pressed or add a delay for 3 FPS
    if cv2.waitKey(frame_delay) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()