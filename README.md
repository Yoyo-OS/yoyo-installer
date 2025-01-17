<div align="center">
    <img src="data/icons/hicolor/scalable/apps/org.yoyoos.Installer.svg" height="64">
    <h1>Yoyo OS Installer</h1>
    <p>A frontend in GTK 4 and Libadwaita for distinst.</p>
    <hr />
    <a href="https://hosted.weblate.org/engage/yoyo-os/">
<img src="https://hosted.weblate.org/widgets/yoyo-os/-/first-setup/svg-badge.svg" alt="Stato traduzione" />
</a>
    <br />
    <img src="data/screenshot.png">
</div>

## Copyright Notice
This project is forked from Vanilla os, the purpose is to adapt to the special functions of Yoyo os.
We follow the original GPLv3 agreement, modify and retain the original open source agreement, please note that if there are related vanilla trademarks or other logos, this organization has no commercial rights.

## TODO

[x] Timezone by ip [currently can not use in china]

[ ] Btrfs support [use btrfs for a/b root by default, which can save storage]

[ ] virtual disks like magisks


## Build
### Dependencies
- build-essential
- meson
- libadwaita-1-dev
- gettext
- desktop-file-utils
- libgnome-desktop-4-dev
- libgweather-4-dev
- python3-tz
- python3-requests

### Build
```bash
meson build
ninja -C build
```

### Install
```bash
sudo ninja -C build install
```

## Run
```bash
yoyo-installer
```

### Using custom recipes
Place a new recipe in `/etc/yoyo-installer/recipe.json` or launch the
utility with the `YOYO_CUSTOM_RECIPE` environment variable set to the path
of the recipe.

## Not on Yoyo OS?
Currently, the installer only supports Yoyo OS due to some specific
tasks that are performed during installation. Supporting other distros
is planned for the future.
