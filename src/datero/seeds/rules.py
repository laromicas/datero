import json
import os
from datero.commands import SEEDS_FOLDER
from datero.commands.seed_manager import seed_available


class Rules:

    _rules = []

    def __init__(self):
        for seed in seed_available():
            rules_file = os.path.join(SEEDS_FOLDER, seed[0], 'rules.json')
            # yield rules_file
            if os.path.exists(rules_file):
                with open(rules_file, 'r') as f:
                    Rules._rules.extend(json.load(f))
        self._rules.sort(key=lambda x: x['priority'], reverse=True)

    @property
    def rules(self):
        return self._rules
