# Welcome to WealthWise

WealthWise is a full stack web application that helps users budget, save, and meet their financial goals.

### Frontend

We use Django templating based on Figma designs.

### Backend

This project uses Django and Python. It hosts user data in a database managed with PostgreSQL and retrieves financial data with the Plaid API.

### DevOps

We use Docker to manage development and are hosted with Azure.

## Using the project

Get started by cloning this repository. We really recommend you install Docker -- it will save you a lot of headaches.

### .env file

Create a .env file following the .env.example file. You'll need to ask your teammates or configure your own database. \
If you are using Docker, your `DB_HOST` variable should be `db`. If not, `DB_HOST` should be `localhost`.\
Add your own values for `POSTGRES_DB`, `POSTGRES_USER`, and `POSTGRES_PASSWORD` variables in the .env file.

### Launch the Server

#### Using Docker

If you've got Docker installed on your computer, run `docker compose up --build`. This will spin up the database and Django, and you can visit the app at `http://localhost:8000/`. You're done!

#### Using Virtual Environment

If you don't have Docker, create your virtual environment and install the dependencies.

Create a new virtual environment:\
`python -m venv .venv`

Activate the new virtual environment:\
 For Unix/macOS: `source .venv/bin/activate`\
 For Windows: `.venv\Scripts\activate`

Then, run `pip install -r requirements.txt` to install the project dependencies.

If not using Docker, head to the root folder and run `python manage.py makemigrations`, then `python manage.py migrate`, then `python manage.py runserver`. You started the Django server. You're done!

## Contribution Guidelines for WealthWise

### I have to change the codebase. What do I do?

All changes will follow this general pattern:

1. Switch to the dev branch using `git checkout dev`
2. Use `git pull` to retrieve all of the latest changes to `dev`.
3. Use `git checkout -b <new_branch_name>`. This creates a new branch for you to work off of. Pick a name that describes what you're doing on this branch.
4. Make your desired changes, committing often. Once the feature is done and works, submit a Pull Request and ask a team member to review and merge your changes into the dev branch. The dev branch is a staging area for production.

### Branching Strategy

We'll follow the Git Feature Branch Workflow:

| Branch           | Purpose                                           |
| ---------------- | ------------------------------------------------- |
| `main`           | Production-ready, stable builds                   |
| `dev`            | Integration branch (latest development)           |
| `feature/<name>` | New features (e.g., `feature/recurring-expenses`) |
| `bugfix/<name>`  | Fixing issues (e.g., `bugfix/login-error`)        |
| `hotfix/<name>`  | Critical production fixes                         |

### When to branch

Create a feature branch off dev before starting any new user story or task.

Only work on one task per branch to keep pull requests clean.

### Committing Code

Follow these commit guidelines to keep history clean and readable:

#### Small commits

Make focused commits for each logical change. **Avoid committing directly to dev or main.**

#### Pull Requests (PRs)

##### When to create a PR

When your task is completed and tested locally.

##### How?

Submit a PR from your feature/ or bugfix/ branch to dev.

##### PR Checklist

- Code compiles without errors.
- You’ve tested your feature or fix locally.
- No console errors or linter warnings.
- At least 1 other teammate has reviewed and approved the PR.

#### Merging & Pulling

Always pull the latest dev before creating or updating a branch.

If your branch is out of date, use:

`git pull origin dev`
`git merge dev`
After PR approval, a designated team member (rotating) merges it into dev.

#### Deployment

To stage for deployment, follow these steps:

1. ensure your .env file has `PIPELINE` set to "production",
2. in the Dockerfile, ensure that lines below "Only needed for production" are NOT commented out.

Once this is configured, you can merge `dev` into `main`. It will trigger a GitHub Action to build and deploy your changes.

You shouldn't have to manually stop and restart the app to see your changes. They should be visible shortly after the build succeeds.
