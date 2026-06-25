# TODO List

## [parser/actions/random_selection_action.py](parser/actions/random_selection_action.py)

- Line 43: "action": "RANDOM_SELECTION",  # TODO: workaround to avoid the 0xFD name collision with AI_COMMAND, which is also 0xFD.

## [parser/actions/ai_command_action.py](parser/actions/ai_command_action.py)

- Line 32: "action": "AI_COMMAND",  # TODO: workaround to avoid the 0xFD name collision with RANDOM_SELECTION, which is also 0xFD.

## [parser/actions/unknown_f5_action.py](parser/actions/unknown_f5_action.py)

- Line 8: # TODO: find out what this action actually does.

## [parser/enums/snes_stats_and_properties_table.py](parser/enums/snes_stats_and_properties_table.py)

- Line 137: return self.name.replace("_", " ").title()  # TODO: refine this.

## [parser/enums/gba_stats_and_properties_table.py](parser/enums/gba_stats_and_properties_table.py)

- Line 5: # TODO: this only works for the SNES version. The GBA version has a different table/order.
- Line 138: return self.name.replace("_", " ").title()  # TODO: refine this.

## [parser/enums/target_count.py](parser/enums/target_count.py)

- Line 6: # TODO: check if it is more fine-grained than the current representation.

## [parser/enums/target.py](parser/enums/target.py)

- Line 45: ENKIDU = 0x27  # TODO: check this.

## [parser/conditions/hit_by_command_category_condition.py](parser/conditions/hit_by_command_category_condition.py)

- Line 1: # TODO: implement this.

## [parser/conditions/hit_by_command_condition.py](parser/conditions/hit_by_command_condition.py)

- Line 10: # TODO: split this class into two separate classes: one for HIT_BY_COMMAND_WITH_ELEMENT and one for HIT_BY_COMMAND_WITH_CATEGORY, since they have different semantics.

## [parser/conditions/lone_enemy_condition.py](parser/conditions/lone_enemy_condition.py)

- Line 7: # TODO: the third byte is the count of enemies (other than this enemy) for this condition to be true.

## [parser/conditions/a2_comparison.py](parser/conditions/a2_comparison.py)

- Line 7: # TODO: find out what this contition actually checks.

## [parser/conditions/hit_by_elemental_command_condition.py](parser/conditions/hit_by_elemental_command_condition.py)

- Line 1: # TODO: implement this.
