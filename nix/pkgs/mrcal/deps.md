## Already Packaged
* [x] re2c: parser-generator for the C code to parse .cameramodel files. At least version 2 is required.
* [x] pythonPackages.pyyaml: yaml parser used for the OpenCV, Kalibr model reading
* [x] freeimage: an image reading/writing library. Most distros have this available.
## Probably super painful (Likely written in C)
* [ ] mrbuild: the build system. If you can't get it from the package manager, just run make, and follow the printed message to get a local copy of mrbuild.
* [ ] libdogleg-dev: the optimization library. You need at least version 0.15.3.
* [ ] mrgingham: the chessboard corner finder. This isn't strictly a requirement - any corner finder can be used. If you want to use this one (and you can't use the packages), you need to build it.
  * [x] opencv
  * [x] boost
  * [x] pkg-config
  * [x] mawk
  * [x] perl
  * [x] python3
  * [x] python3Packages.numpy
## PyPi Allegedly
* [ ] numpysane: The make-numpy-reasonable library. You absolutely need at least version 0.35. Available in the usual places Python libraries live. This is a python-only library. Simply downloading the sources and pointing the PYTHONPATH there is sufficient.
* [ ] gnuplotlib: The plotting library used in all the visualizations. You need at least version 0.38. Available in the usual places Python libraries live. This is a python-only library. Simply downloading the sources and pointing the PYTHONPATH there is sufficient.
## Optional (for mrcal-stereo)
* [ ] pyFltk: Python bindings for the FLTK GUI toolkit. Optional. Used only in the visualizer in the mrcal-stereo tool.
* [ ] python3-gl-image-display: an image widget for FLTK. Optional. Used only in the visualizer in the mrcal-stereo tool.
* [ ] libelas-dev: the ELAS stereo matcher. Used as an option in the mrcal-stereo tool. Optional.
## Tests Only
* [ ] vnlog: the toolkit to manipulate textual tables. You only need this for the test suite. There's nothing to build. Simply downloading the sources and pointing the PATH there is sufficient.
