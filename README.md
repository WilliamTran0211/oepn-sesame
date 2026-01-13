# 🔐 Open Sesame

> "Open sesame." — every client app, politely asking for a token.

## 🤔 What is this?

Open sesame is a small authentication service I built for my personal projects. 

### Why does this exist?

- 😫 Got tired of rewriting login logic
- 🙅‍♂️ Copy-pasting auth code felt... wrong (and it was)
- 🏢 Using a full-blown auth platform felt like bringing a tank to a water gun fight
- 🎯 Wanted one auth service to rule them all (my projects, at least)

So here we are. Sesame open!

## 🧰 Tech Stack

Nothing exotic here, just good reliable tools:

- **FastAPI** — Fast, clean, no drama. Perfect for APIs.
- **PostgreSQL** — Where users live (rent-free!)
- **Redis** — Tokens, sessions, and short-term memory
- **JWT** — Because of course
- **SQLAlchemy** — Database conversations made easy
- **Alembic** — When your database needs to evolve
- **Pydantic** — Data validation that actually makes sense
