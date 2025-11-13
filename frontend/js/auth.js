// Check if user is already logged in
function checkAuth() {
    const token = localStorage.getItem('token');
    if (token) {
        // Redirect to dashboard if already logged in
        window.location.href = 'dashboard.html';
    }
}

// Register new user
async function register(username, password) {
    try {
        const data = await window.api.register(username, password);
        showMessage('Registration successful! Please login.', 'success');
        return true;
    } catch (error) {
        showMessage(error.message, 'error');
        return false;
    }
}

// Login user
async function login(username, password) {
    try {
        const data = await window.api.login(username, password);
        
        // Store token
        localStorage.setItem('token', data.access_token);
        localStorage.setItem('username', username);
        
        // Redirect to dashboard
        window.location.href = 'dashboard.html';
    } catch (error) {
        showMessage(error.message, 'error');
    }
}

// Logout user
function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    window.location.href = 'index.html';
}

// Show message to user
function showMessage(message, type) {
    const messageDiv = document.getElementById('message');
    if (messageDiv) {
        messageDiv.textContent = message;
        messageDiv.className = `message ${type}`;
        messageDiv.style.display = 'block';
        
        // Hide after 3 seconds
        setTimeout(() => {
            messageDiv.style.display = 'none';
        }, 3000);
    }
}

// Verify token is valid (for dashboard)
async function verifyAuth() {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = 'index.html';
        return null;
    }

    try {
        const user = await window.api.getMe();
        return user;
    } catch (error) {
        console.error('Auth verification failed:', error);
        // Token invalid or expired, logout
        logout();
        return null;
    }
}