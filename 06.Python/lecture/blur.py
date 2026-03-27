from PIL import Image, ImageFilter

before = Image.open("NCM.jpg")
after = before.filter(ImageFilter.BoxBlur(1))

after.save("blurred_NCM.jpg")
