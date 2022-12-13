import cv2
from PIL import Image
from numpy import asarray
from algorithms import train_random_forest, classify_image_RF, classify_image_svm, train_svm
import time
import pickle
import os

def png_to_array(path):
    png = Image.open(path)
    png_array = asarray(png)

    return png_array

def run_camera():
    # Open the camera
    clf = pickle.load(open('HandsignInterpreter/finalized_model_RF.sav', 'rb'))
    svm = pickle.load(open('HandsignInterpreter/finalized_model_svm.sav', 'rb'))
    #result = loaded_model.score(X_test, Y_test)
    cap = cv2.VideoCapture(1)

    # Set the camera resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    info = """Press space to read a new letter,"""
    info2 = """c to clear text_RF, q to quit"""
    text_RF = ""
    text_svm = ""

    # Loop until the user hits the 'q' key
    while True:
        # Read a frame from the camera
        ret, frame = cap.read()

        # Check if the frame was successfully read
        if not ret:
            break

        # Wait for the user to hit a key
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

        if key == ord('c'):
            text_RF = ""
            text_svm = ""

        # If the user pressed 'L', put some text_RF on the frame
        if key == ord(' '):
            box = frame[80:276, 50:246]
            # resize the image to 28x28
            box = cv2.resize(box, (28, 28))
            # convert to grayscale
            box = cv2.cvtColor(box, cv2.COLOR_BGR2GRAY)
            # invert the colors
            #box = 255 - box
            cv2.imwrite("HandsignInterpreter/hand.png", box)

            #turn it to 1 long array
            box = box.reshape(1, 784)
            print(box)
            # save the image
            new_letter_RF = classify_image_RF(box, clf)
            new_letter_svm = classify_image_svm(box, svm)
            text_RF += new_letter_RF
            text_svm += new_letter_svm
            print("Found letter RF",new_letter_RF)
            print("Found letter svm",new_letter_svm)

        cv2.putText(frame, info, (20, 460), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (100, 200, 100), 2)
        cv2.putText(frame, info2, (20, 440), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (100, 200, 100), 2)
        cv2.putText(frame, text_RF, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 0, 0), 2)
        cv2.putText(frame, text_svm, (70, 80), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 0, 0), 2)
        cv2.rectangle(frame, (50, 80), (246, 276), (0, 255, 0), 2)


        # Show the frame
        cv2.imshow("Camera", frame)

    # Release the camera and destroy all windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    #png_to_array('HandsignInterpreter/test.png')
    print("Training random forest")
    if 'finalized_model_RF.sav' in os.listdir('HandsignInterpreter'):
        print("Model already trained")
    else:
        training_time = time.time()
        train_random_forest()
        print("Training took", time.time() - training_time, "seconds")
    if 'finalized_model_svm.sav' in os.listdir('HandsignInterpreter'):
        print("Model already trained")
    else:
        training_time = time.time()
        train_svm()
        print("Training took", time.time() - training_time, "seconds")

    print("Starting camera")
    run_camera()
    print("Done")

    # TODO
    # get the 28x28 image from the camera
    # make the image black and white
    # classify the image
