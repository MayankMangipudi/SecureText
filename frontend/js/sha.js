async function hashSha256(text) {
    try {
        const data = await window.api.sha256Hash(text);
        return data.hash;
    } catch (error) {
        throw error;
    }
}

// Export functions
window.sha = {
    hash: hashSha256
};