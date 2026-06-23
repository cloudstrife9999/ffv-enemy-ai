# TODO List

## [parser/special_abilities.py](parser/special_abilities.py)

- Line 1: # TODO: implement this class binding enemy codes/names to special abilities names.

## [parser/actions/random_selection_action.py](parser/actions/random_selection_action.py)

- Line 43: "action": "RANDOM_SELECTION",  # TODO: workaround to avoid the 0xFD name collision with AI_COMMAND, which is also 0xFD.

## [parser/actions/ai_command_action.py](parser/actions/ai_command_action.py)

- Line 32: "action": "AI_COMMAND",  # TODO: workaround to avoid the 0xFD name collision with RANDOM_SELECTION, which is also 0xFD.

## [parser/enums/stats_and_properties_table.py](parser/enums/stats_and_properties_table.py)

- Line 5: # TODO: this only works for the SNES version. The GBA version has a different table/order.
- Line 138: return self.name.replace("_", " ").title()  # TODO: refine this.

## [parser/enums/global_event.py](parser/enums/global_event.py)

- Line 63: return self.name.replace("_", " ").title()  # TODO: refine this.

## [parser/enums/item.py](parser/enums/item.py)

- Line 5: # TODO: migrate to GBA names.
- Line 233: return self.name.replace("_", " ").title()  # TODO: refine this.

## [parser/enums/target_count.py](parser/enums/target_count.py)

- Line 6: # TODO: check if it is more fine-grained than the current representation.

## [parser/enums/action_code.py](parser/enums/action_code.py)

- Line 21: return self.name.title().replace("_", " ")  # TODO: refine this.

## [parser/enums/target.py](parser/enums/target.py)

- Line 45: ENKIDU = 0x27  # TODO: check this.

## [parser/conditions/hit_by_command_condition.py](parser/conditions/hit_by_command_condition.py)

- Line 10: # TODO: split this class into two separate classes: one for HIT_BY_COMMAND_WITH_ELEMENT and one for HIT_BY_COMMAND_WITH_CATEGORY, since they have different semantics.

## [parser/conditions/lone_enemy_condition.py](parser/conditions/lone_enemy_condition.py)

- Line 7: # TODO: the third byte is the count of enemies (other than this enemy) for this condition to be true.
