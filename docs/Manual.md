# Creating a manual (*help.html*, *help/*)
In this step, you will customize the supplied readme/help document to suit the needs of your game.
## Overview

Ren'Py used to ship a generic *README.html* file in the base project folder of compiled games. This included basic controls and a brief allusion to the use of open source software. With the new GUI system, this was replaced by two in-game screens, Help and About.

While these screens work fine for mobile, they may not be ideal for desktop games. First of all, there are many more topics you may want to mention to your players, like the [basic troubleshooting info](https://www.renpy.org/doc/html/problems.html) from Ren'Py's online end-user docs, that would be impractical or non-sensical ("help! I can't launch the game!") to include in an in-game screen.

Furthermore, linking to Ren'Py's docs is not ideal for games aspiring to appear white-label, and requires players to have internet access just to read troubleshooting tips and licensing/software information.

My solution to this is a robust HTML5 document which is viewable offline and has room for all the information you could ever want to impart on your dear players. It's based loosely on [the HTML manual I put together for Pizza Game](https://help.pizzagame.party/), which should give you an idea of the general layout.

The manual included with this project for your use is located in *help.html*, and relies on various styles, images, subpages and scripts located in the base directory's *help* subfolder.

### Cool, but why HTML?!
HTML offers many advantages over other game documentation formats:

#### Why not a text file?
Text files (.txt, .md, .toml, whatever) are suitable for if you want to pass a lot of readme content to Python script in your game, to then be formatted onto a screen. However, for manuals that are accessible outside the game:

1. HTML allows linking between multiple documents, so you don't have to cram everything into one file. This allows us to include the full texts of a variety of licenses without making the manual impossibly long.
1. Lengthy txt files usually rely on arbitrary line breaks to be readible, and are generally styled using ASCII art and other techniques that make them inaccessible to screenreaders.
1. HTML lets you include pictures, audio, video, functional web links, and of course, pretty styles to match your game! :)
1. You can host a functional online version of the manual for users who don't own your game or to accompany non-desktop versions of your game.

#### Why not a PDF?
PDFs are a better fit if you intend to make a print version of your manual for physical distribution. However, for the majority of digital-only Ren'Py games:

1. HTML is much easier to author and style than a PDF. You can do it with the text or code editor you're already using for the rest of your Ren'Py game.
1. You can update the manual without needing re-export it from your word processing or desktop publishing program.
1. An HTML manual is more compatible with version control systems your project might be using already.
1. [You can add accessibility features to HTML without proprietary software](https://equidox.co/blog/pdf-vs-html-which-is-the-best-route-to-reach-wcag-2-0/).
1. HTML is more suitable for digital viewing -- it's mobile-responsive and generally has a smaller file size.

## How to use the manual template
First of all, this setup is intended for desktop games. If your game is <u>only</u> meant to be played on web or mobile, you should delete or ignore these files when building. (You may want to host the manual online, but you certainly don't need it in the compiled build.) Mobile devs, you'll instead have to rely on in-game screens, an app store description, and a passion for creative copywriting.

For everyone else, party time!

### Features
This template comes with a few tools to make your HTML-manual-writing life easier.

Provided you format your sections semantically (i.e., your `H3` isn't randomly followed by an `H6`), *toc.js* will automatically generate a table of contents based on your section heading tags. Make sure your heading tags don't have any additional attributes.

The table of contents sticks to the side on desktop layouts, but keyboard users can skip over it using the tab-accessible "skip to content" button. (Oh no, my WordPress is showing!!)

Inside the *help/licenses* folder, you'll find accessible, HTML5 versions of many open source licenses, which you can link to when mentioning the open source or Creative Commons-licensed resources used by your game.

These include the Artistic License, CC-BY-4.0, CC-BY-3.0 (plus a human-readable version), GPLv2, iconmonstr license, LGPLv2.1, MIT License, Modified (3-clause) BSD License, Pixabay license, SIL-OFL 1.1, Unlicense, and zlib license.

There are also some specific licenses used [Ren'Py and its dependencies](https://www.renpy.org/doc/html/license.html): the Bitstream Vera License, Bzip2 license, FreeType Project License, Independent JPEG Group License, PNG License (for libpng), and the Python License.

Extensive licenses like the LGPL have `<section>` elements with ids so you can link to just a part of the license if you're so inclined.

### Basic steps
This document will explain how to fill in the manual's placeholder text section by section, and then make adjustments depending on unique features of your game. (You are also welcome to delete everything inside the `<main>` tag and TOTALLY FREEWHEEL IT.)

The text you will <u>need</u> to replace (or delete) is wrapped in braces. Some placeholders appear multiple times, so you can do a find/replace for them, ideally across the project folder. These are `{Your Game}` (the name of your project) and `{Your Name}` (you or your dev team).

Most placeholders are pretty self-explanatory.

This boilerplate manual includes a basic troubleshooting section, minimum system requirements, save folder locations, and info on Ren'Py's licensing that you can use out of the box without having to rifle through Ren'Py's documentation.

Here's an overview of the sections. With each section there's a list of non-obvious changes you'll have to make depending on the characteristics of your game. The list omits obvious points like "if you added a feature, you should mention that feature," so use your noggin!

#### Section 1: Introduction
According to the documentation, Ren'Py-built games support down to Windows XP/Vista and Mac OS X 10.6 (Snow Leopard), so that's what's written by default.

- Releasing your game on Steam: change the [minimum Windows/Mac requirements](https://partner.steamgames.com/doc/store/application/platforms) to Windows 7 and Mac OS X 10.11 (El Capitan).
- Releasing your game on Itch app but not Steam: change the [minimum Windows requirements](https://itch.io/docs/app/faq#im-using-windows-xp-windows-vista-and-the-app-doesn-and-rsquot-work) to Windows 7.
- Changed `config.save_directory` to None: remove the section on separate save folders.

#### Section 2: Basics
The control and accessibility information here vaguely corresponds with defaults of this project template, rather than Ren'Py defaults necessarily. For example, the "screenshot" key is F12.

- Disabled rollback: remove rollback and rollforward from the list.
- Restored Ren'Py's accessibility menu: change where it says the features are accessible through preferences.
- Game is mobile only: remove self-/clipboard-voicing list item and section.
- Removed self-voicing: remove self-/clipboard-voicing list items and sections.
- Changed how self-voicing is accessed: update the listed keyboard shortcuts and where it says "preference menu."
- Game is desktop only: remove "Self-voicing mode is not supported on Android, iOS, or Chrome OS."
- Game is OS-exclusive: remove irrelevant OS-specific troubleshooting sections.
- Releasing on Steam: remove the first list item (starting with "10.6 (Snow Leopard)...") and change the second list item to start with "10.11 (El Capitan)."

#### Section 3: Troubleshooting

- Game is mobile only: delete entire "game fails to launch" and "performance issues" sections. Maybe move "Bug Reports" to "Credits & Contact" section and remove "Troubleshooting" entirely.
- Don't want to provide email support: remove the note about offering email support just above "Performance issues."
- Not releasing on Windows: remove "File path encoding issues" section.
- Releasing on Steam: remove "Running on non-primary display" section.

#### Section 5: Legal
(Insert obligatory IANAL warning here.)

Here's a great place to specify include your EULA, product warranty, and usage rights information, as well as the *excessive* amount of text required to document the open source libraries powering your game.

The license section more or less replicates Ren'Py's documentation page on the same. The Ren'Py library comes with its own license file, which mentions the licenses of all the code it depends on. It also includes license files for Deja Vu Sans and OpenDyslexic.

Similarly, the CSS and javascript files included with this manual template have copyright information at the top. Better safe than sorry, but if you absolutely hate how this long-ass section looks, you probably don't need to include all the information on code open source licenses.

However, you should definitely include license info on any copyrighted works used with permission as well as any visual/sound assets that are linkware or Creative Commons-licensed, <u>especially</u> if you don't mention these in the credits at the end of your game.

- Removed ability to change font and use of DejaVu Sans: remove respective font copyright information
- Not releasing on Steam: remove the section on the Steamworks API.
- Added additional third-party Python modules: mention them here.
- Removed dynamic table of contents from manual: remove "Pure JS Table of Contents" from copyrights

### Intermediate steps
#### Styling the manual
Now that your manual has the right info, you can style it to match your game. You can manage most style customizations (such as fonts, backgrounds, and basic elements) in *help/css/style.css*.

This template includes some basic styling and elements from [Spectre.css](https://picturepan2.github.io/spectre/). For more thorough manual styling, be sure to look through *help/css/spectre.css* to adjust colors used in elements such as pull quotes.

#### Changing file structure
If you change this file structure around (like moving the main file into the "help" folder), remember to update file paths pointing to license pages and assets in `help.html`.

For clarity, you may want to delete any files in the help folder you don't end up using, such as images.

The following license files are not used by Ren'Py or its dependencies, and can thus be deleted from the folder if you don't need them:
* cc3-human
* cc3
* cc4
* iconmonstr
* pixabay
* unlicense

#### Adding new licenses
If you need to reference a license that's not included in under *help/licenses*, make a copy of *help/licenses/template.html* and use it to create your own license page. Yeah, you have to format everything manually. Now you know how it feels to be me for a day.

## Removing this feature
If you don't like the built-in HTML manual (wow rude):
1. Delete *help.html*
1. Delete the *help/* folder
1. Set `config.help` (*config.rpy*) to whatever help screen or readme file you replace this with.
1. Update `build.documentation()` (*dev_build.rpy*) with the name if your readme file, or delete the line if you don't have one.
1. If your new help file is called *README.md* and resides in the base directory, remove the line reading `build.classify("README.md", None)` in *dev_build.rpy*, or else it won't show up in the compiled game!
