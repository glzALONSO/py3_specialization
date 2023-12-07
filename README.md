# py3_specialization

## Solutions to the py3 specialization projects

This repo contains solutions to the course projects of the Python 3 Programming Specialization offered by the University of Michigan in Coursera. The code is in a GitHub repo to make it accesible to everyone. However, if you are a student of the specialization I highly encourage you to avoid plaigarism.

The solutions to the final course are particularly visual and displaying them here would provide some notion of the work carried out through the specialization.

The final course introduces the Python libraries pillow, pytesseract and opencv.

# First assignment

The first assignment introduces the Python the pillow library and consists in manipulating the intensity of the RGB channels of a sample image and create a contact sheet of the results.

## Results:

![assignment_1_resutls](/Course_5_project/assignment_1_result.png)

# Final assignment

The final assignmet combines the pillow, pytesseract and opencv libraries to extract the text and faces contained in an image to perform a simple keyword search that returns the faces found in the image when a match for the keyword is found in the extracted text. The [WorkImage file](/Course_5_project/WorkImage.py) file contains the solution to the assignment.

## Face detection

Face detection is performed using the opencv library and the Haar Cascade classifier algorithm. The following code provides the result of the face detection step:

```python  
            with Image.open(my_img) as pil_img:
                work_image = WorkImage(pil_img, file)
                detection = work_image.faceDetectionAndDisplay(draw_b_boxes=1)
                detection.show()
```
### Results:

![assignment_1_resutls](/Course_5_project/face_detection_result.png)

## Optical Character Recognition (OCR)

Text is extracted from the images using the tesseract OCR engine along with its Python wrapper pytesseract. The following code provides the result of the OCR step:

```python  
with Image.open(my_img) as pil_img:
    work_image = WorkImage(pil_img, file)
    contact_sheet = work_image.search_keyword("Christopher")
    
    if contact_sheet == None:
        pass
    else:
        display(contact_sheet)
```
## Keyword search

```python  
with Image.open(my_img) as pil_img:
    work_image = WorkImage(pil_img, file)
    contact_sheet = work_image.search_keyword("Christopher")
    
    if contact_sheet == None:
        pass
    else:
        display(contact_sheet)
```
