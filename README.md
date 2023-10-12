**Instructions for FontForge Language scripts**

10 Oct 2023

These scripts are written in python using the python version 3.8
imbedded in FontForge.

Objective:

Generate backfonts and documentation for the different versions of SUN.

Requirements:

-   FontForge 2020-03-14: <https://fontforge.org/en-US/>. Note. Some
    versions of Fontforge have problems with tkinter

-   Fontforge python documentation <https://fontforge.org/python.html>

-   potrace: potrace is part of fontforge.

-   Font for type style or language i.e. times.ttf

-   Imagemagick: <https://imagemagick.org/index.php>

-   Dictionary of primary words as a csv file In the following columns:

    Symbol, English Name, Language Name, Unicode(string), Reference

    i.e. sym, Aaron, Aaron, eb0d, Acts 7:40

Product::

-   Language backfont.(sfd, woff, ttf)

**Setup:**

> Install Fontforge and Imagemagick per default.
>
> Create a work directory containing all the python scripts and config
> files.
>
> From the work directory create Log, Dist, Input and Svg directories
>
> The Log directory keeps all the log files of the code run
>
> The Dist directory keeps the files for distribution.
>
> Place all files used for input in the Input directory. i.e. sfd, kmn,
> dictionary, times.ttf.
>
> The Svg directory contains the svg images for the backfont file.

**Configuration::**

> **fontsettings.json -** This file contains font parameters and how the
> svg files are built. They shouldn't need to be changed.

**Running Scripts:**

> Open a Command Prompt window and change to the directory where your
> code is.
>
> A basic FontForge command is.
>
> fontforge -script pythonscript.py \...params....
>
> Most of the function names should be self explanatory, however some
> variable names may not be quite so obvious.
>
> The order of running the scripts is important. They should be executed
> in the
>
> following order: csv2svg_ttf, svg2font_ttf
>
> Included are windows batch files which can be used as examples of
> running each script.

**BackFont Procedures:**

> The requirements to generate scripts
>
> A primary reference file as described in the requirements.Times.ttf
> (or other ttf font file)
>
> Execute csv2svg_ttf.py
>
> Execute svg2Font_ttf.py
>
> If need to verify output execute back2doc.py

**Scripts:**

> **csv2svg_ttf.py** -- Takes the input.csv file and generates an image
> of each word as a svg file. The Svg folder should be cleared before
> running to ensure a clean build.
>
> Execution: fontforge -script csv2svg_unicode.py %csv_infile%
> %ttf_file% %language%
>
> Language is a 3 or 4 letter term representing the language i.e. ENG or
> FRAA
>
> **svg2Font_ttf.py** -- Uses the svg files from the previous script to
> import into the backfont sfd file. It also creates a ttf and woff
> file.
>
> Execution: fontforge -quiet -script svg2Font_unicode.py %csv_infile%
> %csv_file% %language% %outfile%
>
> **back2doc_ttf.py** -- This creates a text file for the purpose of
> verifying the quality of the backfont. Glancing through the file will
> show anomalies to be corrected. Either missing or overlayed or out of
> alignment words.
>
> Execution: cmd /c fontforge -quiet -script back2doc_unicode.py
> %sfd_infile% %outfile%
