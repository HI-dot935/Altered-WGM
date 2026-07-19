// Add a spinner element (injected dynamically)
function showSpinner(resultDiv) {
    resultDiv.innerHTML = `
        <div style="text-align:center; padding:10px;">
            <span style="display:inline-block; width:20px; height:20px; border:3px solid #ff00c8; border-top:3px solid transparent; border-radius:50%; animation: spin 1s linear infinite;"></span>
            <span style="color:#ff00c8; margin-left:10px;">Scanning...</span>
        </div>
    `;
}

// In lookup(), replace "⏳ scanning..." with showSpinner(resultDiv)
// Also add smooth scroll on sidebar click
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});
