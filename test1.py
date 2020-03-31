import io

from PIL import Image

with open("test.png", "rb") as file:
    data = file.read()
    dataEnc = io.BytesIO(data)
    img: Image.Image = Image.open(dataEnc)
    img.show()

with open("test.jpg", "rb") as file:
    data = file.read()
    dataEnc = io.BytesIO(data)
    img: Image.Image = Image.open(dataEnc)
    img.show()

with open("test.tiff", "rb") as file:
    data = file.read()
    dataEnc = io.BytesIO(data)
    img: Image.Image = Image.open(dataEnc)
    img.show()
