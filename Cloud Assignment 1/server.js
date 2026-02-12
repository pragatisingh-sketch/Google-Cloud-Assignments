const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const { Storage } = require('@google-cloud/storage');

const app = express();
app.use(bodyParser.json());
app.use(cors());

// --- GCS Setup ---
const storage = new Storage({
    keyFilename: '/home/ipragatisingh30/gcs-key.json'
});

const bucketName = 'pragati_highspring';
const bucket = storage.bucket(bucketName);
const USERS_FILE_NAME = 'users.json'; // The single JSON database file
const usersFile = bucket.file(USERS_FILE_NAME);

app.get('/', (req, res) => {
    res.send('Backend with JSON storage is running');
});

/**
 * Note: Your route is named /login, but the logic performs Registration. 
 * It checks if a user exists and saves them if they don't.
 */
app.post('/login', async (req, res) => {
    const { username, password } = req.body;

    if (!username || !password) {
        return res.status(400).json({ message: 'Missing username or password' });
    }

    const safeUsername = username.toLowerCase().trim();

    try {
        let users = [];

        // 1. Check if the JSON file exists and download it
        const [exists] = await usersFile.exists();
        
        if (exists) {
            const [content] = await usersFile.download();
            users = JSON.parse(content.toString());
        }

        // 2. Check if the user already exists in the array
        const userExists = users.some(u => u.username === safeUsername);

        if (userExists) {
            return res.status(409).json({
                message: 'Username already exists. Please choose another.'
            });
        }

        // 3. Add new user to the array
        users.push({
            username: safeUsername,
            password: password,
            createdAt: new Date().toISOString()
        });

        // 4. Save the updated JSON array back to Cloud Storage
        await usersFile.save(JSON.stringify(users, null, 2), {
            contentType: 'application/json'
        });

        res.json({ message: 'User registered successfully in users.json!' });

    } catch (err) {
        console.error('Cloud Storage Error:', err);
        res.status(500).json({ message: 'Error processing JSON database' });
    }
});

const PORT = 3000;
app.listen(PORT, '0.0.0.0', () => {
    console.log(`Backend running on port ${PORT}`);
});