from enum import IntEnum
from typing import override


# TODO: Complete migrating to GBA version names.
class Ability(IntEnum):
    SPELLBLADE_FIRE = 0x00
    SPELLBLADE_BLIZZARD = 0x01
    SPELLBLADE_THUNDER = 0x02
    SPELLBLADE_POISON = 0x03
    SPELLBLADE_SILENCE = 0x04
    SPELLBLADE_SLEEP = 0x05
    SPELLBLADE_FIRA = 0x06
    SPELLBLADE_BLIZZARA = 0x07
    SPELLBLADE_THUNDARA = 0x08
    SPELLBLADE_DRAIN = 0x09
    SPELLBLADE_BREAK = 0x0A
    SPELLBLADE_BIO = 0x0B
    SPELLBLADE_FIRAGA = 0x0C
    SPELLBLADE_BLIZZAGA = 0x0D
    SPELLBLADE_THUNDAGA = 0x0E
    SPELLBLADE_HOLY = 0x0F
    SPELLBLADE_FLARE = 0x10
    SPELLBLADE_OSMOSE = 0x11
    WHITE_MAGIC_CURE = 0x12
    WHITE_MAGIC_LIBRA = 0x13
    WHITE_MAGIC_POISONA = 0x14
    WHITE_MAGIC_SILENCE = 0x15
    WHITE_MAGIC_PROTECT = 0x16
    WHITE_MAGIC_MINI = 0x17
    WHITE_MAGIC_CURA = 0x18
    WHITE_MAGIC_RAISE = 0x19
    WHITE_MAGIC_CONFUSE = 0x1A
    WHITE_MAGIC_BLINK = 0x1B
    WHITE_MAGIC_SHELL = 0x1C
    WHITE_MAGIC_ESUNA = 0x1D
    WHITE_MAGIC_CURAGA = 0x1E
    WHITE_MAGIC_REFLECT = 0x1F
    WHITE_MAGIC_BERSERK = 0x20
    WHITE_MAGIC_ARISE = 0x21
    WHITE_MAGIC_HOLY = 0x22
    WHITE_MAGIC_DISPEL = 0x23
    BLACK_MAGIC_FIRE = 0x24
    BLACK_MAGIC_BLIZZARD = 0x25
    BLACK_MAGIC_THUNDER = 0x26
    BLACK_MAGIC_POISON = 0x27
    BLACK_MAGIC_SLEEP = 0x28
    BLACK_MAGIC_TOAD = 0x29
    BLACK_MAGIC_FIRA = 0x2A
    BLACK_MAGIC_BLIZZARA = 0x2B
    BLACK_MAGIC_THUNDARA = 0x2C
    BLACK_MAGIC_DRAIN = 0x2D
    BLACK_MAGIC_BREAK = 0x2E
    BLACK_MAGIC_BIO = 0x2F
    BLACK_MAGIC_FIRAGA = 0x30
    BLACK_MAGIC_BLIZZAGA = 0x31
    BLACK_MAGIC_THUNDAGA = 0x32
    BLACK_MAGIC_FLARE = 0x33
    BLACK_MAGIC_DEATH = 0x34
    BLACK_MAGIC_OSMOSE = 0x35
    TIME_MAGIC_SPEED = 0x36
    TIME_MAGIC_SLOW = 0x37
    TIME_MAGIC_REGEN = 0x38
    TIME_MAGIC_MUTE = 0x39
    TIME_MAGIC_HASTE = 0x3A
    TIME_MAGIC_FLOAT = 0x3B
    TIME_MAGIC_GRAVITY = 0x3C
    TIME_MAGIC_STOP = 0x3D
    TIME_MAGIC_TELEPORT = 0x3E
    TIME_MAGIC_COMET = 0x3F
    TIME_MAGIC_SLOWGA = 0x40
    TIME_MAGIC_RETURN = 0x41
    TIME_MAGIC_GRAVIGA = 0x42
    TIME_MAGIC_HASTEGA = 0x43
    TIME_MAGIC_OLD = 0x44
    TIME_MAGIC_METEOR = 0x45
    TIME_MAGIC_QUICK = 0x46
    TIME_MAGIC_BANISH = 0x47
    SUMMON_CHOCOBO = 0x48
    SUMMON_SYLPH = 0x49
    SUMMON_REMORA = 0x4A
    SUMMON_SHIVA = 0x4B
    SUMMON_RAMUH = 0x4C
    SUMMON_IFRIT = 0x4D
    SUMMON_TITAN = 0x4E
    SUMMON_GOLEM = 0x4F
    SUMMON_CATOBLEPAS = 0x50
    SUMMON_CARBUNCLE = 0x51
    SUMMON_SYLDRA = 0x52
    SUMMON_ODIN = 0x53
    SUMMON_PHOENIX = 0x54
    SUMMON_LEVIATHAN = 0x55
    SUMMON_BAHAMUT = 0x56
    SONG_SINEWY_ETUDE = 0x57
    SONG_SWIFT_SONG = 0x58
    SONG_MIGHTY_MARCH = 0x59
    SONG_MANAS_PAEAN = 0x5A
    SONG_HEROS_RIME = 0x5B
    SONG_REQUIEM = 0x5C
    SONG_ROMEOS_BALLAD = 0x5D
    SONG_ALLURING_AIR = 0x5E
    SUMMON_CHOCO_KICK = 0x5F
    SUMMON_WHISPERWIND = 0x60
    SUMMON_CONSTRICT = 0x61
    SUMMON_DIAMOND_DUST = 0x62
    SUMMON_JUDGMENT_BOLT = 0x63
    SUMMON_HELLFIRE = 0x64
    SUMMON_GAIAS_WRATH = 0x65
    SUMMON_EARTHEN_WALL = 0x66
    SUMMON_DEMON_EYE = 0x67
    SUMMON_RUBY_LIGHT = 0x68
    SUMMON_THUNDERSTORM = 0x69
    SUMMON_ZANTETSUKEN = 0x6A
    SUMMON_FLAMES_OF_REBIRTH_FIRE = 0x6B
    SUMMON_TSUNAMI = 0x6C
    SUMMON_MEGA_FLARE = 0x6D
    SUMMON_FAT_CHOCOBO = 0x6E
    SUMMON_GUNGNIR = 0x6F
    SUMMON_FLAMES_OF_REBIRTH_LIFE = 0x70
    LANCE_HP_DRAIN = 0x71
    LANCE_MP_DRAIN = 0x72
    EGG_CHOP = 0x73
    HARP_SILVER_HARP = 0x74
    HARP_DREAM_HARP = 0x75
    HARP_LAMIAS_HARP = 0x76
    HARP_APOLLOS_HARP = 0x77
    ITEM_FAIL = 0x78
    DANCE_MYSTERY_WALTZ = 0x79
    DANCE_JITTERBUG_DUET = 0x7A
    DANCE_TEMPTING_TANGO = 0x7B
    MAGIC_SHELL = 0x7C
    DANCE_SWORD_DANCE = 0x7D
    COMMAND_ICE_AURA_DUMMIED = 0x7E
    COMMAND_ENTANGLE_WHIP_MAGIC = 0x7F
    ENEMY_ATTACK = 0x80
    ENEMY_SPECIAL_ABILITY = 0x81
    BLUE_MAGIC_DOOM = 0x82
    BLUE_MAGIC_ROULETTE = 0x83
    BLUE_MAGIC_AQUA_BREATH = 0x84
    BLUE_MAGIC_LEVEL_5_DEATH = 0x85
    BLUE_MAGIC_LEVEL_4_GRAVIGA = 0x86
    BLUE_MAGIC_LEVEL_2_OLD = 0x87
    BLUE_MAGIC_LEVEL_3_FLARE = 0x88
    BLUE_MAGIC_PONDS_CHORUS = 0x89
    BLUE_MAGIC_LILLIPUTIAN_LYRIC = 0x8A
    BLUE_MAGIC_FLASH = 0x8B
    BLUE_MAGIC_TIME_SLIP = 0x8C
    BLUE_MAGIC_MOON_FLUTE = 0x8D
    BLUE_MAGIC_DEATH_CLAW = 0x8E
    BLUE_MAGIC_AERO = 0x8F
    BLUE_MAGIC_AERA = 0x90
    BLUE_MAGIC_AEROGA = 0x91
    BLUE_MAGIC_FLAME_THROWER = 0x92
    BLUE_MAGIC_GOBLIN_PUNCH = 0x93
    BLUE_MAGIC_DARK_SPARK = 0x94
    BLUE_MAGIC_OFF_GUARD = 0x95
    BLUE_MAGIC_TRANSFUSION = 0x96
    BLUE_MAGIC_MIND_BLAST = 0x97
    BLUE_MAGIC_VAMPIRE = 0x98
    BLUE_MAGIC_MAGIC_HAMMER = 0x99
    BLUE_MAGIC_MIGHTY_GUARD = 0x9A
    BLUE_MAGIC_SELF_DESTRUCT = 0x9B
    BLUE_MAGIC_QUESTION_MARKS = 0x9C
    BLUE_MAGIC_1000_NEEDLES = 0x9D
    BLUE_MAGIC_WHITE_WIND = 0x9E
    BLUE_MAGIC_MISSILE = 0x9F
    ENEMY_MAGIC_KURURURU = 0xA0
    ENEMY_MAGIC_LEVEL_DOWN = 0xA1
    ENEMY_MAGIC_ESCAPE = 0xA2
    ENEMY_MAGIC_STALKER_ATTACK = 0xA3
    ENEMY_MAGIC_UNHIDE_NEXT_PAGE = 0xA4
    ENEMY_MAGIC_WRONG_WAY = 0xA5
    ENEMY_MAGIC_GRAND_CROSS = 0xA6
    ENEMY_MAGIC_DELTA_ATTACK = 0xA7
    ENEMY_MAGIC_INTERCEPTOR_ROCKET = 0xA8
    ENEMY_MAGIC_BARRIER_CHANGE = 0xA9
    NOTHING = 0xAA
    ENEMY_MAGIC_WIND_SLASH = 0xAB
    SCRIPT_TRIGGER = 0xAC
    ENEMY_MAGIC_SEARCH = 0xAD
    ENEMY_MAGIC_GRAVITY_100 = 0xAE
    ENEMY_MAGIC_DARKNESS = 0xAF
    ENEMY_MAGIC_REAPERS_SWORD = 0xB0
    ENEMY_MAGIC_PUNISHMENT = 0xB1
    ENEMY_MAGIC_BLASTER = 0xB2
    ENEMY_MAGIC_BEAK = 0xB3
    ENEMY_MAGIC_HUG = 0xB4
    ENEMY_MAGIC_SPORE = 0xB5
    ENEMY_MAGIC_POISON_BREATH = 0xB6
    ENEMY_MAGIC_DANCE_OF_THE_DEAD = 0xB7
    ENEMY_MAGIC_ZOMBIE_POWDER = 0xB8
    ENEMY_MAGIC_ZOMBIE_BREATH = 0xB9
    ENEMY_MAGIC_SPIRIT = 0xBA
    ENEMY_MAGIC_ALLURE = 0xBB
    ENEMY_MAGIC_ENTANGLE = 0xBC
    ENEMY_MAGIC_RAINBOW_WIND = 0xBD
    ENEMY_MAGIC_STRANGE_DANCE = 0xBE
    ENEMY_MAGIC_ELECTROMAGNETIC_FIELD = 0xBF
    ENEMY_MAGIC_WHITE_HOLE = 0xC0
    ENEMY_MAGIC_NEEDLE = 0xC1
    ENEMY_MAGIC_MAELSTROM = 0xC2
    ENEMY_MAGIC_BONE = 0xC3
    ENEMY_MAGIC_TAILSCREW = 0xC4
    ENEMY_MAGIC_STOMACH_ACID = 0xC5
    ENEMY_MAGIC_ROCKET_PUNCH = 0xC6
    ENEMY_MAGIC_MUSTARD_BOMB = 0xC7
    ENEMY_MAGIC_ALMAGEST = 0xC8
    ENEMY_MAGIC_QUICKSAND = 0xC9
    ENEMY_MAGIC_ATOMIC_RAY = 0xCA
    ENEMY_MAGIC_MINI_BLAZE = 0xCB
    ENEMY_MAGIC_SNOWSTORM = 0xCC
    ENEMY_MAGIC_FROST = 0xCD
    ENEMY_MAGIC_ELECTRIC_SHOCK = 0xCE
    ENEMY_MAGIC_EARTH_SHAKER = 0xCF
    ENEMY_MAGIC_ZANTETSUKEN = 0xD0
    ENEMY_MAGIC_TIDAL_WAVE = 0xD1
    ENEMY_MAGIC_MEGA_FLARE = 0xD2
    ENEMY_MAGIC_SONIC_WAVE = 0xD3
    ENEMY_MAGIC_THREAD = 0xD4
    ENEMY_MAGIC_MUCUS = 0xD5
    ENEMY_MAGIC_EARTHQUAKE = 0xD6
    ENEMY_MAGIC_STRONG_ATTACK = 0xD7
    ENEMY_MAGIC_MEDICINE = 0xD8
    ENEMY_MAGIC_IMAGE = 0xD9
    ENEMY_MAGIC_BREATH_WING = 0xDA
    ENEMY_MAGIC_BLAZE = 0xDB
    ENEMY_MAGIC_LIGHTNING = 0xDC
    ENEMY_MAGIC_WAVE_CANNON = 0xDD
    ENEMY_MAGIC_ATTACK = 0xDE
    ENEMY_MAGIC_REMEDY = 0xDF
    ENEMY_MAGIC_VALIANT_ATTACK = 0xE0
    ENEMY_MAGIC_GIGA_FLARE = 0xE1
    ENEMY_MAGIC_ENCIRCLE = 0xE2
    ENEMY_MAGIC_WORMHOLE = 0xE3
    ENEMY_MAGIC_POSSESS = 0xE4
    ENEMY_MAGIC_DYNAMO = 0xE5
    ENEMY_MAGIC_MAGNET = 0xE6
    ENEMY_MAGIC_REVERSE_POLARITY = 0xE7
    ENEMY_MAGIC_JUMP = 0xE8
    ENEMY_MAGIC_BANISH = 0xE9
    ENEMY_MAGIC_HURRICANE = 0xEA
    ENEMY_MAGIC_DEMON_EYE = 0xEB
    ENEMY_MAGIC_PULL = 0xEC
    ENEMY_MAGIC_WIN_BATTLE = 0xED
    ENEMY_MAGIC_UNHIDE_ENEMY = 0xEE
    ENEMY_MAGIC_TERMINATE = 0xEF

    @override
    def __str__(self) -> str:
        if 0 <= self.value <= 0x11:
            return f"{self.name.split("_")[-1].capitalize()} spellblade"
        elif 0x12 <= self.value <= 0x23:
            return f"{self.name.split("_")[-1].capitalize()}"
        elif 0x24 <= self.value <= 0x35:
            return f"{self.name.split("_")[-1].capitalize()}"
        elif 0x36 <= self.value <= 0x47:
            return f"{self.name.split("_")[-1].capitalize()}"
        elif 0x48 <= self.value <= 0x56:
            return f"{self.name.split("_")[-1].capitalize()}"
        elif 0x57 <= self.value <= 0x5E:
            return f"{self.name.replace("SONG_", "").replace("S_", "'s ").replace("_", " ").title()}"
        elif 0x5F <= self.value <= 0x70:
            return f"{self.name.replace("SUMMON_", "").replace("_", " ").capitalize()} (summon ability)"
        elif 0x71 <= self.value <= 0x72:
            return f"!Lance ({self.name.replace("LANCE_", "").replace("_", " ").capitalize()} effect)"
        elif self is Ability.EGG_CHOP:
            return self.name.replace("_", " ").capitalize()
        elif 0x74 <= self.value <= 0x75:
            return f"{self.name.replace("HARP_", "").replace("_", " ").title()}' s spell"
        elif self is Ability.HARP_LAMIAS_HARP:
            return "Lamia's harp's spell"
        elif self is Ability.HARP_APOLLOS_HARP:
            return "Apollo's harp's spell"
        elif self is Ability.ITEM_FAIL:
            return "A failed item use"
        elif 0x79 <= self.value <= 0x7B or self.value == 0x7D:
            return f"{self.name.replace("DANCE_", "").replace("_", " ").title()}"
        elif self is Ability.MAGIC_SHELL:
            return self.name.replace("_", " ").title()
        elif self is Ability.COMMAND_ICE_AURA_DUMMIED:
            return "Ice Aura (dummied)"
        elif self is Ability.COMMAND_ENTANGLE_WHIP_MAGIC:
            return "Entangle (whip magic)"
        elif self is Ability.ENEMY_ATTACK:
            return "Physical attack"
        elif self is Ability.ENEMY_SPECIAL_ABILITY:
            return "Special ability"
        elif self is Ability.BLUE_MAGIC_QUESTION_MARKS:
            return "????"
        elif 0x82 <= self.value <= 0x9F:
            return f"{self.name.replace("BLUE_MAGIC_", "").replace("_", " ").title()}"
        elif self is Ability.NOTHING:
            return "Do nothing"
        elif self is Ability.SCRIPT_TRIGGER:
            return "Unnamed script trigger"
        elif self is Ability.ENEMY_MAGIC_UNHIDE_ENEMY:
            return "Hide/show enemies"
        elif self.value in (0xD0, 0xD1, 0xD2, 0xD9, 0xDE, 0xE8, 0xE9, 0xEB):
            return f"{self.name.replace("ENEMY_MAGIC_", "").replace("_", " ").title()} (enemy magic)"
        elif 0xA0 <= self.value <= 0xEF:
            return f"{self.name.replace("ENEMY_MAGIC_", "").replace("_", " ").title()}"
        else:
            raise ValueError(f"Invalid ability ID: {self.value:#04x}. It must be between 0x00 and 0xEF (inclusive).")

    @classmethod
    def is_valid_ability_id(cls, value: int) -> bool:
        return value in cls._value2member_map_
