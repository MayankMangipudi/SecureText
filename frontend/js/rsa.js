async function generateRsaKeys() {
    try {
        const data = await window.api.generateRsaKeys();
        return {
            publicKey: data.public_key,
            privateKey: data.private_key
        };
    } catch (error) {
        throw error;
    }
}

async function encryptRsa(plaintext, publicKey) {
    try {
        const data = await window.api.rsaEncrypt(plaintext, publicKey);
        return data.ciphertext;
    } catch (error) {
        throw error;
    }
}

async function decryptRsa(ciphertext, privateKey) {
    try {
        const data = await window.api.rsaDecrypt(ciphertext, privateKey);
        return data.plaintext;
    } catch (error) {
        throw error;
    }
}

// Export functions
window.rsa = {
    generateKeys: generateRsaKeys,
    encrypt: encryptRsa,
    decrypt: decryptRsa
};