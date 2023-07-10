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

def is_ori_tiflash_rule(constraint):
    res = False

    if constraint['key'] == 'engine' and constraint['op'] == 'in':
        values = constraint['values']
        if len(values) == 1 and values[0] == 'tiflash':
            res = True

    return res


with open(sys.argv[1]) as f:
    rules = json.load(f)
    new_rules = []
    for rule in rules:
        # check group_id should be 'tiflash'
        if rule['group_id'] != 'enable_s3_wn_region':
            print(rule['id'] + ' has wrong rule group, should be label_constraints')
            exit()

        constraints = rule['label_constraints']
        check_constraints_ok = True
        if len(constraints) != 2:
            check_constraints_ok = False
        else:
            if (is_enable_wn_rule(constraints[0]) and is_ori_tiflash_rule(constraints[1])) or (is_enable_wn_rule(constraints[1]) and is_ori_tiflash_rule(constraints[0])):
                check_constraints_ok = True
            else:
                check_constraints_ok = False

        if not check_constraints_ok:
            print("unexpect plancement rule: we expect constraints: <engine in tiflash> <engine_role notIn write>")
            print(json.dumps(rule, indent=2))
            exit()

        rule['count'] = 0
        new_rules.append(rule)
    print(json.dumps(new_rules, indent=2))



