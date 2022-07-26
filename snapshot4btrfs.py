#!/usr/bin/env python3

import datetime
import os
import shutil
import subprocess
import sys

snapshotPath: str = "~/snapshots/"
snapshotLimit: int = 5
reservedSnapshotTags: set = {"Backup", "backup"}
reservedSnapshotList: set = set()

if __name__ == "__main__":
  snapshotPath = os.path.expanduser(snapshotPath)
  if not os.path.exists(snapshotPath):
    os.makedirs(snapshotPath)

  # Check command
  snapshotName = sys.argv[1] if len(sys.argv) > 1 else "snapshot4btrfs.py"

  # Get snapshot list
  snapshotList: list[str] = os.listdir(snapshotPath)
  available: int = snapshotLimit - len(snapshotList)
  first: int = 0
  if snapshotList:
    snapshotList.sort()
    for folder in snapshotList:
      if os.path.isdir(os.path.join(snapshotPath, folder)):
        snapshotList.remove(folder)

    # Delete oldest snapshot when reach limit
    while available < 1:
      reserve: bool = False
      for str in reservedSnapshotTags:
        if str in snapshotList[first]:
          first = first + 1
          reserve = True
          break
      for str in reservedSnapshotList:
        if str == snapshotList[first]:
          first = first + 1
          reserve = True
          break
      if not reserve:
        print("Delete oldest snapshot...")
        shutil.rmtree(os.path.join(snapshotPath, snapshotList.pop(first)))
        available = available + 1

  # Create snapshot
  if available > 0:
    timestamp = datetime.datetime.now().astimezone().replace(
        microsecond=0).isoformat()
    subprocess.check_call(
        f"btrfs subvol snapshot / {snapshotPath}/[{timestamp}]{snapshotName}",
        shell=True)
    print("Created successfully")
  else:
    print("!Error: Reach limit")
