#!/usr/bin/env bash

# Parameter: [package...]
# Example: purge.sh package0 package1

removePackageList=""
notRemovePackageList=""

# Check if user is root
if [ $(id -u) != "0" ]; then
  echo "Error: Not root user"
  exit 1
fi

# Check if have input
if [ "$#" == "0" ]; then
  echo "Error: No input"
  echo "These packages have some remain file: "
  dpkg -l | grep "^rc" | cut -d " " -f 3
  exit 1
fi

# Purge packages
for package in $*; do
  apt purge $package && dpkg -l | grep ^rc | awk '{print $2}' | xargs dpkg -P $package
  if [ "$?" == "0" ]; then
    if [ "$removePackageList" == "" ]; then
      removePackageList="$package"
    else
      removePackageList="$removePackageList, $package"
    fi
  else
    if [ "$notRemovePackageList" == "" ]; then
      notRemovePackageList="$package"
    else
      notRemovePackageList="$notRemovePackageList, $package"
    fi
  fi
done

# Clean up
apt autoremove -y
apt clean

# Print result
echo
if [ "$removePackageList" != "" ]; then
  echo "These packages have been purged:"
  echo "$removePackageList"
fi
if [ "$notRemovePackageList" != "" ]; then
  echo "These packages not be purged because of wrong name or non-existent:"
  echo "$notRemovePackageList"
fi
echo
