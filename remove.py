#!/usr/bin/env python3
import json
import sys

with open(sys.argv[1]) as f:
    rules = json.load(f)
    new_rules = []
    for rule in rules:
        if rule['id'].startswith('keyspace-5794'):
            # check and update group_id
            new_rules.append(rule)
    print(json.dumps(new_rules, indent=2))
