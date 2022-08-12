import dice
import draw
import math
import prompt

def ask_to_auto_roll():
    return prompt.multiple_choice(
        "Shall the computer roll for you?",
        ["Yes", "No, I'll enter dice rolls manually",]
    )
def calculate_abilities(character_class, level, stats):
    """Input a class and level.
    Output the abilities of that character."""
    match character_class:
        case "Cleric":
            if level == 1:
                return [
                    f"Channel Energy: Once per day, Thread the Needle below WIS ({stats['WIS']}) and above enemy HD to deal d6 damage, or heal self/ally for d6 damage with no roll.",
                    f"Turn Undead: In combat, Thread the Needle below WIS ({stats['WIS']}) and above undead HD to cause 2d6 undead to flee for 2d6 rounds. Must turn from the lowest HD up. If turning ever fails, no more turning allows until the next combat.",
                ]
            else:
                return [
                    f"Channel Energy: {level} times per day, Thread the Needle below WIS ({stats['WIS']}) and above enemy HD to deal d6 damage, or heal self/ally for d6 damage with no roll.",
                    f"Turn Undead: In combat, Thread the Needle below WIS ({stats['WIS']}) and above undead HD to cause 2d6 undead to flee for 2d6 rounds. Must turn from the lowest HD up. If turning ever fails, no more turning allows until the next combat.",
                ]
        case "Druid":
            return [
                f"Nature: Outside of civilization, you need not consume daily rations, cannot be poisoned, and gain {level} additional HP when resting, in addition to your die (d6).",
                f"Rituals: Once per day, devote an hour to cast any spell of your level ({level}) or lower on the nature spell list as a ritual. If you're interrupted, the spell fails.",
            ]
        case "Dwarf":
            return [
                f"Academia: Add {level} to HP recovered when you bandage injured characters.",
                "Inspire: When resting, you may tell your friends a tale. If a listener later finds themselves in similar circumstances to the tale, they may roll a check or save at Advantage. This can be performed once per tale told.",
            ]
        case "Elf":
            if level == 1:
                return [
                    "Surge: Once per day, if you fail a save or check, readjust, and reroll the die. Alternatively, spend a surge to add your level (1) to a damage roll.",
                    "Spell Strain: If you've run out of spells for the day, you may cast additional spells at the cost of 1 permanent HP lost per spell.", 
                ]
            else:
                return [
                    f"Surge: {level} times per day, if you fail a save or check, readjust, and reroll the die. Alternatively, spend a surge to add {level} to a damage roll.",
                    f"Spell Strain: If you've run out of spells for the day, you may cast additional spells at the cost of {level} permanent HP lost per spell.", 
                ]
        case "Fighter":
            if level == 1:
                return [
                    "Multikill: When you kill an enemy, you may attack another within range.",
                    f"Sunder: If you fail a STR ({stats['STR']}) or DEX ({stats['DEX']}) save, you can destroy your shield, if you have one equipped, to negate damage.",
                ]
            else:
                return [
                    f"Multikill: When you kill an enemy, you may attack another within range. You may attack {level+1} enemies, provided the first {level} attacks are killing blows.",
                    f"Sunder: If you fail a STR ({stats['STR']}) or DEX ({stats['DEX']}) save, you can destroy your shield, if you have one equipped, to negate damage.",
                ]
        case "Halfling":
            return [
                f"Superior Strike: If you attacks from an advantageous position, do {level} additional damage.",
                "Favors: Each time you level up, gain 3d6×level gold worth of favors to collect.",
            ]
        case "Magic-User":
            if level == 1:
                return [
                    "Metamagic: Once per day, you can do one of the following: ignore the result of a spell's usage die roll, treat your level as double for the purposes of spell effects, reverse the effects of a spell, cast a spell discreetly, cast a spell without requirements, or cast two spells in one action.",
                    "Rituals: Once per day, devote an hour to cast any spell on the arcane spell list as a ritual. If you're interrupted, the spell fails.",
                ]
            else:
                return [
                    f"Metamagic: {level} times per day, you can do one of the following: ignore the result of a spell's usage die roll, treat your level as double for the purposes of spell effects, reverse the effects of a spell, cast a spell discreetly, cast a spell without requirements, or cast two spells in one action.",
                    "Rituals: Once per day, devote an hour to cast any spell on the arcane spell list as a ritual. If you're interrupted, the spell fails.",
                ]
        case "Paladin":
            if level == 1:
                return [
                    "Lay On Hands: Once per day, touch someone or yourself to heal d6 damage.",
                    f"Body Shield: In combat, Thread the Needle below CHA ({stats['CHA']}) and above enemy HD to cause all attacks that would target an adjacent ally to target you instead until your next turn.",
                ]
            else:
                return [
                    f"Lay On Hands: {level} times per day, touch someone or yourself to heal d6 damage.",
                    f"Body Shield: In combat, Thread the Needle below CHA ({stats['CHA']}) and above enemy HD to cause all attacks that would target an adjacent ally to target you instead until your next turn.",
                ]
        case "Ranger":
            return [
                f"Quarry: Once during each combat, single out an enemy and add {level} to all damage rolls against them.",
                "Terrain: In your favored terrain, you and your allies can travel quickly, track parties effortlessly, travel without leaving a trace, and avoid encountering people.",
            ]
        case "Warlock":
            return [
                "Gaining Corruption: Each time you level up and complete your favors to learn new spells, you also gain a Corruption point. You may also cast additional spells past your daily limit at the cost of one Corruption point and one Corruption check per spell.",
                "Corruption Checks: When your Corruption is tested, roll a d20. If you roll above your Corruption score, you are safe for yet another day (but at what cost?). If, however, the roll ties or is lower than your Corruption score, you are fully Corrupted.",
            ]

def calculate_AC(DEX, armor_score, shield_score):
    """AC is DEX+Armor+Shield."""
    return DEX + armor_score + shield_score

def calculate_AV(character_class, level):
    """Looks up the inputted class and level and outputs AV."""
    match character_class:
        case "Cleric":
            AV_dict = {
                1: 11,
                2: 11,
                3: 12,
                4: 12,
                5: 12,
                6: 13,
                7: 13,
                8: 14,
                9: 14,
                10: 14,
            }
        case "Druid":
            AV_dict = {
                1: 8,
                2: 8,
                3: 9,
                4: 9,
                5: 9,
                6: 10,
                7: 10,
                8: 11,
                9: 11,
                10: 11,
            }
        case "Dwarf" | "Paladin" | "Ranger":
            AV_dict = {
                1: 11,
                2: 11,
                3: 12,
                4: 12,
                5: 13,
                6: 13,
                7: 14,
                8: 14,
                9: 15,
                10: 15,
            }
        case "Elf":
            AV_dict = {
                1: 11,
                2: 11,
                3: 12,
                4: 13,
                5: 13,
                6: 14,
                7: 15,
                8: 15,
                9: 16,
                10: 17,
            }
        case "Fighter":
            AV_dict = {
                1: 11,
                2: 12,
                3: 12,
                4: 13,
                5: 14,
                6: 14,
                7: 15,
                8: 16,
                9: 16,
                10: 17,
            }
        case "Halfling":
            AV_dict = {
                1: 12,
                2: 12,
                3: 12,
                4: 12,
                5: 13,
                6: 13,
                7: 13,
                8: 13,
                9: 14,
                10: 14,
            }
        case "Magic-User" | "Warlock":
            AV_dict = {
                1: 8,
                2: 8,
                3: 8,
                4: 9,
                5: 9,
                6: 9,
                7: 10,
                8: 10,
                9: 10,
                10: 11,
            }
    return AV_dict[level]

def check_if_armor_is_allowed(type, character_class):
    """Input a type of armor and a character class.
    Makes sure the character class can use that armor."""
    match character_class:
        case "Druid" | "Halfling" | "Magic-User" | "Warlock":
            if type != "Light":
                print(f"\n{character_class}s can only wear Light armor.")
                return "No"
        case "Cleric" | "Ranger":
            if type not in {"Light", "Medium"}:
                print(f"\n{character_class}s can only wear Light or Medium armor.")
                return "No"
        case "Elf":
            if type not in {"Light", "Medium"}:
                print("\nElves can only wear Light or Medium armor.")
                return "No"
        case "Dwarf" | "Fighter" | "Paladin":
            if type not in {"Light", "Medium", "Heavy"}:
                print("\nTHIS SHOULD NEVER HAPPEN. YOU ARE TRYING TO CHECK SOMETHING THAT IS NOT A VALID ARMOR TYPE.")
                return "No"
    return "Yes"

def check_if_shield_is_allowed(type, character_class):
    """Input a type of shield and a character class.
    Makes sure the character class can use that shield."""
    match character_class:
        case "Druid" | "Magic-User" | "Warlock":
            if type != "":
                print(f"\n{character_class}s cannot use shields.")
                return "No"
        case "Halfling" | "Ranger":
            if type != "Small":
                print(f"\n{character_class}s can only use Small shields.")
                return "No"
        case "Elf":
            if type != "Small":
                print("\nElves can only use Small shields.")
                return "No"
        case "Cleric" | "Dwarf" | "Fighter" | "Paladin":
            if type not in {"Small", "Large"}:
                print("\nTHIS SHOULD NEVER HAPPEN. YOU ARE TRYING TO CHECK SOMETHING THAT IS NOT A VALID SHIELD TYPE.")
                return "No"
    return "Yes"

def check_if_weapon_is_allowed(damage, ranged_yes_or_no, character_class):
    """Input an amount of damage dealt by a weapon and a character class.
    If the damage is higher than what the character can use, reject the weapon."""
    if ranged_yes_or_no == "Yes" and damage > 6:
        print("\nRanged weapons cannot deal more than 6 damage. Please start over.")
        return "No"
    match character_class:
        case "Druid" | "Magic-User" | "Warlock":
            if damage > 4:
                print(f"\n{character_class}s cannot wield weapons that deal more than 4 damage. Please start over.")
                return "No"
        case "Cleric" | "Halfling" | "Ranger":
            if damage > 6:
                print(f"\n{character_class}s cannot wield weapons that deal more than 6 damage. Please start over.")
                return "No"
        case "Dwarf" | "Fighter" | "Paladin":
            if damage > 8:
                print(f"\n{character_class}s cannot wield weapons that deal more than 8 damage. Please start over.")
                return "No"
        case "Elf":
            if damage > 8:
                print("\nElves cannot wield weapons that deal more than 8 damage. Please start over.")
                return "No"
    return "Yes"

def draw_character_sheet():
    """Writes the character sheet to the console."""
    return draw.frame(
    100, 
    [
        f"{name}: ({character_class} {level})",
        f"CHA {stats['CHA']}, CON {stats['CON']}, DEX {stats['DEX']}, INT {stats['INT']}, STR {stats['STR']}, WIS {stats['WIS']}",
        f"{current_hp}/{max_hp} HP, {calculate_AC(stats['DEX'], armor_score, shield_score)} AC, {calculate_AV(character_class, level)} AV",
        f"{gold_on_person} gold on person, {gold_stored_away} gold stored away, {gold_spent_this_level} gold spent this level, {gold_to_next_level(gold_spent_this_level, level)} gold to next level",
        f"EQUIPMENT: ({len(inventory)}/{stats['STR']})",
        f"{', '.join([str(item) for item in inventory])}",
        "ABILITIES:",
        "* " + "\n* ".join([ability for ability in calculate_abilities(character_class, level, stats)]),
        "SPELLS:",
        spells_per_day(character_class, level),
        "* " + "\n* ".join([spell for spell in spells]),
    ]
)

def gain_spells_upon_leveling(spells, character_class, level):
    """Takes an inputted character class and handles how to give that class new spells.
    Some classes get to choose their new spells but others do not."""
    dict_of_arcane_spells = {
        1: "Adhere: Your touched target exudes a thick, white, pasty glue. It becomes extremely sticky.",
        2: "Aeromancer: Invoke and control wind up to the intensity of a light breeze.",
        3: "Aethersight: Magic auras glow in the color of song. You can discern when objects have been magically affected or when casters are being discreet.",
        4: "Allure: Creatures within sight are compelled to approach you, but do not change their disposition towards you.",
        5: "Animate: You control an inanimate object.",
        6: "Animate Shadow: Your shadow disconnects from you but remains under your control.",
        7: "Arcane Eye: Your eyeball detaches and you can see through it as it flies at your command.",
        8: "Astral Prison: A surge freezes the target in time and space within an invulnerable crystal shell.",
        9: "Astral Shield: An incorporeal barrier forms in the air.",
        10: "Astral Weapon: A heroic weapon of legend, your choice, appears.",
        11: f"Attract: {level+1} objects are magnetically attracted to each other if they come within 10 feet.",
        12: "Auditory Illusion: You create illusory noises that appear to come from a direction of your choice.",
        13: "Babble: The target must clearly say everything you think but is otherwise mute.",
        14: "Banish Cube: You may destroy 3 foot wide cubes of soil once a round.",
        15: "Beacon: The target emits a black psychic pulse that draws the curiosity of all monsters within 1 mile.",
        16: f"Befuddle: {level} {pluralize('target', level, 0)} cannot form memories, tell creatures apart, or otherwise act intelligently.",
        17: f"Bend Fate: Roll {level+1} d20s. Each time you roll a d20, choose one of the rolled results until they are gone.",
        18: "Blood::Water::Wine: Transform one of blood, water, or wine into another.",
        19: "Body Swap: You temporarily switch bodies with the target. If one body dies, so does the other.",
        20: "Cacophony: An overwhelming sound fills the area.",
        21: "Catherine: A human named Catherine appears until the spell ends. She will obey polite, safe requests.",
        22: f"Charm: {level} {pluralize('target', level, 0)} {pluralize('treat', level, 1)} you as a friend.",
        23: f"Chatter: {level} {pluralize('target', level, 0)} {pluralize('appear', level, 1)} to discuss a topic of your choosing when they speak. Among each other, they hear the true speech.",
        24: "Clean: A target is magically cleaned.",
        25: "Coal Stone: Turn a gem into a source of heat/fire.",
        26: "Combine Powers: Concentrate on this spell to add your caster level to an ally caster.",
        27: "Command: The target obeys a three word command that does not harm it.",
        28: "Comprehend: You become fluent in all languages.",
        29: "Compress Space: Make an area shorter or narrower.",
        30: "Control Weather: You can alter the type of weather at will, but after, the energy can cause natural disasters.",
        31: "Darkness: A shroud blocks all vision in an area.",
        32: "Darkvision: You can see in total darkness.",
        33: "Deafen: All nearby creatures are deafened.",
        34: "Decrease Gravity: The gravity in the area halves.",
        35: f"Déjà Vu: For {level} {pluralize('round', level, 0)}, a touched target experiences everything twice.",
        36: f"Delay Danger: Delay the effects of an attack, spell, trap, etc., which targets you for up to {level} {pluralize('round', level, 0)}. The effects can be activated at any time during the duration but they must occur once time is up.",
        37: f"Delay Potion: Delay the effects of a consumed liquid for up to {level} {pluralize('hour', level, 0)}. The effects can be activated at any time during the duration but they must occur once time is up.",
        38: "Disassemble: Any of your body parts may be removed and attached at will. You can control them.",
        39: f"Disguise: You disguise {level} {pluralize('target', level, 0)}.",
        40: f"Displace: Shift target’s apparent place by {level*10} feet.",
        41: f"Dizzy Drunkard: Unbalance {level} {pluralize('target', level, 0)}.",
        42: "Earthfast: Reinforce a rock formation or wood/stone structure.",
        43: f"Earthquake: The ground shakes for {level} {pluralize('round', level, 0)}.",
        44: f"Elasticity: Your body can stretch up to {level*10} feet.",
        45: f"Elemental Wall: An {level*40} foot long wall of ice, fire, or other element blasts from the ground.",
        46: "Eraser: Erase writing. Magical writing resists this spell and requires a roll.",
        47: "Faegold: Create a coin that vanishes in 10 minutes.",
        48: "Feast: A huge table appears with delicious food.",
        49: f"Feather: {level} falling/flying/propelled {pluralize('item', level, 0)} {pluralize('become', level, 1)} as light as feathers.",
        50: f"Filch: {level} visible {pluralize('item', level, 0)} {pluralize('teleport', level, 1)} to your hands.",
        51: "Flatten: You become two dimensional.",
        52: "Flavor: The target is more appetizing.",
        53: "Fog Cloud: Dense black fog spreads out from you.",
        54: f"Frenzy: {level} {pluralize('creature', level, 0)} {pluralize('erupt', level, 1)} in senseless violence.",
        55: f"Glass Form: A touched surface becomes see-through up to {level} {pluralize('foot', level, 0)}. Lead and silver are immune.",
        56: "Gravity Shift: You can change the direction of gravity for yourself once per round.",
        57: f"Grease: Cast forth a spurt of grease, which can cover {level*10} square feet.",
        58: f"Greed: {level} {pluralize('creature', level, 0)} {pluralize('develop', level, 1)} an overwhelming urge to possess a visible item of your choice.",
        59: "Grow: Double the size of a touched target.",
        60: f"Haste: {level} touched {pluralize('target', level, 0)} {pluralize('move', level, 1)} three times as fast.",
        61: "Hear Whispers: A touched target hears faint sounds.",
        62: f"Hover: An object hovers 2 feet off the ground. It can hold {level} {pluralize('man', level, 0)}.",
        63: f"Hypnotize: The target enters a dreamy trance and will truthfully answer {level} {pluralize('question', level, 0)}.",
        64: f"Ice: An {level*10} foot radius of ice spreads from a point.",
        65: "Increase Gravity: The gravity in the area doubles.",
        66: "Invisible Tether: Two objects must remain less than 10 feet apart.",
        67: f"Knock: {level} nearby {pluralize('lock', level, 0)}, {pluralize('clasp', level, 0)}, or {pluralize('buckle', level, 0)} {pluralize('open', level, 1)}.",
        68: f"Leap: A touched target can jump {level*10} feet in the air.",
        69: "Life Line: Link two targets; one need not eat nor breathe, and the other must eat and breathe for both.",
        70: "Light: A floating light moves as you command.",
        71: "Liquid Air: The air becomes thick enough to swim in.",
        72: "Magic Dampener: Nearby magic has effects halved.",
        73: "Magic Mouth: Enchant an object to deliver a message once a condition is triggered.",
        74: "Manipulate Clockwork: You affect a minor change in a small mechanical item.",
        75: f"Manse: A furnished cottage appears for {level*12} hours.",
        76: "Marble Madness: Your pockets are always full of marbles.",
        77: f"Masquerade: {level} {pluralize('creature', level, 0)} {pluralize('turn', level, 1)} identical to a target.",
        78: "Metal Melt: A touched metal becomes cool liquid and rehardens in 1 round.",
        79: f"Miniaturize: {level} touched {pluralize('creature', level, 0)} {pluralize('is', level, 0)} mouse-sized.",
        80: f"Mirror Image: {level} {pluralize('copy', level, 0)} of yourself {pluralize('appear', level, 1)}.",
        81: "Mirrorwalk: A mirror becomes a gate to another mirror that you have looked into today.",
        82: f"Multiarm: You gain {level} extra {pluralize('arm', level, 0)}.",
        83: f"Multihead: You gain {level} extra {pluralize('head', level, 0)}.",
        84: f"Multileg: You gain {level} extra {pluralize('leg', level, 0)}.",
        85: f"Multitask: Split your mind in two and perform twice as many actions for {level} {pluralize('round', level, 0)}. When this spell ends, roll a CON save or collapse in exhaustion.",
        86: f"Night Orb: A {level*40} foot radius ball of night appears.",
        87: "Objectify: You become an inanimate object.",
        88: "Ooze Form: You melt into a living jelly.",
        89: f"Pacify: {level} {pluralize('target', level, 0)} {pluralize('has', level, 0)} a sudden aversion to violence.",
        90: "Phantom Coach: A ghostly coach appears, slightly translucent in direct light, with billowing wisps of night. It moves unnaturally fast over any terrain, even water.",
        91: f"Phobia: {level} {pluralize('target', level, 0)} {pluralize('is', level, 0)} terrified of an object you choose.",
        92: "Photo: Instantly transcribe what you see to paper.",
        93: f"Pit: A pit 10 feet wide and {level*5} feet deep appears.",
        94: "Presence: The target feels as though they are being watched.",
        95: "Primeval Surge: An object is grown to the size of an elephant. If it is an animal, it is enraged.",
        96: f"Psychometry: Discern the answers to {level} yes/no {pluralize('question', level, 0)} about a touched object.",
        97: f"Pull: An object is pulled with the strength of {level} {pluralize('man', level, 0)} for 1 round.",
        98: f"Push: An object is pushed with the strength of {level} {pluralize('man', level, 0)} for 1 round.",
        99: "Quench: Extinguish a small controlled flame, like a torch or campfire.",
        100: f"Raise Spirit: For a favor, a touched corpse’s spirit appears and answers {level} {pluralize('question', level, 0)}.",
        101: "Read Mind: You hear thoughts of creatures nearby.",
        102: f"Repel: {level+1} objects are magnetically repelled from each other if they come within 10 feet.",
        103: "Root: Touched target cannot be moved against their will.",
        104: f"Scribe: Copy 1 page of text, or transcribe what is said for {level} {pluralize('minute', level, 0)}.",
        105: "Scry: You see the POV of a creature touched today.",
        106: "Sculpt Elements: Inanimate material behaves like wet clay in your hands.",
        107: "Share Senses: You and a touched target freely exchange sensory information.",
        108: "Shrink: Halve the size of a touched target.",
        109: f"Shroud: {level} {pluralize('target', level, 0)} {pluralize('is', level, 0)} invisible until they move.",
        110: f"Shuffle: {level} {pluralize('target', level, 0)} randomly {pluralize('switch', level, 0)} places.",
        111: f"Sigil of Channeling: Inscribe a sigil on an object or person to be able to cast spells as if you are at the location of the sigil. The sigil remains for {level} {pluralize('hour', level, 0)}.",
        112: "Sixth Sense: You cannot be surprised.",
        113: "Skunk: A bad smell fills the area.",
        114: f"Sleep: {level} {pluralize('creature', level, 0)} {pluralize('fall', level, 1)} into a light sleep.",
        115: "Sleepwalk: You can act during a full night’s rest. You cannot use this spell to gain the benefits of rest more than once per day.",
        116: "Slow Spell: In a chosen area, spells occur 1 round after they are cast.",
        117: "Smoke Form: Your body becomes living smoke.",
        118: "Snail Knight: A time after casting, a knight astride a giant snail rides into view. He answers most questions related to quests, and may aid you if you are worthy.",
        119: "Sniff: You smell the faintest traces of scents.",
        120: "Soil: A target is magically dirtied.",
        121: "Sort: Inanimate items sort themselves as you specify.",
        122: "Sour: The target is more unappetizing.",
        123: "Spatial Distortion: A nearby object shrinks to the size of an apple.",
        124: "Spectacle: A clearly unreal but impressive illusion appears under your control, with motion and sound.",
        125: "Spellseize: Remove a spell from a caster’s mind and store it to cast later. After casting, the spell is gone.",
        126: "Spider Climb: A target climbs surfaces like a spider.",
        127: "Stone::Flesh: Transform stone into flesh, or vice versa.",
        128: "Stretch Space: Make an area longer or wider.",
        129: "Summon Cube: You may create 3 foot wide cubes of soil once a round.",
        130: "Summon Idol: A carved idol rises from the ground.",
        131: "Swarm: You become a swarm of crows, rats, or piranha.",
        132: "Taste: You taste the faintest of sapors.",
        133: f"Telekinesis: You may mentally move {level} {pluralize('item', level, 0)}.",
        134: f"Telepathy: {level+1} targets hear each other’s thoughts.",
        135: f"Teleport: An object teleports up to {level*40} feet.",
        136: "Thaumaturgic Anchor: The target becomes the target of all spells cast near it, and all casters must roll under their spellcasting stat to target anything else.",
        137: f"Time Jump: The target hurls itself up to {level*10} minutes into the future.",
        138: f"Time Pocket: You dislocate in time for up to {level} {pluralize('minute', level, 0)}. You can see and be seen by creatures in normal time, but as if in a fog. You ignore all effects and objects other than those that originate with you. Likewise, you cannot affect normal time.",
        139: "Time Rewind: Time in a chosen area flows backwards.",
        140: "Time Rush: Time in a chosen area becomes 10 times faster.",
        141: "Time Share: You give the target your time. It can act on your turn as if it were its own. You are petrified until the end of your turn.",
        142: "Time Slow: Time in a chosen area becomes 10 times slower.",
        143: "Transcribe Sigil: Touch a magical sigil, glyph, or symbol to pick it up. Make a save or it activates, targeting you. You must set it down before the spell ends.",
        144: "Transfer Heat: Transfer heat between two targets.",
        145: "Tremorsense: Your sense of touch heightens.",
        146: "True Sight: You see through all illusions.",
        147: "Upwell: A spring of seawater appears.",
        148: "Ventriloquism: Project your voice to a different place.",
        149: "Vision: You control what a target sees.",
        150: "Visual Illusion: A silent immobile illusion appears.",
        151: "Ward: A silver ring of radius 40 feet appears. Choose one thing that cannot cross it: the living, the dead, projectiles, or metal.",
        152: "Web: Your hands can shoot thick webbing.",
        153: "Wizard Lock: A close-able thing is magically sealed.",
        154: "Wizard Mark: You can leave marks visible only to casters that can be seen at any distance and through solid objects.",
        155: "Wristpocket: A held object can be hidden in an extradimensional space and retrieved at will.",
        156: "X-Ray Vision: You gain X-ray vision.",
    }
    dict_of_divine_spells = {
        1: {
            1: "Alacrity: For the rest of the day, your touched target has Advantage on initiative rolls.",
            2: "Combine Powers: Concentrate on this spell to add your caster level to an ally caster.",
            3: "Cure Light Wounds: Target heals d8 HP.",
            4: "Detect Undead: Nearby undead glow.",
            5: "Inflict Light Wounds: Target loses d8 HP.",
            6: "Light: A floating light moves as you command.",
            7: "Message: Send a discreet message up to 1 mile.",
            8: "Protection From Evil: Gain Advantage on all rolls against Evil.",
            9: "Purify Food/Water: Remove disease from food/water.",
            10: "Resist Cold: The target is immune to mundane cold and gains Advantage against magical cold.",
            11: "Rousing Cry: Allies gain Advantage on morale rolls.",
            12: "Sanctify Corpse: Prevent corpse from turning undead.",
            13: "Sanctuary: As long as you remain pacifist, roll with Advantage on saves.",
        },
        2: {
            1: "Augury: Determine whether a future action will bring weal or woe.",
            2: "Bless: Allies gain +1 to stats and AV when attacking and saving for 1 hour.",
            3: "Command: The target obeys a three word command that does not harm it.",
            4: "Hold Person: Paralyze d4 targets. Roll each round to maintain the hold; the effect lasts until the roll fails.",
            5: "Life Pact: Link two targets; if one falls below 0 HP, the other loses enough HP to bring the first back to 0 HP.",
            6: "Magic Appraisal: Touch an object. You learn one: who last possessed it, who created it, how to fix it, what it’s used for, where to use it, or where to sell it.",
            7: "Martyr ’s Bargain: Delay all damage in a round to take maximum damage in the following round.",
            8: "Resist Fire: The target is immune to mundane heat and gains Advantage against magical heat.",
            9: "Silence: No sound can pass through a specified area.",
            10: "Speak With Animals: Speak to/understand animals.",
        },
        3: {
            1: "Cause Disease: Inflict a target with a disease.",
            2: "Cure Disease: Cure a target of a disease.",
            3: "Daylight: An area is illuminated with sunlight.",
            4: "Greater Augury: Determine whether the next hour will be safe, perilous, or bring great danger.",
            5: "Locate: Discern the direction of a known object.",
            6: "Prayer: Allies gain Advantage when attacking and saving for 1 combat.",
            7: "Prevent Lies: Creatures within range that attempt to tell a direct lie cannot speak.",
            8: "Raise Spirit: For a favor, a touched corpse’s spirit appears and answers 3 questions.",
            9: "Remove Curse: Remove a curse from a target.",
            10: "Ward: A silver ring of radius 40 feet appears. Choose one thing that cannot cross it: the living, the dead, projectiles, or metal.",
        },
        4: {
            1: "Consecrate: In an area, undead have 1 less HD.",
            2: "Cure Serious Wounds: Target heals 2d8+1 HP.",
            3: "Feast: A huge table appears with delicious food.",
            4: "Superior Augury: The next hour is actually a dream; after 1 hour is up, the timeline is reset back to the moment of casting, and you retain your knowledge of one possible sequence of events. At the end of this spell, you can choose not to reset; this was the true timeline.",
            5: "Heart Sight: Know the intentions and character of a touched target.",
            6: "Hold Undead: Nearby undead are paralyzed for 4 rounds.",
            7: "Inflict Serious Wounds: Target loses 2d8+1 HP.",
            8: "Neutralize Poison: Remove or immunize vs. poison.",
            9: "Sticks::Snakes: Transform sticks into snakes, or vice versa.",
        },
        5: {
            1: "Checkpoint: If the target dies today, their body and gear disintegrate and they reappear in the same condition as when the spell was cast (including stats, gear, memory, etc.).",
            2: "Commune: Directly ask a deity 3 questions.",
            3: "Cure Critical Wounds: Target heals 3d8+2 HP.",
            4: "Dispel Evil: Remove and negate an Evil spell.",
            5: "Inflict Critical Wounds: Target loses 3d8+2 HP.",
            6: "Plague: Anyone in an area loses d6 HP for 2d6 turns.",
            7: "Quest: Compel a target to complete a task for you.",
            8: "True Sight: You see through all illusions.",
        },
        6: {
            1: "Animate: You control an inanimate object.",
            2: "Blade Barrier: A wall of whirling blades appears. Any creature that passes through takes 6d4 damage.",
            3: "Conjure Elemental: Summon a 6 HD elemental.",
            4: "Create Undead: Turn a corpse/skeleton into undead.",
            5: "Find Path: For 1 hour, the path to a location is known.",
            6: "Mind Blank: The target is immune to scrying, divination, and mind reading.",
            7: "Part Waters: Cause water or similar liquid to move apart, forming a rift.",
            8: "Raise Dead: Bring a recent corpse back to life.",
            9: "Speak With Monsters: Speak to/understand monsters.",
            10: "Word Of Recall: For 1 year, you can teleport back to where this spell was cast.",
        },
        7: {
            1: "Aerial Servant: Summon a servant to recover an object or creature.",
            2: "Astral Spell: Project the caster to the Astral Plane.",
            3: "Control Weather: You can alter the type of weather at will, but after, the energy can cause natural disasters.",
            4: "Divine Sacrifice: For 1 hour, your attacks do an extra 5d6 damage if they hit. You take 10 damage each time you attack, whether or not you hit.",
            5: "Earthquake: The ground shakes for 7 rounds.",
            6: "Energy Drain: The target is drained of one level/HD.",
            7: "Holy Word: Targets nearby with less than 5 HD die, 6+ HD paralyzed.",
            8: "Regeneration: Lost body parts are restored.",
            9: "Restoration: The target regains one drained level.",
            10: "Resurrection: Bring back alive from even a tiny piece.",
            11: "Traveler ’s Ward: For 1 week, allies near the caster can travel difficult terrain effortlessly, need not rest, take no damage from mundane plants and minor hazards, and gain the effects of the spell Sanctuary.",
            12: "Wind Walk: For 1 day, you can turn into mist at will.",
            13: "Wither: A touched body part shrivels and falls off.",
        },
        8: {
            1: "Antimagic Field: Declare an area devoid of magic.",
            2: "Command Undead: Undead act at your behest.",
            3: "Overwhelming Presence: 8 targets bow to you.",
            4: "Screen: When scrying, divination, or mind reading targets in an area, you become aware and can feed them false information.",
        },
        9: {
            1: "Astral Projection: Project a group to the Astral Plane.",
            2: "Create Demiplane: Build a pocket dimension of your design.",
            3: "Cursed Earth: In an area, plants cannot grow and the dead rise.",
            4: "Eternal Spell: The next spell you cast is permanent.",
            5: "Finger Of Death: Reduce a touched target to 0 HP.",
            6: "Greater Energy Drain: Target loses d6 levels/HD.",
            7: "Mass Heal: All in an area gain 3d8+2 HP.",
            8: "Miracle: Request a deity’s intervention.",
            9: "Soul Bind: Trap a soul to prevent Resurrection et al.",
        },
    }
    dict_of_nature_spells = {
        1: {
            1: "Animal Repulsion: Target is offensive to mundane animals, which try to flee or attack.",
            2: "Blossom: A touched plant seeds, buds, or blooms.",
            3: "Combine Powers: Concentrate on this spell to add your caster level to an ally caster.",
            4: "Entangle: The present plants in an area attempt to grab ankles and prevent movement.",
            5: "Fog Cloud: Dense black fog spreads out from you.",
            6: "Forecast: Predict local weather over the next day.",
            7: "Invisible To Animals: Mundane animals cannot see you.",
            8: "Magic Spurs: A touched mount moves twice as fast.",
            9: "Pass Without Trace: For 1 hour, travel without leaving tracks or scent.",
            10: "Purify Food/Water: Remove disease from food/water.",
            11: "Quench: Extinguish a small controlled flame, like a torch or campfire.",
            12: "Resist Elements: Choose either heat or cold. The target is immune to mundane heat/cold and gains Advantage against magical heat/cold.",
            13: "Skunk: A bad smell fills the area.",
            14: "Speak With Animals: Speak to/understand animals.",
            15: "Web: Your hands can shoot thick webbing.",
        },
        2: {
            1: "Anthropomorphize: Touched animal gains human intelligence or human appearance for 1 day.",
            2: "Barkskin: Touch to add +1 to AC and stats for saves.",
            3: "Charm Person Or Animal: Target treats you as a friend.",
            4: "Countermoon: A lycanthrope is forced into its natural form and cannot transform, willingly or involuntarily, for 1 hour.",
            5: "Feign Death: A target is indistinguishable from dead.",
            6: "Moonbeam: Bathe an area in moonlight.",
            7: "Songbird: A songbird’s music gives allies +1 to stats and AV when attacking and saving for 1 hour.",
            8: "Speak With Plants: Speak to/understand plants.",
            9: "Thicket: A thicket of dense brush bursts in an area.",
            10: "Transfer Heat: Transfer heat between two targets.",
            11: "Tremorsense: Your sense of touch heightens.",
            12: "Updraft: A column of powerful rising air appears.",
            13: "Upwell: A spring of seawater appears.",
            14: "Warp Wood: Reform a piece of wood the size of a tree branch.",
        },
        3: {
            1: "Arboriate: You are a walking tree up to 10 feet tall.",
            2: "Enchanted Forest: Target cannot leave the forest for 1 week, even if they travel straight indefinitely.",
            3: "Cure Light Wounds: Target heals d8 HP.",
            4: "Fins::Feet: Transform fins into feet, or vice versa.",
            5: "Neutralize Poison: Remove or immunize vs. poison.",
            6: "Pocket of Air: Touched target’s head is surrounded by clean air.",
            7: "Sculpt Dreams: Enter and control the dreams of a touched target.",
            8: "Sculpt Elements: Inanimate material behaves like wet clay in your hands.",
            9: "Speak With Stones: Speak to/understand rock.",
            10: "Sticks::Snakes: Transform sticks into snakes, or vice versa.",
            11: "Summon Insects: A swarm of insects attacks a target.",
        },
        4: {
            1: "Bird Person Your arms become wings.",
            2: "Coldsnap: The area is exposed to a sudden burst of frigid cold.",
            3: "Control Plants: Plants move/attack at your command.",
            4: "Cure Serious Wounds: Target heals 2d8+1 HP.",
            5: "Feast: A huge table appears with delicious food.",
            6: "Wilt: Draw all the water out of an area.",
        },
        5: {
            1: "Beast Form: You become a mundane animal.",
            2: "Dragon Call: You call a dragon within 10 miles. If there are none, the spell fails. You may ask for one task in exchange for payment or favor. You must be able to communicate with the dragon.",
            3: "Elemental Wall: A 100 foot long wall of ice, fire, or other element blasts from the ground.",
            4: "Ironbane: Iron that touches you rusts, disintegrating.",
            5: "Plague: Anyone in an area loses d6 HP for 2d6 turns.",
            6: "Primeval Surge: An animal is grown to the size of an elephant and is enraged.",
            7: "True Path: You can backtrack your steps over the last hour.",
        },
        6: {
            1: "Control Weather: You can alter the type of weather at will, but after, the energy can cause natural disasters.",
            2: "Cure Critical Wounds: Target heals 3d8+2 HP.",
            3: "Earthquake: The ground shakes for 1 minute.",
            4: "Eclipse: An eclipse occurs for 6 hours.",
            5: "Lonely Road: Create an extradimensional pathway, easily traversed. When you exit the road you reappear in the real world at a location corresponding to the distance traveled on the road.",
            6: "Pool of Past Times: Once per week gaze into water to view a scene from the past. The base chance of viewing the chosen event is 60%, modified as follows:\n• Caster was originally present at the event: +30%.\n• Caster knows only the barest details: -20%.\n• Caster knows only the name of the event: -40%.",
            7: "Swarm: You become a swarm of crows, rats, or piranha.",
            8: "Turn Wood: All wood is repelled from the caster.",
            9: "Wall Of Thorns: A wall of brambles appears. Any creature that passes through takes 6d4 damage.",
        },
        7: {
            1: "Animate: You control an inanimate object.",
            2: "Befuddle: 7 targets cannot form memories, tell creatures apart, or otherwise act intelligently.",
            3: "Chariot Of Fire: A flaming chariot transports allies and burns enemies.",
            4: "Conjure Elemental: Summon a 7 HD elemental.",
            5: "Metal::Wood: Transform metal into wood, or vice versa.",
            6: "Transport Via Plants: Travel instantly between two of the same plant.",
        },
        8: {
            1: "Creeping Doom: Summon a swarm of deadly poisonous spiders.",
            2: "Feeblemind: Revert a mind to that of a child’s.",
            3: "Greater Feign Death: A target needs no air, does not age, can withstand extreme environments, and is indistinguishable from dead for up to 8 months."
        },
        9: {
            1: "Eternal Spell: The next spell you cast is permanent.",
            2: "Finger Of Death: Reduce a touched target to 0 HP.",
            3: "Reincarnate: Bring back a soul in a random incarnation.",
        },
    }
    dict_of_necronomicon_spells = {
        1: "Ability Strike: Permanently lose 1 point in a stat of your choice to reduce the enemy HD by d6.",
        2: "Addiction: The target gains a severe addiction.",
        3: "Adjust Memories: Read, erase, or plant memories in a touched target.",
        4: f"Age: Others look on in horror as the target ages {level*10} years.",
        5: f"Agony: Target experiences wracking pain, unable to act for {level} {pluralize('round', level, 0)}.",
        6: "Blind: The target’s eyes are gouged out.",
        7: f"Bloodletting: You open festering sores on your body and bleed midnight blood. Lose {level}d6 HP and then heal the target by {level}d8.",
        8: "Cannibal Curse: An incredible hunger comes over the target. Food and drink no longer satisfy it. It hungers, until it tastes the flesh of a  freshly slain foe.",
        9: "Command: The target obeys a three word command that does not harm it.",
        10: "Compulsive Liar: The target is unable to tell the truth.",
        11: "Consume Mind: The caster eats the brain. They have a 25% chance of gaining the brain’s knowledge/spells.",
        12: "Consume Strength: The caster eats the flesh. They gain d4 STR, DEX, and CON.",
        13: "Create Undead: Turn a corpse/skeleton into undead.",
        14: "Curse Of Worms: When the target takes damage, a swarm of worms pours forth from the wound. The worms act as a swarm and attack mindlessly.",
        15: "Deafen: All nearby creatures are deafened.",
        16: f"Death Mark: If a chosen creature dies before the end of your next turn, you gain {level}d6 HP. If not, they gain {level}d6 HP.",
        17: "Death Mask: You touch a corpse and the face peels off like a mask, while the rest of the corpse quickly rots into dust. When you wear the mask, you will look and sound like the person whose face you’re wearing.",
        18: "Death Scythe: The corpse disintegrates as you pluck a weightless black scythe (2d4 damage) from its core. It does double damage when attacking creatures of the same type.",
        19: f"Death Throes: If the touched target dies in the next hour, its body explodes, dealing {level}d10 damage. The body is irrecoverable.",
        20: "Desecrate: In an area, undead have 1 more HD.",
        21: f"Elemental Blast: An explosion of flame, electricity,  ice, water, or other element detonates with a low roar and deals {level}d6 damage.",
        22: "Erase: You erase a small object from time. No trace remains and any memories of its existence are altered to reflect that it never did. History is rewritten to explain its absence. The smallest possible changes that provide a plausible explanation are used.",
        23: f"Feast of Ashes: The target feels as if they are starving for {level} {pluralize('day', level, 0)} but will not die. Eating food causes horrible nausea.",
        24: f"Forgettable: After you leave their sight, anyone who has seen you for less than {level} {pluralize('round', level, 0)} will forget you.",
        25: "Healing Thief: Any time the target is healed, you steal half the healing.",
        26: "Hold Person: Paralyze d4 targets. Roll each round to maintain the hold; the effect lasts until the roll fails.",
        27: "Isolate: The target cannot be seen or heard by their allies.",
        28: f"Lover ’s Quarrel: The target’s most beloved person takes {level}d6 damage, wherever they may be. The target feels their loved one’s pain.",
        29: "Lycanthropy: The target is cursed with lycanthropy.",
        30: f"Magic Missile: An unerring eldritch blast deals {level}d4 damage (no roll needed to hit).",
        31: "Masochism: Calculate the caster’s max HP - current HP. This number is dealt as damage to the target.",
        32: f"Meat Servant: A blob of dead meat forms into a helpful servant for {level} {pluralize('hour', level, 0)}.",
        33: "Meld: Two targets are fused together.",
        34: f"Memory Wipe: The target forgets everything in the last {level} {pluralize('round', level, 0)}.",
        35: "Mental Killswitch: Create a trigger that will kill the touched target if their mind is tampered with in a specific way.",
        36: "Mind Swap: Permanently switch minds with a touched target, retaining mental stats and swapping physical stats. Both parties roll a CON save or fall into a coma.",
        37: "Negative Energy Zone: No healing can occur in an area.",
        38: f"Nightmare: The target cannot sleep for {level} {pluralize('day', level, 0)}.",
        39: f"Overkill: An intense blast of {level}d12 necrotic damage strikes the target. The caster takes {level}d6 damage. If the target is reduced below 0 HP, the excess damage is done to the caster.",
        40: "Preserve Organ: The caster preserves a severed organ from a creature so that it does not rot or decay.",
        41: "Putty Flesh: When struck by a mundane weapon, you may sacrifice an additional d4 HP to fuse your flesh with the weapon temporarily, making it impossible for the wielder to dislodge it. The effect lasts for d4+1 rounds per damage originally inflicted.",
        42: f"Raise Spirit: For a favor, a touched corpse’s spirit appears and answers {level} {pluralize('question', level, 0)}.",
        43: "Sadism: All damage done by the caster in the next round is added to all their stats for {level} rounds.",
        44: "Selectively Mute: The target cannot communicate a specific piece of information.",
        45: "Soul Shackle: The caster draws out the soul of a dead creature and imprisons it within a gem.",
        46: "Thick of It: Your melee attacks do 1 extra damage for each enemy within striking range of you.",
        47: "Transmogrify: Turn the target into an insignificant creature.",
        48: "Vampirism: The target is cursed with vampirism.",
        49: "Willing Sacrifice: The target submits, allowing the ceremonial dagger to pierce their heart. As the life leaves their body, a terrible beast is summoned.",
        50: "Wither: A touched body part shrivels and falls off.",
        51: "100 Yard Strike: The caster can make a melee attack at any target within sight.",
    }
    match character_class:
        case "Cleric":
            print("\nUpon leveling up, a Cleric gains d4+2 spells that the patron chooses.")
            number_of_new_spells = dice.roll(1,4,1) + 2
            while number_of_new_spells > 0:
                level_of_next_spell = dice.roll(1,level,1)
                potential_next_spell_number = dice.roll(1,len(dict_of_divine_spells[level_of_next_spell]),1)
                potential_next_spell = dict_of_divine_spells[level_of_next_spell][potential_next_spell_number]
                if potential_next_spell not in spells:
                    spells.append(potential_next_spell)
                    number_of_new_spells -= 1
        case "Druid":
            print("\nUpon leveling up, a Druid gains d4+2 spells.")
            print("\nLet's pick your spells.")
            number_of_new_spells = dice.roll(1,4,1) + 2
            while number_of_new_spells > 0:
                if level == 1:
                    level_of_next_spell = 1
                else:
                    level_of_next_spell = prompt.multiple_choice(
                        "What level do you want your next spell to be?",
                        [number for number in range(1,level+1)]
                    )
                potential_next_spell = prompt.multiple_choice(
                    "What is your next spell?",
                    [dict_of_nature_spells[level_of_next_spell][value] for value in dict_of_nature_spells[level_of_next_spell]]
                )
                if potential_next_spell not in spells:
                    print(f"\nYou selected {potential_next_spell}")
                    spells.append(potential_next_spell)
                    number_of_new_spells -= 1
                else:
                    print("\nYou already have that spell. Pick another spell.")
        case "Elf" | "Magic-User":
            if character_class == "Elf":
                print("\nUpon leveling up, an Elf gains 1 spell.")
            else:
                print(f"\nUpon leveling up, a Magic-User gains 1 spell.")
            print("\nLet's pick your spells.")
            potential_next_spell_number = prompt.open_response_number(
                "From the arcane spell list, type the number of the spell you want.",
                [number for number in range(1,len(dict_of_arcane_spells)+1)]
            )
            potential_next_spell = dict_of_arcane_spells[potential_next_spell_number]
            if potential_next_spell not in spells:
                print(f"\nYou selected {potential_next_spell}")
                spells.append(potential_next_spell)
            else:
                print("\nYou already have that spell. Pick another spell.")
        case "Paladin":
            if level < 4:
                print("\nA Paladin cannot learn spells until level 4.")
            else:
                print("\nUpon leveling up, a Paladin gains 2 spells that the patron chooses.")
                number_of_new_spells = 2
                while number_of_new_spells > 0:
                    level_of_next_spell = dice.roll(1,math.floor(0.5*level-1),1)
                    potential_next_spell_number = dice.roll(1,len(dict_of_divine_spells[level_of_next_spell]),1)
                    potential_next_spell = dict_of_divine_spells[level_of_next_spell][potential_next_spell_number]
                    if potential_next_spell not in spells:
                        spells.append(potential_next_spell)
                        number_of_new_spells -= 1
        case "Ranger":
            if level < 4:
                print("\nA Ranger cannot learn spells until level 4.")
            else:
                print("\nUpon leveling up, a Ranger gains 2 spells.")
                print("\nLet's pick your spells.")
                number_of_new_spells = 2
                while number_of_new_spells > 0:
                    if level not in {4,5}:
                        level_of_next_spell = 1
                    else:
                        level_of_next_spell = prompt.multiple_choice(
                            "What level do you want your next spell to be?",
                            [number for number in range(1,math.floor(0.5*level-1)+1)]
                        )
                    potential_next_spell = prompt.multiple_choice(
                        "What is your next spell?",
                        [dict_of_nature_spells[level_of_next_spell][value] for value in dict_of_nature_spells[level_of_next_spell]]
                    )
                    if potential_next_spell not in spells:
                        print(f"\nYou selected {potential_next_spell}")
                        spells.append(potential_next_spell)
                        number_of_new_spells -= 1
                    else:
                        print("\nYou already have that spell. Pick another spell.")
        case "Warlock":
            print("\nUpon leveling up, a Warlock gains d5-1 spells.")
            print("\nLet's pick your spells.")
            number_of_new_spells = dice.roll(1,5,1) - 1
            while number_of_new_spells > 0:
                potential_next_spell_number = prompt.open_response_number(
                    "From the Necronomicon spell list, type the number of the spell you want.",
                    [number for number in range(1,len(dict_of_necronomicon_spells)+1)]
                )
                potential_next_spell = dict_of_necronomicon_spells[potential_next_spell_number]
                if potential_next_spell not in spells:
                    print(f"\nYou selected {potential_next_spell}")
                    spells.append(potential_next_spell)
                    number_of_new_spells -= 1
                else:
                    print("\nYou already have that spell. Pick another spell.")
            

def gold_to_next_level(gold_spent_this_level, level):
    """Input the gold you've spent this level and your current level.
    Output how much more you have to spend to level up."""
    wealth_required_to_spend = 125*pow(base = 2, exp = level+1)
    return wealth_required_to_spend - gold_spent_this_level

def manual_hp(character_class):
    """Manually enter starting HP for the inputted class. 
    Rejects HP values smaller than one or bigger than a max die roll plus four."""
    hp = 0
    match character_class:
        case "Magic-User" | "Warlock":
            hp = prompt.open_response_number(
                "What is your starting HP?",
                [number for number in range(1,9)]
            )
        case "Druid" | "Elf" | "Halfling":
            hp = prompt.open_response_number(
                "What is your starting HP?",
                [number for number in range(1,11)]
            )
        case "Cleric" | "Dwarf" | "Ranger":
            hp = prompt.open_response_number(
                "What is your starting HP?",
                [number for number in range(1,13)]
            )
        case "Fighter" | "Paladin":
            hp = prompt.open_response_number(
                "What is your starting HP?",
                [number for number in range(1,15)]
            )
    return hp

def manual_stats():
    """Lets the user enter their stats. 
    Returns the character's stats as a dictionary {"CHA": #, "CON": #, "DEX": #, "INT": #, "STR": #, "WIS": #,}."""
    stats = {"CHA": 0, "CON": 0, "DEX": 0, "INT": 0, "STR": 0, "WIS": 0,}
    for stat in ["CHA", "CON", "DEX", "INT", "STR", "WIS"]:
        score = prompt.open_response_number(
            f"{stat}:",                    
            [number for number in range(0,21)]
        )
        stats.update({stat: score})
    return stats
    
def pick_class():
    """Returns the chosen class."""
    return prompt.multiple_choice(
        "What is your class?",
        ["Cleric", "Druid", "Dwarf", "Elf", "Fighter", "Halfling", "Magic-User", "Paladin", "Ranger", "Warlock",]
    )

def pluralize(word, number, verb_boolean):
    """Input a word and a number.
    If the number is 1, return the word.
    Otherwise, make it plural.
    Nouns gain an "s" on pluralizing.
    Verbs gain an "s" on singularizing."""
    if number == 1 and verb_boolean == 0:
        return word
    else:
        if word == "is":
            return "are"
        elif word == "foot":
            return "feet"
        elif word == "man":
            return "men"
        elif word == "copy":
            return "copies"
        elif word == "has":
            return "have"
        elif word == "switch":
            return "switches"
        word += "s"
        return word

def roll_hp(character_class):
    """Determines starting HP for the inputted class."""
    hp = 0
    match character_class:
        case "Magic-User" | "Warlock":
            hp = dice.roll(1,4,1) + 4
        case "Druid" | "Elf" | "Halfling":
            hp = dice.roll(1,6,1) + 4
        case "Cleric" | "Dwarf" | "Ranger":
            hp = dice.roll(1,8,1) + 4
        case "Fighter" | "Paladin":
            hp = dice.roll(1,10,1) + 4
    return hp

def roll_stats():
    """Randomly rolls for stats. 
    Returns the character's stats as a dictionary {"CHA": #, "CON": #, "DEX": #, "INT": #, "STR": #, "WIS": #,}."""
    stats = {"CHA": 0, "CON": 0, "DEX": 0, "INT": 0, "STR": 0, "WIS": 0,}
    power_level = prompt.multiple_choice(
        "Are you using EXTREME, STANDARD, or CLASSIC powered characters?",
        ["EXTREME", "STANDARD", "CLASSIC",]
    )
    match power_level:
        case "EXTREME":
            for stat in ["CHA", "CON", "DEX", "INT", "STR", "WIS"]:
                score = dice.roll(3,20,1)
                stats.update({stat: score})
        case "STANDARD":
            for stat in ["CHA", "CON", "DEX", "INT", "STR", "WIS"]:
                score = dice.roll(3,10,2)
                stats.update({stat: score})
        case "CLASSIC":
            for stat in ["CHA", "CON", "DEX", "INT", "STR", "WIS"]:
                score = dice.roll(3,6,3)
                stats.update({stat: score})
    return stats

def spells_per_day(character_class, level):
    """Input a class and a level.
    Outputs how many spells of each kind you can cast per day."""
    match character_class:
        case "Cleric" | "Druid":
            usage_die_dict = {
                1: "u4 level 1 spells per day.",
                2: "u4 level 1, u4 level 2 spells per day.",
                3: "u6 level 1, u4 level 2, u4 level 3 spells per day.",
                4: "u6 level 1, u6 level 2, u4 level 3, u4 level 4 spells per day.",
                5: "u8 level 1, u6 level 2, u4 level 3, u4 level 4, u4 level 5 spells per day.",
                6: "u8 level 1, u8 level 2, u6 level 3, u4 level 4, u4 level 5, u4 level 6 spells per day.",
                7: "u10 level 1, u8 level 2, u6 level 3, u6 level 4, u4 level 5, u4 level 6, u4 level 7 spells per day.",
                8: "u10 level 1, u10 level 2, u6 level 3, u6 level 4, u4 level 5, u4 level 6, u4 level 7, u4 level 8 spells per day.",
                9: "u12 level 1, u10 level 2, u8 level 3, u6 level 4, u6 level 5, u4 level 6, u4 level 7, u4 level 8, u4 level 9 spells per day.",
                10: "u12 level 1, u12 level 2, u8 level 3, u8 level 4, u6 level 5, u6 level 6, u4 level 7, u4 level 8, u4 level 9 spells per day.",
            }
            return usage_die_dict[level]
        case "Elf":
            daily_spells_dict = {
                1: "1 spell per day.",
                2: "2 spells per day.",
                3: "2 spells per day.",
                4: "3 spells per day.",
                5: "4 spells per day.",
                6: "4 spells per day.",
                7: "5 spells per day.",
                8: "6 spells per day.",
                9: "6 spells per day.",
                10: "7 spells per day.",
            }
            return daily_spells_dict[level]
        case "Magic-User":
            usage_die_dict = {
                1: "u4 spells per day.",
                2: "u6 spells per day.",
                3: "u8 spells per day.",
                4: "u10 spells per day.",
                5: "u12 spells per day.",
                6: "u20 spells per day.",
                7: "u4, then u20 spells per day.",
                8: "u6, then u20 spells per day.",
                9: "u8, then u20 spells per day.",
                10: "u10, then u20 spells per day.",
            }
            return usage_die_dict[level]
        case "Paladin" | "Ranger":
            daily_spells_dict = {
                1: "No spells yet.",
                2: "No spells yet.",
                3: "No spells yet.",
                4: "1 level 1 spell per day.",
                5: "2 level 1 spells per day.",
                6: "2 level 1 spells, 1 level 2 spell per day.",
                7: "2 level 1 spells, 2 level 2 spells per day.",
                8: "2 level 1 spells, 2 level 2 spells, 1 level 3 spell per day.",
                9: "3 level 1 spells, 2 level 2 spells, 2 level 3 spells per day.",
                10: "3 level 1 spells, 2 level 2 spells, 2 level 3 spells, 1 level 4 spell per day.",
            }
            return daily_spells_dict[level]
        case "Warlock":
            usage_die_dict = {
                1: "u4 spells per day.",
                2: "u5>u4 spells per day.",
                3: "u6>u5>u4 spells per day.",
                4: "u7>u6>u5>u4 spells per day.",
                5: "u8>u7>u6>u5>u4 spells per day.",
                6: "u10>u8>u7>u6>u5>u4 spells per day.",
                7: "u12>u10>u8>u7>u6>u5>u4 spells per day.",
                8: "u14>u12>u10>u8>u7>u6>u5>u4 spells per day.",
                9: "u16>u14>u12>u10>u8>u7>u6>u5>u4 spells per day.",
                10: "u20>u16>u14>u12>u10>u8>u7>u6>u5>u4 spells per day.",
            }
            return usage_die_dict[level]

if __name__ == "__main__":
    print("\nGold & Gallows character creator version 1\nBy Eric -- https://locallyringed.space")
    new_or_load = prompt.multiple_choice(
        "Are you making a new character or loading an old one?", 
        ["New", "Load",]
    )
    match new_or_load:
        case "New":
            inventory = []
            abilities = []
            spells = []
            level = 1
            armor_score = 0
            shield_score = 0
            gold_spent_this_level = 0
            gold_stored_away = 0
            auto_roll = ask_to_auto_roll()
            print("\nLet's start with your stats.")
            match auto_roll:
                case "Yes":
                    stats = roll_stats()
                case "No, I'll enter dice rolls manually":
                    stats = manual_stats()
            print(
                f'\nYour stats are CHA: {stats["CHA"]}, CON: {stats["CON"]}, DEX: {stats["DEX"]}, INT: {stats["INT"]}, STR: {stats["STR"]}, and WIS: {stats["WIS"]}.'
            )
            character_class = pick_class()
            print(f"\nYour class is {character_class}.")
            match auto_roll:
                case "Yes":
                    max_hp = roll_hp(character_class)
                case "No, I'll enter dice rolls manually":
                    max_hp = manual_hp(character_class)
            current_hp = max_hp
            print(f"Your starting HP is {max_hp}.")
            print(f"Your AC is {calculate_AC(stats['DEX'], armor_score, shield_score)} and your AV is {calculate_AV(character_class, level)}.")
            match auto_roll:
                case "Yes":
                    gold_on_person = dice.roll(3,6,3)*10
                case "No, I'll enter dice rolls manually":
                    gold_on_person = prompt.open_response_number(
                        "How much gold do you start with?",
                        [number for number in range(0,181)]
                    )
            print(f"You start with {gold_on_person} gold.")
            need_starting_weapon = True 
            while need_starting_weapon:
                starting_weapon = prompt.unbounded_open_response(
                    "What is your starting weapon?",
                    "My starting weapon is a >",
                )
                starting_weapon_damage = prompt.multiple_choice(
                    "What damage die does it use?",
                    [4,6,8]
                )
                starting_weapon_ranged = prompt.multiple_choice(
                    "Is it a ranged weapon?",
                    ["Yes", "No",]
                )
                if check_if_weapon_is_allowed(starting_weapon_damage, starting_weapon_ranged, character_class) == "Yes":
                    if starting_weapon_ranged == "Yes":
                        starting_weapon += f" (d{starting_weapon_damage} damage, ranged)"
                    else:
                        starting_weapon += f" (d{starting_weapon_damage} damage)"
                    need_starting_weapon = False
            print(f"\nYour starting weapon is a {starting_weapon} that deals d{starting_weapon_damage} damage.")
            inventory.append(starting_weapon)
            gain_spells_upon_leveling(spells, character_class, level)
            name = prompt.unbounded_open_response(
                "What is your name?",
                "My name is >",
            )
        case "Load":
            print("TODO: Load a character")
    while True:
        draw_character_sheet()
        action = prompt.multiple_choice(
            "What would you like to do?",
            [
                "Roll a die",
                "Add an item to your inventory",
                "Remove an item from your inventory",
                "Edit an item in your inventory",
                "Equip an item in your inventory",
                "Unequip an item in your inventory",
                "Spend gold on person",
                "Gain gold on person",
                "Lose gold on person",
                "Store gold away",
                "Get gold out of storage",
                "Spend gold in storage",
                "Gain gold in storage",
                "Lose gold in storage",
                "Level up",
                "Lose HP",
                "Heal HP",
                "Edit a value",
                "Learn a spell",
                "Save and quit",
            ]
        )
    