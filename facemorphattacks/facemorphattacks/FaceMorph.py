import pywt
import numpy as np
import matplotlib.pyplot as plt
import random
import cv2

def channelTransform(ch1,ch2,ch3, shape):
    cooef1 = pywt.dwt2(ch1, 'db5', mode = 'periodization')
    cooef2 = pywt.dwt2(ch2, 'db5', mode = 'periodization')
    cooef3 = pywt.dwt2(ch3, 'db5', mode = 'periodization')
    cA1, (cH1, cV1, cD1) = cooef1
    cA2, (cH2, cV2, cD2) = cooef2
    cA3, (cH3, cV3, cD3) = cooef2

    cA = (cA1+cA2+cA3)/3
    cH = (cH1 +cH2+cH3)/3
    cV = (cV1+cV2+cV3)/3
    cD = (cD1+cD2+cD3)/3
    fincoC = cA, (cH,cV,cD)
    outImageC = pywt.idwt2(fincoC, 'db5', mode = 'periodization')
    outImageC = cv2.resize(outImageC,(shape[0],shape[1])) 
    return outImageC

def facemorph(img1,img2,img3):
    # Params
    FUSION_METHOD = 'mean' # Can be 'min' || 'max || anything you choose according theory
    img1 = 'media/'+str(img1)
    img2 = 'media/'+str(img2)
    img3 = 'media/'+str(img3)
    # Read the two image
    I1 = cv2.imread(img1)
    I2 = cv2.imread(img2)
    I3 = cv2.imread(img3)

    # Resizing image if both are in different shapes
    I2 = cv2.resize(I2,(I1.shape[1],I1.shape[0])) 
    I3 = cv2.resize(I3,(I1.shape[1],I1.shape[0]))
    
    print (I1.shape)
    print (I2.shape)
    print (I3.shape)
    ## Seperating channels
    iR1 = I1.copy()
    iR1[:,:,1] = iR1[:,:,2] = 0
    iR2 = I2.copy()
    iR2[:,:,1] = iR2[:,:,2] = 0
    iR3 = I3.copy()
    iR3[:,:,1] = iR3[:,:,2] = 0

    iG1 = I1.copy()
    iG1[:,:,0] = iG1[:,:,2] = 0
    iG2 = I2.copy()
    iG2[:,:,0] = iG2[:,:,2] = 0
    iG3 = I3.copy()
    iG3[:,:,0] = iG3[:,:,2] = 0

    iB1 = I1.copy()
    iB1[:,:,0] = iB1[:,:,1] = 0
    iB2 = I2.copy()
    iB2[:,:,0] = iB2[:,:,1] = 0
    iB3 = I3.copy()
    iB3[:,:,0] = iB3[:,:,1] = 0

    shape = (I1.shape[1], I1.shape[0])
    # Wavelet transformation on red channel
    outImageR = channelTransform(iR1, iR2, iR3, shape)
    outImageG = channelTransform(iG1, iG2, iG3, shape)
    outImageB = channelTransform(iB1, iB2, iB3, shape)

    outImage = I1.copy()
    outImage[:,:,0] = outImage[:,:,1] = outImage[:,:,2] = 0
    outImage[:,:,0] = outImageR[:,:,0]
    outImage[:,:,1] = outImageG[:,:,1]
    outImage[:,:,2] = outImageB[:,:,2] 

    outImage = np.multiply(np.divide(outImage - np.min(outImage),(np.max(outImage) - np.min(outImage))),255)
    outImage = outImage.astype(np.uint8)

    x = random.randint(1000, 2000)
    # cv2.imwrite('morphed2.jpg',outImage)
    return outImage
