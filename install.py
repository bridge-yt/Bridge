import os
import shutil

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


def update_config(cert_dest, key_dest):
    """Update the config file or environment variables to reflect the new paths."""
    # Here, you can modify the config.py file or update a .env file with the new paths
    env_file = './.env'

    # Append SSL_CERT_FILE and SSL_KEY_FILE to the .env file (or environment variables)
    with open(env_file, 'a') as f:
        f.write(f"SSL_CERT_FILE={cert_dest}\n")
        f.write(f"SSL_KEY_FILE={key_dest}\n")

    print(f"Updated environment file with new certificate paths.")


def main():
    print("Welcome to the Bridge App Installer")

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

    print("Installation complete! SSL certificates have been set up.")


if __name__ == "__main__":
    main()
