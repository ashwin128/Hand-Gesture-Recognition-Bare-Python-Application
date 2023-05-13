import cv2
import os

def create_folder_if_not_exists(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

def main():
    cap = cv2.VideoCapture(0)
    cv2.namedWindow("Capture")
    number = -1

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        cv2.putText(frame, "Enter any number between 0-9", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Capture", frame)

        key = cv2.waitKey(1) & 0xFF
        if key >= ord('0') and key <= ord('9'):
            number = key - ord('0')
            break
        # Exit if the 'q' key is pressed
        elif key == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

    if number >= 0:
        folder_name = os.path.join("data2", str(number))
        create_folder_if_not_exists(folder_name)
        for i in range(100):
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            if not ret:
                break
            file_name = os.path.join(folder_name, f"{i}.png")
            cv2.imwrite(file_name, frame)
            cap.release()

if __name__ == '__main__':
    main()
