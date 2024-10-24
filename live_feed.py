import cv2
import numpy as np

# Function to do nothing, used as a placeholder for the trackbar callbacks
def nothing(x):
    pass

# Initialize webcam
cap = cv2.VideoCapture(0)

# Create a window named 'HSV Adjuster'
cv2.namedWindow('HSV Adjuster')

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

    # Print the original frame size for debugging
    print(f"Original frame shape: {frame.shape}")
    
    # Ensure the frame width is greater than 200 pixels
    if frame.shape[1] > 200:
        # Crop the frame to keep only the part starting from column 200 onwards
        frame_cropped = frame[:, 600:]
    else:
        print("Frame width is less than 200 pixels, cannot crop.")
        frame_cropped = frame

    # Convert the cropped part of the frame to HSV
    hsv = cv2.cvtColor(frame_cropped, cv2.COLOR_BGR2HSV)

    # Get current positions of all trackbars
    h_min = cv2.getTrackbarPos('Hue Min', 'HSV Adjuster')
    h_max = cv2.getTrackbarPos('Hue Max', 'HSV Adjuster')
    s_min = cv2.getTrackbarPos('Sat Min', 'HSV Adjuster')
    s_max = cv2.getTrackbarPos('Sat Max', 'HSV Adjuster')
    v_min = cv2.getTrackbarPos('Val Min', 'HSV Adjuster')
    v_max = cv2.getTrackbarPos('Val Max', 'HSV Adjuster')

    # Define lower and upper HSV range
    lower_hsv = np.array([h_min, s_min, v_min])
    upper_hsv = np.array([h_max, s_max, v_max])

    # Threshold the HSV image to get only the desired colors
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)

    # Apply the mask to get the result
    result = cv2.bitwise_and(frame_cropped, frame_cropped, mask=mask)

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw contours and area
    for cnt in contours:
        # Calculate area
        cv2.drawContours(result, [cnt], -1, (0, 255, 0), 2)
        area = cv2.contourArea(cnt)
        if area > 5000:  # Adjust this threshold as needed
            x, y, w, h = cv2.boundingRect(cnt)
            # Draw bounding box
            cv2.rectangle(result, (x, y), (x + w, y + h), (255, 0, 0), 2)
            # Put area text
            cv2.putText(result, f"Area: {int(area)}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

    # Display the result and mask
    cv2.imshow('HSV Adjuster', result)
    cv2.imshow('Mask', mask)

    # Exit the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()