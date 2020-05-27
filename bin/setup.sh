#!/bin/bash

# verify motion is installed on system
if [ ! -d "/etc/motion" ]
then
    echo "Error: motion-project must be installed on this system"
    exit 1
else
    echo "Motion-project is installed"
fi

# verify required envrionment variables exist
if [ -z "$EMAIL_PASS" ]
then
    echo "Error: EMAIL_PASS environment variable is not set"
    exit 1
fi

if [ -z "$EMAIL_ACCOUNT" ]
then
    echo "Error: EMAIL_ACCOUNT environment variable is not set"
    exit 1
fi

echo "Required environment variables are set"

# verify garden project has correct directory structure
if [ ! -d "/opt/gardenview/output" ]
then
    echo "Creating video output directory"
    mkdir /opt/gardenview/output
fi

if [ ! -d "/opt/gardenview/archive" ]
then
    echo "Creating video archive directory"
    mkdir /opt/gardenview/archive
fi

# check for and retrieve any updates from source project repository
echo "Checking for project updates..."
git pull
echo "Done!"
