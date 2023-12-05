# py3_specialization
Solutions to the py3 specialization projects

This repo contains solutions to the course projects of the Python 3 Programming Specialization offered by the University of Michigan in Coursera. The code is in a GitHub repo to make it accesible to everyone. However, if you are a student of the specialization I highly encourage you to avoid plaigarism.

The solutions to the final course are particularly visual and displaying them here would provide some notion of the work carried out through the specialization.

The final course introduces the Python libraries pillow, pytesseract and opencv.

The first assignment introduces the Python the pillow library and consists in manipulating the intensity of the RGB channels of a sample image and create a contact sheet of the results.

Results:

!(/Course_5_project/assignment_1_result.png)

The final assignmet combines the pillow, pytesseract and opencv libraries to extract the text and faces contained in an image to perform a simple keyword search that returns the faces found in the image when a match for the keyword is found in the extracted text.

```python
  
with Image.open(my_img) as pil_img:
    work_image = WorkImage(pil_img, file)
    contact_sheet = work_image.search_keyword("Christopher")
    
    if contact_sheet == None:
        pass
    else:
        display(contact_sheet)
```
