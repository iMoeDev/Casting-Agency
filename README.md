# Casting Agency API

## Motivation for the Project

The **Casting Agency API** is designed to help casting directors manage actors and movies efficiently. The API allows users with different permission levels to **view, add, update, and delete actors and movies**, ensuring secure role-based access control (RBAC) for different user roles.

This project was developed as part of a **full-stack web application**, where the backend is powered by **Flask**, and authentication is handled using **Auth0**. The frontend, built with **React.js**, interacts with this API to provide a user-friendly interface.

---

## Hosted API URL

The API is currently deployed on **Heroku**:

```
https://finalone-6c4264b75abb.herokuapp.com
```

To access the API, append endpoints like `/api/movies` or `/api/actors`.

Example:

```
GET https://finalone-6c4264b75abb.herokuapp.com/api/movies
```

**Note:** Authentication is required to interact with most endpoints.

---

## API Endpoints

The API provides the following endpoints:

### **Actors**

#### **GET** `/api/actors`

- Retrieves a list of all actors.
- Requires `view:actors` permission.

**Example Response:**

```json
{
  "success": true,
  "actors": [
    {"id": 1, "name": "John Doe", "age": 35, "gender": "Male"},
    {"id": 2, "name": "Jane Smith", "age": 28, "gender": "Female"}
  ]
}
```

#### **POST** `/api/actors`

- Adds a new actor.
- Requires `add:actors` permission.

**Request Body:**

```json
{
  "name": "New Actor",
  "age": 30,
  "gender": "Male"
}
```

**Example Response:**

```json
{
  "success": true,
  "created": 3,
  "actor": {
    "id": 3,
    "name": "New Actor",
    "age": 30,
    "gender": "Male"
  }
}
```

#### **PATCH** `/api/actors/<actor_id>`

- Updates an actor's details.
- Requires `patch:actors` permission.

#### **DELETE** `/api/actors/<actor_id>`

- Deletes an actor.
- Requires `delete:actors` permission.

### **Movies**

#### **GET** `/api/movies`

- Retrieves a list of all movies.
- Requires `view:movies` permission.

**Example Response:**

```json
{
  "success": true,
  "movies": [
    {"id": 1, "title": "Inception", "release_date": "2010-07-16"},
    {"id": 2, "title": "Interstellar", "release_date": "2014-11-07"}
  ]
}
```

#### **POST** `/api/movies`

- Adds a new movie.
- Requires `add:movies` permission.

**Request Body:**

```json
{
  "title": "New Movie",
  "release_date": "2025-01-01"
}
```

#### **PATCH** `/api/movies/<movie_id>`

- Updates movie details.
- Requires `patch:movies` permission.

#### **DELETE** `/api/movies/<movie_id>`

- Deletes a movie.
- Requires `delete:movies` permission.

### **User Authentication**

#### **GET** `/api/user-info`

- Retrieves user details from the authentication token.


---

## **Authentication & RBAC Setup**
The API uses **Auth0** for authentication and role-based access control (RBAC). To set up authentication, follow these steps:

### **1. Create an Auth0 Account & Application**
- Sign up at [Auth0](https://auth0.com/)
- Create a new **Regular Web Application**
- Configure the **Allowed Callback URLs** to include:
  ```
  http://localhost:3000
  https://finalone-6c4264b75abb.herokuapp.com
  ```

### **2. Define API & Permissions**
- In the Auth0 dashboard, go to **APIs** → **Create API**
- Name: `Casting Agency API`
- Identifier: `coffee`
- Grant Types: `Authorization Code`
- Add permissions:
  - `view:movies` → View movies
  - `add:movies` → Add movies
  - `patch:movies` → Edit movies
  - `delete:movies` → Delete movies
  - `view:actors` → View actors
  - `add:actors` → Add actors
  - `patch:actors` → Edit actors
  - `delete:actors` → Delete actors

### **3. Configure Roles**
Define roles and assign them permissions:
- **Casting Assistant:** `view:movies`, `view:actors`
- **Casting Director:** All permissions except `delete:movies`
- **Executive Producer:** All permissions



Use the returned token in API requests:
```sh
curl --request GET \
  --url http://127.0.0.1:5000/api/movies \
  --header 'Authorization: Bearer YOUR_ACCESS_TOKEN'
```

---

## Project Dependencies

This project relies on the following dependencies:

### **Backend Dependencies**

- Python 3.10
- Flask
- Flask-CORS
- SQLAlchemy
- PostgreSQL
- Gunicorn (for production server hosting)
- Auth0 (for authentication & authorization)

### **Frontend Dependencies**

- React.js
- Auth0 React SDK
- Fetch API for making API requests

---

## **Local Development Setup**

Follow these steps to set up and run the project locally:

### **1. Clone the Repository**

```sh
git clone https://github.com/iMoeDev/Casting-Agency.git
cd Casting-Agency/backend
```

### **2. Set Up a Virtual Environment**

```sh
python -m venv myenv
source myenv/bin/activate  # macOS/Linux
myenv\Scripts\activate  # Windows
```

### **3. Install Dependencies**

```sh
pip install -r requirements.txt
```

### **4. Set Up Environment Variables**

Create a `setup.sh` file and define the required environment variables:

```sh

export FLASK_APP='api.py' # Don't change this
export FLASK_ENV='development' # Change it to 'testing' if you want to migrate a test database
export AUTH0_DOMAIN="Enter your AUTH0_DOMAIN" 
export API_AUDIENCE='Enter your API Audience' 
export DB_URL="postgresql://postgres:password@localhost:5432/agency" #Change username & password
export DB_TEST_URL="postgresql://postgres:password@localhost:5432/casting_test" #Change username & password
```

Load environment variables:

```sh
source setup.sh  # macOS/Linux
```

### **Frontend Environment Variables**

The frontend also requires environment variables. Create a `.env` file inside the frontend directory and add:

```sh
REACT_APP_AUTH0_DOMAIN=dev-hsd210wqnr1cmu4f.us.auth0.com
REACT_APP_AUTH0_CLIENT_ID=XB9N8QSz5Js70hHK9aDLVelEb0pCTGbT
REACT_APP_AUTH0_AUDIENCE=coffee
```

Ensure you update these values based on your Auth0 setup.

---

## **5. Database Setup**

Run database migrations:

```sh
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

**To migrate the test database:**

1. **Drop all tables in the production database**.
2. **Remove the `migrations` folder**.
3. **Re-run migrations**:

```sh
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

---

### **6. Run the Development Server**

```sh
flask run
```

The API will be available at:

```
http://127.0.0.1:5000
```

---

## **Testing**

### **Local Testing**

Run the following command to test the API locally:

```sh
python test.py
```

### **Testing on Heroku**

To run tests using Heroku endpoints, use:

```sh
Agency.postman_collection.json
```

**Tests Include:**

- Successful responses for each endpoint.
- Error responses for invalid requests.
- RBAC tests to ensure access control is enforced.

---





