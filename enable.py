#!/usr/bin/env python3
import json
import sys

def is_disable_wn_rule(constraint):
    res = False

    if constraint['key'] == 'engine_role' and constraint['op'] == 'notIn':
        values = constraint['values']
        if len(values) == 1 and values[0] == 'write':
            res = True

    return res

with open(sys.argv[1]) as f:
    rules = json.load(f)
    new_rules = []
    for rule in rules:
        if rule['id'].startswith('keyspace-' + sys.argv[2]):
            # check and update group_id
            if rule['group_id'] != 'tiflash':
                print(rule['id'] + ' has wrong rule group, should be tiflash')
                exit()
            rule['group_id'] = 'enable_s3_wn_region'

            constraints = rule['label_constraints']
            new_constraints = []
            has_disable_wn_rule = False

            # del 'engine_role' notIn 'write'
            for constraint in constraints:
                if is_disable_wn_rule(constraint):
                    has_disable_wn_rule = True
                else:
                    new_constraints.append(constraint)

            if not has_disable_wn_rule:
                print(rule['id'] + ' has no disable wn rule')
                exit()

            # add 'engine_role' in 'write'
            enable_wn_rule = {'key': 'engine_role', 'op': 'in', 'values': ['write']}
            new_constraints.append(enable_wn_rule)
            rule['label_constraints'] = new_constraints
            rule['count'] = 1
            new_rules.append(rule)
    print(json.dumps(new_rules, indent=2))
