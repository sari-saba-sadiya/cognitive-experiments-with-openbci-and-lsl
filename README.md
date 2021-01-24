# Cognitive Experiments with Openbci and LSL
A guide on how to run cognitive experiments with openBCI and lsl streaming layer. 

## Setup
The number of combinations of platforms, system libraries, toolchains, and matlab versions means that things are unlikely to work out of the box for you. Personally I began with an El Capitan macOS, lsl v1.14.0, and matlab 2015b with the latest openBCI GUI running with cyton+daisy setup. I quickly ran into mex issues and spent had to download Xcode 7 which built max files that didn't compile on macOS 10.11. The particular setup that ended up workign for me was macOS high sierra (10.13.6), matlab to 2017b, liblsl 1.13.1 and building the mex files with Xcode 9.

There is no was to tackle every concievable problem, but the following are some pointers I hope can be of assitance:
 - Even after you download the dylib files you might have to manually relink "liblsl.dylib" to "liblsl64.1.13.1.dylib", not that if you are running "buid_mex" and you get "Could not locate the file "liblsl.dylib" on your computer. Attempting to download..." then there is an issue.
 - If you get "Symbol not found: ____chkstk_darwin" then the macOS is too old for the dylib being compiled, I upgraded to OS 10.13.6 and used liblsl release 1.13.1 which has dylib for MacOS 10.12 and 10.13 
