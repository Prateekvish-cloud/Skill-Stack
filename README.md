# Skill Stack — Login / Signup / Dashboard

This is the first working piece of the Skill Stack project: account
creation, login, and a dashboard shell. Coding-profile fetching
(LeetCode/GitHub APIs), badges, and the leaderboard come in the next
phases — the dashboard already has placeholder sections for them.

## 1. Install MySQL (if you don't have it)

Download and install MySQL Community Server from
https://dev.mysql.com/downloads/installer/ and note the root password
you set during installation.

## 2. Create the database

Open MySQL command line (or MySQL Workbench) and run the schema file:

```bash
mysql -u root -p < schema.sql
```

This creates the `skill_stack` database and the `users` table (plus
empty tables for `coding_profiles`, `projects`, and `badges` that
we'll wire up later).

## 3. Set up the Python environment

```bash
cd skill-stack
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
```

## 4. Configure your database credentials

Copy `.env.example` to `.env` and fill in your real MySQL password:

```bash
copy .env.example .env        # Windows
# cp .env.example .env        # macOS/Linux
```

Edit `.env`:
```
SECRET_KEY=pick-any-random-string
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_actual_mysql_password
MYSQL_DB=skill_stack
```

## 5. Run it

```bash
python app.py
```

Open **http://localhost:5000** — you'll land on the landing page. Click
"Create an account" to sign up, then log in to see the dashboard.

## What's here vs. what's next

**Working now:**
- Sign up (name, email, password — hashed, never stored in plain text)
- Log in / log out with sessions
- Dashboard shell with stat cards and a sample Chart.js chart

**Next phases (from the project methodology):**
- Connect coding profiles (LeetCode, GitHub, CodeChef) — the
  `coding_profiles` table is already in `schema.sql`, ready for this
- Add projects & skills — `projects` table is ready
- Badges & leaderboard — `badges` table is ready
- Replace the sample chart data with real analytics from synced profiles

## Project structure

```
skill-stack/
├── app.py                  — Flask app (routes: /, /signup, /login, /logout, /dashboard)
├── schema.sql               — MySQL schema (users + tables for next phases)
├── requirements.txt          — Python dependencies
├── .env.example                — copy to .env and fill in your MySQL password
├── templates/
│   ├── base.html                — shared layout, flash messages
│   ├── login.html
│   ├── signup.html
│   └── dashboard.html
└── static/
    ├── css/style.css
    └── js/ (empty — chart init is inline in dashboard.html for now)
```
