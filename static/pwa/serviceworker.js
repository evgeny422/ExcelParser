// This is the "Offline copy of pages" service worker

// Имя кэша для страниц приложения.
const CACHE = "pwabuilder-offline";

// Сторонний модуль для работы с Service Worker. https://github.com/GoogleChrome/workbox.
// Он предоставляет API для более простой настройки Service Worker.
importScripts('/static/pwa/workbox-sw.js');

// Подписка на событие, когда приложение отправляется сообщения в Service Worker.
self.addEventListener("message", (event) =>
{
  // Если при получении данных в сообщении Service Worker прибывает в состоянии ожидания,
  // то при помощи skipWaiting мы выходим из этого ожидания.
  if (event.data && event.data.type === "SKIP_WAITING") {
    self.skipWaiting();
  }
});

// workbox.routing.registerRoute регулирует запросы клиента и запускает для них нужную функцию.
// В данном случае, для любой страниц будет происходить проверка, сохранена ли она в кэше или доступна в онлайн.
// По умолчанию кэшируются только успешные ответы.
workbox.routing.registerRoute(
  new RegExp('/*'),
  new workbox.strategies.StaleWhileRevalidate({
    cacheName: CACHE
  })
);