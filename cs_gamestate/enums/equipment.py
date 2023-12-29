# Generic enumeration types
from enum import Enum


# Known internal weapon names and their string representation
class WeaponName(Enum):
    C4 = "weapon_c4"
    KNIFE = "weapon_knife"
    KNIFE_T = "weapon_knife_t"
    TASER = "weapon_taser"
    SHIELD = "weapon_shield"
    BUMPMINE = "weapon_bumpmine"
    BREACHCHARGE = "weapon_breachcharge"
    DECOY = "weapon_decoy"
    FLASHBANG = "weapon_flashbang"
    HEALTHSHOT = "weapon_healthshot"
    HEGRENADE = "weapon_hegrenade"
    INCGRENADE = "weapon_incgrenade"
    MOLOTOV = "weapon_molotov"
    SMOKEGRENADE = "weapon_smokegrenade"
    TAGRENADE = "weapon_tagrenade"
    M249 = "weapon_m249"
    MAG7 = "weapon_mag7"
    NEGEV = "weapon_negev"
    NOVA = "weapon_nova"
    SAWEDOFF = "weapon_sawedoff"
    XM1014 = "weapon_xm1014"
    CZ75A = "weapon_cz75a"
    DEAGLE = "weapon_deagle"
    ELITE = "weapon_elite"
    FIVESEVEN = "weapon_fiveseven"
    GLOCK = "weapon_glock"
    HKP2000 = "weapon_hkp2000"
    P250 = "weapon_p250"
    REVOLVER = "weapon_revolver"
    TEC9 = "weapon_tec9"
    USP_SILENCER = "weapon_usp_silencer"
    AK47 = "weapon_ak47"
    AUG = "weapon_aug"
    AWP = "weapon_awp"
    FAMAS = "weapon_famas"
    G3SG1 = "weapon_g3sg1"
    GALILAR = "weapon_galilar"
    M4A1 = "weapon_m4a1"
    M4A1_SILENCER = "weapon_m4a1_silencer"
    SCAR20 = "weapon_scar20"
    SG553 = "weapon_sg556"
    SSG08 = "weapon_ssg08"
    BIZON = "weapon_bizon"
    MAC10 = "weapon_mac10"
    MP5SD = "weapon_mp5sd"
    MP7 = "weapon_mp7"
    MP9 = "weapon_mp9"
    P90 = "weapon_p90"
    UMP45 = "weapon_ump45"


# Weapon types and their string representation
class WeaponType(Enum):
    PISTOL = "Pistol"
    KNIFE = "Knife"
    RIFLE = "Rifle"
    SNIPER_RIFLE = "SniperRifle"
    SUBMACHINE_GUN = "Submachine Gun"
    C4 = "C4"
    GRENADE = "Grenade"
    SHOTGUN = "Shotgun"
    MACHINE_GUN = "Machine Gun"
    STACKABLE_ITEM = "StackableItem"


# Possible weapon states
class WeaponState(Enum):
    ACTIVE = "active"
    HOLSTERED = "holstered"
    RELOADING = "reloading"


# Known grenade types and their string representation
class GrenadeType(Enum):
    DECOY = "decoy"
    HEGRENADE = "frag"
    FLASHBANG = "flashbang"
    SMOKEGRENADE = "smoke"
    INCGRENADE = "inferno"
    MOLOTOV = "firebomb"
