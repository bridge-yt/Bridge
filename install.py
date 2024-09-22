import os
import subprocess
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

def install_mkcert():
    """Install mkcert if it's not already installed."""
    try:
        subprocess.run(['mkcert', '-install'], check=True)
        print("mkcert is already installed and configured.")
    except subprocess.CalledProcessError:
        print("mkcert is not installed. Please install it first.")
        exit(1)

def generate_mkcert_cert():
    """Generate SSL certificates for localhost using mkcert."""
    cert_dest = os.path.join(CERT_DIR, 'localhost.pem')
    key_dest = os.path.join(CERT_DIR, 'localhost-key.pem')

    # Use mkcert to generate certificates for localhost
    print("Generating SSL certificates for localhost using mkcert...")
    try:
        subprocess.run(['mkcert', '-cert-file', cert_dest, '-key-file', key_dest, 'localhost'], check=True)

        print(f"Generated SSL certificate at {cert_dest}")
        print(f"Generated SSL key at {key_dest}")

        # Update the .env file with the paths
        update_config(cert_dest, key_dest)

    except subprocess.CalledProcessError as e:
        print(f"Error generating SSL certificate with mkcert: {e}")

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
        subprocess.run(["pip", "install", "-r", "backend/requirements.txt"], check=True)
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
        subprocess.run(["npm", "install"], cwd="frontend/bridge-ui", check=True)
        subprocess.run(["npm", "run", "build"], cwd="frontend/bridge-ui", check=True)
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

    # Step 1: Install mkcert if necessary
    install_mkcert()

    # Step 2: Generate mkcert certificates for localhost
    create_cert_directory()
    generate_mkcert_cert()

    # Step 3: Install dependencies and set up backend and frontend
    install_backend_dependencies()
    setup_frontend()

    # Step 4: Set up the Flask application and database
    setup_flask_app()

    print("Installation complete! SSL certificates and application have been set up.")

if __name__ == "__main__":
    main()
