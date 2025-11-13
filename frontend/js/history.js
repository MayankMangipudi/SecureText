async function loadHistory() {
    try {
        const history = await window.api.getHistory();
        return history.map(item => ({
            ...item,
            expanded: false
        }));
    } catch (error) {
        throw error;
    }
}

function getAlgorithmIcon(algorithm) {
    if (algorithm.includes('AES')) return '🔐';
    if (algorithm.includes('RSA')) return '🔑';
    if (algorithm.includes('SHA')) return '🔒';
    return '📝';
}

function formatTimestamp(timestamp) {
    const date = new Date(timestamp + 'Z'); // Add 'Z' to treat as UTC
    const now = new Date();
    const diff = Math.floor((now - date) / 1000);
    
    if (diff < 60) return 'Just now';
    if (diff < 3600) return Math.floor(diff / 60) + ' mins ago';
    if (diff < 86400) return Math.floor(diff / 3600) + ' hours ago';
    return Math.floor(diff / 86400) + ' days ago';
}

// Export functions
window.historyUtils = {
    load: loadHistory,
    getIcon: getAlgorithmIcon,
    formatTime: formatTimestamp
};