import cv2
import mediapipe as mp
import numpy as np
from keras.models import load_model
import csv

# Load the trained model
model = load_model('hand_gesture_model.h5')

# Read the labels 
labels = []

with open('Data/labels.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        labels.append(row)

# Set up Mediapipe
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Set up video capture
cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()
    
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    # Convert the frame to RGB and pass it through Mediapipe
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    with mp_hands.Hands(static_image_mode=False, max_num_hands=1) as hands:
        results = hands.process(frame)

    # Draw landmarks and lines on the hand
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get the coordinates of the hand landmarks
            coords = []
            for landmark in hand_landmarks.landmark:
                coords.append(landmark.x)
                coords.append(landmark.y)

            # Preprocess the coordinates and make a prediction using the trained model
            coords = np.array(coords).reshape(1, -1) / 255.0
            prediction = model.predict(coords, verbose=0)

            # Get the predicted label and display it on the screen
            label = np.argmax(prediction)
            text = str(labels[label]).strip("[]''")
            cv2.putText(frame, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Show the resulting frame
    cv2.imshow('Hand Gesture Recognition', frame)

    # Exit the program when 'q' is pressed
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Clean up
cap.release()
cv2.destroyAllWindows()
