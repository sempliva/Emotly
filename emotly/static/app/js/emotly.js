/*
 * Emotly - Frontend
 *
 * The internal logic is being managed by the ServiceWorkers file
 * in sw.js.
 *
 * DEED
 */

var emotly_jwt = null; // JWT global.

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

  $('#navbrandtext').text('Update: login working, pls test.');

  // Check for LocalStorage support.
  if (!window.localStorage) {
    showAlert('danger', 'LocalStorage APIs are not suppored. Really?!');
    setProgressBarStatus('danger');
  }

  // Fetch something from the Emotly APIs.
  if (!self.fetch) {
    showAlert('danger', 'Fetch APIs are not supported. Nothing is gonna work.')
    setProgressBarStatus('danger');
  } else {
    setProgressBarStatus('warning', true);

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

  // Attempt to read the JWT from localStorage
  // localStorage.removeItem('emotly_jwt');
  emotly_jwt = JSON.parse(localStorage.getItem('emotly_jwt'));
  if (emotly_jwt != null) {
    $('#liLogin').hide();
    $('#liLogout').show();
    $('#navbrandtext').text('Logged as ' +
                            emotly_jwt.payload.nickname + '.');
  }

  $('#alogout').click(logout_button_pressed);
});

/*
 * Logout link handler.
 */
function logout_button_pressed() {
  $('#navbar').collapse('hide');
  localStorage.removeItem('emotly_jwt');
  $('#liLogin').show();
  $('#liLogout').hide();
  showAlert('success', 'Logged out');
  emotly_jwt = null;
  $('#navbrandtext').text('');
}

/*
 * Login link handler.
 */
function login_button_pressed() {
  setProgressBarStatus('warning', true);
  $('#loginModal').modal('toggle');
  $('#navbar').collapse('hide');

  // Let's try to login...
  var n = $('#useridinput').val();
  var p = $('#passwordinput').val();

  emotlyLogin(n, p).then(function(jwt_from_emotly) {
    emotly_jwt = jwt_from_emotly;
    localStorage.setItem('emotly_jwt', JSON.stringify(emotly_jwt));
    setProgressBarStatus('success');
    showAlert('success', 'Logged in!');
    $('#liLogin').hide();
    $('#liLogout').show();
    $('#navbrandtext').text('Logged as ' +
                            emotly_jwt.payload.nickname + '.');
  }).catch(function(jwt_error) {
    setProgressBarStatus('danger');
    showAlert('danger', 'Login failed ' + jwt_error);
    $('#liLogin').show();
    $('#liLogout').hide();
  })

  //       fetch('/api/1.0/emotlies/new', {
  //         method: 'post',
  //         headers: {
  //           "Content-type": "application/json; charset=UTF-8",
  //           "auth_token": JSON.stringify(global_token)
  //         },
  //         body: JSON.stringify({
  //           mood: 2,
  //         })
  //       }).then(function(newemotlyresponse) {
  //         showAlert('succes', 'NEW EMOTLY STATUS CODE: ' + newemotlyresponse.status);
  //       });
}

/*
 * This function returns a Promise with the JWT obtained by the Emotly Service.
 *
 * Parameters:
 *  login: it's the email address
 *  password: well, you know!:)
 */
function emotlyLogin(login, password) {
  return new Promise(function(resolve, reject) {
    fetch('/api/1.0/login', {
      method: 'post',
      headers: {
        'Content-type': 'application/json; charset=utf-8',
        'X-EMOTLY': 'JSONAPI' /* Pass-through for the Emotly ServiceWorker. */
      },
      body: JSON.stringify({ user_id: login, password: password})
    }).then(function(raw_response) { /* Fetch success. */
      if (raw_response.status == 200) {
        raw_response.json().then(function(json_response) { /* response.json()
                                                              success. */
          /* We check that the JWT has all the requried fields before
             fulfilling the promise. */
          if (json_response.header && json_response.payload &&
              json_response.signature) {
                /* Fulfill the promise with the whole JWT. */
                resolve(json_response);
              } else { /* The JSON response is OK but it's not a valid JWT. */
                reject(Error('JWT Error: invalid response'));
              }
        }).catch(function(json_error) { /* response.json() error. */
          reject(Error('JWT Error: invalid JSON (' + json_error + ')'));
        });
      } else { /* Fetch response is not 200. */
        reject(Error('JWT Error: invalid return status (' +
               raw_response.status + ')'));
      }
    }).catch(function(fetch_error) { /* Fetch error. */
      reject(Error('JWT Error: fetch/networking error (' + fetch.error + ')'));
    });
  } /* new Promise body. */
); /* Promise() Arguments. */
} /* emotlyLogin() */

/*
 * Show a message box in the top of the drawing area.
 * 'Type' should be one of: success, info, warning, danger.
 * 'Timeout' is in seconds.
 *
 * By default, the box will disappear after 5 seconds.
 * TODO: Find a better way to deal with this use case.
 */
function showAlert(type, text, timeout = 5) {
  var msgbox = $('#emlmsg');
  msgbox.removeClass('alert-success alert-info alert-warning alert-danger');
  msgbox.addClass('alert-' + type);
  msgbox.text(text);
  msgbox.toggle('slow', function() {
    msgbox.delay(timeout * 1000).toggle('slow');
  })
}

/*
 * Set the progressbar in a specified state.
 * 'Status' should be one of: success, info, warning, danger.
 * 'Active' enables the animation.
 */
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
