import os
import subprocess

# Define the destination directory for the certificates
CERT_DIR = 'backend/api/Certs'


def create_cert_directory():
    """Create the Certs directory if it doesn't exist."""
    if not os.path.exists(CERT_DIR):
        os.makedirs(CERT_DIR)
        print(f"Created directory {CERT_DIR} for storing SSL certificates.")
    else:
        print(f"Directory {CERT_DIR} already exists.")


def copy_certificates(cert_path, key_path):
    """Copy the SSL certificate and key files to the Certs directory, maintaining the original file names."""
    try:
        # Extract file names from the provided paths
        cert_filename = os.path.basename(cert_path)
        key_filename = os.path.basename(key_path)

        # Destination paths in the Certs directory
        cert_dest = os.path.join(CERT_DIR, cert_filename)
        key_dest = os.path.join(CERT_DIR, key_filename)

        # Copy the certificate and key to the Certs directory
        shutil.copyfile(cert_path, cert_dest)
        shutil.copyfile(key_path, key_dest)

        print(f"Copied SSL certificate to {cert_dest}")
        print(f"Copied SSL key to {key_dest}")

        # Optionally, update environment variables or config file with paths
        update_config(cert_dest, key_dest)

    except Exception as e:
        print(f"Error copying certificates: {e}")


def generate_self_signed_cert():
    """Generate a self-signed SSL certificate and key."""
    cert_dest = os.path.join(CERT_DIR, 'self-signed-cert.pem')
    key_dest = os.path.join(CERT_DIR, 'self-signed-key.pem')

    # Use OpenSSL to generate a self-signed certificate and key
    print("Generating self-signed certificate and key...")
    try:
        subprocess.run([
            'openssl', 'req', '-x509', '-newkey', 'rsa:4096', '-keyout', key_dest,
            '-out', cert_dest, '-days', '365', '-nodes', '-subj', '/CN=localhost'
        ], check=True)

        print(f"Generated self-signed SSL certificate at {cert_dest}")
        print(f"Generated self-signed SSL key at {key_dest}")

        # Update the .env file with the paths
        update_config(cert_dest, key_dest)

    except subprocess.CalledProcessError as e:
        print(f"Error generating self-signed certificate: {e}")


def update_config(cert_dest, key_dest):
    """Update the config file or environment variables to reflect the new paths."""
    # Here, you can modify the config.py file or update a .env file with the new paths
    env_file = './.env'

    # Append SSL_CERT_FILE and SSL_KEY_FILE to the .env file (or environment variables)
    with open(env_file, 'a') as f:
        f.write(f"SSL_CERT_FILE={cert_dest}\n")
        f.write(f"SSL_KEY_FILE={key_dest}\n")

    print(f"Updated environment file with new certificate paths.")


def install_backend_dependencies():
    """Install Python dependencies for the backend."""
    print("Installing backend dependencies...")
    try:
        subprocess.run(["pip", "install", "-r", "Backend/requirements.txt"], check=True)
        print("Backend dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing backend dependencies: {e}")
        exit(1)


def setup_frontend():
    """Install frontend dependencies and build the frontend."""
    print("Setting up frontend...")
    try:
        # Export the NODE_OPTIONS environment variable
        os.environ['NODE_OPTIONS'] = '--openssl-legacy-provider'

        # Navigate to the frontend directory and install dependencies
        subprocess.run(["npm", "install"], cwd="Frontend/bridge-ui", check=True)
        subprocess.run(["npm", "run", "build"], cwd="Frontend/bridge-ui", check=True)
        print("Frontend setup and build complete.")
    except subprocess.CalledProcessError as e:
        print(f"Error setting up frontend: {e}")
        exit(1)


def setup_flask_app():
    """Set up the Flask application environment and database."""
    print("Setting up Flask application...")

    # Set environment variables for Flask
    os.environ['FLASK_APP'] = 'backend.api.bridge'
    os.environ['FLASK_ENV'] = 'development'

    try:
        # Check if the 'migrations' directory already exists
        if not os.path.exists('migrations'):
            print("Initializing database migrations...")
            subprocess.run(["flask", "db", "init"], check=True)
        else:
            print("Migrations directory already exists, skipping 'flask db init'.")

        # Always run the migrate and upgrade commands
        subprocess.run(["flask", "db", "migrate", "-m", "Initial migration."], check=True)
        subprocess.run(["flask", "db", "upgrade"], check=True)
        print("Flask application setup and database migration complete.")

    except subprocess.CalledProcessError as e:
        print(f"Error setting up Flask application: {e}")
        exit(1)


def main():
    print("Welcome to the Bridge App Installer")

    # Ask the user if they want to provide SSL certificates or generate self-signed ones
    choice = input("Do you want to provide your own SSL certificates? (y/n): ").strip().lower()

    if choice == 'y':
        # Ask the user for the location of their SSL certificate and key
        cert_path = input("Enter the full path to your SSL certificate file: ").strip()
        key_path = input("Enter the full path to your SSL key file: ").strip()

        # Validate the provided paths
        if not os.path.exists(cert_path):
            print(f"Error: SSL certificate not found at {cert_path}")
            return
        if not os.path.exists(key_path):
            print(f"Error: SSL key not found at {key_path}")
            return

        # Create the Certs directory and copy the certificates
        create_cert_directory()
        copy_certificates(cert_path, key_path)

    else:
        # If the user chooses not to provide their own certificate, generate a self-signed certificate
        create_cert_directory()
        generate_self_signed_cert()

    # Install dependencies and setup backend and frontend
    install_backend_dependencies()
    setup_frontend()

    # Set up the Flask application and database
    setup_flask_app()

    print("Installation complete! SSL certificates and application have been set up.")


if __name__ == "__main__":
    main()
