/*
 * EmotlyCache instance
 */
const DB_NAME = 'emotly';
const DB_VERSION = 1; // Use a long long for this value
const DB_STORE_EMOTLY = 'emotly';

class EmotlyCache {
  /*
   * Open connection to the indexedDB and create the emotly object store.
   */
  static openDB() {
    return new Promise(function(resolve, reject) {
      var db;
      var request = indexedDB.open(DB_NAME, DB_VERSION);
      request.onupgradeneeded = function(e) {
        db = e.target.result;
        e.target.transaction.onerror = indexedDB.onerror;
        if(db.objectStoreNames.contains(DB_STORE_EMOTLY)) {
          db.deleteObjectStore(DB_STORE_EMOTLY);
        }
        var store = db.createObjectStore(DB_STORE_EMOTLY, { keyPath: 'id',
                                         autoIncrement: true });
      };
      request.onsuccess = function(e) {
        db = e.target.result;
        console.log("openDb DONE");
        resolve();
      };
      request.onerror = function(e) {
        reject("Couldn't open DB");
      };
    } /* Promise scope. */
   ); /* Promise () */
 } /* OpenDB*/

  /*
   * Add emotly to emotly object store in the indexedDB.
   */
  static addEmotly(nickname, timestamp, mood) {
    var openDBrequest = indexedDB.open(DB_NAME, DB_VERSION);
      openDBrequest.onsuccess = function(e) {
        var db = e.target.result;
        var obj = { nickname: nickname, mood: mood, timestamp: timestamp };
        var store = db.transaction(DB_STORE_EMOTLY, "readwrite").objectStore(DB_STORE_EMOTLY);
        var addRequest = store.add(obj);

        addRequest.onsuccess = function () {
          console.log("Insertion in DB successful id: ", addRequest.result);
          db.close();
        };
        addRequest.onerror = function() {
          console.error("addEmotly error", this.error);
        };
      };  /* openDB request onsuccess */
      openDBrequest.onerror = function(e) {
        reject("Couldn't open DB");
      };
  }  /* addEmotly */

  /*
   * Get the number of emotlies in the object store.
   */
  static getEmotlyStoreNumber() {
    return new Promise(function(resolve, reject) {
      var openDBrequest = indexedDB.open(DB_NAME, DB_VERSION);
      openDBrequest.onsuccess = function(e) {
        var db = e.target.result;
        var store = db.transaction(DB_STORE_EMOTLY, "readonly").objectStore(DB_STORE_EMOTLY);
        var countRequest = store.count();
        countRequest.onsuccess = function () {
          db.close();
          resolve(countRequest.result);
        };
        countRequest.onerror = function() {
          console.error("getEmotly count error", this.error);
        };
      };  /* openDB request onsuccess */
      openDBrequest.onerror = function(e) {
        reject("Couldn't open DB");
      };
    } /* Promise scope. */
   ); /* Promise () */
  }

  /*
   * Delete all the emotlies from the object store.
   */
  static deleteAllEmotlies() {
    return new Promise(function(resolve, reject) {
      var openDBrequest = indexedDB.open(DB_NAME, DB_VERSION);
      openDBrequest.onsuccess = function(e) {
        var db = e.target.result;
        var store = db.transaction(DB_STORE_EMOTLY, "readwrite").objectStore(DB_STORE_EMOTLY);
        var clearRequest = store.clear();
        clearRequest.onsuccess = function () {
          console.log("Deleted all emotlies.");
          db.close();
          resolve();
        };
        clearRequest.onerror = function() {
          console.error("error deleting emotlies", this.error);
        };
      }; /* openDB request onsuccess */
      openDBrequest.onerror = function(e) {
        reject("Couldn't open DB");
      };
    } /* Promise scope. */
   ); /* Promise () */
  }

  /*
   * Delete the first emotly from the object store.
   */
  static deleteFirstEmotly() {
    return new Promise(function(resolve, reject) {
      var openDBrequest = indexedDB.open(DB_NAME, DB_VERSION);
      openDBrequest.onsuccess = function(e) {
        var db = e.target.result;
        var store = db.transaction(DB_STORE_EMOTLY, "readwrite").objectStore(DB_STORE_EMOTLY);
        store.openCursor().onsuccess = function(event) {
          var cursor = event.target.result;
          if (cursor) {
            var deleteRequest = cursor.delete(cursor.primaryKey);
            deleteRequest.onsuccess = function() {
              console.log("removed id: ", cursor.primaryKey);
              db.close();
              resolve();
            };
            deleteRequest.onerror = function(e) {
              reject("Couldn't delete first element");
            };
          }
        } /* Cursor iterator */
      }; /* openDB request onsuccess */
      openDBrequest.onerror = function(e) {
        reject("Couldn't open DB");
      };
     } /* Promise scope. */
    ); /* Promise () */
  }


  /*
   * Get all the emotlies from the object store.
   */
  static getAllEmotlies() {
    return new Promise(function(resolve, reject) {
      var openDBrequest = indexedDB.open(DB_NAME, DB_VERSION);
      openDBrequest.onsuccess = function(e) {
        var db = e.target.result;
        var trans = db.transaction(DB_STORE_EMOTLY, "readonly")
        var store = trans.objectStore(DB_STORE_EMOTLY);
        var emotlies = new Array();
        trans.oncomplete = function(evt) {
          resolve(emotlies);
        };

        var cursorRequest = store.openCursor();
        cursorRequest.onerror = function(error) {
          reject(error);
        };
        cursorRequest.onsuccess = function(evt) {
          var cursor = evt.target.result;
          if (cursor) {
            emotlies.push(new Emotly(cursor.value.nickname,
                                     cursor.value.timestamp, cursor.value.mood));
            cursor.continue();
          }
        }
      } /* OpenDB request success */
    } /* Promise scope. */
    ); /* Promise () */
  }

}
