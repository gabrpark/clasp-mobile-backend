# Flask REST API Server for CLaSP Mobile App

This repository contains the Flask REST API server designed to provide backend services for an CLaSP Mobile application. The API server facilitates data exchange with a MongoDB database and supports Google login authentication for users. It is deployed on Heroku using gunicorn as the WSGI HTTP server.

## Features

- **CRUD Operations**: Supports create, read, update, and delete operations on data stored in MongoDB.
- **Google Login**: Integrates Google login for authentication, tailored for iOS app users.
- **Heroku Deployment**: Configured for easy deployment on Heroku, ensuring scalability and ease of access.
- **gunicorn Integration**: Utilizes gunicorn as the WSGI server for enhanced performance and concurrent request handling.
- **Docker Support**: Includes a Dockerfile and docker-compose.yml for containerized deployment.
- **Kubernates Support**: Includes a k8s folder with deployment and service files for k8s deployment.
- **NGINX Support**: Includes an NGINX configuration file for reverse proxying requests to the gunicorn server.
- **Supervisor Support**: Includes a supervisord configuration file for automated process management.

## Getting Started
In case, Heroku is being used for deployment, the main branch is automatically deployed to Heroku.

For self-hosting, please check the lab server (clasp-iml) if the server is running. If not, run the script `start_services.sh` to start the server.

### Prerequisites

- Python 3.9
- MongoDB
- Flask
- gunicorn (for production deployment)
- NGINX (for production deployment)
- Supervisor (for production deployment)
- Docker
- Docker Compose
- Google Cloud Platform account for Google Login integration
- (Optional) Kubernates (for production deployment)
- (Optional) Heroku account for deployment

### Installation

1. **Clone the repository**

   ```
   git clone https://github.com/clasp-iml/flask-rest-api.git
   ```

2. **Navigate to the project directory**

   ```
   cd flask-rest-api
   ```

3. **Install required Python packages**

   ```
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   Create a `.env` file in the root directory of the project and add the following variables:

   ```
  MONGODB_URI=mongodb://localhost:27017/flask-rest-api
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

5. **Run the application locally**

   ```
   flask run
   ```

### Deployment on Heroku

This project is configured for easy deployment on Heroku. Follow these steps to deploy your API server:

1. **Create a Heroku app (if not already created)**

   ```
   heroku create your-app-name
   ```

2. **Login to Heroku account**
	```
	heroku login
	```

3. **Set environment variables in Heroku**

   Use the Heroku dashboard or CLI to set the environment variables as specified in your `.env` file.

4. **Deploy to Heroku**

   ```
   git push main
   ```

5. **Scale your application** (optional)

   To scale your application to run with multiple dynos, use the Heroku CLI:

   ```
   heroku ps:scale web=1
   ```

	 Please note that this will incur charges on your Heroku account. If you do not want to incur charges, you can set the number of dynos to 0 which will stop the application from running.

6. **Monitor your application logs**
		```
		heroku logs -tails -a clasp-iml-flask-api
		```

## Usage

Provide documentation on how to use your API, including endpoints, request/response formats, and authentication methods.

### Endpoints

- **GET /tasks/<task_type>**: Returns a specific task from the database.
- **POST /responses**: Adds a new response to the database.

### Authentication

Both endpoints require a valid Google ID token to be included in the `Authorization` header of the request. The token should be obtained from the Google Sign-In API and should be sent as a Bearer token.