import nox

nox.options.sessions = "lint", "tests"


@nox.session
def tests(session):
    args = session.posargs
    session.install("pipenv")
    session.run("pipenv", "sync")
    session.run("pytest", *args)


@nox.session
def lint(session):
    args = session.posargs or ["oura", "tests", "samples"]
    session.install("flake8", "flake8-black")
    session.run("flake8", *args)


@nox.session
def black(session):
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)
