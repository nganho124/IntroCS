from PIL import Image, ImageFilter

before = Image.open("NCM.jpg")
after = before.filter(ImageFilter.FIND_EDGES)

after.save("edged_NCM.jpg")
