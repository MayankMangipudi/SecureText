const API_BASE_URL = 'http://127.0.0.1:8000';

// Helper function to make API calls
async function apiCall(endpoint, options = {}) {
    const token = localStorage.getItem('token');
    
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };

    if (token && !options.skipAuth) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            ...options,
            headers
        });

        const data = await response.json();

        if (!response.ok) {
            // Better error handling
            const errorMessage = data.detail 
                ? (Array.isArray(data.detail) 
                    ? data.detail.map(e => e.msg).join(', ') 
                    : data.detail)
                : 'Something went wrong';
            throw new Error(errorMessage);
        }

        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Export for use in other files
window.api = {
    // Auth endpoints
    register: (username, password) => apiCall('/auth/register', {
        method: 'POST',
        body: JSON.stringify({ username, password }),
        skipAuth: true
    }),

    login: (username, password) => apiCall('/auth/login', {
        method: 'POST',
        body: JSON.stringify({ username, password }),
        skipAuth: true
    }),

    getMe: () => apiCall('/auth/me'),

    // AES endpoints
    aesEncrypt: (text, key) => apiCall('/crypto/aes/encrypt', {
        method: 'POST',
        body: JSON.stringify({ text, key })
    }),

    aesDecrypt: (text, key) => apiCall('/crypto/aes/decrypt', {
        method: 'POST',
        body: JSON.stringify({ text, key })
    }),

    generateAesKey: () => apiCall('/crypto/aes/generate_key'),

    // RSA endpoints
    rsaEncrypt: (text, public_key) => apiCall('/crypto/rsa/encrypt', {
        method: 'POST',
        body: JSON.stringify({ text, public_key })
    }),

    rsaDecrypt: (text, private_key) => apiCall('/crypto/rsa/decrypt', {
        method: 'POST',
        body: JSON.stringify({ text, private_key })
    }),

    generateRsaKeys: () => apiCall('/crypto/rsa/generate_keys'),

    // SHA-256 endpoint
    sha256Hash: (text) => apiCall('/crypto/sha256/hash', {
        method: 'POST',
        body: JSON.stringify({ text })
    }),

    // History endpoints
    getHistory: () => apiCall('/history/list'),
    
    clearHistory: () => apiCall('/history/clear', {
        method: 'DELETE'
    }),

    // Learn endpoints - FIXED parameter names
    visualizeAes: (plaintext, key) => apiCall('/learn/aes/visualize', {
        method: 'POST',
        body: JSON.stringify({ plaintext, key })  // Changed from { plaintext, key } object format
    }),

    visualizeRsa: (plaintext) => apiCall('/learn/rsa/visualize', {
        method: 'POST',
        body: JSON.stringify({ plaintext })  // Changed parameter name
    })
};