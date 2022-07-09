#!/usr/bin/env bash

# Parameter: [<7z switches>...]
# Example: zip27z.sh -mx=0 -ms=off -mmt=11

# Dependencies: unar, p7zip

IFS=$'\n'
zipList=$(ls -1 *.zip)

for fileName in $zipList; do
  unar "$fileName"
  dirName="${fileName%".zip"}"
  7zr a $* "./output/${dirName}.7z" "$dirName"
  rm -r "$dirName"
done

echo
echo "Convertion completed."
echo
