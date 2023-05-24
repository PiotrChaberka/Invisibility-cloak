import cv2
import numpy as np
import os
import platform

# Get the absolute path of the image file
script_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_dir, 'pink.jpeg')

# Load the image of pink
pink_image = cv2.imread(image_path)

# Check if pink_image is None (failed to load the image)
if pink_image is None:
    raise ValueError("Failed to load the pink image. Please make sure 'pink.png' exists in the same directory.")

# Define the lower and upper bounds for pink color in HSV color space
lower_pink = np.array([140, 50, 50])
upper_pink = np.array([170, 255, 255])

# Start capturing the video
cap = cv2.VideoCapture(0)

# Read the frame from the video capture to get dimensions
ret, frame = cap.read()
if not ret:
    raise ValueError("Failed to read video feed")

# Resize the pink image to match the frame dimensions
pink_image = cv2.resize(pink_image, (frame.shape[1], frame.shape[0]))

# Resize the window using platform-specific command
if platform.system() == 'Windows':
    os.system("powershell -Command (New-Object -ComObject Shell.Application).ToggleDesktopIcons('Desktop',0)")
    cv2.setWindowProperty("Processed Frame", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
else:
    cv2.namedWindow("Processed Frame", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("Processed Frame", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:
    # Read the frame from the video capture
    ret, frame = cap.read()

    if ret:
        # Convert the frame to the HSV color space
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Create a mask to identify pink pixels
        pink_mask = cv2.inRange(hsv_frame, lower_pink, upper_pink)

        # Bitwise-AND the original frame with the inverse of the pink mask
        processed_frame = cv2.bitwise_and(frame, frame, mask=cv2.bitwise_not(pink_mask))

        # Replace pink pixels with the corresponding pixels from the pink image
        processed_frame[pink_mask != 0] = pink_image[pink_mask != 0]

        # Display the processed frame
        cv2.imshow('Processed Frame', processed_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release the video capture and close the window
cap.release()
cv2.destroyAllWindows()

