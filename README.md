## Adventure planner - Aventura

The purpose of this application is to assist users in discovering engaging activities, whether you're seeking solo adventures or shared experiences. The app gives you personalizied adventure suggestions based on your choices, regardless of your current location.

Current key features:

- The user can log in, log out and create a new account.
- The app gives users personalized adventure suggestions based on their choices, including duration, cost, difficulty level, environment and group size.

### Instructions for starting the app:

Clone the repository to your computer.

Create an .env file in the root folder of the repository.

Add the following content to the env. file:

```bash
DATABASE_URL=<databases-local-address>
SECRET_KEY=<your-secret-key>
```

Activate the virtual environment and install the application dependencies with the following commands:

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

```bash
pip install -r ./requirements.txt
```

Define the database schema with the following command:

```bash
psql < schema.sql
```

Start the application with the following command:

```bash
flask run
```

Ideas for expansion:
- Each adventure has detailed descriptions.
- The user can give an adventure stars as a review.
- The user can see how many stars an adventure has.
- The user can see the most liked adventures on the main page.
- The user can add an adventure to favorites.
- The admin can add and delete adventures.

#### Use of large language models:

Creation of adventures.json with assistance from ChatGPT.