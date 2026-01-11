import qrcode

def generate_qr_code(data="", output_file="qr_code.png"):
	# Create a QR code object with a larger size and higher error correction
	qr = qrcode.QRCode(version=None, box_size=20, border=1, error_correction=qrcode.constants.ERROR_CORRECT_H)

	# Add the data to the QR code object
	qr.add_data(data)

	# Make the QR code
	qr.make(fit=True)

	# Create an image from the QR code with a black fill color and white background
	img = qr.make_image(fill_color="black", back_color="white")

	# Save the QR code image
	img.save(output_file)