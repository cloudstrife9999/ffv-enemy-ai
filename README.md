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
      Turn #1: random(Maelstrom, !Attack, Roulette)
      Turn #2: random(Ice Storm, Atomic Ray, Lightning)
      Turn #3: Consecutive actions:
                 random(Maelstrom, !Attack, Roulette)
                 random(Mighty Guard, Level 2 Old, Level 3 Flare)
      Turn #4: Consecutive actions:
                 random(!Attack, !Attack, Evil Eye)
                 random(!Attack, !Attack, Poison Breath)
  Default rule:
    Conditions:
      Unconditional
    Actions:
      Turn #1: [Stay idle]
      Turn #2: Consecutive actions:
                 Set Var_00 to 1
                 Ability: Tidal Wave
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
      random([Unnamed script trigger], [Stay idle], [Stay idle])
```
