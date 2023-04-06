# toolbox

A tool scripts collection.

## 7zAll.sh

Compress each folder as an individual 7z file.

Requirements: `p7zip`

Parameter:`[<7z switches>...]`

Example: `7zAll.sh -mx=0 -ms=off -mmt=11`

## docker-gui.sh

Warp some docker options for create a docker container with GUI support.

Requirements: `docker`

Parameter:`[OPTIONS] IMAGE [COMMAND] [ARG...]`

Example: `docker-gui.sh -it --gpus all -v ~/shares:/shares --name cuda12.0.1 nvidia/cuda:12.0.1-cudnn8-devel-ubuntu22.04`

## extractOpus.py

Extract Opus from all Matroska (.mkv, .webm) files in current directory.

Requirements: `ffmpeg`

## purge.sh

Purge package by use `apt` and `dpkg`.

Parameter: `[package...]`

Example: `purge.sh package0 package1`

## snapshot4btrfs.py

Create a btrfs snapshot and delete the oldest snapshot when reach the specific limit of amount.

Can use `reservedSnapshotList` to specific which snapshot should be reserved when delete. Or specific the tag in `reservedSnapshotTags`.

Parameter: `[snapshot name]`

Example: `snapshot4btrfs.py backup`

## upgrade.sh

Update packages index and upgrade packages. It also runs `apt-get autoremove -y` and `apt-get clean` at last.

Parameter: `[<apt-get dist-upgrade options>...]`

Example: `upgrade.sh -y`

## zip27z.sh

Decompress all zip files and recompress as 7z files.

Requirements: `unar, p7zip`

Parameter: `[<7z switches>...]`

Example: `zip27z.sh -mx=0 -ms=off -mmt=11`
