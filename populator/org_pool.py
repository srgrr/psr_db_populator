import logging
from collections import namedtuple
from populator.org_archetype import OrgArchetype
from populator.rng import random_integer

weighted_org = namedtuple("WeightedOrg", "score org")


class OrgPool(object):
    def __init__(self):
        self.orgs = []

    def add_org(self, score, org: OrgArchetype):
        self.orgs.append(weighted_org(score, org))

    def pick_org(self):
        score_sum = sum(x.score for x in self.orgs)
        chosen_score = random_integer(1, score_sum)
        current_score = 0
        for score, org in self.orgs:
            if current_score <= chosen_score <= current_score + score:
                return org
            current_score += score
        raise RuntimeError(f"This should never happen")