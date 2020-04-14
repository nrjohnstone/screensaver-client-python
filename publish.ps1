New-Item -ItemType Directory -Force -Path ./artifacts
Remove-Item .\artifacts\*.*

Copy-Item .\screensaver.py .\artifacts
Copy-Item .\install.sh .\artifacts