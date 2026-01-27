#!/usr/bin/env bash

SUBMODULE_NAME=Cloudjumper-Sensors
SUBMODULE_PUSH_URL=git@github.com:UMass-Lowell-Rocketry-Club/Cloudjumper-Sensors.git

# check if the current directory is a submodule
cd ..  # go to parent dir
if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then  # check if in a git repo
    echo "Error: Not in a submodule."
    exit 1
fi

# use --merge by default for git submodule update
echo "Setting git submodule update to merge incoming changes by default."
git config submodule.$SUBMODULE_NAME.update merge

# set up alias for git pull and git submodule update --merge
echo "Creating an alias to pull changes for submodules correctly."
read -p "Enter alias name (default: spull): " ALIAS_NAME
if [ -z "$ALIAS_NAME" ]; then
    ALIAS_NAME="spull"
fi
git config alias.$ALIAS_NAME '!git pull && git submodule update --merge'

# use --recurse-submodules=on-demand by default for git push
echo "Setting git push to push submodule commits first by default."
git config push.recurseSubmodules on-demand

# set push URL to the SSH address
cd $SUBMODULE_NAME
echo "Setting the submodule push URL to the SSH address."
git remote set-url --push origin $SUBMODULE_PUSH_URL

# switch to the main branch
echo "Switching the submodule to the main branch."
git switch main
