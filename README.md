# ACOReader
[![License: The Unlicense](https://img.shields.io/badge/license-The%20Unlicense-success)](https://unlicense.org/)

## Table of Contents
* [General Information](#general-information)
* [Usage](#usage)
* [To-Do](#todo)
* [Issues/Feature Requests](#issues-feature-requests)

## General Information
ACOReader was created as a direct response to the 2022 decision by
Adobe and Pantone to hide the information regarding color reproduction
of Pantone swatches.

It allows a user with access to .aco color swatch files, including those
originally provided by Adobe for Pantone swatches, to convert them into
both a text file with the color information, as well as into a different
.aco file.

## Usage
To use ACOReader, you will need to download a release once it is available,
or you can download the source directly and use it with Python.

Once you do, you can just drop the executable into the folder alongside the
.aco files that need to be converted, open it, and let it do its magic.

If you are using the direct source, you can simply open a terminal window
and:

```
$ python3 ./main.py
```

## To-Do
This is a brand-new project that I scripted very quickly. There is almost
guaranteed to be bugs in the code, as well as being generally unoptimized.
However, the current focuses are:

* Create executable files for Linux, Windows, and Apple to allow for easier use.
* Add the ability to create new .aco files, as opposed to simply getting the color information.

## Issues/Feature Requests
If you have any problems using ACOReader, feel free to [report it](https://github.com/char-lock/aco_reader/issues). You are also to welcome to [request additional features](https://github.com/char-lock/aco_reader/issues).
