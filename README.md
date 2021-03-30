# Cognitive Experiments with Openbci and LSL
A guide on how to run cognitive experiments with openBCI and lsl streaming layer. Currently, in Python, as matlab still seems to have too many issues.

## Setup
The number of combinations of platforms, system libraries, toolchains, and matlab / python versions means that things are unlikely to work out of the box for you. Personally I began with an El Capitan macOS, lsl v1.14.0, and matlab 2015b with the latest openBCI GUI running with cyton+daisy setup. I quickly ran into mex issues and had to download Xcode 7 which built mex files which ofcourse didn't compile on macOS 10.11.... 

The particular setup that ended up working for me was macOS high sierra (10.13.6), python 3.6, liblsl 1.13.1, [psychopy](https://www.psychopy.org/), and [LabRecorder](https://github.com/labstreaminglayer/App-LabRecorder).

There is no was to tackle every concievable problem, but the following are some pointers I hope can be of assitance:
 - Even after you download the dylib files you might have to manually relink "liblsl.dylib" to "liblsl64.1.13.1.dylib", not that if you are running "buid_mex" and you get "Could not locate the file "liblsl.dylib" on your computer. Attempting to download..." then there is an issue.
 - MATLAB: If you get "Symbol not found: ____chkstk_darwin" then the macOS is too old for the dylib being compiled, I upgraded to OS 10.13.6 and used liblsl release 1.13.1 which has dylib for MacOS 10.12 and 10.13
 - labRecorder uses `xdf` which can be opened with "pyxdf", sadly this package doesn't work for python 3 out of the box, but the code can be fixed in 30 minutes to run on python 3, if you have the time please consider putting out a pull request with your fixed code on pyxdf git repo.

## Requirements
- Working openBCI board + GUI
- [psychopy](https://www.psychopy.org/)
- [LabRecorder](https://github.com/labstreaminglayer/App-LabRecorder)
- [liblsl-python](https://github.com/labstreaminglayer/liblsl-Python): needed to send markers
- [pyxdf](https://github.com/xdf-modules/pyxdf)
- [traces](https://pypi.org/project/traces/): For analysis, becuase number of samples varies between trials a bit.
- [mne](https://mne.tools/0.16/auto_tutorials/plot_introduction.html?highlight=segment%20epochs): Optional, makes EEG analysis much easier.

## Running the Experiment
The file `visual_oddball.py` contains the code to run a simple visual odd ball paradigm. Each trial draws a green or a purple circle in the middle of the screen. More specifically, each sequence of 5 circles will contain 4 green ones and one purple circle. The P3 ERP (a positive wave around the 300ms mark) should be elevated for the oddball purple circles compared to the green ones.

Note that line 43 initializes a markers stream which sends a code at the start of each trial to mark if it's a green circle (x) or an oddball (o) trial.

To run the experiment:
- Place the openBCI cap on the head of the participant and make sure the channels are not railed.
- Start streaming in the openBCI GUI and [initialize an lsl stream](https://docs.openbci.com/docs/06Software/01-OpenBCISoftware/GUIWidgets#lsl). This is done by going to "Networking" and choosing the "LSL" protocol, remember to name the channel (for instance "openbci_eeg") and hit start.
- In a terminal, start running the `visual_oddball.py` experiment.
- In a separate terminal shell, start the labRecorder. You should see both the Markers and openbci_eeg streams, check both to record eeg and markers data concurrently. This + xdf solves synchronization pretty well (up to a few milliseconds), this used to be a [huge issue](https://openbci.com/forum/index.php?p=/discussion/1928/timestamps-to-sync-stimulus-and-eeg-vs-external-hardware-trigger).
- Have the subject run the task.

## Analysis
The code in `analysis/analyze_P300.ipynb` uses the recorded stream from the `xdf` file. Please find the data from 3 subjects to play with.
- When loading the XDF files please `synchronize_clocks` see [the issue I had](https://github.com/xdf-modules/pyxdf/issues/75) to get the right time stamps. If something does not look right.
- As you see I used `traces` to resample the data as the number of samples per trials and the time between the samples can vary a little.
-`MNE` has a really nice system for EEG analysis that I strongly recommend, I used it after regularizing the data. It allows for averaging, ERP extraction, outlier removal, and ERP manipulation (such as taking the difference).

## Epilogue
Openbci is on the cusp of being an actual option for EEG research. The difficulty of running visual experiments, sending markers, and recording data is still threatening for the average user, but it can all be overcome in less than a day. Please do not hesitate to ask sari saba-sadiya if you get stuck when following this guide.

