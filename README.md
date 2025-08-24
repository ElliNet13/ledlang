# LEDLang
[![Publish to PyPI](https://github.com/ElliNet13/ledlang/actions/workflows/deploy.yml/badge.svg)](https://github.com/ElliNet13/ledlang/actions/workflows/deploy.yml)
![PyPI - Version](https://img.shields.io/pypi/v/ledlang)
![GitHub License](https://img.shields.io/github/license/ElliNet13/ledlang)
[![Run Pytest](https://github.com/ElliNet13/ledlang/actions/workflows/pytest.yml/badge.svg)](https://github.com/ElliNet13/ledlang/actions/workflows/pytest.yml)

<br>
LED Programming Language, mostly for controlling a Micro:bit but others can be used.

[to-the-serial Micro:bit Makecode Helper](https://ellinet13.github.io/to-the-serial/)

| Command  | What they do                    |
|----------|---------------------------------|
| PLOT     | Turn on a pixel on the screen   |
| CLEAR    | Clear the screen                |

# Problems
| Item     | Problem                                                                                        |
|----------|------------------------------------------------------------------------------------------------|
| TEXT     | Only works if the height of your display is 5, you can get around this bug by using REALSIZE   |

# Notes
| Item         | Problem                                     |
|--------------|---------------------------------------------|
| REALSIZE     | Can lag since division is used every PLOT   |

# TODO
| What I need to do                                            |
|--------------------------------------------------------------|
| Make a intermediate layer of compiling so the conpiled code will be correct and won't be changed by runtime stuff
| Make plot be able to batch
| Use a local echo to know if a point is already drawn
| Use one letter for each command 

[Github repo]({{githubRepoLink}})<br>
Test Status for this: {{badgeForTests}}<br>
[View this deploy]({{runLink}})
