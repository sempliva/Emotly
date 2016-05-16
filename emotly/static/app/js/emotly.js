/*
 * MIT License
 *
 * Copyright (c) 2016 Emotly Contributors
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

/*
 * Emotly - Frontend
 *
 * The internal logic is being managed by the ServiceWorkers file
 * in sw.js.
 */

var emotly_jwt = null;    // JWT global.
var emotly_allMoods = null;  // Moods global.
var emoService = new EmotlyService();

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

  // Customize the template for the PWA.
  $('#navbrandtext').text('Update 20160508');
  $('#emotlybrand').attr('href', '/static/app/pwa');
  $('.liLogin').show();

  // Check for LocalStorage support.
  if (!window.localStorage) {
    showAlert('danger', 'LocalStorage APIs are not suppored. Really?!');
    setProgressBarStatus('danger');
  }

  // If the Fetch API are not supported just yell. Everything is gonna fail.
  if (!self.fetch) {
    showAlert('danger',
              'Fetch APIs are not supported. Nothing is gonna work.', 15);
    setProgressBarStatus('danger');
  }

  // Check if we have to show the login dialog.
  var hash = window.location.hash.substring(1).toLowerCase();
  if (hash === 'showlogin') {
    $('#loginModal').modal('toggle');
  }

  setProgressBarStatus('warning', true);

  // Populate the main list of emotlies.
  EmotlyService.getEmotlies().then(function(EmoArray) {
    EmoArray.forEach(function(s_emotly) {
      setProgressBarStatus('success');
      prependEmotly(s_emotly.nickname, s_emotly.timestamp, s_emotly.mood);
    });
  }).catch(function(e) {
    setProgressBarStatus('danger');
    showAlert('danger', `Error getting the latest emotlies: ${e.message}`, 10);
  });

  // Update the global list of all the available moods.
  EmotlyService.getMoods().then(function(MoodArray) {
    MoodArray.forEach(function(s_mood) {
      $('#ulmoods').append(`<li class='list-group-item'
                             emotly-data-mood-id='${s_mood.id}'>
                             ${s_mood.value}</li>`);
    });
  }).catch(function(e) {
    setProgressBarStatus('danger');
    showAlert('danger', `Error while fetching the moods: ${e.message}`, 10);
  });

  // If the User is logged, set the UI accordingly.
  if (emoService.isLogged()) {
    $('.liLogin').hide();
    $('.liLogout').show();
    $('#navbrandtext').text(`Logged as ${emoService.user.nickname}`);
  }

  $('#alogout').click(logout_button_pressed);
  $('#ulmoods').click(li_mood_selected);
});

/*
 * Logout link handler.
 */
function logout_button_pressed() {
  emoService.logout();
  $('#navbar').collapse('hide');
  $('.liLogin').show();
  $('.liLogout').hide();
  showAlert('success', 'Logged out');
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

  emoService.postLogin(n, p).then(function(t_user) {
    setProgressBarStatus('success');
    showAlert('success', 'Logged in!');
    $('.liLogin').hide();
    $('.liLogout').show();
    $('#navbrandtext').text(`Logged as ${t_user.nickname}`);
  }).catch(function(e) {
    setProgressBarStatus('danger');
    showAlert('danger', `Login error: ${e.message}`, 10);
    $('.liLogin').show();
    $('.liLogout').hide();
  })
}

/*
 * This handler gets called when the user taps on one of the moods to post a
 * new Emotly.
 */
function li_mood_selected(e) {
  setProgressBarStatus('warning', true);
  $('#newEmotlyModal').modal('toggle');
  $('#navbar').collapse('hide');

  // Get the relevant MoodID from the targetElement.
  var mid = $(e.target).attr('emotly-data-mood-id');

  emoService.postNewEmotly(mid).then(function(posted_mood) {
    setProgressBarStatus('success');
    var n = emoService.user.nickname;
    prependEmotly(n, new Date(), posted_mood.value);
  }).catch(function(err) {
    setProgressBarStatus('danger');
    showAlert('danger', err);
    linewemotly.remove();
  });
}

/*
 * Prepend a new Emotly in the list.
 */
function prependEmotly(nickname, timestamp, mood) {
  var d = moment(timestamp).fromNow();
  $('#ulemotlies').prepend(`<li class='list-group-item'>${nickname} feels
                       <strong><cite>${mood}</cite></strong>
                       <span class='badge'>${d}</span></li>`);
}

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
