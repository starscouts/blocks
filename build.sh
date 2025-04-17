#!/bin/bash
source ./venv/bin/activate
rm -rf ./dist ./_temp
mkdir -p ./dist/darwin-arm64 ./dist/darwin-x64 ./dist/win32 ./dist/linux-arm64 ./dist/linux-x64 ./_temp

#podman machine start
#ssh -i ~/.ssh/podman-machine-default -R 10000:$(hostname):22 -p $(podman machine --log-level=debug ssh -- exit 2>&1 | grep Executing | awk {'print $8'}) core@localhost sshfs -p 10000 $USER@127.0.0.1:/Volumes/Projects /mnt/Projects&

# macOS
cp -rv ./assets ./_temp/assets
pyinstaller --distpath ./dist/darwin-arm64 --workpath ./_temp --noconfirm --specpath ./_temp -n Blocks --add-data assets:assets -p src -s --noconsole --osx-bundle-identifier dev.equestria.blocks -i ./assets/textures/icon-mac.icns --target-architecture arm64 main.py
rm -rf ./_temp

source ./venv_x86/bin/activate
mkdir -p ./_temp
cp -rv ./assets ./_temp/assets
arch -x86_64 pyinstaller --distpath ./dist/darwin-x64 --workpath ./_temp --noconfirm --specpath ./_temp -n Blocks --add-data assets:assets -p src -s --noconsole --osx-bundle-identifier dev.equestria.blocks -i ./assets/textures/icon-mac.icns --target-architecture x86_64 main.py
rm -rf ./_temp

source ./venv_x86/bin/activate
exit

# Linux
mkdir -p ./_temp
cp -rv ./assets ./_temp/assets
podman start blocks-build
podman exec blocks-build bash -c "cd /blocks && pyinstaller --distpath ./dist/linux-arm64 --workpath ./_temp --noconfirm --specpath ./_temp -n Blocks --add-data assets:assets -p src -s --noconsole --hidden-import=pygame -i ./assets/textures/icon.png --onefile main.py"
rm -rf ./_temp
podman stop blocks-build
podman machine stop
mkdir -p ./_temp
cp -rv ./assets ./_temp/assets
ssh zephyrheights umount -lf /blocks
ssh zephyrheights sshfs $USER@192.168.1.23:/Volumes/Projects/blocks /blocks
ssh zephyrheights 'bash -c "cd /blocks && pyinstaller --distpath ./dist/linux-x64 --workpath ./_temp --noconfirm --specpath ./_temp -n Blocks --add-data assets:assets -p src -s --noconsole --hidden-import=pygame -i ./assets/textures/icon.png --onefile main.py && cd / && umount /blocks"'
rm -rf ./_temp

# Windows
mkdir -p ./_temp
cp -rv ./assets ./_temp/assets
wine64 $PWD/win32/Scripts/pyinstaller.exe --distpath ./dist/win32 --workpath ./_temp --noconfirm --specpath ./_temp -n Blocks --add-data "assets;assets" -p src --noconsole -i ./assets/textures/icon.ico --onefile main.py
rm -rf ./_temp
