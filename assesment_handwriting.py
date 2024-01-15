import pytesseract
from PIL import Image
import Levenshtein

def calculate_cer(hypothesis, reference):
    return Levenshtein.distance(reference, hypothesis) / len(reference)

def perform_ocr(image_path):
    # Perform OCR on the image
    text = pytesseract.image_to_string(Image.open(image_path), lang='eng')

    # Get ground truth (you need to provide the actual text for comparison)
    reference_text = "Ground truth text"

    # Calculate Character Error Rate (CER)
    cer = calculate_cer(text, reference_text)

    # Get word recognition accuracy
    reference_words = reference_text.split()
    recognized_words = text.split()
    correct_words = [w for w in recognized_words if w in reference_words]
    word_accuracy = len(correct_words) / len(reference_words)

    # Get word confidence levels
    word_confidences = pytesseract.image_to_data(Image.open(image_path), lang='eng', output_type=pytesseract.Output.DICT)['conf']

    # Print results
    print("OCR Output:")
    print(text)
    print("\nGround Truth:")
    print(reference_text)
    print("\nCharacter Error Rate (CER): {:.2%}".format(cer))
    print("Word Recognition Accuracy: {:.2%}".format(word_accuracy))
    print("\nWord Confidence Levels:")
    for word, confidence in zip(recognized_words, word_confidences):
        print("{}: {:.2%}".format(word, confidence / 100.0))

if __name__ == "__main__":
    image_path = "screenshot.png" 
    perform_ocr(image_path)
