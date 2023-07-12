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


def is_disable_wn_rule(constraint):
    res = False

    if constraint['key'] == 'engine_role' and constraint['op'] == 'notIn':
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
    ignore_rule = 0
    for rule in rules:
        # check group_id should be 'tiflash'
        if rule['group_id'] != 'tiflash':
            print(rule['id'] + ' has wrong rule group, should be label_constraints')
            exit()

        constraints = rule['label_constraints']
        has_ori_rule = False
        has_disable_wn_rule = False
        has_enable_wn_rule = False

        # 如果 rule 已经有 <engine in tiflash> <engine_role notIn write> 则忽略
        for con in constraints:
            if is_ori_tiflash_rule(con):
                has_ori_rule = True
            if is_disable_wn_rule(con):
                has_disable_wn_rule = True
            if is_enable_wn_rule(con):
                has_enable_wn_rule = True

        check_constraints_ok = False
        if has_ori_rule and has_disable_wn_rule:
            check_constraints_ok = True
        if has_enable_wn_rule:
            check_constraints_ok = False

        if not check_constraints_ok:
            print("unexpect plancement rule: we expect constraints: <engine in tiflash> and should not <engine_role in write>")
            print(json.dumps(rule, indent=2))
            exit()

        if has_disable_wn_rule:
            ignore_rule += 1
            continue

    print("ignore count: " + str(ignore_rule))



