from typing import List

from shin_roulette.core.jobs import Role, Subrole


class Fight:

    def __init__(self, name: str, composition: List[Role | Subrole],
                 duplicate_jobs_allowed: bool, show_role: bool):
        self.name = name
        self.composition = composition
        self.duplicate_jobs_allowed = duplicate_jobs_allowed
        self.show_role = show_role


normal_fights = ['T1N', 'T2N', 'T3N', 'T4N', 'T5N', 'T10N', 'T11N', 'T12N', 'T13N']

extreme_fights = [
    'Ultima Weapon', 'Garuda', 'Titan', 'Ifrit', 'Moogle', 'Leviathan',
    'Ramuh', 'Shiva', 'Ravana', 'Bismarck', 'Thordan', 'Sephirot', 'Nidhogg',
    'Sophia', 'Zurvan', 'Susano', 'Lakshmi', 'Shinryu', 'Byakko', 'Tsukuyomi',
    'Suzaku', 'Seiryu', 'Titania', 'Innocence', 'Hades', 'Ruby', 'Varis',
    'Warrior of Light', 'Emerald', 'Diamond', 'Zodiark', 'Hydaelyn',
    'Endsinger', 'Barbariccia', 'Rubicante', 'Golbez', 'Zeromus',
    'Valigarmanda', 'Zoraal Ja'
]
extreme_fights = [s + ' EX' for s in extreme_fights]

savage_fights = []
for a in ['T', 'A', 'O', 'E', 'P', 'M']:
    if a == 'T':
        for i in range(6, 10):
            savage_fights.append(f'{a}{i}S')
    elif a == 'M':
        for i in range(1, 5):
            savage_fights.append(f'{a}{i}S')
    else:
        for i in range(1, 13):
            savage_fights.append(f'{a}{i}S')

ultimate_fights = ['UCOB', 'UWU', 'TEA', 'DSR', 'TOP']

alliance_fights = [
    'The Royal City of Rabanastre', 'Ridorana Lighthouse', 'Orbonne Monastery',
    'The Copied Factory', 'The Puppet\'s Bunker',
    'The Tower at Paradigms Breach', 'Aglaia', 'Euphrosyne', 'Thaleia'
]

guildhest_fights = ['Solemn Trinity Guildhest']

exploration_fights = ['Delubrum Reginae']

standard_composition = [
    Role.TANK, Role.TANK, Subrole.REGEN, Subrole.SHIELD, Subrole.MELEE,
    Subrole.PHYS, Subrole.CASTER, Role.DPS
]

alliance_composition = [
    Role.TANK, Role.HEALER, Role.HEALER, Role.DPS, Role.DPS, Role.DPS,
    Role.DPS, Role.DPS
]

guildhest_composition = [
    Role.TANK, Role.TANK, Role.HEALER, Role.HEALER, Role.DPS, Role.DPS,
    Role.DPS, Role.DPS
]

exploration_composition = [Role.ANY] * 8

all_fights = []
all_fights.extend(
    [Fight(s, standard_composition, False, True) for s in normal_fights])
all_fights.extend(
    [Fight(s, standard_composition, False, True) for s in extreme_fights])
all_fights.extend(
    [Fight(s, standard_composition, False, True) for s in savage_fights])
all_fights.extend(
    [Fight(s, standard_composition, False, True) for s in ultimate_fights])
all_fights.extend(
    [Fight(s, alliance_composition, True, True) for s in alliance_fights])
all_fights.extend(
    [Fight(s, guildhest_composition, True, True) for s in guildhest_fights])
all_fights.extend([
    Fight(s, exploration_composition, True, False) for s in exploration_fights
])
