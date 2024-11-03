import cv2
import numpy as np

# Function to handle the trackbar movements
def update_image(val):
    # Get current positions of trackbars
    angle = cv2.getTrackbarPos('Rotate', 'Image')
    zoom_percent = cv2.getTrackbarPos('Zoom', 'Image')
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

    # Display the updated image
    cv2.imshow('Image', zoomed_image)

# Load an image
image = cv2.imread('snapshots/globalWiper.JPG')
height, width = image.shape[:2]

# Create a window with reduced height
cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Image', width, height - 1000)

# Create trackbars
cv2.createTrackbar('Rotate', 'Image', 0, 360, update_image)
cv2.createTrackbar('Zoom', 'Image', 0, 100, update_image)
cv2.createTrackbar('Vertical Line 1', 'Image', width // 3, width, update_image)
cv2.createTrackbar('Vertical Line 2', 'Image', 2 * width // 3, width, update_image)
cv2.createTrackbar('Horizontal Line 1', 'Image', height // 3, height, update_image)
cv2.createTrackbar('Horizontal Line 2', 'Image', 2 * height // 3, height, update_image)

# Initial display
update_image(0)

# Wait until user exits
cv2.waitKey(0)
cv2.destroyAllWindows()
