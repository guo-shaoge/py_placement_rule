#!/usr/bin/env python3
import json
import sys

def is_enable_wn_rule(constraint):
    res = False

    if constraint['key'] == 'engine_role' and constraint['op'] == 'in':
        values = constraint['values']
        if len(values) == 1 and values[0] == 'write':
            res = True

    return res

with open(sys.argv[1]) as f:
    rules = json.load(f)
    new_rules = []
    for rule in rules:
        if rule['id'].startswith('keyspace-' + sys.argv[2]):
            continue
        else:
            # check and update group_id
            if rule['group_id'] != 'enable_s3_wn_region':
                print(rule['id'] + ' has wrong rule group, should be label_constraints')
                exit()

            constraints = rule['label_constraints']
            has_disable_wn_rule = False
            for constraint in constraints:
                if is_enable_wn_rule(constraint):
                    has_disable_wn_rule = True

            if not has_disable_wn_rule:
                print(rule['id'] + ' has no enable wn rule')
                exit()

            rule['count'] = 0
            new_rules.append(rule)
    print(json.dumps(new_rules, indent=2))

