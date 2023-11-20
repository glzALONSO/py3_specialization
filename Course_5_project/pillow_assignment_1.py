import PIL
from PIL import Image, ImageDraw, ImageFont

# read image and convert to RGB
original = Image.open("readonly/msi_recruitment.gif")
original = image.convert('RGB')

# define the font to draw the text

fnt = ImageFont.truetype("readonly/fanwood-webfont.ttf", 75)

# split the image into RGB bands
original_channels = image.split()

# define the channels and intesities tuples to iterate over
channels = (0, 1, 2)
intensities = (0.1, 0.5, 0.9)

# create an empty list to contain the processed images.

processed_images = list()

for channel in channels:
    for intensity in intensities:
        # define a blank canvas
        canvas = Image.new(original.mode, (original.width, original.height + 75))

        # define a drawing context
        d_context = ImageDraw.Draw(canvas, original.mode)

        # draw full opacity
        d_context.text((10, original.height),
                       "channel {} intensity {}".format(channel, intensity),
                       font=fnt,
                       fill=(255, 255, 255, 255))

        # split the blank canvas into RGB
        canvas_channels = canvas.split()

        # process the original image channel
        processed_channel = original_channels[channel].point(lambda px: px * intensity)

        # paste the process channel into the blank canvas
        canvas_channels[channel].paste(processed_channel)

        # paste the unprocessed channels into the blank canvas
        if channel == 0:
            canvas_channels[1].paste(original_channels[1])
            canvas_channels[2].paste(original_channels[2])

        elif channel == 1:
            canvas_channels[0].paste(original_channels[0])
            canvas_channels[2].paste(original_channels[2])

        else:
            canvas_channels[0].paste(original_channels[0])
            canvas_channels[1].paste(original_channels[1])

        # merge the canvas channels to generate a new image.
        processed_image = Image.merge(original.mode, canvas_channels)
        processed_images.append(processed_image)

# create a contact sheet of different intensities

contact_sheet = Image.new(original.mode, (original.width * 3, (original.height + 75) * 3))

x = 0
y = 0

for processed_image in processed_images:
    # Lets paste the current image into the contact sheet
    contact_sheet.paste(processed_image, (x, y))
    # Now we update our X position. If it is going to be the width of the image, then we set it to 0
    # and update Y as well to point to the next "line" of the contact sheet.
    if x + original.width == contact_sheet.width:
        x = 0
        y = y + (original.height + 75)
    else:
        x = x + original.width

# resize and display the contact sheet
contact_sheet = contact_sheet.resize((int(contact_sheet.width / 2), int(contact_sheet.height / 2)))
display(contact_sheet)