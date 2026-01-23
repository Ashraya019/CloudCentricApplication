#what this file is responsible for:
# creating the db engine
# managing db sessions
# reading configuration from environment variables
# working in local, Docker and Kubernetes

# Design Priniciples:
# Env-based Config
# connetion pooling
# one session per request
# no global session reuse

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# why this matters:
# local dev -> uses default
# docker/K8s -> inject via env vars / secrets
# no hardcoding creds
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@db:5432/postgres"
)

# create_engine is the starting point for any SQLAlchemy application. It creates an Engine object, which acts as the central "control center" for connecting your Python code to your database.
# When you call this function, it builds an object that contains two critical internal component
# The Dialect: This is a "translator." Since every database (PostgreSQL, MySQL, SQLite) speaks a slightly different version of SQL, the Dialect translates your Python commands into the specific dialect your database understands.
# The Connection Pool: This is a "management system." Instead of opening and closing a brand new connection for every single query (which is slow), the Engine keeps a "pool" of already-open connections ready to be used instantly. 
engine = create_engine(
    DATABASE_URL,
    # prevents stale DB connections
    # critical for Kubernetes pods that get rescheduled
    # Avoids random connection closed errors
    # When your application wants to talk to the database, it grabs a connection from a "pool" (a collection of already-open connections).
    # Without Pre-Ping: Your app assumes the connection is still alive. If the database or network cut that connection while it was sitting idle, your app will crash with a Connection unexpectedly closed error.
    # With Pre-Ping: Every time your app grabs a connection from the pool, it sends a tiny "heartbeat" (usually SELECT 1) to the database first. If the database doesn't answer, SQLAlchemy quietly throws that dead connection away and creates a fresh one for you.
    pool_pre_ping = True
)

# Explicit commits
# Predictable transactions
# Works cleanly with FastAPI dependency injection
# sessionmaker is a "factory" for database sessions. While the engine is the physical connection to the database, SessionLocal is the tool you use to actually talk to it.
# 
SessionLocal = sessionmaker(
    # The Action: Prevents SQLAlchemy from automatically saving every change the moment it happens.
    # Why it matters: It ensures your database operations are Atomic. If you are doing three things (e.g., deducting money from one account and adding it to another), you want them to happen as a single "transaction."
    # You must explicitly call db.commit() to save your work. If something goes wrong, you can call db.rollback() to undo everything.
    autocommit=False,
    # Prevents the session from sending "pending" changes to the database every time you perform a query.
    # we prefer manual control over when data is sent to the database. By turning this off, you reduce unnecessary network traffic.
    # You manually decide when to "flush" (send data to the DB) and when to "commit" (save it permanently).
    autoflush=False,
    # Connects this session factory to the engine
    # It tells the session: "Whenever a user needs a database connection, use the settings and connection pool defined in this specific engine."
    bind=engine
)

# base class for projects
# all SQLAlchemy models inherit from this
# used to create tables
Base = declarative_base()


