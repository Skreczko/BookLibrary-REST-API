from imutils.video import VideoStream
from pyzbar import pyzbar
import imutils
import time
import cv2

def capture_barcode(capture=True):
	vs = VideoStream().start()
	time.sleep(0.0)
	while capture == True:
		frame = vs.read()
		frame = imutils.resize(frame, width=480)
		barcodes = pyzbar.decode(frame)
		for barcode in barcodes:
			(x, y, w, h) = barcode.rect
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
			barcodeData = barcode.data.decode("utf-8")
			if (len(barcodeData) == 13 or len(barcodeData) == 10) and (barcodeData[:3] == '978' or barcodeData[:3] == '979'):
				cv2.destroyAllWindows()
				vs.stop()
				print("\a")
				capture = False
				VideoStream().stop()
				break
		cv2.imshow("Barcode Scanner", frame)
		key = cv2.waitKey(1) & 0xFF
	return barcodeData

def capture_user_barcode(capture=True):
	vs = VideoStream().start()
	time.sleep(0.0)
	while capture == True:
		frame = vs.read()
		frame = imutils.resize(frame, width=480)
		barcodes = pyzbar.decode(frame)
		for barcode in barcodes:
			(x, y, w, h) = barcode.rect
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
			barcodeData = barcode.data.decode("utf-8")
			cv2.destroyAllWindows()
			vs.stop()
			print("\a")
			capture = False
			VideoStream().stop()
			break
		cv2.imshow("Barcode Scanner", frame)
		key = cv2.waitKey(1) & 0xFF
	return barcodeData








