#!/usr/bin/env bash

# Parameter: [<apt-get dist-upgrade options>...]
# Example: upgrade.sh -y

# Check if user is root
if [ $(id -u) != "0" ]; then
  echo "Error: Not root user"
  exit 1
fi

echo "Updating package lists..."
apt-get update > /dev/null
apt-get dist-upgrade $*
apt-get autoremove -y
apt-get clean
echo "~~~~~~~~~ $(date) ~~~~~~~~~"
echo
