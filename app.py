from flask import Flask, render_template, request, send_file
import pyqrcode
import base64
from io import BytesIO
from PIL import Image
import tempfile

app = Flask(__name__)

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for generating QR code
@app.route('/generate', methods=['POST'])
def generate_qr():
    # Retrieve data from the form
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    blood_group = request.form.get('blood_group')
    phone_number = request.form.get('phone_number')
    emergency_phone = request.form.get('emergency_phone')
    email = request.form.get('email')
    address = request.form.get('address')
    city = request.form.get('city')

    # Combine all the details into a single string for the QR code
    qr_data = (
        f"Firstname: {firstname}\n"
        f"Lastname: {lastname}\n"
        f"Blood Group: {blood_group}\n"
        f"Phone Number: {phone_number}\n"
        f"Emergency Phone: {emergency_phone}\n"
        f"Email: {email}\n"
        f"Address: {address}\n"
        f"City: {city}"
    )

    # Generate the QR code
    qr = pyqrcode.create(qr_data)

    # Create a temporary PNG file
    temp_png_path = tempfile.mktemp(suffix='.png')
    qr.png(temp_png_path, scale=5)

    # Convert PNG to JPEG
    img = Image.open(temp_png_path)
    temp_jpeg_path = tempfile.mktemp(suffix='.jpeg')
    img.convert("RGB").save(temp_jpeg_path, format="JPEG")

    # Render the result page with the QR code and user details
    return render_template('qr_display.html', qr_code=base64.b64encode(open(temp_png_path, 'rb').read()).decode('utf-8'), user_details=qr_data, jpeg_path=temp_jpeg_path)

# Route to download JPEG
@app.route('/download/jpeg')
def download_jpeg():
    jpeg_path = request.args.get('path')  # Get JPEG path from request
    return send_file(jpeg_path, as_attachment=True, download_name='qrcode.jpeg', mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)
