// Файл подключается в теги head html-страницы.
// Он нужен, чтобы запустить работу Service Worker и проверить её поддержку у клиента.

// Функция проверки, доступна ли работа Service Worker у клиента. Доступность зависит от версии браузера или OC.
function isSupported() {
    if (!('serviceWorker' in navigator)) {
        return;
    }
    return true;
}

// Функция регистрирует Service Worker. В случае успешной регистрации или ошибки выводим лог в консоль.
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

// Запуск Service Worker происходит после загрузки всей страницы событием 'load'.
window.addEventListener('load', function () {
    const supported = isSupported();
    if (supported) {
        registerSW();
    }
});

