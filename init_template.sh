#!/bin/bash

log()
{
  echo "[Unity Init] $1"
}

prompt()
{
  read -p "$1 (y/n) " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]
    promptresult="yes"
  then
    promptresult="no"
  fi
}

clone_submodules()
{
  log "Initializing submodules"
  git submodule init

  log "Updating submodules"
  git submodule update
}

delete_prompt()
{
  prompt "Delete this init script?"

  echo $promptresult
}

finish()
{
  log "Initialization complete."
}

main()
{
  log "Running Init Script"

  clone_submodules

  delete_prompt

  finish
}

main
