import nox

nox.options.sessions = "lint", "tests"
locations = ["oura", "tests", "samples", "noxfile.py"]


@nox.session
def tests(session):
    args = session.posargs
    session.install("pipenv")
    session.run("pipenv", "sync", "--dev")
    session.run("pipenv", "run", "pytest", *args)


@nox.session
def lint(session):
    args = session.posargs or locations
    session.install("flake8", "black", "isort")
    session.run("flake8", *args)
    session.run("black", "--check", "--diff", *args)
    session.run("isort", "--profile", "black", "--check", "--diff", *args)


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
    session.run("isort", "--profile", "black", *args)


@nox.session
def docs(session):
    session.chdir("docs")
    session.install("-r", "requirements.txt")
    # session.run("sphinx-apidoc", "-f", "-o", "source", "../oura")
    # session.run("make", "clean", external=True)
    session.run("make", "html", external=True)
