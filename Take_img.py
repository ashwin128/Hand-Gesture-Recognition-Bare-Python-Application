import os
import cv2

DATA_DIR = './Data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

number_of_classes = 10
dataset_size = 300

cap = cv2.VideoCapture(0)

class_dir = 0
while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2.putText(frame, "Press any number keys between 0-9.", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 1)
    cv2.imshow('frame', frame)

    key = cv2.waitKey(1) & 0xFF
    if key >= ord('0') and key <= ord(str(number_of_classes - 1)):
        class_num = key - ord('0')
        class_dir = os.path.join(DATA_DIR, str(class_num))
        if not os.path.exists(class_dir):
            os.makedirs(class_dir)
        print('Collecting data for class {}'.format(class_num))
        break

    if key == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        exit()

counter = 0
while counter < dataset_size:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2.imshow('frame', frame)
    cv2.waitKey(25)
    
    img_path = os.path.join(class_dir, '{}.jpg'.format(counter))
    if os.path.exists(img_path):
        img = cv2.imread(img_path)
    cv2.imwrite(img_path, frame)

    counter += 1

    key = cv2.waitKey(1) & 0xFF
    if key >= ord('0') and key <= ord(str(number_of_classes - 1)):
        new_class_num = key - ord('0')
        if new_class_num != class_num:
            class_num = new_class_num
            class_dir = os.path.join(DATA_DIR, str(class_num))
            if not os.path.exists(class_dir):
                os.makedirs(class_dir)
            print('Collecting data for class {}'.format(class_num))
            counter = 0
    elif key == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        exit()

cap.release()
cv2.destroyAllWindows()
