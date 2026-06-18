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
- **AI visualiser**: for each parsed AI, it generates:
  - A JSON representation of its rules.
  - An indentation-based AI script representing its rules.

## Usage

TBA

## AI script example

```text
Enemy ID: 169
Enemy Name: Shinryu
ACTIVE RULES:
  Rule #1:
    Conditions:
      Variable Var_00 == 1
    Actions:
      Turn #1: random(Maelstrom, Physical attack, Roulette)
      Turn #2: random(Snowstorm, Atomic Ray, Lightning)
      Turn #3: Consecutive actions:
                 random(Maelstrom, Physical attack, Roulette)
                 random(Mighty Guard, Level 2 Old, Level 3 Flare)
               Consecutive actions:
                 random(Physical attack, Physical attack, Demon Eye (enemy magic))
                 random(Physical attack, Physical attack, Poison Breath)
  Default rule:
    Conditions:
      Unconditional
    Actions:
      Turn #1: Nothing
      Turn #2: Consecutive actions:
                 Set Var_00 to 1
                 Ability: Tidal Wave (enemy magic)
REACTIVE RULES:
  Rule #1:
    Conditions:
      Hit by the unnamed script trigger spell
    Actions:
      Set Var_00 to 0
      Ability: Zombie Breath
  Rule #2:
    Conditions:
      Current HP < 20000
      HP damage just taken
    Actions:
      random(Unnamed script trigger, Nothing, Nothing)
```
