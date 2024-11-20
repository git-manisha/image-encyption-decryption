# Image Encryption and Decryption Web Application

This project is a web application that allows users to encrypt and decrypt images using a password. The application is built using Flask and leverages cryptographic techniques to ensure the security of the images.

## Features

- **Image Encryption**: Users can upload an image and encrypt it with a password. The encrypted image is saved with a random suffix in the filename.
- **Image Decryption**: Users can select an encrypted image and decrypt it using the correct password.
- **User Feedback**: The application provides feedback messages to users, such as incorrect password notifications.

## Technologies Used

- **Flask**: A lightweight WSGI web application framework in Python.
- **PyCryptodome**: A self-contained Python package of low-level cryptographic primitives.
- **Pillow**: A Python Imaging Library that adds image processing capabilities.
- **Bootstrap**: A front-end framework for building responsive and modern web applications.

## Project Structure

- `app.py`: Main application file containing routes and logic for encryption and decryption.
- `templates/index.html`: HTML file for the application's user interface.
- `uploads/`: Directory where uploaded and encrypted files are stored.
- `requirements.txt`: Contains the list of dependencies for the project.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/image-encryption.git
   cd image-encryption
   ```

2. **Set Up Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**:
   ```bash
   python app.py
   ```

5. Open your web browser and go to `http://127.0.0.1:5000` to access the application.

## Usage

1. **Encrypt an Image**:
   - Navigate to the "Encrypt an Image" section.
   - Upload an image file and enter a password.
   - Click "Encrypt" to encrypt the image.

2. **Decrypt an Image**:
   - Navigate to the "Decrypt an Image" section.
   - Select an encrypted file from the dropdown list.
   - Enter the password used for encryption.
   - Click "Decrypt" to download the decrypted image.

## Security Considerations

- Ensure that the passwords used are strong to prevent unauthorized access.
- The application uses AES encryption in CBC mode with SHA-256 hashed passwords for security.


## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.