from PIL import Image

# Create a new blank image with size 690x420 and fill it with a specified color
image = Image.new('RGBA', (690, 420), (52, 146, 235, 123))

# Set specific pixels with desired colors
image.putpixel((412, 309), (52, 146, 235, 123))
image.putpixel((12, 209), (42, 16, 125, 231))
image.putpixel((264, 143), (122, 136, 25, 213))

# Save the image to a file
image.save('output_image.png')

# Close the image
image.close()
# ictf{7ruly_th3_n3x7_p1c4ss0_753433}