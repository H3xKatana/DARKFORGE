

# DARKFORGE

DARKFORGE is a full-stack website built with the Django framework, representing a game store with personalized features.

## Installation

To get started, follow these steps:

1. **Install pipenv**: If you haven't already, you can install `pipenv` using pip:
   
   ```
   pip install pipenv
   ```

2. **Clone the Repository**: Clone the DARKFORGE repository using Git:

   ```
   git clone https://github.com/H3xKatana/DARKFORGE.git
   ```

3. **Navigate to the Backend Directory**: Go into the `backend` directory of the cloned repository:

   ```
   cd DARKFORGE/backend
   ```

4. **Create and Activate Virtual Environment**: Use pipenv to create a virtual environment and activate it:

   ```
   pipenv shell
   ```

5. **Install Dependencies**: Once inside the virtual environment, install the project dependencies listed in `requirements.txt`:

   ```
   pipenv install -r requirements.txt
   ```

6. **Navigate to the App Directory**: Go into the `App` directory:

   ```
   cd ../App
   ```

7. **Run Migrations**: Apply database migrations to set up the database schema:

   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

8. **Run the Development Server**: Start the Django development server:
   

   ```
   python manage.py runserver
   ```
   and in another cmd seesion u should run the server Email server 

    ```
    python -m smtpd -n -c DebuggingServer localhost:1025
    ```


## Usage

Once the development server is running, you can access DARKFORGE by navigating to `http://localhost:8000` in your web browser.

---

This README provides clear and concise instructions for installing and running DARKFORGE, making it easier for users to get started with your project.