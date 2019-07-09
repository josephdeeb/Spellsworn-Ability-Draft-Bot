from enum import Enum

SpellTypes = Enum('SpellTypes', 'Offensive Defensive Area Utility Travel')

class Spell:
    def __init__(self, name, type):
        self.name = name
        self.type = type

allSpells = [
    Spell('Bouncer', SpellTypes.Offensive),
    Spell('Chakram', SpellTypes.Offensive),
    Spell('Crescent', SpellTypes.Offensive),
    Spell('Fireball', SpellTypes.Offensive),
    Spell('Frostbolt', SpellTypes.Offensive),
    Spell('Homing', SpellTypes.Offensive),
    Spell('Magic Missile', SpellTypes.Offensive),
    Spell('Shock', SpellTypes.Offensive),

    Spell('Counter Pulse', SpellTypes.Defensive),
    Spell('Energy Shield', SpellTypes.Defensive),
    Spell('Lockdown', SpellTypes.Defensive),
    Spell('Phase Shift', SpellTypes.Defensive),
    Spell('Rock Pillar', SpellTypes.Defensive),
    Spell('Time Anchor', SpellTypes.Defensive),
    Spell('Windwalk', SpellTypes.Defensive),
    Spell('Consuming Void', SpellTypes.Defensive),

    Spell('Gravity', SpellTypes.Area),
    Spell('Lightning Strike', SpellTypes.Area),
    Spell('Meteor', SpellTypes.Area),
    Spell('Acid Pool', SpellTypes.Area),
    Spell('Arcane Mines', SpellTypes.Area),

    Spell('Chain Hook', SpellTypes.Utility),
    Spell('Dimension Gate', SpellTypes.Utility),
    Spell('Speed Boost', SpellTypes.Utility),
    Spell('Fetch', SpellTypes.Utility),
    Spell('Time Zone', SpellTypes.Utility),

    Spell('Blink', SpellTypes.Travel),
    Spell('Charge', SpellTypes.Travel),
    Spell('Swap Ball', SpellTypes.Travel),
    Spell('Side Step', SpellTypes.Travel)
]
