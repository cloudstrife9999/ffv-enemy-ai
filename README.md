# Final Fantasy V enemy AI utils

This repository contains a collection of utilities for loading, parsing, and visualising the enemy AI in Final Fantasy V.

## Compatibility

The utilities are compatible with the following versions of Final Fantasy V:

- **SNES** (at least Japanese, RPGe, and Project Demi versions)
- **GBA** (at least US and EU versions)

## Features

- **AI loader**: loads AI data for each enemy from the game ROM, and stores each raw AI as a hex string in a global AI JSON file (keyed by enemy ID).
- **AI tokeniser**: for each raw AI, it splits it into a list of tokens, where each token is a list of bytes representing either:
  - a condition
  - an action
  - the block separator byte (0xFE)
  - the active/reactive terminator byte (0xFF)
- **AI parser**: for each tokenised AI, it splits it into active AI and reactive AI, and parses both into a class structure based on condition-action rules.
- **AI visualiser**: for each parsed AI, it generates both a JSON representation of its rules, and a more compact text representation of its rules, which is easier to read and understand.

The tokeniser and the parser also validate the AI syntactically and semantically.

## Usage

TBA
