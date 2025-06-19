import cv2
import mediapipe as mp
import pyautogui

# Initialize variables for hand landmark detection
x1 = x2 = y1 = y2 = 0

# Create a webcam capture object
webcam = cv2.VideoCapture(0)

# Create a MediaPipe Hands object for hand landmark detection
my_hands = mp.solutions.hands.Hands()

# Create drawing utilities object for visualizing landmarks
drawing_utils = mp.solutions.drawing_utils

while True:
    # Capture a frame from the webcam
    _ , image = webcam.read()

    # Flip the image horizontally (optional, depending on your camera setup)
    image = cv2.flip(image,1)

    # Get frame dimensions for landmark normalization
    frame_height, frame_width, _ = image.shape()

    # Convert the image to RGB format, required by MediaPipe
    rgb_image = cv2cvtColor(image,cv2.COLOR_BGR2RGB)

    # Process the frame with MediaPipe
    output = my_hands.process(rgb_image)

    # Extract detected hands, if any
    hands = output.multi_hand_landmarks

    # Draw landmarks on the image if hands were detected
    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(image,hand)

            # Get landmarks for index finger and finger
            landmarks = hand.landmarks
            for id, landmark in enumerate(landmarks):

                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)

                # Normalize landmark coordinates to image dimensions
                if id == 8:
                    cv2.circle(img=image,center=(x,y),radius=8,color=(0,255,255),thickness=3)
                    x1 = x
                    y1 = y
                if id == 4:
                    cv2.circle(img=image,center=(x,y),radius=8,color=(0,0,255),thickness=3)
                    x2 = x
                    y2 = y

        # Calculate the distance between the fingertips
        dist = ((x2-x1)**2 + (y2-y1)**2)**(0.5)//4

        # Draw a line connecting the fingertips
        cv2.line(image,(x1,y1),(x2,y2),(0,255,0),5)

        # Control volume based on distance (adjust threshold as needed)
        if dist > 50 :
            pyautogui.press("volumeup")
        else :
            pyautogui.press("volumedown")

    # Display the frame with hand landmarks and volume control feedback
    cv2.imshow("Hand volume control using python", image)

    # Exit on pressing Esc key
    key = cv2.waitKey(10)
    if key == 27:
        break

# Release resources
webcam.release()
cv2.destroyAllWindows()

#Aman Maheshwari