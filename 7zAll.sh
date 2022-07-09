#!/usr/bin/env bash

# Parameter: [<7z switches>...]
# Example: 7zAll.sh -mx=0 -ms=off -mmt=11

# Dependencies: p7zip

IFS=$'\n'
dirList=$(ls -F | grep "/$")

for dirName in $dirList; do
  dirName="${dirName%/}"
  7zr a $* "$dirName.7z" "$dirName"
done

echo
echo "Compression completed."
echo
