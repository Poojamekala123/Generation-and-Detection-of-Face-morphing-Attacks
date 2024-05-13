import cv2
from skimage.metrics import structural_similarity as ssim

def compare_images(image1, image2):
    # Load the images and convert them to grayscale
    # print(image2,'yyyyy')
    img1 = cv2.imread(image1, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(image2, cv2.IMREAD_GRAYSCALE)

    # Compute the SSIM between the two images
    img2 = cv2.resize(img2,(img1.shape[1],img1.shape[0])) 

    score = ssim(img1, img2)
    return score

# Test the function
# print(compare_images('image1.jpg', 'image2.jpg'))
