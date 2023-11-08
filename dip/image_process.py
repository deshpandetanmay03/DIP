from modules import np, KMeans, pd, silhouette_score, cv
import time
import concurrent.futures

def load_image(url):
    image = cv.imread(url, cv.IMREAD_GRAYSCALE)
    return image

def expand_range(image):
    m = image.min()
    image -= m
    M = image.max()
    image *= (255//M)
    return image

def classify_pixel(pixel):
    f = 10
    return round(pixel/f)*f

def classify_pixels(image):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        image = np.array(list(executor.map(classify_pixel, image.flatten()))).reshape(image.shape)
    return image

def blur_image(image):
    image = cv.medianBlur(image, 151, (51, 51))
    return image

def color_pixel(pixel):
    return cv.convertScaleAbs((0, 255-pixel, 0))

def color_image(image):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        image = np.array(list(executor.map(color_pixel, image.flatten()))).reshape(image.shape)
    return image

def process_image(url):
    image = load_image(url)

    # image = classify_pixels(image)
    t1 = time.time()
    image = blur_image(image)
    t2 = time.time()
    print(t2-t1)

    t1 = time.time()
    image = classify_pixels(image)
    t2 = time.time()
    print(t2-t1)

    t1 = time.time()
    image = expand_range(image)
    t2 = time.time()
    print(t2-t1)

    t1 = time.time()
    image = color_image(image)
    t2 = time.time()
    print(t2-t1)
    return image
