async function generateAesKey() {
    try {
        const data = await window.api.generateAesKey();
        return data.key;
    } catch (error) {
        throw error;
    }
}

async function encryptAes(plaintext, key) {
    try {
        const data = await window.api.aesEncrypt(plaintext, key);
        return data.ciphertext;
    } catch (error) {
        throw error;
    }
}

async function decryptAes(ciphertext, key) {
    try {
        const data = await window.api.aesDecrypt(ciphertext, key);
        return data.plaintext;
    } catch (error) {
        throw error;
    }
}

// Export functions
window.aes = {
    generateKey: generateAesKey,
    encrypt: encryptAes,
    decrypt: decryptAes
};