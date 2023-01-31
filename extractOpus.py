#!/usr/bin/env python3

# Dependencies: ffmpeg

from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from multiprocessing import cpu_count
import os
import subprocess
import sys

extensions: tuple = (".mkv", ".webm")


def extractOpus(inputPath: str, outputPath: str) -> subprocess.CompletedProcess:
  result = subprocess.run(
      f"ffmpeg -i \"{inputPath}\" -c copy -y \"{outputPath}\"",
      capture_output=True,
      text=True)
  return result


def checkCliExist(path: str) -> bool:
  try:
    subprocess.run(path, capture_output=True)
  except FileNotFoundError:
    return False
  else:
    return True


def clenCliLine(override: str = "", end: str = "\n", width: int = 90):
  print("\r" + " " * width, end="")
  if override:
    print("\r" + override, end=end)


def getFilesByExt(path: str, extensions: tuple) -> list[str]:
  fileList: list[str] = []
  for file in os.listdir(path):
    if file.endswith(extensions):
      fileList.append(file)
  return fileList


def processFiles(processPaths: dict[str, str], fun) -> dict[str, str]:
  threadLimit = int(cpu_count() / 2)
  errorList: dict[str, str] = {}

  # Init thread
  total: int = len(processPaths)
  threadResult: dict[Future, str] = {} # Future: inputPath
  with ThreadPoolExecutor(max_workers=threadLimit) as threadPool:

    # Run subprocess
    for inputPath, outputPath in processPaths.items():
      try:
        future = threadPool.submit(fun, inputPath, outputPath)
        threadResult[future] = inputPath
      except Exception as e:
        errorList[inputPath] = str(e)

    # Wait all subprocess
    current: int = 0
    for future in as_completed(threadResult):
      current = current + 1
      clenCliLine(f"Processing {current}/{total}...", end="")

      inputPath = threadResult[future]
      result = future.result()
      if result.returncode != 0:
        errorList[inputPath] = f"{result.stderr}\n{result.stdout}".strip()

    clenCliLine(f"Processing {current}/{total}.")
  return errorList


def stripExt(fileName: str) -> str:
  return fileName[0:fileName.rfind(".")]


if __name__ == "__main__":

  # Check path
  path: str = sys.path[0]
  outputDirPath: str = os.path.join(path, "output")
  if not os.path.exists(outputDirPath):
    os.makedirs(outputDirPath)

  # Check available CLI
  if not checkCliExist("ffmpeg"):
    print("Can't find ffmpeg!")
    sys.exit(1)

  # Get input file list
  inputFiles = getFilesByExt(path, extensions)
  if len(inputFiles) < 1:
    print("No file can be processed!\n")
    sys.exit(0)

  # Extract all files
  processPaths: dict[str, str] = {} # inputPath: outPath
  for file in inputFiles:
    inputPath = os.path.join(path, file)
    outputPath = os.path.join(outputDirPath, f"{stripExt(file)}.opus")
    processPaths[inputPath] = outputPath
  errorList = processFiles(processPaths, extractOpus)

  # Print error
  if errorList:
    print("Complete with error!\n")
    for file, error in errorList.items():
      print(f"{file}: {error}")
  else:
    print("Complete!\n")
