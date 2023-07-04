from typing import Dict, List
import random

rolesStandardList = [
    'Tank', 'Tank', 'Healer', 'Healer', 'Melee', 'Phys', 'Caster', 'Flex DPS'
]
rolesAllianceList = [
    'Tank', 'Healer', 'Healer', 'Melee', 'Phys', 'Caster', 'Flex DPS',
    'Flex DPS'
]

rolesStandardChallenge = [
    'Tank', 'Tank', 'Healer', 'Healer', 'Flex DPS', 'Flex DPS', 'Flex DPS',
    'Flex DPS'
]
rolesAllianceChallenge = [
    'Tank', 'Healer', 'Healer', 'Flex DPS', 'Flex DPS', 'Flex DPS', 'Flex DPS',
    'Flex DPS'
]

jobsDict = {
    'Tank': ['DRK', 'PLD', 'GNB', 'WAR'],
    'Healer': ['WHM', 'AST', 'SCH', 'SGE'],
    'Melee': ['DRG', 'RPR', 'SAM', 'MNK', 'NIN'],
    'Caster': ['RDM', 'BLM', 'SMN'],
    'Phys': ['BRD', 'MCH', 'DNC']
}

fightsList = []
for a in ['T', 'A', 'O', 'E', 'P']:
    if a == 'T':
        for i in range(5, 9):
            fightsList.append(str(a) + (str(i + 1) + 'S'))
    else:
        for i in range(12):
            fightsList.append(str(a) + (str(i + 1) + 'S'))

fightsList += [
    'Ultima Weapon', 'Garuda', 'Titan', 'Ifrit', 'Moogle', 'Leviathan',
    'Ramuh', 'Shiva', 'Ravana', 'Bismarck', 'Thordan', 'Sephirot', 'Nidhogg',
    'Sophia', 'Zurvan', 'Susano', 'Lakshmi', 'Shinryu', 'Byakko', 'Tsukuyomi',
    'Rathalos', 'Suzaku', 'Seiryu', 'Titania', 'Innocence', 'Hades', 'Ruby',
    'Varis', 'WoL', 'Emerald', 'Diamond', 'Zodiark', 'Hydaelyn', 'Endsinger',
    'Barbariccia', 'Rubicante', 'Golbez'
]
fightsList += ['UWU', 'UCOB', 'TEA', 'DSR', 'TOP']
allianceList = [
    'The Royal City of Rabanastre', 'Ridorana Lighthouse', 'Orbonne Monastery',
    'The Copied Factory', 'The Puppet\'s Bunker',
    'The Tower at Paradigms Breach', 'Aglaia', 'Euphrosyne'
]
fightsList += allianceList

thePlayers = []
theTeam = {}
theFight = ''


def RoleAssign(pList, allianceCheck, challengeCheck):
    if allianceCheck:
        if challengeCheck:
            pRoles = dict(zip(pList, rolesAllianceChallenge))
        else:
            pRoles = dict(zip(pList, rolesAllianceList))
    else:
        if challengeCheck:
            pRoles = dict(zip(pList, rolesStandardChallenge))
        else:
            pRoles = dict(zip(pList, rolesStandardList))
    return pRoles


def JobAssign(pList, allianceCheck, challengeCheck):
    pJobList = {}
    count = 0
    useList = []
    if allianceCheck:
        if challengeCheck:
            useList = rolesAllianceChallenge
        else:
            useList = rolesAllianceList
    else:
        if challengeCheck:
            useList = rolesStandardChallenge
        else:
            useList = rolesStandardList

    for p in pList:
        if useList[count] != 'Flex DPS':
            role = str(useList[count])
        else:
            role = str(random.choice(['Melee', 'Caster', 'Phys']))
        job = random.choice(jobsDict[role])
        pJobList[p] = ','.join([role, job])
        count += 1
    return pJobList


def ShinRoulette(players: List[str], assign_jobs: bool,
                 standard_composition: bool) -> (str, Dict[str, str]):
    """
    Runs the Shin Roulette

    returns: A tuple of (fight, assigned_players)
    """

    isAlliance = False
    random.shuffle(players)
    theFight = random.choice(fightsList)
    if theFight in allianceList:
        isAlliance = True

    if assign_jobs:
        theTeam = JobAssign(players, isAlliance, not standard_composition)
    else:
        theTeam = RoleAssign(players, isAlliance, not standard_composition)

    return (theFight, theTeam)


def RoleIndex(role: str):
    if role not in rolesStandardList:
        return 99
    return rolesStandardList.index(role)
