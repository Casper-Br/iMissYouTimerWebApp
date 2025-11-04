# iMissYouTimer
#### Description:
My project is a timer in which a user can submit an amount of time in days hours minutes seconds format.
This time is submitted to a backend server.
This time is then used for a countdown timer which counts down to zero.
The time is counted down on both the frontend and the backend, in case the server ever stops the time is also saved to a database with a timestamp. This time and timestamp can then be retreived by the server to figure out how much time elapsed while the server was offline. This is to ensure the timer keeps tracking accurately even if the server goes offline.
Both the frontend and the backend calculate the time increments. This is so that the frontend does not have to continuously call the backend. The frontend calls the backend for the remaining time and updates it every now and then to make sure the timers are still in sync.
The time remaining is displayed on the frontend in days hours minutes seconds format.

#### index.html:

The HTML document is just a standard barebones HTML webpage.
There are some standard HTML and meta tags and a link tag for the CSS stylesheet and script.js
The most important elements are the two buttons on the page.
The submitBtn and syncBtn. The submitBtn allows you to submit the values inserted into the input fields for
days, hours, months and seconds. The submitBtn id is linked to a POST request in javascript.

The syncBtn allows you to request the values from the timer on the backend and update the frontend with those values. The syncBtn id is linked to a GET request in javascript.

All the input tags are for the days, hours, minutes and seconds to be input.
These are linked to the javascript and python to be used in further calculations.
The timerDisplay id is used to display the remaining time in days, hours, minutes, seconds format.

#### styles.css:

The styles.css sheet is very simplistic and can later be modified according to the design choice.
It currently only serves as a placeholder with some minimal visual changes to the html and by setting the font.

#### app.py:
app.py is the backend of the server, it is made using python, SQLAlchemy and Flask.
Lines 1-3 are used to import all the necessary resources, Flask, request module, jsonify, SQLAlchemy and datetime.

Line 5 creates the Flask app instance. static_folder='' defines where the necessary static files are. 
static_url_path='' makes the static files accessible at the root /.

Line 8-10 sets up the SQLite database. The database is named timer.db, SQLALCHEMY_TRACK_MODIFICATIONS is disabled.
The database and Flask app are then connected by SQLAlchemy.

Lines 13-16 Create the Timer model allowing an id, duration_seconds, and start_time to be saved.
The id is the primary key, useful for scaling the app.
the duration_seconds saves how long the timer is in seconds.
start_time saves the exact time at which the timer was started.

Lines 19-20 Create a table for Timer if there isn't one already.

Lines 22-31 Reads the JSON data sent by the javascript for the timer and converts it into integers for days, hours, minutes, seconds, returns an error if invalid.

Lines 34-35 Failsafe to make sure the entered values are not negative. Returns error if values are negative.

Line 37 converts the time from days, hours, minutes, seconds format to seconds.

Lines 40-41 Failsafe, ensures timer is not zero.

Line 43 Creates a timestamp in UTC.

Lines 45-54 This retrieves the first timer from the database. This code only works with a single timer. For scaling this should be updated. If there is no timer one is created and added to the database. If a timer does exist the timer values are updated.

Lines 56-72 Accessed using GET method, requests the amount of time remaining. If there is no timer or start time in database returns 0 seconds. start_time is made timezone-aware because SQLite removes timezone info. It is set to UTC time, which can be assumed because it is also set to UTC time before saving. Remaining time is calculated from database by using start_time and current time. If there is no time remaining it returns 0, if there is time remaining it will return the remaining seconds as JSON

Lines 74-76 Makes sure the standard index.html is returned when visiting '/'

Lines 78-79 Run the app, debug is currently set to true. Should be set to false before commercial use.

#### script.js:

Line 1 declares the variable timerInterval

Lines 3-15 The formatTime function is defined here, it takes a total amount of seconds and converts it into dd:hh:mm:ss format. First the days hours minutes and seconds are calculated, they are each then converted to a two digit string with padstart.
The resulting dd:hh:mm:ss string is returned.

Lines 17-31 The startLocalCountdown function is defined here. This function keeps track of a timer on the front-end (To reduce the amount of necessarry calls to the backend to retrieve remaining time). The total seconds in the timer goes down by 1 every second. The total time remaining is displayed on the frontend (using the formatTime function). The timer is stopped when the time remaining reaches 0.

Lines 33-42 The fetchRemainingTime function is defined here. It fetches the time remaining from the backend with a GET request to /get-remaining-time (the timer on the backend is seen as the "primary" timer). A JSON response is received and the remaining_seconds value is returned. If it fails, the error is logged and it returns 0.

Lines 44-79 The ability for a user to submit time to the timer is defined here. There is an eventlistener for the Submit Time button. When pressed the values that have been submitted are parsed, if they are empty or invalid they are defaulted to 0. There are checks set up to prevent inserting negative time or zero time. The submit button is temporarily disabled on click to prevent double submitting the data. A POST request is made to /submit-time with the submitted time. After submitting, the remaining time is fetched and the local countdown is started. If there are any errors they are logged and the submit time button is reenabled.

Lines 81-84 Add an event listener to the syncBtn that fetches the remaining time from the backend and resyncs the local countdown timer.

Lines 86-89 Whenever the window is loaded it immediatly checks if there is any time remaining on the backend timer. If so it will start the local countdown timer and display the correct values on the frontend.

#### Design choices
The project is mostly a proof of concept. It can be scaled to be used by multiple users, using many different timers. These timers would still be stored in the database, except with a unique key for each user. This was not yet implemented due to time constraints.

The decision to have a timer on both the frontend and the backend was made to reduce server load. The frontend timer can be updated with values from the backend timer to fix any desync.

The decision to store the time remaining in a database with a timestamp was made incase the server ever shuts off. This way submitted timers will not be lost upon restart.

SQLAlchemy is used to avoid manual SQL and to allow for more easy scaling to multiple users in the future.

A decision was made to not set an upper limit on the values for the timer, this is because for example; a user might prefer subimitting 30 hours instead of 1 day and 6 hours.

The code timer.query.first in app.py only works with one timer, if there are multiple timers due to multiple users this needs to be changed. It can be fixed with unique keys for each user.

There are currently barely any security implementations, if this project were to be opened to the public these implementations have to be made first.