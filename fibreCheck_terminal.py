import sys
import os
import MySQLdb
import MySQLdb.cursors
import cv2
import numpy as np
import scipy as sp
from MySQLdb import OperationalError
from skimage.feature import greycomatrix,greycoprops
from random import uniform
from matplotlib import pyplot


def syntaxValidate (sargv):
   validSyntax = True
   pSegmented = True

   if (len(sargv)!=3 and len(sargv)!=4):
       validSyntax = False
   if (len(sargv)==4):
       if (sargv[3]!='-q'):
           validSyntax = False
       else:
           pSegmented = False
   if (sargv[1]!='-i' and sargv[1]!='-c'):
       validSyntax = False

   if not validSyntax:
       print('Usage\: python fibreCheck.py [OPTION] [FILE]')
       print('Image comparison tool\n')
       print('-i\tImport image to database')
       print('-c\tCompare image to database')
       sys.exit('\nSyntaxError: invalid syntax')

   return pSegmented


def preprocessImage(img):
    imgGrayscale = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgGaussian = cv2.GaussianBlur(imgGrayscale,(3,3),0)
    return imgGaussian

def acquireImage(img,images):
    # Read image from argument
    imgOriginal = cv2.imread(img)
    images['Original'] = imgOriginal

    # Image preprocessing (grayscale and blur)
    imgPreprocessed = preprocessImage(imgOriginal)
    images['Preprocessed'] = imgPreprocessed

    return imgPreprocessed

def edImage(img):
    imgCanny = cv2.Canny(img,100,200)
    return imgCanny

def heImage(img):
    objCLAHE = cv2.createCLAHE(clipLimit=2.0,tileGridSize=(8,8))
    imgCLAHE = objCLAHE.apply(img)
    return imgCLAHE

def atgImage(img):
    imgATGauss= cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    return imgATGauss

def segmentImage(img,images):

    # Apply edge detection (Canny)
    imgEdgeDetect = edImage(img)
    images['Edge Detection'] = imgEdgeDetect

    # Apply histogram equalisation (CLAHE)
    imgHistogramEqualize = heImage(imgEdgeDetect)
    images['Histogram Equalization'] = imgHistogramEqualize

    # Apply adaptive threshold (Gaussian)
    imgAdaptiveThreshold = atgImage(imgHistogramEqualize)
    images['Adaptive Threshold'] = imgAdaptiveThreshold

    return imgAdaptiveThreshold

def plotImages (imgs):
    subplotPosition=0
    for k,v in imgs.items():
        pyplot.subplot(1,len(imgs),subplotPosition+1),pyplot.imshow(v,'gray')
        pyplot.title(k)
        pyplot.xticks([]),pyplot.yticks([])
        subplotPosition=subplotPosition+1
    pyplot.show()

    return


def f1(imgMatrix):
    featMax = imgMatrix.max(0).max(0)
    return featMax

def f2(imgMatrix):
    featContrast = greycoprops(imgMatrix, 'contrast')
    return featContrast

def f3(imgMatrix):
    featHomogeneity = greycoprops(imgMatrix, 'homogeneity')
    return featHomogeneity

def f4(imgMatrix):
    featASM = greycoprops(imgMatrix, 'ASM')
    return featASM

def f5(imgMatrix):
    featDissimilarity = greycoprops(imgMatrix, 'dissimilarity')
    return featDissimilarity

def f6(imgMatrix):
    featEnergy = greycoprops(imgMatrix, 'energy')
    return featEnergy

def f7(imgMatrix):

    featVar = np.var(imgMatrix)
    return featVar

def f8(imgMatrix):
    featCorrelation = greycoprops(imgMatrix, 'correlation')
    return featCorrelation

def f9(imgMatrix):
    featEntropy = -np.sum(imgMatrix*np.log(imgMatrix+0.000001))
    return featEntropy


def extractFeatures(img):
    imgGCMatrix = greycomatrix(img, [1], [0, np.pi/4, np.pi/2, 3*np.pi/4], symmetric=False, normed=True )
    featsTuple = ('null', f1(imgGCMatrix),f2(imgGCMatrix),f3(imgGCMatrix),f4(imgGCMatrix),f5(imgGCMatrix),f6(imgGCMatrix),f7(imgGCMatrix),f8(imgGCMatrix),f9(imgGCMatrix))
    return featsTuple

def importToDB (img,fList,target,namedesc):

    # Get image data for extraction
    IMGDESC = namedesc
    imgY = img.shape[0]
    imgX = img.shape[1]
    imgColour = len(img.shape)-2

    # Determine target table for storing image
    if (target == '-i'):
        tImages = 'iImages'
    elif (target == '-c'):
        tImages = 'cImages'

    # Connect to DB
    db = MySQLdb.connect("localhost","root","P@ssw0rd","images" )

    # Populate DB with image, data & features values
    with db:
        cursor = db.cursor()

        # Initialize SQL command & arguments with image & image data
        sql = "INSERT INTO %s(IMG,IMGDESC, IMGY, IMGX, IMGC, F1, F2, F3, F4, F5, F6, F7, F8, F9) VALUES (%%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s)" %tImages
        sqlArgs = (img.tostring(),IMGDESC, imgY, imgX, imgColour)

        # Properly convert features to strings depending on type and append to sqlArgs
        for i in range(len(fList)):
            # print(type(fList[i]))
            if (type(fList[i]) is np.float64):
                sqlArgs = sqlArgs + (str(fList[i]),)
            elif (type(fList[i]) is np.ndarray):
                sqlArgs = sqlArgs + (fList[i].tostring(),)

        # Execute SQL command
        cursor.execute(sql,sqlArgs)

    return

def compareFeatures(iFeat, cFeat):

    if (type(cFeat) is np.float64):
        iFeat = np.float64(iFeat)
        dFeat = abs(iFeat-cFeat)
    elif (type(cFeat) is np.ndarray):
        iFeat = np.fromstring(iFeat, dtype=cFeat.dtype).reshape(cFeat.shape)
        #dFeat = 99
        dFeat = sp.spatial.distance.euclidean(iFeat, cFeat)

    return dFeat

def compareImages(cFeatsTuple, featsSelected):

    # Connect to DB
    db = MySQLdb.connect("localhost","root","P@ssw0rd","images")

    # Compare with stored images' features
    with db:
        cursor = db.cursor()

        sql = 'SELECT ID, F1, F2, F3, F4, F5, F6, F7, F8, F9 FROM iImages'
        cursor.execute(sql)
        iFeatsTable = cursor.fetchall()
        resDict = {}

        # For each selected feature...
        for i in featsSelected:

            cFeature = cFeatsTuple[i]
            minDelta = 100

            # ...calculate list of best matches (minList)...
            for j in range(len(iFeatsTable)):
                iFeatsTuple = iFeatsTable[j]
                iFeature = iFeatsTuple[i]

                iID = iFeatsTuple[0]
                deltaFeature = compareFeatures(iFeature, cFeature)
                if (deltaFeature < minDelta):
                    minID = iID
                    minDelta = deltaFeature
                    minList = [(minID, minDelta)]
                elif (deltaFeature == minDelta):
                    minID = iID
                    minDelta = deltaFeature
                    minList.append((minID,minDelta))

            print(minList)

            # ...and fetch them all under results dictionary (resDict)
            for k in range(len(minList)):
                sql = "SELECT IMG, IMGY, IMGX, IMGC FROM iImages WHERE ID=%s" %minList[k][0]
                cursor.execute(sql)
                imgRow = cursor.fetchone()
                imgShape = (int(imgRow[1]), int(imgRow[2]), int(imgRow[3])*3)
                imgTitle = 'F%s: IMG%s (%s)' % (str(i), minList[k][0], minList[k][1])
                resDict[imgTitle] = np.fromstring(imgRow[0], dtype=np.uint8).reshape(imgShape)

    return resDict

# ------------------------------------------------------------------------------------------

images = {}

# ===== VALID SYNTAX CHECK ======
plotTrue = syntaxValidate(sys.argv)

# ===== ACQUISITION =====
# Acquire and preprocess image
imgAcquired = acquireImage(sys.argv[2],images)

# ===== SEGMENTATION =====
# Segment Image (Init, threshold, edge detection & histogram equalisation)
imgSegmented = segmentImage(imgAcquired,images)

# ===== IMAGES PLOT (optional) =====
# Plot images sequence
if plotTrue:
    plotImages(images)

# ===== FEATURE EXTRACTION =====
featuresTuple = extractFeatures(imgSegmented)

# ===== SAVE IMAGE TO DB (corresponding table) =====
importToDB(images['Original'],featuresTuple,sys.argv[1])
print("Succesfully saved image",sys.argv[2])

featuresSelected = (3,7)

# ===== MATCH RANKING =====
if (sys.argv[1] == '-c'):
    results = compareImages(featuresTuple, featuresSelected)

    # Plot results
    plotImages(results)
