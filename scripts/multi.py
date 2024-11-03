import cv2
import numpy as np
import pygame
import os

# Folder containing the images
image_folder = "cyclic_dataset"

# Get the list of images in the folder
image_files = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
image_index = 0  # To keep track of the current image

# Load the first image
frame = cv2.imread(os.path.join(image_folder, image_files[image_index]))
framea = frame[:, 0:500]

# Convert the image to HSV
hsv_image = cv2.cvtColor(framea, cv2.COLOR_BGR2HSV)

# Initialize Pygame
pygame.init()

# Set up display
window_width, window_height = framea.shape[1], framea.shape[0]
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("HSV Threshold Adjuster")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Button dimensions
button_width, button_height = 50, 30

# Initial HSV threshold values
hue_min = 0
hue_max = 180
sat_min = 0
sat_max = 255
val_min = 0
val_max = 255

# Variables to count accepted and rejected frames
accepted_count = 0
rejected_count = 0
prediction_result = ""

# Function to draw buttons
def draw_buttons():
    pygame.draw.rect(window, RED, (10, 10, button_width, button_height))  # Decrease min hue
    pygame.draw.rect(window, GREEN, (70, 10, button_width, button_height))  # Increase min hue
    pygame.draw.rect(window, RED, (150, 10, button_width, button_height))  # Decrease max hue
    pygame.draw.rect(window, GREEN, (210, 10, button_width, button_height))  # Increase max hue

    pygame.draw.rect(window, RED, (10, 50, button_width, button_height))  # Decrease min saturation
    pygame.draw.rect(window, GREEN, (70, 50, button_width, button_height))  # Increase min saturation
    pygame.draw.rect(window, RED, (150, 50, button_width, button_height))  # Decrease max saturation
    pygame.draw.rect(window, GREEN, (210, 50, button_width, button_height))  # Increase max saturation

    pygame.draw.rect(window, RED, (10, 90, button_width, button_height))  # Decrease min value
    pygame.draw.rect(window, GREEN, (70, 90, button_width, button_height))  # Increase min value
    pygame.draw.rect(window, RED, (150, 90, button_width, button_height))  # Decrease max value
    pygame.draw.rect(window, GREEN, (210, 90, button_width, button_height))  # Increase max value

    # Next button to cycle through images
    pygame.draw.rect(window, GREEN, (window_width - 60, 10, 50, 30))  # Next button
    font = pygame.font.SysFont(None, 24)
    window.blit(font.render('Next', True, BLACK), (window_width - 55, 15))

    # Predict button to check the contour
    pygame.draw.rect(window, GREEN, (window_width - 60, 50, 50, 30))  # Predict button
    window.blit(font.render('Predict', True, BLACK), (window_width - 60, 55))

    # Display the accepted and rejected counts
    window.blit(font.render(f"Accepted: {accepted_count}", True, BLACK), (10, window_height - 40))
    window.blit(font.render(f"Rejected: {rejected_count}", True, BLACK), (200, window_height - 40))

    # Display the prediction result (Accepted/Rejected)
    window.blit(font.render(f"Result: {prediction_result}", True, BLACK), (10, window_height - 80))

# Function to apply HSV threshold and convert the image to a Pygame surface
# Shows only the largest contour based on area
def apply_threshold():
    lower_hsv = np.array([hue_min, sat_min, val_min])
    upper_hsv = np.array([hue_max, sat_max, val_max])

    # Apply threshold to isolate colors in the range
    mask = cv2.inRange(hsv_image, lower_hsv, upper_hsv)

    # Apply the mask to the image
    result = framea.copy()  # Display the bounding box on the original image (framea)

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    largest_contour = None
    largest_area = 0

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
    surface = pygame.surfarray.make_surface(result.transpose((1, 0, 2)))
    return surface, largest_area

# Function to load the next image
def load_next_image():
    global image_index, frame, framea, hsv_image
    image_index = (image_index + 1) % len(image_files)  # Cycle through images
    frame = cv2.imread(os.path.join(image_folder, image_files[image_index]))
    framea = frame[:, 0:500]
    hsv_image = cv2.cvtColor(framea, cv2.COLOR_BGR2HSV)  # Convert the new image to HSV

# Function to predict and evaluate the largest contour
def predict(largest_area):
    global accepted_count, rejected_count, prediction_result
    if largest_area > 2000:
        prediction_result = "Accepted"
        accepted_count += 1
    else:
        prediction_result = "Rejected"
        rejected_count += 1

# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            # Next button click detection
            if window_width - 60 <= mouse_x <= window_width - 10 and 10 <= mouse_y <= 40:
                load_next_image()

            # Predict button click detection
            if window_width - 60 <= mouse_x <= window_width - 10 and 50 <= mouse_y <= 80:
                _, largest_area = apply_threshold()
                predict(largest_area)

            # Decrease min hue button
            if 10 <= mouse_x <= 10 + button_width and 10 <= mouse_y <= 10 + button_height:
                hue_min = max(0, hue_min - 5)
                print(f"Updated hue_min: {hue_min}")

            # Increase min hue button
            elif 70 <= mouse_x <= 70 + button_width and 10 <= mouse_y <= 10 + button_height:
                hue_min = min(180, hue_min + 5)
                print(f"Updated hue_min: {hue_min}")

            # Decrease max hue button
            elif 150 <= mouse_x <= 150 + button_width and 10 <= mouse_y <= 10 + button_height:
                hue_max = max(0, hue_max - 5)
                print(f"Updated hue_max: {hue_max}")

            # Increase max hue button
            elif 210 <= mouse_x <= 210 + button_width and 10 <= mouse_y <= 10 + button_height:
                hue_max = min(180, hue_max + 5)
                print(f"Updated hue_max: {hue_max}")

            # Decrease min saturation button
            elif 10 <= mouse_x <= 10 + button_width and 50 <= mouse_y <= 50 + button_height:
                sat_min = max(0, sat_min - 5)
                print(f"Updated sat_min: {sat_min}")
                        # Increase min saturation button
            elif 70 <= mouse_x <= 70 + button_width and 50 <= mouse_y <= 50 + button_height:
                sat_min = min(255, sat_min + 5)
                print(f"Updated sat_min: {sat_min}")

            # Decrease max saturation button
            elif 150 <= mouse_x <= 150 + button_width and 50 <= mouse_y <= 50 + button_height:
                sat_max = max(0, sat_max - 5)
                print(f"Updated sat_max: {sat_max}")

            # Increase max saturation button
            elif 210 <= mouse_x <= 210 + button_width and 50 <= mouse_y <= 50 + button_height:
                sat_max = min(255, sat_max + 5)
                print(f"Updated sat_max: {sat_max}")

            # Decrease min value button
            elif 10 <= mouse_x <= 10 + button_width and 90 <= mouse_y <= 90 + button_height:
                val_min = max(0, val_min - 5)
                print(f"Updated val_min: {val_min}")

            # Increase min value button
            elif 70 <= mouse_x <= 70 + button_width and 90 <= mouse_y <= 90 + button_height:
                val_min = min(255, val_min + 5)
                print(f"Updated val_min: {val_min}")

            # Decrease max value button
            elif 150 <= mouse_x <= 150 + button_width and 90 <= mouse_y <= 90 + button_height:
                val_max = max(0, val_max - 5)
                print(f"Updated val_max: {val_max}")

            # Increase max value button
            elif 210 <= mouse_x <= 210 + button_width and 90 <= mouse_y <= 90 + button_height:
                val_max = min(255, val_max + 5)
                print(f"Updated val_max: {val_max}")

    # Update the display
    window.fill(WHITE)
    draw_buttons()
    threshold_surface, _ = apply_threshold()
    window.blit(threshold_surface, (0, 130))  # Adjusted height for buttons
    pygame.display.flip()

# Quit Pygame
pygame.quit()