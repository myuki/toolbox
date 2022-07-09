#!/usr/bin/env python3

# Dependencies: ffmpeg

from concurrent.futures import Future, ThreadPoolExecutor
from multiprocessing import cpu_count
import os
import subprocess
import sys

extensions: tuple = (".mkv", ".webm")

# Init
threadLimit = int(cpu_count() / 2)
## Check available CLI
try:
  result = subprocess.run("ffmpeg", capture_output=True)
except FileNotFoundError:
  print("Can't find ffmpeg!")
  sys.exit(1)


def extractOpus(srcFile: str, dstFile: str) -> subprocess.CompletedProcess:
  result = subprocess.run(
      f"ffmpeg -i \"{srcFile}\" -c copy \"{dstFile}\"",
      capture_output=True,
      text=True)
  return result


def clenCliLine(override: str = "", end: str = "\n", width: int = 90):
  print("\r" + " " * width, end="")
  if override:
    print("\r" + override, end=end)


if __name__ == "__main__":
  # Check path
  path: str = sys.path[0]
  outputPath: str = os.path.join(path, "output")
  if not os.path.exists(outputPath):
    os.makedirs(outputPath)

  errorList: dict[str, str] = {}

  # Get input file list
  inputFileList: dict[str, str] = {} # File: Filename without extension
  dirList: list[str] = os.listdir(path)
  for inputFile in dirList:
    if inputFile.endswith(extensions):
      for extension in extensions:
        if extension in inputFile:
          inputFileList[inputFile] = inputFile.rstrip(extension)
          break

  # Extract
  total: int = len(inputFileList)
  threadPool = ThreadPoolExecutor(threadLimit if total > threadLimit else total)
  threadResult: dict[str, Future] = {} # File: Result
  for file, name in inputFileList.items():
    try:
      threadResult[file] = threadPool.submit(
          extractOpus, os.path.join(path, file),
          f"{os.path.join(outputPath, name)}.opus")
    except Exception as e:
      errorList[file] = str(e)

  ## Wait all ffmpeg subprocess
  current: int = 0
  for file, future in threadResult.items():
    current = current + 1
    if file not in errorList:
      if len(file) > 35:
        file = file[:35] + "..."
      clenCliLine(f"Extract {current}/{total}: {file}", end="")
      # Print 7z output if return code is not 0
      result: subprocess.CompletedProcess = future.result()
      if result.returncode != 0:
        errorList[file] = result.stdout.strip().replace("\n\n", "\n")
        currentExtractNum = current - 1
  clenCliLine(f"Extract {current}/{total}.")

  # Print error
  if errorList:
    print("Complete with error!\n")
    for file, error in errorList.items():
      print(f"{file}: {error}")
  else:
    print("Complete!\n")
