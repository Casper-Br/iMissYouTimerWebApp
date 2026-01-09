# iMissYou Timer

iMissYou Timer is a full-stack Flask web application that provides a persistent, shared countdown timer using an SQL database and a simple frontend interface

## Everything you need to know before you start

### Login
The app uses HTTP Basic Authentication.

Default login (local development):

Username: us

Password: mypassword1

Changing the password:

You can change the password by either changing the default in app.py or setting the environment variable MY_PASSWORD before running the app. When deploying on for example render.com this can be done using the environment variables in render.

### Running the project locally
1. Clone the repository
2. Create and activate a virtual environment (optional but recommended)
3. Install the dependencies:
   `pip install -r requirements.txt`
4. Run the application
   `python app.py`
5. Open the browser at:
   `http://127.0.0.1:5001`

## Features

- Shared countdown timer
- Backend timer persistence using a SQL database
- Frontend and backend synchronization
- Timer remains accurate across page refreshes
- Built as a deployable full-stack web application
- Password protected

## Tech Stack

- Python
- Flask
- PostgreSQL (production)
- SQLite (local development)
- HTML
- CSS
- JavaScript (ES6+)

## Why I made this

I initially created iMissYou Timer as a final project for my HarvardX CS50x course. Later I wanted to continur developing it and actually deploy it. My goal was to learn full-stack development while building something practical that I could actually use once it was finished.
Through this project, I learned a lot about building web applications from end to end:
- Handling HTTP requests with Flask
- Connecting the frontend and backend so they communicate properly
- Using a database to store and manage data
- Handling user input
- Deploying a live application to Render

One of the most rewarding parts of this project was seeing the app fully deployed online. It’s one thing to test locally on localhost, but having it running live made it much more rewarding. I particularly enjoyed implementing the backend logic and the timer mechanics, and seeing it all work together in a deployed environment was extremely satisfying. Using render to deploy my app was very simple and useful and I will probably use it again.
