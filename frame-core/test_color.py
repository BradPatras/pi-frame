from image_utils import adjust_image_temp, load_and_scale_image
from PIL import Image

img = Image.open("../images/donuts1.jpg")
timg = adjust_image_temp(img, 9000)
timg.save("out.jpg")
