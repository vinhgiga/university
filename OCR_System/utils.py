import cv2
import numpy as np
import pytesseract

def read_image(file_path):
    return cv2.imread(file_path)


def detect_text(cvImage, tesseract_path = None) -> str:
    default_tesseract_path = "C:/Program Files/Tesseract-OCR/tesseract.exe"
    if tesseract_path is None:
        pytesseract.pytesseract.tesseract_cmd = default_tesseract_path
    else:
        pytesseract.pytesseract.tesseract_cmd = tesseract_path
    # Vietnamese language
    config = '-l vie'
    text = pytesseract.image_to_string(cvImage, config=config)
    return text


def isgray(cvImage):
    return len(cvImage.shape) < 3


def convert_to_rgb(cvImage):
    if isgray(cvImage):
        return cvImage
    else:
        return cv2.cvtColor(cvImage, cv2.COLOR_BGR2RGB)


def grayscale(cvImage):
    if isgray(cvImage):
        return cvImage
    else:
        return cv2.cvtColor(cvImage, cv2.COLOR_BGR2GRAY)


def convert_to_binary(cvImage):
    # convert image to grayscale
    if not isgray(cvImage):
        img = grayscale(cvImage)
    else:
        img = cvImage
    
    # adaptive thresholding
    return cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)


def denoise(cvImage):
    # grayscale or color image
    if isgray(cvImage):
        return cv2.fastNlMeansDenoising(cvImage, h=10)
    else:
        return cv2.fastNlMeansDenoisingColored(cvImage, None, 10, 10, 7, 15)


def rotate(image, angle):
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)


def find_score(arr, angle):
    data = rotate(arr, angle)
    hist = np.sum(data, axis=1)
    score = np.sum((hist[1:] - hist[:-1]) ** 2)
    return hist, score


def deskew(cvImage):
    img = convert_to_binary(cvImage)
    delta = 0.5
    limit = 5
    angles = np.arange(-limit, limit+delta, delta)
    scores = []
    for angle in angles:
        hist, score = find_score(img, angle)
        scores.append(score)
    best_score = max(scores)
    best_angle = angles[scores.index(best_score)]
    # correct skew
    return rotate(cvImage, best_angle)