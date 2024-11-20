from flask import Flask, render_template, request, send_file, redirect, url_for
import os
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from io import BytesIO
import hashlib
import random

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def encrypt(file_path, password):
    with open(file_path, 'rb') as f:
        data = f.read()

    cipher = AES.new(password, AES.MODE_CBC)
    iv = cipher.iv
    padded_data = pad(data, AES.block_size)
    ciphertext = cipher.encrypt(padded_data)

    # Generate a new file name with a random 2-digit number
    original_filename = os.path.splitext(os.path.basename(file_path))[0]
    random_number = random.randint(10, 99)
    encrypted_filename = f"{original_filename}_{random_number}.aes"
    encrypted_path = os.path.join(app.config['UPLOAD_FOLDER'], encrypted_filename)

    with open(encrypted_path, 'wb') as f:
        f.write(iv + ciphertext)  # Store IV + ciphertext

    return encrypted_path


def decrypt(file_path, password):
    with open(file_path, 'rb') as f:
        data = f.read()

    iv = data[:16]  # First 16 bytes are the IV
    ciphertext = data[16:]
    cipher = AES.new(password, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)

    # Use BytesIO to create an in-memory binary stream for the decrypted image
    decrypted_image = BytesIO(decrypted_data)
    decrypted_image.seek(0)  # Reset the pointer to the beginning of the stream
    return decrypted_image


@app.route('/')
def index():
    # List all `.aes` files in the uploads folder
    encrypted_files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.endswith('.aes')]
    return render_template('index.html', encrypted_files=encrypted_files)


@app.route('/encrypt', methods=['POST'])
def encrypt_image():
    file = request.files['image']
    password = request.form['password']
    if file and password:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(image_path)

        # Encrypt the image
        password_bytes = hashlib.sha256(password.encode()).digest()[:16]  # 16-byte key
        encrypted_path = encrypt(image_path, password_bytes)

        return send_file(encrypted_path, as_attachment=True)
    return "Error: Please provide an image and password."


@app.route('/decrypt', methods=['POST'])
def decrypt_image():
    filename = request.form.get('encrypted_file')  # Fetch selected file name
    password = request.form['password']
    if filename and password:
        encrypted_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        try:
            # Decrypt the image
            password_bytes = hashlib.sha256(password.encode()).digest()[:16]  # 16-byte key
            decrypted_image = decrypt(encrypted_path, password_bytes)

            # Serve the decrypted image directly from memory
            return send_file(
                decrypted_image,
                mimetype="image/jpeg",
                as_attachment=True,
                download_name="decrypted_image.jpeg",
            )
        except ValueError:  # Handle padding errors when the password is incorrect
            return render_template(
                'index.html',
                encrypted_files=os.listdir(app.config['UPLOAD_FOLDER']),
                message="Incorrect password. Please try again!"
            )
    return "Error: Please select an encrypted file and provide a password."


if __name__ == '__main__':
    app.run(debug=True)