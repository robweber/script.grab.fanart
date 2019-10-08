# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

## [Version 0.15.2](https://github.com/robweber/script.grab.fanart/compare/krypton-0.15.1...robweber:leia-0.15.2)

### Added
- added flake8 tests to TravisCI
- added TravisCI build file to test addon agains kodi-addon-checker
- added Changelog format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
- added badges for license, code style, and kodi version compatibility

### Changed

- changed some code styling based on [flake8](https://github.com/pycqa/flake8/) linting

## [Version 0.15.1](https://github.com/robweber/script.grab.fanart/compare/krypton-0.15.0...robweber:leia-0.15.1)

### Changed
- Make compatible with Leia
- Update libs for python 2/3 compatibility
- use getSettingInt() for numbers

## [Version 0.15.0](https://github.com/robweber/script.grab.fanart/compare/helix-0.14.1...robweber:krypton-0.15.0)

### Changed
- Made compatible with Krypton+ structure
- only update on library change, removed timer
- use waitForAbort to set image refresh, less processor intensive

### Removed

- Removed call to xbmc.sleep with timer value, replaced with Monitor class

## Version 0.14.1

### Changed
- fix for if bad refresh time is given

### Version 0.14.0

### Changed
updated addon.xml for Helix, no longer backwards compatible with Gotham and below. 

## Version 0.13.2

don't change window property until the first set of images have been loaded

## Version 0.13.1

decode json string before parsing

## Version 0.13.0

added logo to Global properties per Jeroen's request

## Version 0.12.9

added path and logo properties for videos

## Version 0.12.8

removed constant logging of what is being displayed

## Version 0.12.7

added a startup window property, per request from Jeroen

## Version 0.12.6

added website tag
removed settings visibility
removed strings

## Version 0.12.5

change startup type to "login" 

## Version 0.12.4

only clear lists when we know there is new content
added try/catch for index error
changed some logging to debug only
icon file updated

## Version 0.12.3

added script ext back but removed visibility in programs area

## Version 0.12.2

### Added
- added source and forum to addon file


### Removed
- Removed Programs extension point. No need for this anymore.

## Version 0.12.1

### Changed
- start populating arrays right away, cuts down initial wait time. Thanks to SpaceMonkey

## Version 0.12.0

### Changed
- fixed incorrect logging, thanks MilhouseVH

## Version 0.11.9

### Added
- added 'global' property

## Version 0.11.8

### Changed
- updated xbmc python version for Frodo/Gotham

## Version 0.11.7

### Changed
- should be greater than or equal to

## Version 0.11.6

### Added
- randomize the array and march through it in order- ensures all fanarts display

## Version 0.11.5

### Added
- added verify to make sure media has required attributes

## Version 0.11.4

### Added
- added additional window properties - thanks MassIV for suggestions

## Version 0.11.3

### Changed
- fixed indentation error, caused update threads to spawn constantly

## Version 0.11.2

### Changed
- Extended refresh time from 10 min to 1 hr
- 10% chance of "video" property showing tv show instead of 25%

## Version 0.11.1

### Added
- Added more window properties

### Changed
- misc fixes

### Removed
- removed need for "mediatype" variable

## Version 0.11.0

### Added
- Total rewrite to use skin properties instead of cache fanart into directory

## Version 0.10.0

### Added
- added check for first run so that cache can be built automatically

## Version 0.0.9

### Added
- added music fanart can be run manually or listen for DB updates

## Version 0.0.8

### Added
- added startup service for fanart grabber. will run on video database update automatically

## Version 0.0.7

### Added
- Added arguments for calling in skins or other programs

## Version 0.0.6

### Added
- added support for ignore_paths

## Version 0.0.5

### Changed
- now prompt to create fanart directory
- minor bug fixes

## Version 0.0.4

### Added
- Added progress bar (if wanted)
- old files removed automatically

### Removed
- Because of CRC hash "download new" option removed

## Version 0.0.3

### Added
- calc the CRC hash like xbmc does

## Version 0.0.2

### Changed
- Use xbmcvfs in case of local paths

## Version 0.0.1

### Added
- First version, should copy files as intended