from __future__ import annotations
from enum import Enum
import logging
from typing import List


class Job:

    def __init__(self, name: str, role: str, subrole: str = ''):
        self.name = name
        self.role = role
        self.subrole = subrole

    @property
    def role_name(self):
        if self.role == Role.DPS:
            return "DPS"
        return self.role.name.title()


class Role(Enum):
    TANK = 1
    HEALER = 2
    DPS = 3
    ANY = 4


class Subrole(Enum):
    REGEN = 1
    SHIELD = 2
    MELEE = 3
    PHYS = 4
    CASTER = 5


all_jobs = [
    Job("PLD", Role.TANK),
    Job("WAR", Role.TANK),
    Job("DRK", Role.TANK),
    Job("GNB", Role.TANK),
    Job("WHM", Role.HEALER, Subrole.REGEN),
    Job("SCH", Role.HEALER, Subrole.SHIELD),
    Job("AST", Role.HEALER, Subrole.REGEN),
    Job("SGE", Role.HEALER, Subrole.SHIELD),
    Job("MNK", Role.DPS, Subrole.MELEE),
    Job("DRG", Role.DPS, Subrole.MELEE),
    Job("NIN", Role.DPS, Subrole.MELEE),
    Job("SAM", Role.DPS, Subrole.MELEE),
    Job("RPR", Role.DPS, Subrole.MELEE),
    Job("BRD", Role.DPS, Subrole.PHYS),
    Job("MCH", Role.DPS, Subrole.PHYS),
    Job("DNC", Role.DPS, Subrole.PHYS),
    Job("BLM", Role.DPS, Subrole.CASTER),
    Job("SMN", Role.DPS, Subrole.CASTER),
    Job("RDM", Role.DPS, Subrole.CASTER),
]

available_jobs = {
    Role.TANK: [j for j in all_jobs if j.role == Role.TANK],
    Role.HEALER: [j for j in all_jobs if j.role == Role.HEALER],
    Role.DPS: [j for j in all_jobs if j.role == Role.DPS],
    Role.ANY: all_jobs,
    Subrole.REGEN: [j for j in all_jobs if j.subrole == Subrole.REGEN],
    Subrole.SHIELD: [j for j in all_jobs if j.subrole == Subrole.SHIELD],
    Subrole.MELEE: [j for j in all_jobs if j.subrole == Subrole.MELEE],
    Subrole.PHYS: [j for j in all_jobs if j.subrole == Subrole.PHYS],
    Subrole.CASTER: [j for j in all_jobs if j.subrole == Subrole.CASTER],
}

job_names = [j.name for j in all_jobs]


def get_jobs(role: Role | Subrole) -> List[str]:
    if role not in available_jobs:
        logging.error('Invalid role/subrole %s', role)
        return []
    return available_jobs[role]


def get_job_id(job: Job) -> int:
    if job.name not in job_names:
        logging.error('Invalid job name %s', job.name)
        return 99
    return job_names.index(job.name)
