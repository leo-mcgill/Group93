window.addEventListener('DOMContentLoaded', () => {
    const canvases = document.querySelectorAll('canvas');
    const targetWidth = 20;
    const targetHeight = 30;

    canvases.forEach(canvas => {
        const src = canvas.getAttribute('data-src');
        const ctx = canvas.getContext('2d');
        const img = new Image();
        img.crossOrigin = 'anonymous'; // allow cross-origin if necessary
        img.src = src;

        img.onload = () => {
            canvas.width = targetWidth;
            canvas.height = targetHeight;

            // Draw the image very small (downscaled)
            ctx.drawImage(img, 0, 0, targetWidth, targetHeight);
        };
    });
});
