#!/bin/bash

# ---- Date & Time ----
echo "Date & Time: $(date)" > log.txt

# ---- Disk usage ----
echo "" >> log.txt
echo "Disk Usage:" >> log.txt
df -h >> log.txt

# ---- Logged in user ----
echo "" >> log.txt
echo "Current User: $(whoami)" >> log.txt


# ---- Directory check ----
if [ ! -d "deploy_app" ]; then
    mkdir deploy_app
    echo "deploy_app directory created"
fi

# ---- Move log file ----
mv log.txt deploy_app/

echo "System check completed. Log moved to deploy_app/"





<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Secure Login | Premium Portal</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

    <style>
        :root {
            --primary: #4f46e5;
            --primary-hover: #4338ca;
            --bg-gradient: radial-gradient(circle at top left, #f8fafc, #cbd5e1);
            --card-bg: rgba(255, 255, 255, 0.8);
            --text-main: #1e293b;
            --text-muted: #64748b;
        }

        * {
            box-sizing: border-box;
            font-family: 'Inter', sans-serif;
        }

        body {
            margin: 0;
            height: 100vh;
            background: var(--bg-gradient);
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
        }

        /* Subtle background shapes for depth */
        body::before {
            content: "";
            position: absolute;
            width: 300px;
            height: 300px;
            background: linear-gradient(135deg, #6366f1, #a855f7);
            border-radius: 50%;
            top: -100px;
            right: -50px;
            z-index: -1;
            filter: blur(80px);
            opacity: 0.4;
        }

        .card {
            background: var(--card-bg);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            width: 100%;
            max-width: 400px;
            padding: 40px;
            border-radius: 24px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.3);
            animation: slideUp 0.6s ease-out;
        }

        @keyframes slideUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        h2 {
            text-align: center;
            color: var(--text-main);
            margin-bottom: 8px;
            font-size: 28px;
            font-weight: 700;
        }

        p.subtitle {
            text-align: center;
            color: var(--text-muted);
            font-size: 14px;
            margin-bottom: 32px;
        }

        .input-group {
            position: relative;
            margin-bottom: 20px;
        }

        label {
            font-size: 13px;
            font-weight: 600;
            color: var(--text-main);
            margin-bottom: 8px;
            display: block;
        }

        input {
            width: 100%;
            padding: 12px 16px;
            border-radius: 12px;
            border: 1px solid #e2e8f0;
            background: rgba(255, 255, 255, 0.9);
            font-size: 15px;
            transition: all 0.2s ease;
            outline: none;
        }

        input:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 4px rgba(79, 70, 229, 0.1);
        }

        /* Password toggle style */
        .password-container {
            position: relative;
        }

        .toggle-password {
            position: absolute;
            right: 12px;
            top: 50%;
            transform: translateY(-50%);
            cursor: pointer;
            color: var(--text-muted);
            font-size: 14px;
        }

        button {
            width: 100%;
            padding: 14px;
            background: var(--primary);
            border: none;
            border-radius: 12px;
            color: white;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.1s ease, background 0.2s ease;
            margin-top: 10px;
        }

        button:hover {
            background: var(--primary-hover);
        }

        button:active {
            transform: scale(0.98);
        }

        #error {
            margin-top: 16px;
            color: #ef4444;
            font-size: 13px;
            text-align: center;
            min-height: 18px;
            font-weight: 500;
        }

        .footer-text {
            text-align: center;
            margin-top: 24px;
            font-size: 13px;
            color: var(--text-muted);
        }

        .footer-text a {
            color: var(--primary);
            text-decoration: none;
            font-weight: 600;
        }
    </style>
</head>
<body>

<div class="card">
    <h2>Welcome Back</h2>
    <p class="subtitle">Please enter your details to sign in.</p>

    <form id="loginForm">
        <div class="input-group">
            <label for="username">Username</label>
            <input type="text" id="username" placeholder="e.g. jdoe123" required>
        </div>

        <div class="input-group">
            <label for="password">Password</label>
            <div class="password-container">
                <input type="password" id="password" placeholder="••••••••" required>
                <i class="fa-regular fa-eye toggle-password" id="eyeIcon"></i>
            </div>
        </div>

        <button type="submit">Sign In</button>
        <div id="error"></div>
    </form>

  
</div>

<script>
    const form = document.getElementById('loginForm');
    const error = document.getElementById('error');
    const passwordInput = document.getElementById('password');
    const eyeIcon = document.getElementById('eyeIcon');

    // Toggle Password Visibility
    eyeIcon.addEventListener('click', () => {
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        eyeIcon.classList.toggle('fa-eye');
        eyeIcon.classList.toggle('fa-eye-slash');
    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        error.textContent = '';
        
        const usernameInput = document.getElementById('username');
        const username = usernameInput.value.trim();
        const password = passwordInput.value.trim();

        // Regex: letters and numbers only
        const passwordRegex = /^[a-zA-Z0-9]+$/;

        if (!passwordRegex.test(password)) {
            error.textContent = 'Password must be alphanumeric only.';
            return;
        }

        // Show a "loading" state on the button
        const submitBtn = form.querySelector('button');
        const originalBtnText = submitBtn.textContent;
        submitBtn.textContent = 'Verifying...';
        submitBtn.disabled = true;

        try {
            const response = await fetch('http://34.83.26.64:3000/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });

            // Handling the case where backend isn't real/setup yet
            if (!response.ok && response.status === 404) {
                throw new Error('Endpoint not found');
            }

            const data = await response.json();
            alert(data.message);

            usernameInput.value = '';
            passwordInput.value = '';

        } catch (err) {
            error.textContent = 'Unable to connect to the server.';
            console.error('Fetch error:', err);
        } finally {
            submitBtn.textContent = originalBtnText;
            submitBtn.disabled = false;
        }
    });
</script>

</body>
</html>