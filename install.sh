#!/bin/bash


ENV_ACTIVE=0
VERSION=$1

case $VERSION in
    1)
        echo "Creating executable for version 1..."
        git fetch --all
        git switch v1
        git pull
        ;;
    2)
        echo "Creating executable for version 2..."
        git fetch --all
        git switch main
        git pull
        ;;
    *)
        echo "Invalid version. Please provide a valid version number. Valid versions are 1 and 2."
        exit 1
        ;;
esac




ENVDIR_1="venv/bin/activate"
if [ -f "${ENVDIR_1}" ]; then
    echo "Activating virtual environment ${ENVDIR_1}..."
    source "${ENVDIR_1}"
    echo "Virtual environment ${ENVDIR_1} activated."
    ENV_ACTIVE=1
else
    echo "Virtual environment ${ENVDIR_1} not found."
fi


ENVDIR_2="venv/Scripts/activate"
if [ -f "${ENVDIR_2}" ]; then
    echo "Activating virtual environment ${ENVDIR_2}..."
    source "${ENVDIR_2}"
    echo "Virtual environment ${ENVDIR_2} activated."
    ENV_ACTIVE=1
else
    echo "Virtual environment ${ENVDIR_2} not found."
fi


if [ $ENV_ACTIVE -eq 0 ]; then
    echo "No virtual environment found. Creating a new one..."
    python -m venv venv
    source venv/bin/activate
    source venv/Scripts/activate
    echo "Virtual environment created and activated."
fi


echo "Installing dependencies..."
pip install -r requirements.txt


echo "Creating the executable..."
pyinstaller --clean --noconfirm --windowed main.py
echo "Executable created. You can find it in the dist folder."
