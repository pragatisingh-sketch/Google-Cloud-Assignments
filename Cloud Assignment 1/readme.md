# Cloud Assignment 1  
Secure Login System using Node.js, Express, and Google Cloud Storage

## Project Overview
This project is a cloud-based login/registration system built using a frontend HTML login page and a Node.js backend deployed on a cloud virtual machine.  
User credentials are stored in a JSON file inside a Google Cloud Storage bucket instead of a traditional database.

The system demonstrates how a web application interacts with a cloud storage service to persist user data securely.

---

## Architecture Flow

User → Login Page (index.html) → HTTP Request → Node.js Server → Google Cloud Storage → JSON File → Response to User

### Step-by-Step Flow
1. User opens the login page in browser.
2. User enters username and password.
3. Frontend sends POST request to backend `/login` API.
4. Backend checks if `users.json` exists in Cloud Storage.
5. If file exists → download and read users.
6. Check if username already exists.
7. If user exists → return error.
8. If user does not exist → save new user into users.json.
9. Upload updated JSON file back to Cloud Storage.
10. Send success response to frontend.

---

## Tech Stack
Frontend  
- HTML  
- CSS  
- JavaScript  

Backend  
- Node.js  
- Express  
- Google Cloud Storage SDK  

Cloud  
- Google Cloud Storage bucket  
- VM instance running Node server  

---

## Project Structure
```
Cloud Assignment 1/
│
├── index.html
├── server.js
├── package.json
└── users.json (stored in GCS bucket)
```

---

## Features Implemented

### Frontend Features
- Secure login UI design
- Password visibility toggle
- Input validation
- Alphanumeric password restriction
- Loading state on submit
- Error handling if server not reachable
- Sends POST request to backend

### Backend Features
- Express server
- REST API endpoint `/login`
- JSON-based user storage
- Google Cloud Storage integration
- Username duplicate check
- Automatic users.json creation if not exists
- Timestamp stored for each user
- CORS enabled for frontend requests

### Cloud Storage Features
- Uses a single JSON file as database
- Stores all users in users.json
- File downloaded, updated, and re-uploaded
- Bucket used as persistent storage

---

## Backend API

### POST /login
Registers a new user.

Request Body
```
{
  "username": "user1",
  "password": "pass123"
}
```

Responses

Success  
```
User registered successfully in users.json
```

If username exists  
```
Username already exists
```

Error  
```
Error processing JSON database
```

---

## Google Cloud Storage Setup

1. Create bucket
2. Create service account
3. Download key file
4. Place key file on VM
5. Update path in server.js

```
const storage = new Storage({
  keyFilename: '/home/ipragatisingh30/gcs-key.json'
});
```

Bucket used
```
pragati_highspring
```

File stored in bucket
```
users.json
```

---

## How to Run Locally

### Install dependencies
```
npm install express body-parser cors @google-cloud/storage
```

### Start server
```
node server.js
```

Server runs on
```
http://localhost:3000
```

---

## Deployment on VM

1. SSH into VM
2. Install Node.js
3. Upload project files
4. Place service account key
5. Run server

```
node server.js
```

Optional (background run)
```
nohup node server.js &
```

---

## Security Notes
- Password stored as plain text (for learning purpose)
- In production, use hashing (bcrypt)
- Use HTTPS instead of HTTP
- Restrict service account permissions

---

## Learning Outcomes
- Frontend to backend communication
- REST API creation
- JSON database handling
- Google Cloud Storage integration
- VM deployment
- Cloud authentication with service account
- Real cloud storage instead of local file

---

## Author
Pragati Singh
