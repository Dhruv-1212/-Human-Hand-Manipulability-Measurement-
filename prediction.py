import cv2
import numpy as np
from tensorflow.keras.models import load_model

class prediction:
    def __init__(self, model_path='model_handwritting.h5'):
        # Load the pre-trained model
        self.model = load_model(model_path)

        self.word_dict = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'K', 11: 'L', 12: 'M',
                          13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S', 19: 'T', 20: 'U', 21: 'V', 22: 'W', 23: 'X', 24: 'Y', 25: 'Z'}

    def perform_character_recognition(self):
        # Import and make copy
        img = cv2.imread("screenshot.png")
        imgc = img

        # Resize for window and change color space
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (400, 440))

        # Grayscale image
        img_gray = cv2.cvtColor(imgc, cv2.COLOR_BGR2GRAY)
        _, img_thresh = cv2.threshold(img_gray, 100, 255, cv2.THRESH_BINARY_INV)

        # Final resize and reshape
        img_final = cv2.resize(img_thresh, (28, 28))
        img_final = np.reshape(img_final, (1, 28, 28, 1))

        # Get prediction of the image
        img_pred = self.word_dict[np.argmax(self.model.predict(img_final))]

        # Add text and display
        cv2.putText(img, "  English character recognition", (20, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color=(0, 0, 0))
        cv2.putText(img, "  Prediction: " + img_pred, (20, 410), cv2.FONT_HERSHEY_DUPLEX, 1.3, color=(255, 0, 0))
        cv2.imshow('CharCNN', img)

        prediction_probabilities = self.model.predict(img_final)
        predicted_class_index = np.argmax(prediction_probabilities)
        predicted_character = self.word_dict[predicted_class_index]
        confidence = prediction_probabilities[0][predicted_class_index]

        return confidence

       

