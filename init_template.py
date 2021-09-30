#!/usr/bin/env python
import subprocess
import pathlib
import os

ORIGINAL_PROJ_NAME = "Reccy 3D Template"

def current_directory():
    return pathlib.Path(__file__).parent.resolve()

def current_file_path():
    return pathlib.Path(__file__).resolve()

def log(str):
    print("[Unity Init] " + str)

def prompt(question):
    yes = set(['yes','ye','y'])
    no = set(['no', 'n'])

    while True:
        choice = input("[Unity Init] " + question + "\n(Yes/No) > ").lower()
        if choice in yes:
            return True
        elif choice in no:
            return False
        else:
            log("Please respond with 'Yes' or 'No'")

def prompt_str(question):
    response = input("[Unity Init] " + question + "\n > ").strip()
    return response

def clone_submodules():
    log("Initializing submodules")
    subprocess.run("git submodule init")
    log("Updating submodules")
    subprocess.run("git submodule update")

def set_project_name(projectName):
    settings_file = os.path.join(current_directory(), "ProjectSettings", "ProjectSettings.asset")

    with open(settings_file, "r+") as f:
        texts = f.read()
        texts = texts.replace(ORIGINAL_PROJ_NAME, projectName)

    with open(settings_file, "w") as f:
        f.write(texts)

def set_repo_url(newUrl):
    log("Setting new Repository Remote URL to " + newUrl)
    subprocess.run("git remote set-url origin " + newUrl)

def clear_repo_url():
    log("Clearing Repository Remote")
    subprocess.run("git remote remove origin")

def squash_commits():
    log("Squashing commits")
    subprocess.run("git checkout --orphan new-master master")
    subprocess.run("git commit -m \"Initialized Unity Project from Template\"")
    subprocess.run("git branch -M new-master master")
    log("Commits squashed")

def delete_file():
    log("Deleting " + str(current_file_path()))
    os.remove(current_file_path())
    log("Done")

def delete_prompt():
    if prompt("Delete this init script?"):
        delete_file()
    else:
        log("Skipping deletion")

def main():
    projectName = prompt_str("Please enter your project name")
    if prompt("Do you have an existing empty repo you would like to push this project to?"):
        repoName = prompt_str("Please enter your repo URL")
    else
        repoName = None

    log("Initializing Unity Project")

    clone_submodules()
    set_project_name(projectName)

    if repoName:
        set_repo_url(repoName)
    else:
        clear_repo_url()

    #squash_commits()
    #delete_prompt()

main()
