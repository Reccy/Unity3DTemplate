#!/usr/bin/env python
import subprocess
import requests
import pathlib
import io
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

def prompt_int(question):
    response = input("[Unity Init] " + question + "\n > ").strip()

    try:
        response = int(response)
    except ValueError:
        return -1

    return response

def prompt_list(question, options):
    question_str = question

    length = len(options)
    for i in range(length):
        s = options[i]
        question_str += "\n[Unity Init] (" + str(i + 1) + ") " + s

    while True:
        choice = prompt_int(question_str)
        if choice > 0 and choice <= length:
            return choice
        else:
            log("Please enter a valid option within the range")

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

def github_login():
    proc = subprocess.Popen(["gh", "auth", "status"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    lines = []
    for line in io.TextIOWrapper(proc.stdout, encoding="utf-8"):
        lines.append(line.strip())

    if lines[0] == "You are not logged into any GitHub hosts. Run gh auth login to authenticate.":
        log("It appears you're not currently logged into GitHub. Please login now.")
        subprocess.run("gh auth login")
        proc2 = subprocess.Popen(["gh", "auth", "status"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        lines2 = []
        for line in io.TextIOWrapper(proc2.stdout, encoding="utf-8"):
            lines2.append(line.strip())

        if lines2[0] != "You are not logged into any GitHub hosts. Run gh auth login to authenticate.":
            return True
        else:
            return False
    else:
        proc2 = subprocess.Popen(["gh", "auth", "status"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        lines2 = []
        for line in io.TextIOWrapper(proc2.stdout, encoding="utf-8"):
            lines2.append(line.strip())
        log(lines2[1])
        return True

def create_github_repo(repoName):
    proc = subprocess.Popen(["gh", "repo", "create", repoName, "--private", "-y"])
    pass

def update_readme(projectName):
    log("Generating README.MD")

    template_readme_file = os.path.join(current_directory(), "template_readme.md")
    readme_file = os.path.join(current_directory(), "readme.md")

    with open(template_readme_file, "r+") as f:
        texts = f.read()
        texts = texts.replace("[PROJECT_TITLE]", projectName)

    with open(readme_file, "w") as f:
        f.write(texts)

    log("Deleting " + str(template_readme_file))

    os.remove(template_readme_file)

def commit_changes():
    log("Committing changes")
    subprocess.run("git add --all")
    subprocess.run("git commit -m \"Finish setup\"")

def squash_commits():
    log("Squashing commits")
    subprocess.run("git checkout --orphan new-master master")
    subprocess.run("git commit -m \"Initialized Unity Project from Template\"")
    subprocess.run("git branch -M new-master master")
    log("Commits squashed")

def push_changes(newRepo):
    log("Pushing changes to " + newRepo)
    subprocess.run("git push -u origin master")

def delete_file():
    log("Deleting " + str(current_file_path()))
    os.remove(current_file_path())

def main():
    projectName = prompt_str("Please enter your project name")

    ans = prompt_list("How would you like to handle your git repo?",
    [
        "Clear the remote URL and configure manually later",
        "Set the URL to an existing empty repo",
        "Create a new repo on GitHub"
    ])

    if ans == 2:
        repoName = prompt_str("Please enter your repo URL")
    elif ans == 3:
        if not github_login():
            log("Fatal error: Cannot login to GitHub. Please ensure you can login and run this script again.")
            exit(1)
        repoName = prompt_str("Please enter your new repo name")

    log("Initializing Unity Project")

    clone_submodules()
    set_project_name(projectName)

    if ans == 1:
        clear_repo_url()
    elif ans == 2:
        set_repo_url(repoName)
    elif ans == 3:
        clear_repo_url()
        create_github_repo(repoName)

    delete_file()
    update_readme(projectName)
    commit_changes()
    squash_commits()

    if repoName:
        push_changes(repoName)

    log("Done! Good luck with " + projectName + "! :)")

main()
