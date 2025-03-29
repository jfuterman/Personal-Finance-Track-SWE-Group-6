# Welcome to WealthWise

WealthWise is a full stack web application that helps users budget, save, and meet their financial goals.

## Frontend

We use React with TypeScript based on Figma designs.

## Backend

We built this project with Django and Python. It hosts user data in a database managed with PostgreSQL and retrieves financial data with the Plaid API.

### Using the project

Get started by cloning this repository. Then, create your virtual environment and install the dependencies. Depending on your system and version of Python, you'll run `python -m venv .venv` to create the virtual environment. Then, run `pip install -r requirements.txt` to install the project dependencies.

#### Launch Django

Head to the `django` folder and run `python manage.py runserver`. You started the Django server!

## Contribution Guidelines for WealthWise
### Branching Strategy
We'll follow the Git Feature Branch Workflow:

| Branch          | Purpose                                  |
|----------------|------------------------------------------|
| `main`         | Production-ready, stable builds         |
| `dev`          | Integration branch (latest development) |
| `feature/<name>` | New features (e.g., `feature/recurring-expenses`) |
| `bugfix/<name>`  | Fixing issues (e.g., `bugfix/login-error`) |
| `hotfix/<name>`  | Critical production fixes             |


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
Code from dev will be deployed to a staging environment.

Only tested and approved features will be merged into main for production deployment.
