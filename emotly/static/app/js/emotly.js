/*
 * Emotly - Frontend
 *
 * The internal logic is being managed by the ServiceWorkers file
 * in sw.js.
 *
 * DEED
 */

$(document).ready(function() {
    /*
     * Attempt to register the SW; if it fails just
     * yell.
     * TODO: Ask the user to download a native client.
     */
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/static/app/sw.js').then(function(reg) {
          console.log("SW registered, scope: ", reg.scope);
          return navigator.serviceWorker.ready;

        }).then(function () {
          console.log('ServiceWorker is READY!');
        }).catch(function(err) {
            console.log("Error in registering the SW: ", err);
    });} else {
        alert("Your browser ain't support ServiceWorkers yet.");
    }

    // Fetch something from the Emotly APIs.
    if (!self.fetch) {
      showAlert('danger', 'Fetch APIs are not supported. Nothing is gonna work.')
      setProgressBarStatus('danger');
    } else {
      setProgressBarStatus('info', true);

      // TODO: Wrap in a Promise. Let's promise. Make me a promise.
      // FIXME: And, please, don't break the promise.
      var fetchInit = { headers: {'X-EMOTLY': 'JSONAPI'} };
      var fetchReq = new Request('/api/1.0/emotlies', fetchInit);

      fetch(fetchReq).then(function(stuff) {
        stuff.json().then(function(js) {
          setProgressBarStatus('success');
          js.emotlies.forEach(function(single_emotly) {
            var ulemotlies = $('#ulemotlies');
            n = single_emotly.user.nickname;
            m = single_emotly.mood;
            ulemotlies.append("<li class='list-group-item'>" + n +
                              "<span class='badge'>" + m + "</span></li>");
          });
        }).catch(function() {
          setProgressBarStatus('warning');
          showAlert('warning', 'Error while parsing emotlies');
        });
      }
    ).catch(function() {
      setProgressBarStatus('warning');
      showAlert('warning', 'Error while fetching emotlies');
    })
    }
});

// Show a message box in the top of the drawing area.
// Type should be one of: success, info, warning, danger
// By default, the box will disappear after 5 seconds.
// TODO: Find a better way to deal with this use case.
function showAlert(type, text) {
  var msgbox = $('#emlmsg');
  msgbox.removeClass('alert-success alert-info alert-warning alert-danger');
  msgbox.addClass('alert-' + type);
  msgbox.text(text);
  msgbox.toggle('slow', function() {
    msgbox.delay(5000).toggle('slow');
  })
}

// Set the progressbar in a specified state.
// status should be one of: success, info, warning, danger
// active specifies animation.
function setProgressBarStatus(status, active = false) {
  var pbar = $('#progressbar');
  pbar.removeClass('active progress-bar-success progress-bar-info\
                    progress-bar-warning progress-bar-danger\
                    progress-bar-striped');
  pbar.addClass('progress-bar-' + status);
  if (active)
    pbar.addClass('active progress-bar-striped');
}

/*
 * This wraps a promise to send/receive messages from the SW.
 */
// function sendMessage(message) {
//   // This wraps the message posting/response in a promise, which will resolve if the response doesn't
//   // contain an error, and reject with the error if it does. If you'd prefer, it's possible to call
//   // controller.postMessage() and set up the onmessage handler independently of a promise, but this is
//   // a convenient wrapper.
//   return new Promise(function(resolve, reject) {
//     var messageChannel = new MessageChannel();
//     messageChannel.port1.onmessage = function(event) {
//       if (event.data.error) {
//         reject(event.data.error);
//       } else {
//         resolve(event.data);
//       }
//     };
//
//     // This sends the message data as well as transferring messageChannel.port2 to the service worker.
//     // The service worker can then use the transferred port to reply via postMessage(), which
//     // will in turn trigger the onmessage handler on messageChannel.port1.
//     // See https://html.spec.whatwg.org/multipage/workers.html#dom-worker-postmessage
//     navigator.serviceWorker.controller.postMessage(message,
//       [messageChannel.port2]);
//   });
// }
//
// /*
//  * This is the handler for the messages coming from the ServiceWorker.
//  */
// function handleServiceWorkerMessage (event) {
//   console.log('Message from the ServiceWorker: ' + event.data);
// }
