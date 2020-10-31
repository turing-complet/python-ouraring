import nox

nox.options.reuse_existing_virtualenvs = True
nox.options.sessions = "lint", "tests"
locations = ["oura", "tests", "samples"]


@nox.session
def tests(session):
    args = session.posargs
    session.install("pipenv")
    session.run("pipenv", "sync")
    session.run("pipenv", "run", "pytest", *args)


@nox.session
def lint(session):
    args = session.posargs or locations
    session.install("flake8", "black", "isort")
    session.run("flake8", *args)
    session.run("black", "--check", "--diff", *args)
    session.run("isort", "-m", "3", "--tc", "--check", "--diff", *args)


@nox.session
def format(session):
    black(session)
    isort(session)


def black(session):
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)


def isort(session):
    args = session.posargs or locations
    session.install("isort")
    session.run("isort", "-m", "3", "--tc", *args)


@nox.session
def docs(session):
    session.chdir("docs")
    session.install("-r", "requirements.txt")
    session.run("make", "html", external=True)
