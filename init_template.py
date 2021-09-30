#!/usr/bin/env python
import subprocess
import pathlib
import os

def cwd():
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
    response = input("[Unity Init] " + question + "\n > ").lower().strip()
    return response

def clone_submodules():
    log("Initializing submodules")
    subprocess.run("git submodule init")
    log("Updating submodules")
    subprocess.run("git submodule update")

def squash_commits():
    log("Squashing commits")
    subprocess.run("git checkout --orphan new-master master")
    subprocess.run("git commit -m \"Initialized Unity Project from Template\"")
    subprocess.run("git branch -M new-master master")
    log("Commits squashed")

def delete_file():
    log("Deleting " + str(cwd()))
    os.remove(cwd())
    log("Done")

def delete_prompt():
    if prompt("Delete this init script?"):
        delete_file()
    else:
        log("Skipping deletion")

def main():
    log("Initializing Unity Project")
    clone_submodules()
    squash_commits()
    delete_prompt()

main()
