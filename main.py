#!/usr/bin/env python3

from parser.snes_ai_parser import SNESAIParser
from parser.gba_ai_parser import GBAAIParser

def main() -> None:
    snes_parser: SNESAIParser = SNESAIParser()
    gba_parser: GBAAIParser = GBAAIParser()

    snes_parser.run()
    gba_parser.run()

if __name__ == "__main__":
    main()
