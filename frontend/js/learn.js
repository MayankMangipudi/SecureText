// Format hex bytes for display
function formatHexBytes(hexString) {
    return hexString.match(/.{1,2}/g).join(' ').toUpperCase();
}

// Animate number changes
function animateNumber(element, start, end, duration) {
    const startTime = performance.now();
    
    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        const current = Math.floor(start + (end - start) * progress);
        element.textContent = current;
        
        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }
    
    requestAnimationFrame(update);
}

// Export functions
window.learnUtils = {
    formatHexBytes,
    animateNumber
};