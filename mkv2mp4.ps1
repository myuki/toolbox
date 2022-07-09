$fileList = @()
Get-ChildItem | ForEach-Object -Process { $fileList += @($_.name | findstr .mkv) }
foreach ($file in $fileList) {
  Write-Output "$file`:"
  Write-Output "Conversing..."
  ffmpeg -loglevel warning  -i ("""$file""") -c copy ("""C:\Users\Myuki\Downloads\Conversion\" + $file.replace(".mkv", ".mp4") + """")
  Write-Output ""
}
