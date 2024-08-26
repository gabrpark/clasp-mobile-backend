# CLaSP Mobile Backend

This repository contains the Flask REST API server designed to provide backend services for the CLaSP Mobile application. The API server facilitates data exchange with a MongoDB database and supports Google login authentication for users. It is self-hosted using Gunicorn as the WSGI HTTP server.

## Features

- **CRUD Operations**: Supports create, read, update, and delete operations on data stored in MongoDB.
- **Google Login**: Integrates Google login for authentication, tailored for iOS app users.
- **Self-Hosting**: Configured for deployment on a self-hosted server, ensuring full control over the hosting environment.
- **Gunicorn Integration**: Utilizes Gunicorn as the WSGI server for enhanced performance and concurrent request handling.
- **Docker Support**: Includes a Dockerfile and docker-compose.yml for containerized deployment.
- **Kubernetes Support**: Includes a k8s folder with deployment and service files for Kubernetes deployment.
- **NGINX Support**: Includes an NGINX configuration file for reverse proxying requests to the Gunicorn server.
- **Supervisor Support**: Includes a Supervisord configuration file for automated process management.

## Getting Started

### Self-Hosting

Ensure that the lab server (`clasp-iml`) is running. If not, run the `start_services.sh` script to start the server.

## Prerequisites

- Python 3.9
- MongoDB
- Flask
- Gunicorn (for production deployment)
- NGINX (for production deployment)
- Supervisor (for production deployment)
- Docker
- Docker Compose
- Google Cloud Platform account for Google Login integration
- (Optional) Kubernetes (for production deployment)

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/clasp-iml/clasp-mobile-backend.git
   ```

2. **Navigate to the project directory**

   ```bash
   cd clasp-mobile-backend
   ```

3. **Create and activate a virtual environment** (optional but recommended)

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

4. **Install required Python packages**

   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**

   Create a `.env` file in the root directory of the project and add the following variables:

   ```bash
   MONGODB_URI=mongodb://localhost:27017/clasp-mobile-backend
   FIREBASE_TYPE=your-firebase-type
   FIREBASE_PROJECT_ID=your-firebase-project-id
   FIREBASE_PRIVATE_KEY_ID=your-firebase-private-key-id
   FIREBASE_PRIVATE_KEY=your-firebase-private-key
   FIREBASE_CLIENT_EMAIL=your-firebase-client-email
   FIREBASE_CLIENT_ID=your-firebase-client-id
   FIREBASE_AUTH_URI=your-firebase-auth-uri
   FIREBASE_TOKEN_URI=your-firebase-token-uri
   FIREBASE_AUTH_PROVIDER_X509_CERT_URL=your-firebase-auth-provider-x509-cert-url
   FIREBASE_CLIENT_X509_CERT_URL=your-firebase-client-x509-cert-url
   ```

6. **Run the application locally**

   ```bash
   flask run
   ```

## Deployment

### Self-Hosted Deployment

For self-hosting, follow these steps:

1. **Set up your server environment**: Ensure your server has Python, MongoDB, Gunicorn, NGINX, and Supervisor installed.

2. **Deploy the application**:
   
   - Use Gunicorn to serve the Flask application.
   - Configure NGINX to reverse proxy requests to the Gunicorn server.
   - Use Supervisor to manage the Gunicorn process and ensure it stays running.

3. **Monitor your application**:

   - Logs are typically stored in the `/var/log` directory for both NGINX and Supervisor.
   - Use tools like `htop` or `systemctl` to monitor server performance and service status.

## Usage

Provide documentation on how to use your API, including endpoints, request/response formats, and authentication methods.

### Endpoints

- **GET /tasks/<task_type>**: Returns a specific task from the database.
- **POST /responses**: Adds a new response to the database.

### Authentication

Both endpoints require a valid Google ID token to be included in the `Authorization` header of the request. The token should be obtained from the Google Sign-In API and should be sent as a Bearer token.