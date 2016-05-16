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
 * Emotly Service Abstraction
 */

/*
 * An Emotly, pure and simple.
 */
class Emotly {
  constructor(nickname, timestamp, mood) {
    this.nickname = nickname;
    this.timestamp = timestamp;
    this.mood = mood;
  }
}

/*
 * Sorting function for the array of Emotly.
 */
function emotly_sort(a, b) {
    return new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime();
}

/*
 * A Mood.
 */
class Mood {
  constructor(id, value) {
    this.id = id;
    this.value = value;
  }
}

/*
 * Sorting function for the array of Mood.
 * Order is lexicographic.
 */
function mood_sort(a, b) {
  if (a.value < b.value) { return -1; }
  if (a.value > b.value) { return 1; }

  return 0;
}

/*
 * The logged User.
 *
 * TODO: Pull more data from the service.
 */
class User {
  constructor(nickname, jwt) {
    this.nickname = nickname;
    this.jwt = jwt;
  }
}

var LOCALSTORAGE_PROPERTY = 'emotly_user';

/*
 * EmotlyService instance
 *
 * This class mirrors whatever method the Emotly service provides. For the sake
 * of clarity every method signature is comprised of the actual HTTP method
 * followed by the method name so, for example: getEmotlies is a GET request
 * to the 'emotlies' method/endpoint.
 *
 * Service methods return promises.
 */
class EmotlyService {
  constructor() {
    var emotly_stored_user = JSON.parse(localStorage.getItem(LOCALSTORAGE_PROPERTY));
    if (emotly_stored_user != null) {
      this.user = emotly_stored_user;
    }
  }

  /*
   * Perform a logout by dumping the user data.
   */
  logout() {
    localStorage.removeItem(LOCALSTORAGE_PROPERTY);
    this.user = null;
  }

  /*
   * Check whether the user is currently active.
   */
  isLogged() {
    return this.user != null;
  }

  /*
   * Static GET all the latest global emotlies.
   *
   * TODO: Pagination.
   */
  static getEmotlies() {
    return new Promise(function(resolve, reject) {
      fetch('/api/1.0/emotlies', {
        headers: { 'X-EMOTLY': 'JSONAPI' }
      }).then(function(raw_response) {
        if (raw_response.status != 200) {
          reject(Error(`HTTP ${raw_response.status}`));
        }

        raw_response.json().then(function(json_response) {
          var EmotlyArray = new Array();
          json_response.emotlies.forEach(function(t_emotly) {
            EmotlyArray.push(new Emotly(t_emotly.user.nickname,
                                        t_emotly.created_at, t_emotly.mood));
          });

          // Success: fulfill the promise with the whole array.
          resolve(EmotlyArray.sort(emotly_sort));
        }).catch(function(e) { /* json().catch() */
          reject(Error(`JSON (${e.message})`));
        })
      }).catch(function(e) { /* fetch().catch() */
        reject(Error(`fetch (${e.message})`));
      })
    } /* Promise scope. */
  ); /* Promise() */
  } /* getEmotlies() */

  /*
   * Static GET all moods.
   */
  static getMoods() {
    return new Promise(function(resolve, reject) {
      fetch('/api/1.0/moods', {
        headers: { 'X-EMOTLY': 'JSONAPI'}
      }).then(function(raw_response) {
        if (raw_response.status != 200) {
          reject(Error(`HTTP ${raw_response.status}`));
        }

        raw_response.json().then(function(json_response) {
          var MoodArray = new Array();
          json_response.moods.forEach(function(t_mood) {
            MoodArray.push(new Mood(t_mood.id, t_mood.value));
          });

          // Success: fulfill the promise with the whole array.
          resolve(MoodArray.sort(mood_sort));
        }).catch(function(e) { /* json().catch() */
          reject(Error(`JSON (${e.message})`));
        })
      }).catch(function(e) { /* fetch().catch() */
        reject(Error(`fetch (${e.message})`));
      })
    } /* Promise scope. */
  ); /* Promise() */
  } /* getMoods() */

  /*
   * Attempts to login.
   * Overwrited user credentials in localStorage if the user is already
   * logged in.
   *
   * Returns a Promise with the actual user.
   */
  postLogin(login, password) {
    var thisPointer = this;

    return new Promise(function(resolve, reject) {
      fetch('/api/1.0/login', {
        method: 'post',
        headers: {
          'Content-Type': 'application/json; charset=utf-8',
          'X-EMOTLY': 'JSONAPI'
        },
        body: JSON.stringify({ user_id: login, password: password })
      }).then(function(raw_response) {
        if (raw_response.status != 200) {
          reject(Error(`HTTP ${raw_response.status}`));
        }

        raw_response.json().then(function(json_response) {
          // Check if the JWT structure is valid.
          if (json_response.header && json_response.payload &&
              json_response.signature) {
                var u = new User(json_response.payload.nickname, json_response);
                thisPointer.user = u;
                localStorage.setItem(LOCALSTORAGE_PROPERTY, JSON.stringify(u));
                resolve(u);
              } else {
                reject(Error('invalid JWT'));
              }
        }).catch(function(e) { /* json().catch() */
          reject(Error(`JSON (${e.message})`));
        })

      }).catch(function(e) { /* fetch().catch() */
        reject(Error(`fetch (${e.message})`));
      })
    } /* Promise scope. */
  ); /* Promise() */
  } /* postLogin() */

  /*
   * Posts a new emotly.
   *
   * Returns a Promise with the posted Mood.
   */
  postNewEmotly(mood_id) {
    var thisPointer = this;
    return new Promise(function(resolve, reject) {
      if (thisPointer.user == null) {
        reject(Error('not logged'));
      }

      fetch('/api/1.0/emotlies/new', {
        method: 'post',
        headers: {
          'Content-type': 'application/json; charset=utf-8',
          'X-EMOTLY': 'JSONAPI',
          'X-Emotly-Auth-Token': JSON.stringify(thisPointer.user.jwt)
        },
        body: JSON.stringify({ mood: mood_id })
      }).then(function(raw_response) {
        if (raw_response.status != 200) {
          reject(Error(`HTTP ${raw_response.status}`));
        }

        raw_response.json().then(function(json_response) {
          if (json_response.emotly.mood) {
            resolve(new Mood(mood_id, json_response.emotly.mood));
          } else {
            reject(Error('garbled but valid JSON response'));
          }
        }).catch(function(e) {
          reject(Error(`JSON (${e.message})`));
        }) /* json.catch() */
      }).catch(function(e) {

        // TODO: Here we may want to check for the actual error and eventually
        // fore the user to logout and login again.
        reject(Error(`fetch (${e.message})`));
      }) /* fetch.catch() */

    } /* Promise scope. */
  ); /* Promise() */
  } /* postNewEmotly() */

} /* class EmotlyService */
