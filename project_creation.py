import base64
import errno
import json
import os
import subprocess
from pathlib import Path

import requests
import typer
from dotenv import load_dotenv

load_dotenv()

mobile_repo = os.getenv('mobile_repo')
frontend_repo = os.getenv('frontend_repo')
backend_repo = os.getenv('backend_repo')
pat = os.getenv('pat')
username = os.getenv('username')


app = typer.Typer(help="Project Creator Tools")


def create_remote_repository(project_name):
    # url of the organization repository.
    url = "https://api.github.com/orgs/#Your Username or Organization Name#/repos"
    # concatenation of username and personal access token.
    user_credential = username + ":" + pat
    user_credential_bytes = user_credential.encode("ascii")
    base64_bytes = base64.b64encode(user_credential_bytes)
    base64_string = base64_bytes.decode("ascii")

    payload = {
        "name": project_name,
        "private": True,
    }
    payload = json.dumps(payload)
    headers = {
        'Authorization': 'Basic' + " " + base64_string,
        'Content-Type': 'text/plain',
    }

    requests.request("POST", url, headers=headers, data=payload)


# checking git version
def checkout_git_version():
    try:
        subprocess.check_output(" git --version", shell=True)
    except subprocess.CalledProcessError as e:
        typer.echo(
            "Please Configure the Git Credentials first and then re run the program.")
        typer.Abort()


# create the directory for the project
def project_directory(out_path, name):
    typer.echo("Creating directory for project ")

    project_folder = os.path.join(out_path, name)
    try:
        os.mkdir(project_folder)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
        pass
    return project_folder


# clone the repo in the directory
def clone_repo(repo_url, out_path):
    clone_repo = subprocess.Popen(
        f"git clone {repo_url} {out_path}", shell=True)
    clone_repo.wait()


@app.command()
def main(project_template: str, project_name: str, out_path: Path = typer.Option(
    ...,
    writable=True,
    dir_okay=True,
)):
    checkout_git_version()
    out_path = project_directory(out_path, project_name)
    project_template = project_template.lower()
    if project_template == "mobile":
        clone_repo(mobile_repo, out_path)
        create_remote_repository(project_name)

    elif project_template == "frontend":
        clone_repo(frontend_repo, out_path)
        create_remote_repository(project_name)

    elif project_template == "backend":
        clone_repo(backend_repo, out_path)
        create_remote_repository(project_name)

    else:
        typer.echo(
            f"Bad Project template name:{project_template}", fg=typer.colors.RED, bold=True)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
