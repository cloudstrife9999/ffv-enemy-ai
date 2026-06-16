# TODO List

## [parser/rule.py](parser/rule.py)

- Line 7: # TODO: Implement this.

## [parser/enemy_ai.py](parser/enemy_ai.py)

- Line 6: # TODO: Implement this.

## [parser/parser.py](parser/parser.py)

- Line 16: # TODO: rather than simply moving through the states, build a tree of rule objects as we parse the tokens, and add a getter property to return the tree of rule objects.

## [parser/enums/party_member_offset.py](parser/enums/party_member_offset.py)

- Line 137: return self.name.replace("_", " ").title()  # TODO: refine this.

## [parser/enums/global_event.py](parser/enums/global_event.py)

- Line 47: return self.name.replace("_", " ").title()  # TODO: refine this.

## [parser/enums/item.py](parser/enums/item.py)

- Line 5: # TODO: migrate to GBA names.
- Line 233: return self.name.replace("_", " ").title()  # TODO: refine this.

## [parser/enums/action_code.py](parser/enums/action_code.py)

- Line 21: return self.name.title().replace("_", " ")  # TODO: refine this.

## [parser/enums/target.py](parser/enums/target.py)

- Line 45: ENKIDU = 0x27  # TODO: check this.
- Line 53: PARTY_MEMBER_1_IF_DEAD = 0x2F  # TODO: check if it targets Bartz specifically, or whoever is in the first party slot.
- Line 54: PARTY_MEMBER_2_IF_DEAD = 0x30  # TODO: check if it targets Lenna specifically, or whoever is in the second party slot.
- Line 55: PARTY_MEMBER_3_IF_DEAD = 0x31  # TODO: check if it targets Galuf specifically, or whoever is in the third party slot.
- Line 56: PARTY_MEMBER_4_IF_DEAD = 0x32  # TODO: check if it targets Faris specifically, or whoever is in the fourth party slot.
- Line 140: return "Enkidu (TODO: check if this is correct)"

## [parser/enums/ability.py](parser/enums/ability.py)

- Line 5: # TODO: Complete migrating to GBA version names.
- Line 250: return self.name.replace("_", " ").title()  # TODO: refine this.
