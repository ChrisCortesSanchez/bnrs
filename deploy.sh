#!/bin/bash
# This shell script deploys a new version to a server.

PROJ_DIR=bnrs
VENV=venv
PA_DOMAIN="bnrs.pythonanywhere.com"
PA_USER='bnrs'
PA_API_TOKEN = 19275349cbb7f23da8004df8c56ebc61306bd889
echo "Project dir = $PROJ_DIR"
echo "PA domain = $PA_DOMAIN"
echo "Virtual env = $VENV"

if [ -z "$BNRS_PA_PWD" ]
then
    echo "The PythonAnywhere password var (BNRS_PA_PWD) must be set in the env."
    exit 1
fi

echo "PA user = $PA_USER"
echo "PA password = $BNRS_PA_PWD"

echo "SSHing to PythonAnywhere."
sshpass -p $BNRS_PA_PWD ssh -o "StrictHostKeyChecking no" $PA_USER@ssh.pythonanywhere.com << EOF
    cd ~/$PROJ_DIR; PA_USER=$PA_USER PROJ_DIR=~/$PROJ_DIR VENV=$VENV PA_DOMAIN=$PA_DOMAIN ./rebuild.sh
EOF
