New-Item -ItemType Directory -Force -Path ./artifacts
Remove-Item .\artifacts\*.*

Copy-Item .\screensaver.py .\artifacts
Copy-Item .\PhotoRepository.py .\artifacts
Copy-Item .\config.template.yml .\artifacts
Copy-Item .\screensaver.service .\artifacts
Copy-Item .\install.sh .\artifacts