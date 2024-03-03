function isSupported() {
    if (!('serviceWorker' in navigator)) {
        return;
    }
    return true;
}

function registerSW() {
    navigator.serviceWorker.register('/static/pwa/serviceworker.js').then(
        (registration) => {
            console.log('PWA ServiceWorker registration');
        },
        (error) => {
            console.log('PWA ServiceWorker registration: failed: ', error);
            return false;
        }
    );
    return true;
}

window.addEventListener('load', function () {
    const supported = isSupported();
    if (supported) {
        registerSW();
    }
});

