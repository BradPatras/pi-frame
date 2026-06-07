import qrcode


def generate_qr_code(data="", output_file="qr_code.png"):
    qr = qrcode.QRCode(
        version=None,
        box_size=20,
        border=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output_file)
