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
        })
    .catch(function(err) {
            console.log("Error in registering the SW: ", err);
    });}
    else {
        alert("Your browser ain't support ServiceWorkers yet.");
    }

});

