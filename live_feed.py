import cv2
import numpy as np
import pygame

# Initialize Pygame
pygame.init()

# Initialize webcam capture
cap = cv2.VideoCapture(0)

# Desired frame size (you can adjust these values if needed)
desired_width = 320
desired_height = 240

# Set up display
window_width = desired_width * 2
window_height = desired_height * 2
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("HSV Thresholding")

# Define HSV thresholds
thresholds = [
    {'hue_min': 0, 'hue_max': 180, 'sat_min': 70, 'sat_max': 255, 'val_min': 5, 'val_max': 255},
    {'hue_min': 0, 'hue_max': 180, 'sat_min': 40, 'sat_max': 255, 'val_min': 75, 'val_max': 255},
    {'hue_min': 0, 'hue_max': 180, 'sat_min': 75, 'sat_max': 255, 'val_min': 0, 'val_max': 255},
]

# Function to apply HSV threshold and process the image
def apply_threshold(frame, hsv_threshold):
    # Convert the frame to HSV
    hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    lower_hsv = np.array([hsv_threshold['hue_min'], hsv_threshold['sat_min'], hsv_threshold['val_min']])
    upper_hsv = np.array([hsv_threshold['hue_max'], hsv_threshold['sat_max'], hsv_threshold['val_max']])
    
    # Apply threshold to isolate colors in the range
    mask = cv2.inRange(hsv_image, lower_hsv, upper_hsv)
    
    # Apply the mask to the image
    result = cv2.bitwise_and(frame, frame, mask=mask)
    
    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Draw contours and area
    for cnt in contours:
        # Draw the contour on the result
        cv2.drawContours(result, [cnt], -1, (0, 255, 0), 2)
        # Calculate and put the area text
        area = cv2.contourArea(cnt)
        x, y, w, h = cv2.boundingRect(cnt)
        if area > 5000:
            cv2.putText(result, f"Area: {int(area)}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
            # Draw bounding box
            cv2.rectangle(result, (x, y), (x + w, y + h), (255, 0, 0), 2)
    return result

clock = pygame.time.Clock()

# Main loop
running = True
while running:
    # Read a frame from the webcam
    ret, frame = cap.read()
    if not ret:
        print("Failed to read from webcam.")
        break

    # Flip the frame horizontally if needed
    frame = cv2.flip(frame, 1)
    
    # Resize the frame to the desired size
    frame_resized = cv2.resize(frame, (desired_width, desired_height))
    
    # Apply the three thresholds
    processed_images = []
    for hsv_threshold in thresholds:
        processed_image = apply_threshold(frame_resized, hsv_threshold)
        processed_images.append(processed_image)
    
    # Create Pygame surfaces from the images
    # Convert the images to RGB format and transpose axes to match Pygame's coordinate system
    frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
    frame_surface = pygame.surfarray.make_surface(frame_rgb.transpose((1, 0, 2)))

    processed_surfaces = []
    for img in processed_images:
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_surface = pygame.surfarray.make_surface(img_rgb.transpose((1, 0, 2)))
        processed_surfaces.append(img_surface)
    
    # Display the images in a 2x2 grid
    window.blit(frame_surface, (0, 0))
    window.blit(processed_surfaces[0], (desired_width, 0))
    window.blit(processed_surfaces[1], (0, desired_height))
    window.blit(processed_surfaces[2], (desired_width, desired_height))
    
    pygame.display.flip()
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Limit frame rate
    clock.tick(30)

# Release resources
cap.release()
pygame.quit()