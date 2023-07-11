import random
from typing import List

from shin_roulette.core.fights import Fight, all_fights
from shin_roulette.core import jobs


class AssignedPlayer:

    def __init__(self, player_name: str, job: jobs.Job):
        self.player_name = player_name
        self.job = job


class RouletteResult:

    def __init__(self, fight: Fight, players: List[AssignedPlayer]):
        self.fight = fight
        self.players = players


def run_roulette(players: List[str]) -> RouletteResult:
    random.shuffle(players)

    fight = random.choice(all_fights)

    assigned_players = []

    # Assign each role in the composition
    for i, role in enumerate(fight.composition):
        # Check that there's a player available to assign
        if i < len(players):
            job_pool = jobs.get_jobs(role)

            if not fight.duplicate_jobs_allowed:
                # Get list of assigned job strings
                assigned_jobs = [p.job.name for p in assigned_players]
                # Remove any already-assigned job strings from the job pool
                job_pool = [j for j in job_pool if j.name not in assigned_jobs]

            job = random.choice(job_pool)
            assigned_players.append(AssignedPlayer(players[i], job))

    # Sort assigned players by job ID
    assigned_players = sorted(assigned_players,
                              key=lambda p: jobs.get_job_id(p.job))

    return RouletteResult(fight, assigned_players)
