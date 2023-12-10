from PIL import Image
import pytesseract
import cv2 as cv
import numpy as np


class WorkImage:
    # loading the face detection classifier as a class attribute
    face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')

    # define the instance attributes
    def __init__(self, pil_img, file_name):
        self.pil_img = pil_img
        self.bounding_boxes = list()
        self.text = ''
        self.scaleFactor = 1.15
        self.minNeighbors = 7
        self.minSize = (30, 30)
        self.maxSize = (300, 300)
        self.file_name = file_name

    def faceDetectionAndDisplay(self, draw_b_boxes=0,
                                face_cascade=face_cascade):  # detection should be improved as it is detecting other things
        # convert the PIL image into a numpy array in order to work with opencv
        # print(pil_image)
        img_array = np.asarray(self.pil_img)
        # print(type(img_array))

        # transform the numpy RGB array into a numpy GRAY array
        img_gray = cv.cvtColor(img_array, cv.COLOR_RGB2GRAY)

        # make the white background black to improve the detection
        # img_gray[img_gray == 255] = 0

        # although I am not sure what it does, this operation improves the detection
        img_gray = cv.equalizeHist(img_gray)

        # detect the faces in the image by calling the Haar cascade classifier, set the instance attribute bounding_boxes
        self.bounding_boxes = face_cascade.detectMultiScale(img_gray,
                                                            scaleFactor=self.scaleFactor,
                                                            minNeighbors=self.minNeighbors,
                                                            minSize=self.minSize,
                                                            maxSize=self.maxSize)

        if draw_b_boxes == 1:
            # draw bounding boxes
            for (x, y, w, h) in self.bounding_boxes:
                start_point = (x, y)  # top left
                end_point = (x + w, y + h)
                color = (255, 0, 255)
                thickness = 4
                img_array = cv.rectangle(img_array, start_point, end_point, color, thickness)

            detection = Image.fromarray(img_array)
            print(detection.mode)
            return detection

    def buildContactSheet(self):
        detected_faces = list()
        thumbnail_size = (128, 128)  ##(w,h)

        for (x, y, w, h) in self.bounding_boxes:
            # create a cropping box as a (left, upper, right, lower)-tuple.
            box = (x, y, x + w, y + h)

            face_crop = self.pil_img.crop(box)

            if face_crop.width < thumbnail_size[0] or face_crop.height < thumbnail_size[1]:
                face_crop = face_crop.resize((128, 128))

            else:
                face_crop.thumbnail(thumbnail_size)

            detected_faces.append(face_crop)

        # define in initial x, y, cols and row_count values
        x = 0
        y = 0
        cols = 5
        row_count = 1

        # create a a base contact sheet
        contact_sheet = Image.new(self.pil_img.mode, (128 * cols, 128))  # (w, h)

        for detected_face in detected_faces:

            #  check x limit. if there is no more space in the row, add another one
            if x == contact_sheet.width:
                # update row_count value
                row_count += 1
                # create an empty contact sheet with space for another image
                extended_contact_sheet = Image.new(self.pil_img.mode, (128 * cols, 128 * row_count))
                # paste the old contact sheet into the empty-extended
                extended_contact_sheet.paste(contact_sheet)
                # assign the extended contact sheet as the current one
                contact_sheet = extended_contact_sheet
                # jump to the new row (x, y) position
                x = 0
                y += detected_face.height

            # paste current face in the contact sheet
            contact_sheet.paste(detected_face, (x, y))
            # update x and row_count values
            x += detected_face.width

            # resize and display the contact sheet
            # contact_sheet = contact_sheet.resize((int(contact_sheet.width / 2), int(contact_sheet.height / 2)))
        return contact_sheet

    def extract_text(self, draw_b_boxes=0):
        # load the pil_img
        img_array = np.asarray(self.pil_img)

        # convert to gray scale
        img_gray = cv.cvtColor(img_array, cv.COLOR_RGB2GRAY)

        # binarize the image with otsu thresholding and gaussian blur
        img_blur = cv.GaussianBlur(img_gray, (5, 5), 0)
        threshold = cv.threshold(img_blur, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)[1]

        # store the string in the text instance attribute
        self.text = pytesseract.image_to_string(threshold)

        if draw_b_boxes == 1:
            # get the bounding boxes
            boxes = pytesseract.image_to_boxes(threshold, output_type=pytesseract.Output.DICT)

            #draw the boxes one character at a time
            for char in enumerate(boxes['char']):
                #extract the bounding_boxes dimensions
                (x, y, w, h) = (boxes['left'][char[0]],
                                boxes['top'][char[0]],
                                boxes['right'][char[0]],
                                boxes['bottom'][char[0]])

                start_point = (x, y)  # top left
                end_point = (x + w, y + h)
                #image in RGBA Mode
                color = (0, 255, 0)
                thickness = 2
                # draw the bounding boxes
                img_array = cv.rectangle(img_array, start_point, end_point, color, thickness)

            detection = Image.fromarray(img_array)

            return detection


    def search_keyword(self, keyword):

        self.extract_text()

        if keyword in self.text:
            print("Results for {} found in {}".format(keyword, self.file_name))
            self.faceDetectionAndDisplay()

            if len(self.bounding_boxes) == 0:
                print("But no faces in that file")
                return None

            else:
                contact_sheet = self.buildContactSheet()
                return contact_sheet

        else:
            print("No match for {} in {}".format(keyword, self.file_name))
            return None

