#!/usr/bin/env sh
# Script Name: generate_ssh_key.sh
# Author: Aina
# Date Created: 2025-08-20 | Date Modified: 2025-08-23

# Exit immediately if a command exits with a non-zero status
# Treat unset variables as an error and exit immediately
set -eu

# Define variables
username=${1:?Plesae enter the username.}
remote_host="192.168.1.3"
src="/home/akiyama/docsfile/hgsrq.fun/site/"
des="${username}@${remote_host}:/var/www/debian.local"
key_file="${HOME}/.ssh/${username}_key"

# Check the directory
if [ ! -d "${HOME}/.ssh" ]; then
    mkdir -p "${HOME}/.ssh"
fi

# Generate the ssh key and copy to remote host 
if [ -f "${key_file}" ]; then
    echo "${key_file} already exist!"
else
    ssh-keygen -t ed25519 -C "Created by ${username}." -N "" -f "${key_file}"
fi

ssh-copy-id -o StrictHostKeyChecking=accept-new \
            -i "${key_file}" "${username}@${remote_host}"

cat >> ${HOME}/.ssh/config <<- EOF
    Match Host ${remote_host}, User ${username}
        IdentityFile ${key_file}
EOF

rsync -rltD -zvu --delete "${src}" "${des}"
