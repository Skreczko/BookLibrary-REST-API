from imutils.video import VideoStream
from pyzbar import pyzbar
import imutils
import time
import cv2



def capture_barcode(capture=True):
	# initialize the video stream and allow the camera sensor to warm up
	vs = VideoStream().start()
	time.sleep(0.0)

	while capture == True:
		# grab the frame from the threaded video stream and resize it to
		# have a maximum width of 480 pixels
		frame = vs.read()
		frame = imutils.resize(frame, width=480)

		# find the barcodes in the frame and decode each of the barcodes
		barcodes = pyzbar.decode(frame)

		# loop over the detected barcodes
		for barcode in barcodes:
			# extract the bounding box location of the barcode and draw
			# the bounding box surrounding the barcode on the image
			(x, y, w, h) = barcode.rect
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

			# the barcode data is a bytes object so if we want to draw it
			# on our output image we need to convert it to a string first
			barcodeData = barcode.data.decode("utf-8")
			if (len(barcodeData) == 13 or len(barcodeData) == 10) and (barcodeData[:3] == '978' or barcodeData[:3] == '979'):
				cv2.destroyAllWindows()
				VideoStream().stop()
				print("\a")
				capture = False
				break

		# show the output frame
		cv2.imshow("Barcode Scanner", frame)
		key = cv2.waitKey(1) & 0xFF

	return barcodeData






ISBN = capture_barcode()

print (ISBN)


