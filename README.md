# Connect-U-Project 
[View Demo](https://youtu.be/5fOqXF_yU9w)
A social media application that allows users to create their own accounts, publish posts, and join groups with other users with similar interests. 

## About the Project
Connect-U-Project is a full-stack application utilizing Flask for the backend and React for the frontend.

### Backend 
The backend is built with Flask, providing a simple REST API using the Flask-RESTful extension for routes defined in `app.py`. It uses several Flask extensions:

* **Flask-SQLAlchemy:** An ORM for defining models and querying table data in `models.py`.
* **Flask-Migrate:** Manages schema migrations.
* **SQLAlchemy-Serializer:** Serializes database models into dictionaries, including or excluding attributes to prevent recursion issues in nested data.
* **Flask-Bcrypt:** Provides hashing abilities for password protection.
* **Flask-Authlib-Client:** Implements Google OAuth2, allowing users to log in/sign up using a Google account.

### Frontend

The frontend is developed using React to create an interactive and dynamic user experience. React Router DOM is used for client side routing configuration and navigation. This library enables the application to handle navigation between different pages seamlessly, without requiring full page reloads, enhancing the user experience by providing smooth transitions and maintaining state across the application.

## Getting Started
To get a local copy of this project up and running follow these simple steps. 

### Prerequisites
* pip: If you have Homebrew installed you can use:

  ```brew install python```

* pyenv

  ```curl https://pyenv.run | bash```

* pipenv 

  ```pip install pipenv```

* npm: If you have Homebrew installed you can use:

  ```brew install node```

### Installation
1. **Backend Setup:**

* The project contains a default `Pipfile` with the necessary dependencies.To download the dependencies for the backend server, run:

```sh
pipenv install
pipenv shell
```

* Run your Flask API on [`localhost:5555`](http://localhost:5555) by running:

```sh
python server/app.py
```

2. **Frontend Setup:** 
* The `package.json` file has been configured with common React application dependencies, including `react-router-dom`. It also sets the `proxy` field to forward requests to `"http://localhost:5555"`.

* To download the dependencies for the frontend client, run:

```sh
npm install --prefix client
```

* Run React app on [`localhost:3000`](http://localhost:3000) by
running:

```sh
npm start --prefix client
```

## Usage
### Basic Functionality

Connect-U allows users to:
* Create an account
* Log in using Google OAuth or `Login` route 
* Create, read, update, and delete posts
* Like and comment on other users posts 
* Join groups with other users who have similar intrests

### User Interface Walkthrough
1. **Home Page:** After logging in, users are directed to the home page where they can create a new post, view all their posts, and edit/delete those posts.
2. **Navigation Bar:** The navigation bar includes links to the home page, all user's posts, and all groups. 
3. **Posts Page:** Users can view posts for all other users.
4. **Groups Page:** Users can view and join groups.
5. **Logout button:** Users can logout of their account and return to the login page.

## Contributing 
Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

If you have a suggestion that would make this project better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement". Thanks again!

## Contact 
Jordan Primas - [email](jorprimas20@gmail.com)
Project Link: [github link](https://github.com/jordanprimas/Connect-U-Project.git)

## Resources
[Flask Application With Google Login](https://realpython.com/flask-google-login/)
[Flask - Google OAuth2 Video](https://www.youtube.com/watch?v=BfYsdNaHrps&t=388s)
[Flask SQLAlchemy Documentation](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/quickstart/)