from PIL import Image

text = ""

with Image.open("./dripping.png") as image:
    for x in range(image.width):
        # Loop through all the pixels in the column, starting at the bottom
        for y in range(image.height):
            # If this pixel is white, this means can take the ascii value of the number of yellow pixels in the column
            if image.getpixel((x, y)) == (255, 255, 255):
                text += chr(y)
                break

print(text)
