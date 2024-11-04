import cv2
import numpy as np
import pygame
import time

# Function to handle the trackbar movements
def update_image(val):
    # Get current positions of trackbars
    angle = cv2.getTrackbarPos('Rotate', 'Image')
    zoom_percent = cv2.getTrackbarPos('Zoom', 'Image')
    global vertical_position_1, vertical_position_2, horizontal_position_1, horizontal_position_2
    vertical_position_1 = cv2.getTrackbarPos('Vertical Line 1', 'Image')
    vertical_position_2 = cv2.getTrackbarPos('Vertical Line 2', 'Image')
    horizontal_position_1 = cv2.getTrackbarPos('Horizontal Line 1', 'Image')
    horizontal_position_2 = cv2.getTrackbarPos('Horizontal Line 2', 'Image')

    # Rotate the image
    rotation_matrix = cv2.getRotationMatrix2D((width // 2, height // 2), angle, 1)
    rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height))

    # Zoom and crop the image
    if zoom_percent > 0:
        scale = zoom_percent / 100
        new_width = int(width * scale)
        new_height = int(height * scale)
        start_x = (width - new_width) // 2
        start_y = (height - new_height) // 2
        cropped_image = rotated_image[start_y:start_y + new_height, start_x:start_x + new_width]
        zoomed_image = cv2.resize(cropped_image, (width, height))
    else:
        zoomed_image = rotated_image

    # Draw guide lines
    cv2.line(zoomed_image, (vertical_position_1, 0), (vertical_position_1, height), (0, 255, 0), 1)
    cv2.line(zoomed_image, (vertical_position_2, 0), (vertical_position_2, height), (0, 255, 0), 1)
    cv2.line(zoomed_image, (0, horizontal_position_1), (width, horizontal_position_1), (255, 0, 0), 1)
    cv2.line(zoomed_image, (0, horizontal_position_2), (width, horizontal_position_2), (255, 0, 0), 1)

    # Determine the bounding box of the cropped area between guide lines
    top = min(horizontal_position_1, horizontal_position_2)
    bottom = max(horizontal_position_1, horizontal_position_2)
    left = min(vertical_position_1, vertical_position_2)
    right = max(vertical_position_1, vertical_position_2)
    cropped_area = zoomed_image[top:bottom, left:right]

    # Convert the cropped area to HSV
    hsv_cropped = cv2.cvtColor(cropped_area, cv2.COLOR_BGR2HSV)

    # Get HSV trackbar positions
    hue_min = cv2.getTrackbarPos('Hue Min', 'Image')
    hue_max = cv2.getTrackbarPos('Hue Max', 'Image')
    sat_min = cv2.getTrackbarPos('Sat Min', 'Image')
    sat_max = cv2.getTrackbarPos('Sat Max', 'Image')
    val_min = cv2.getTrackbarPos('Val Min', 'Image')
    val_max = cv2.getTrackbarPos('Val Max', 'Image')

    # Apply HSV thresholding
    lower_hsv = np.array([hue_min, sat_min, val_min])
    upper_hsv = np.array([hue_max, sat_max, val_max])
    mask = cv2.inRange(hsv_cropped, lower_hsv, upper_hsv)
    result = cv2.bitwise_and(cropped_area, cropped_area, mask=mask)

    # Find contours and draw bounding boxes
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        area = cv2.contourArea(cnt)
        if area > 0:
            cv2.rectangle(result, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(result, f"Area: {int(area)}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

    # Place the processed cropped area back into the zoomed image
    zoomed_image[top:bottom, left:right] = result

    # Display the updated image
    cv2.imshow('Image', zoomed_image)

# Function to capture a snapshot of the current cropped area
def take_snapshot():
    # Determine the bounding box of the cropped area between guide lines
    top = min(horizontal_position_1, horizontal_position_2)
    bottom = max(horizontal_position_1, horizontal_position_2)
    left = min(vertical_position_1, vertical_position_2)
    right = max(vertical_position_1, vertical_position_2)
    cropped_area = image[top:bottom, left:right]

    # Save the cropped area as a snapshot
    snapshot_filename = f'snapshots/snapshot_{int(time.time())}.jpg'
    cv2.imwrite(snapshot_filename, cropped_area)
    print(f"Snapshot saved as {snapshot_filename}")

# Load an image
image = cv2.imread('snapshots/globalWiper.JPG')
height, width = image.shape[:2]

# Create a window with reduced height
cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Image', width, height - 500)

# Create trackbars
cv2.createTrackbar('Rotate', 'Image', 0, 360, update_image)
cv2.createTrackbar('Zoom', 'Image', 0, 100, update_image)
cv2.createTrackbar('Vertical Line 1', 'Image', width // 3, width, update_image)
cv2.createTrackbar('Vertical Line 2', 'Image', 2 * width // 3, width, update_image)
cv2.createTrackbar('Horizontal Line 1', 'Image', height // 3, height, update_image)
cv2.createTrackbar('Horizontal Line 2', 'Image', 2 * height // 3, height, update_image)
cv2.createTrackbar('Hue Min', 'Image', 0, 180, update_image)
cv2.createTrackbar('Hue Max', 'Image', 180, 180, update_image)
cv2.createTrackbar('Sat Min', 'Image', 0, 255, update_image)
cv2.createTrackbar('Sat Max', 'Image', 255, 255, update_image)
cv2.createTrackbar('Val Min', 'Image', 0, 255, update_image)
cv2.createTrackbar('Val Max', 'Image', 255, 255, update_image)

# Initial display
update_image(0)

while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):
        take_snapshot()
    elif key == 27:  # ESC key to exit
        break

cv2.destroyAllWindows()
