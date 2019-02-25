from pyzbar import pyzbar
import argparse
import cv2

def capture_barcode():
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--image", required=True,
					help="path to input image")
	args = vars(ap.parse_args())
	image = cv2.imread(args["image"])
	barcodes = pyzbar.decode(image)
	for barcode in barcodes:
		(x, y, w, h) = barcode.rect
		cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
		barcodeData = barcode.data.decode("utf-8")

		if (len(barcodeData) == 13 or len(barcodeData) == 10) and (
				barcodeData[:3] == '978' or barcodeData[:3] == '979'):
			return barcodeData
		else:
			return 'Invalid barcode'

ISBN = capture_barcode()


