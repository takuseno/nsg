from PIL import Image
from selenium import webdriver


def capture(url):
    driver = webdriver.PhantomJS()
    driver.get(url)
    driver.set_window_size(1024, 768)
    driver.save_screenshot('static/screenshot.png')
    image = Image.open('static/screenshot.png')
    image = image.crop((0, 0, 1024, 720))
    image = image.resize((512, 360))
    image.save('static/screenshot.png')
    return image
