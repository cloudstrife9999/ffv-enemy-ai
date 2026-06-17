# Final Fantasy V enemy AI utils

This repository contains a collection of utilities for loading, parsing, and visualising the enemy AI in Final Fantasy V.

## Compatibility

The utilities are compatible with the following versions of Final Fantasy V:

- **SNES** (at least Japanese, RPGe, and Project Demi versions)
- **GBA** (at least US and EU versions)

## Features

- **AI loader**: loads AI data for each enemy from the game ROM, and stores each raw AI as a hex string in a global AI JSON file (keyed by enemy ID).
- **AI parser**: given an enemy AI hex string, it:
  - Tokenises it.
  - Validates it syntactically and semantically.
  - Splits it into active AI and reactive AI.
  - Parses both active and reactive AI into a class structure based on condition-action rules.
- **AI visualiser**: for each parsed AI, it generates both a JSON representation of its rules, and a more compact text representation of its rules, which is easier to read and understand.

## Usage

TBA
