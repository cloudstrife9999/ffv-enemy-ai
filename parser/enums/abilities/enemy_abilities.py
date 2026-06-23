from enum import IntEnum
from typing import override


class EnemyAbilities(IntEnum):
    PHYSICAL_ATTACK = 0x80
    UNNAMED_SPECIAL_ABILITY = 0x81
    RIBBIT = 0xA0
    UNNAMED_LEVEL_DOWN = 0xA1
    FLEE = 0xA2
    UNNAMED_FALSE_IMAGE_SWITCH = 0xA3  # Used by Wendigo, etc. to switch the False Image status with another random enemy.
    UNNAMED_UNHIDE_NEXT_PAGE = 0xA4
    UNNAMED_SELF_KILL = 0xA5  # Bypasses death immunity and heavy nature.
    GRAND_CROSS = 0xA6
    DELTA_ATTACK = 0xA7
    INTERCEPTOR = 0xA8
    BARRIER_CHANGE = 0xA9
    UNNAMED_STAY_IDLE = 0xAA
    WIND_SLASH = 0xAB
    UNNAMED_SCRIPT_TRIGGER = 0xAC
    SEARCH = 0xAD
    HUNDRED_GS = 0xAE
    VANISH = 0xAF  # Self-kill by some enemies when hit by a Gold Needle. Bypasses death immunity and heavy nature.
    REAPER_S_SWORD = 0xB0
    UNNAMED_EXPLODE = 0xB1  # Self-kill by Soul Cannon, Wave Cannon, and all Launcher enemies. Bypasses death immunity and heavy nature.
    BLASTER = 0xB2
    BEAK = 0xB3
    EMBRACE = 0xB4
    SPORE = 0xB5
    POISON_BREATH = 0xB6
    DANCE_MACABRE = 0xB7
    ZOMBIE_POWDER = 0xB8
    ZOMBIE_BREATH = 0xB9
    PARACLETE = 0xBA
    ENTICE = 0xBB
    ENTANGLE = 0xBC
    RAINBOW_WIND = 0xBD
    DANCEHALL_DAZE = 0xBE
    GAMMA_RAY = 0xBF
    WHITE_HOLE = 0xC0
    NEEDLE = 0xC1
    MAELSTROM = 0xC2
    BONE = 0xC3
    TAIL_SCREW = 0xC4
    DIGESTIVE_ACID = 0xC5
    ROCKET_PUNCH = 0xC6
    MUSTARD_BOMB = 0xC7
    ALMAGEST = 0xC8
    QUICKSAND = 0xC9
    ATOMIC_RAY = 0xCA
    FROSTBITE = 0xCB
    ICE_STORM = 0xCC
    FROST = 0xCD
    ELECTROCUTE = 0xCE
    EARTH_SHAKER = 0xCF
    ZANTETSUKEN = 0xD0
    TIDAL_WAVE = 0xD1
    MEGA_FLARE = 0xD2
    DISCHORD = 0xD3
    WEB = 0xD4
    SLIMER = 0xD5
    EARTHQUAKE = 0xD6
    UNNAMED_STRONG_ATTACK = 0xD7
    PANACEA = 0xD8  # Status cleansing.
    IMAGE = 0xD9
    BREATH_WING = 0xDA
    BLAZE = 0xDB
    LIGHTNING = 0xDC
    WAVE_CANNON = 0xDD
    ATTACK = 0xDE
    REMEDY = 0xDF  # Full heal.
    UNNAMED_LAUNCHER_ATTACK = 0xE0  # Used by all Launcher enemies to inflict fractional damage.
    GIGA_FLARE = 0xE1
    ENCIRCLE = 0xE2
    WORMHOLE = 0xE3
    POSSESS = 0xE4
    REVERSE_POLARITY = 0xE5  # Switches all targets' battle row.
    MAGNET = 0xE6
    UNNAMED_FLIP_SPRITE_HORIZONTALLY = 0xE7
    JUMP = 0xE8
    BANISH = 0xE9
    HURRICANE = 0xEA
    EVIL_EYE = 0xEB
    UNNAMED_PULL = 0xEC  # Used by Atomos to pull dead targets.
    UNNAMED_FORFEIT_BATTLE = 0xED  # i.e., let the party win. Used by Sandworm.
    UNNAMED_UNHIDE_ENEMY = 0xEE
    UNNAMED_TERMINATE = 0xEF  # Just terminate the battle. Used by some enemies such as Mover.

    @override
    def __str__(self) -> str:
        match self:
            case EnemyAbilities.PHYSICAL_ATTACK:
                return "!Attack"
            case EnemyAbilities.HUNDRED_GS:
                return "100 Gs"
            case _:
                if self.name.startswith("UNNAMED_"):
                    return self.__unnamed_ability_to_str()
                else:
                    return self.name.replace("_", " ").title().replace(" S ", "'s ")

    def __unnamed_ability_to_str(self) -> str:
        match self:
            case EnemyAbilities.UNNAMED_SPECIAL_ABILITY:
                return "[Special ability]"
            case EnemyAbilities.UNNAMED_LEVEL_DOWN:
                return "[Level down]"
            case EnemyAbilities.UNNAMED_FALSE_IMAGE_SWITCH:
                return "[False Image switch]"
            case EnemyAbilities.UNNAMED_UNHIDE_NEXT_PAGE:
                return "[Unhide next page]"
            case EnemyAbilities.UNNAMED_SELF_KILL:
                return "[Unconditional self-kill]"
            case EnemyAbilities.UNNAMED_STAY_IDLE:
                return "[Nothing]"
            case EnemyAbilities.UNNAMED_SCRIPT_TRIGGER:
                return "[Unnamed script trigger]"
            case EnemyAbilities.UNNAMED_EXPLODE:
                return "[Explode]"
            case EnemyAbilities.UNNAMED_STRONG_ATTACK:
                return "[Strong Attack]"
            case EnemyAbilities.UNNAMED_LAUNCHER_ATTACK:
                return "[Fractional Launcher attack]"
            case EnemyAbilities.UNNAMED_FLIP_SPRITE_HORIZONTALLY:
                return "[Flip sprite horizontally]"
            case EnemyAbilities.UNNAMED_PULL:
                return "[Pull dead targets]"
            case EnemyAbilities.UNNAMED_FORFEIT_BATTLE:
                return "[Forfeit battle]"
            case EnemyAbilities.UNNAMED_UNHIDE_ENEMY:
                return "[Unhide enemy]"
            case EnemyAbilities.UNNAMED_TERMINATE:
                return "[Terminate battle]"
            case _:
                raise ValueError(f"Unknown unnamed ability: {self.name}.")

    @classmethod
    def is_valid_id(cls, value: int) -> bool:
        return value in cls._value2member_map_
