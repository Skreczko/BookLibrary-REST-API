from pyzbar import pyzbar
import argparse
import cv2

# loop over the detected barcodes
def capture_barcode():
	# construct the argument parser and parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--image", required=True,
					help="path to input image")
	args = vars(ap.parse_args())

	# load the input image
	image = cv2.imread(args["image"])

	# find the barcodes in the image and decode each of the barcodes
	barcodes = pyzbar.decode(image)
	for barcode in barcodes:
		# extract the bounding box location of the barcode and draw the
		# bounding box surrounding the barcode on the image
		(x, y, w, h) = barcode.rect
		cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

		# the barcode data is a bytes object so if we want to draw it on
		# our output image we need to convert it to a string first
		barcodeData = barcode.data.decode("utf-8")

		if (len(barcodeData) == 13 or len(barcodeData) == 10) and (
				barcodeData[:3] == '978' or barcodeData[:3] == '979'):
			return barcodeData
		else:
			return 'Invalid barcode'


ISBN = capture_barcode()


