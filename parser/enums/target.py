from enum import IntEnum
from typing import override


class Target(IntEnum):
    BARTZ = 0x00
    LENNA = 0x01
    GALUF = 0x02
    FARIS = 0x03
    KRILE = 0x04
    ENEMY_IN_SLOT_1 = 0x05
    ENEMY_IN_SLOT_2 = 0x06
    ENEMY_IN_SLOT_3 = 0x07
    ENEMY_IN_SLOT_4 = 0x08
    ENEMY_IN_SLOT_5 = 0x09
    ENEMY_IN_SLOT_6 = 0x0A
    ENEMY_IN_SLOT_7 = 0x0B
    ENEMY_IN_SLOT_8 = 0x0C
    SELF_UNLESS_FORCED = 0x0D
    ALL_NON_SELF_ENEMIES = 0x0E
    ALL_ENEMIES = 0x0F
    RANDOM_NON_SELF_ENEMY = 0x10
    RANDOM_ENEMY = 0x11
    ALL_FRONT_ROW_PARTY_MEMBERS = 0x12
    ALL_BACK_ROW_PARTY_MEMBERS = 0x13
    RANDOM_FRONT_ROW_PARTY_MEMBER = 0x14
    RANDOM_BACK_ROW_PARTY_MEMBER = 0x15
    ALL_FEMALE_PARTY_MEMBERS = 0x16
    ALL_MALE_PARTY_MEMBERS = 0x17
    RANDOM_FEMALE_PARTY_MEMBER = 0x18
    RANDOM_MALE_PARTY_MEMBER = 0x19
    ALL_DEAD_PARTY_MEMBERS = 0x1A
    RANDOM_DEAD_PARTY_MEMBER = 0x1B
    ALL_ENEMIES_WITH_REFLECT = 0x1C
    RANDOM_ENEMY_WITH_REFLECT = 0x1D
    ALL_ENEMIES_WITH_CRITICAL = 0x1E
    RANDOM_ENEMY_WITH_CRITICAL = 0x1F
    ALL_ENEMIES_WITH_LESS_THAN_HALF_HP = 0x20
    RANDOM_ENEMY_WITH_LESS_THAN_HALF_HP = 0x21
    RANDOM_PARTY_MEMBER_WITHOUT_REFLECT = 0x22
    ALL_PARTY_MEMBERS = 0x23
    RANDOM_PARTY_MEMBER = 0x24
    ALL_DEAD_ENEMIES = 0x25
    RANDOM_DEAD_ENEMY = 0x26
    ENKIDU = 0x27  # TODO: check this.
    BARTZ_IF_JUMPING = 0x28
    LENNA_IF_JUMPING = 0x29
    FARIS_IF_JUMPING = 0x2A
    GALUF_IF_JUMPING = 0x2B
    KRILE_IF_JUMPING = 0x2C
    TICK_ACTOR = 0x2D
    ALL_PARTY_MEMBERS_MATCHING_CONDITION = 0x2E  # Condition from event bitmask
    PARTY_MEMBER_1_IF_DEAD = 0x2F  # TODO: check if it targets Bartz specifically, or whoever is in the first party slot.
    PARTY_MEMBER_2_IF_DEAD = 0x30  # TODO: check if it targets Lenna specifically, or whoever is in the second party slot.
    PARTY_MEMBER_3_IF_DEAD = 0x31  # TODO: check if it targets Galuf specifically, or whoever is in the third party slot.
    PARTY_MEMBER_4_IF_DEAD = 0x32  # TODO: check if it targets Faris specifically, or whoever is in the fourth party slot.

    def get_nominal_predicate(self) -> str:
        match self:
            case Target.BARTZ | Target.LENNA | Target.GALUF | Target.FARIS | Target.KRILE |\
                    Target.ENEMY_IN_SLOT_1 | Target.ENEMY_IN_SLOT_2 | Target.ENEMY_IN_SLOT_3 | Target.ENEMY_IN_SLOT_4 |\
                    Target.ENEMY_IN_SLOT_5 | Target.ENEMY_IN_SLOT_6 | Target.ENEMY_IN_SLOT_7 | Target.ENEMY_IN_SLOT_8 |\
                    Target.SELF_UNLESS_FORCED | Target.RANDOM_NON_SELF_ENEMY | Target.RANDOM_ENEMY | Target.RANDOM_FRONT_ROW_PARTY_MEMBER |\
                    Target.RANDOM_BACK_ROW_PARTY_MEMBER | Target.RANDOM_FEMALE_PARTY_MEMBER | Target.RANDOM_MALE_PARTY_MEMBER |\
                    Target.RANDOM_DEAD_PARTY_MEMBER | Target.RANDOM_ENEMY_WITH_REFLECT | Target.RANDOM_ENEMY_WITH_CRITICAL |\
                    Target.RANDOM_ENEMY_WITH_LESS_THAN_HALF_HP | Target.RANDOM_PARTY_MEMBER_WITHOUT_REFLECT | Target.RANDOM_PARTY_MEMBER |\
                    Target.RANDOM_DEAD_ENEMY | Target.ENKIDU | Target.BARTZ_IF_JUMPING | Target.LENNA_IF_JUMPING | Target.FARIS_IF_JUMPING |\
                    Target.GALUF_IF_JUMPING | Target.KRILE_IF_JUMPING | Target.TICK_ACTOR | Target.PARTY_MEMBER_1_IF_DEAD |\
                    Target.PARTY_MEMBER_2_IF_DEAD | Target.PARTY_MEMBER_3_IF_DEAD | Target.PARTY_MEMBER_4_IF_DEAD:
                return "is"
            case Target.ALL_NON_SELF_ENEMIES | Target.ALL_ENEMIES | Target.ALL_FRONT_ROW_PARTY_MEMBERS | Target.ALL_BACK_ROW_PARTY_MEMBERS |\
                    Target.ALL_FEMALE_PARTY_MEMBERS | Target.ALL_MALE_PARTY_MEMBERS | Target.ALL_DEAD_PARTY_MEMBERS | Target.ALL_ENEMIES_WITH_REFLECT |\
                    Target.ALL_ENEMIES_WITH_CRITICAL | Target.ALL_ENEMIES_WITH_LESS_THAN_HALF_HP | Target.ALL_PARTY_MEMBERS |\
                    Target.ALL_DEAD_ENEMIES | Target.ALL_PARTY_MEMBERS_MATCHING_CONDITION:
                return "are"
            case _:
                raise ValueError(f"{self} is not a valid {self.__class__.__name__}.")

    def for_mid_sentence(self) -> str:
        name: str = str(self)

        if name.split()[0] not in ["Bartz", "Lenna", "Galuf", "Faris", "Krile", "Enkidu"]:
            return name[0].lower() + name[1:]
        else:
            return name

    @override
    def __str__(self) -> str:
        match self:
            case Target.BARTZ | Target.LENNA | Target.GALUF | Target.FARIS | Target.KRILE:
                return f"{self.name.capitalize()}"
            case Target.ENEMY_IN_SLOT_1 | Target.ENEMY_IN_SLOT_2 | Target.ENEMY_IN_SLOT_3 | Target.ENEMY_IN_SLOT_4 | Target.ENEMY_IN_SLOT_5 | Target.ENEMY_IN_SLOT_6 | Target.ENEMY_IN_SLOT_7 | Target.ENEMY_IN_SLOT_8:
                return f"The enemy in slot #{self.value - Target.ENEMY_IN_SLOT_1.value + 1}"
            case Target.SELF_UNLESS_FORCED:
                return "Self"
            case Target.ALL_NON_SELF_ENEMIES:
                return "All non-self enemies"
            case Target.ALL_ENEMIES:
                return "All enemies"
            case Target.RANDOM_NON_SELF_ENEMY:
                return "A random non-self enemy"
            case Target.RANDOM_ENEMY:
                return "A random enemy"
            case Target.ALL_FRONT_ROW_PARTY_MEMBERS:
                return "All front row party members"
            case Target.ALL_BACK_ROW_PARTY_MEMBERS:
                return "All back row party members"
            case Target.RANDOM_FRONT_ROW_PARTY_MEMBER:
                return "A random front row party member"
            case Target.RANDOM_BACK_ROW_PARTY_MEMBER:
                return "A random back row party member"
            case Target.ALL_FEMALE_PARTY_MEMBERS:
                return "All female party members"
            case Target.ALL_MALE_PARTY_MEMBERS:
                return "All male party members"
            case Target.RANDOM_FEMALE_PARTY_MEMBER:
                return "A random female party member"
            case Target.RANDOM_MALE_PARTY_MEMBER:
                return "A random male party member"
            case Target.ALL_DEAD_PARTY_MEMBERS:
                return "All dead party members"
            case Target.RANDOM_DEAD_PARTY_MEMBER:
                return "A random dead party member"
            case Target.ALL_ENEMIES_WITH_REFLECT:
                return "All enemies with the reflect status effect"
            case Target.RANDOM_ENEMY_WITH_REFLECT:
                return "A random enemy with the reflect status effect"
            case Target.ALL_ENEMIES_WITH_CRITICAL:
                return "All enemies with the critical status effect"
            case Target.RANDOM_ENEMY_WITH_CRITICAL:
                return "A random enemy with the critical status effect"
            case Target.ALL_ENEMIES_WITH_LESS_THAN_HALF_HP:
                return "All enemies with less than half HP"
            case Target.RANDOM_ENEMY_WITH_LESS_THAN_HALF_HP:
                return "A random enemy with less than half HP"
            case Target.RANDOM_PARTY_MEMBER_WITHOUT_REFLECT:
                return "A random party member without the reflect status effect"
            case Target.ALL_PARTY_MEMBERS:
                return "All party members"
            case Target.RANDOM_PARTY_MEMBER:
                return "A random party member"
            case Target.ALL_DEAD_ENEMIES:
                return "All dead (or with 0 HP) enemies"
            case Target.RANDOM_DEAD_ENEMY:
                return "A random dead (or with 0 HP) enemy"
            case Target.ENKIDU:
                return "Enkidu"
            case Target.BARTZ_IF_JUMPING | Target.LENNA_IF_JUMPING | Target.FARIS_IF_JUMPING | Target.GALUF_IF_JUMPING | Target.KRILE_IF_JUMPING:
                return f"{self.name.split("_")[0].capitalize()} (while jumping)"
            case Target.TICK_ACTOR:
                return "Whoever acted in the current tick"
            case Target.ALL_PARTY_MEMBERS_MATCHING_CONDITION:
                return "All party members matching the condition"
            case Target.PARTY_MEMBER_1_IF_DEAD | Target.PARTY_MEMBER_2_IF_DEAD | Target.PARTY_MEMBER_3_IF_DEAD | Target.PARTY_MEMBER_4_IF_DEAD:
                return f"Party member #{self.value - Target.PARTY_MEMBER_1_IF_DEAD.value + 1} (while dead)"
            case _:
                raise ValueError(f"{self} is not a valid {self.__class__.__name__}.")

    @classmethod
    def is_valid_target_id(cls, value: int) -> bool:
        return value in cls._value2member_map_
