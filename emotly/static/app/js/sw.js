/*
 * Emotly Service Worker.
 *
 * DEED
 */

function L(msg) {
    console.log(`Emotly SW: ${msg}`);
}

// EMOTLY_CACHE_NAME should also be used in the UI
// to identify the version.
var EMOTLY_CACHE_NAME = "pwa-dev-client-20160508-3";
var EMOTLY_CACHE_FLES = [
    '/static/app/pwa', '/static/app/ext/bootstrap/css/bootstrap.min.css',
    '/static/app/css/emotly.css', '/static/app/ext/js/jquery/jquery-1.12.2.min.js',
    '/static/app/ext/bootstrap/js/bootstrap.min.js',
    '/static/app/js/emotly.js', '/static/app/js/emotly-sa.js',
    '/static/app/img/dandelion.jpg', '/static/app/img/sloth.jpg',
    '/static/app/ext/css/ie10-viewport-bug-workaround.css',
    '/static/app/ext/js/ie10-viewport-bug-workaround.js',
    '/static/app/ext/bootstrap/fonts/glyphicons-halflings-regular.woff2',
    '/static/app/ext/js/moment-with-locales.min.js'
];

L(`booted up, cache version ${EMOTLY_CACHE_NAME}`);

// Install handler.
self.addEventListener('install', function(e) {
    L('install');
    e.waitUntil(
        caches.open(EMOTLY_CACHE_NAME).then(function(c) {
            L('cache opened');
            return c.addAll(EMOTLY_CACHE_FLES);
        }));
});

// Activate handler.
// We get rid of all the caches when this event fires, with
// the sole exception of the CURRENT cache and whatever else
// is specified into the cacheWhitelist array.
self.addEventListener('activate', function(event) {
    L('activate');

    // Populate with eventual stuff to keep.
    var cacheWhitelist = [EMOTLY_CACHE_NAME];

    event.waitUntil(caches.keys().then(function(cacheNames) {
        return Promise.all(cacheNames.map(function(cacheName) {
            if (cacheWhitelist.indexOf(cacheName) === -1) {
                L(cacheName + " is gonna be deleted");
                return caches.delete(cacheName);
            }
            })
        );
        })
    );
});

// Fetch handler.
this.addEventListener('fetch', function(event) {
  L('fetch');

  // This is a pass-through for every Request that has an X-EMOTLY header.
  // X-EMOTLY requests should be the ones coming from emotly.js.
  //
  // TODO: This might be a security issue given the open file...:)
  if (event.request.headers.get('X-EMOTLY')) {
    L(`fetch pass-through for ${event.request.url}`);
    return;
  }

  var response;
  event.respondWith(caches.match(event.request).catch(function() {
    return fetch(event.request);
  }).then(function(r) {
    response = r;
    caches.open(EMOTLY_CACHE_NAME).then(function(cache) {
      cache.put(event.request, response);
    });
    return response.clone();
  }).catch(function() {
    console.log(`!!! Returning the sloth for URL: ${response.url}`);
    return caches.match('/static/app/img/sloth.jpg');
  }));
});

// self.addEventListener('message', function handler (event) {
//     console.log('OKOK From SW: ' + event.data);
//     if (event.data == 'ONE') {
//       console.log('ONE IS CONFIRMED!!!');
//       event.ports[0].postMessage('TWO');
//     }
// });
