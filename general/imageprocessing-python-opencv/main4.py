import cv2
import matplotlib.pyplot as plt

def img2sketch(photo, output, k_size):
    # Read Image
    img = cv2.imread(photo)

    # Convert to Grey Image
    grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Invert Image
    invert_img = cv2.bitwise_not(grey_img)
    # invert_img=255-grey_img

    # Blur image
    blur_img = cv2.GaussianBlur(invert_img, (k_size, k_size), 0)

    # Invert Blurred Image
    invblur_img = cv2.bitwise_not(blur_img)
    # invblur_img=255-blur_img

    # Sketch Image
    sketch_img = cv2.divide(grey_img, invblur_img, scale=256.0)

    # Save Sketch
    cv2.imwrite(output, sketch_img)

    # Display sketch
    #cv2.imshow('sketch image', sketch_img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    plt.figure(figsize=(14, 8))
    plt.subplot(1, 2, 1)
    plt.title('Original image', size=18)
    plt.imshow(img)
    plt.axis('off')
    plt.subplot(1, 2, 2)
    plt.title('Sketch', size=18)
    rgb_sketch = cv2.cvtColor(sketch_img, cv2.COLOR_BGR2RGB)
    plt.imshow(rgb_sketch)
    plt.axis('off')
    plt.show()

img = "image/m.jpg"
out = "image/m4.png"

# Function call
img2sketch(photo=img, output=out, k_size=9)