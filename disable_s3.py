#!/usr/bin/env python3
# From:
# {
#     group_id: tiflash,
#     constraints: [
#         {
#             key: engine,
#             op: in,
#             values: [
#                 tiflash,
#             ],
#         },
#         {
#         },
#     ],
# }
#
# To:
# {
#     group_id: tiflash,
#     constraints: [
#         {
#             key: engine,
#             op: in,
#             values: [
#                 tiflash,
#             ],
#         },
#         {
#             key: engine_role,
#             op: notIn,
#             values: [
#                 write,
#             ],
#         },
#     ],
# }

import json
import sys

with open(sys.argv[1]) as f:
    rules = json.load(f)
    new_rules = []
    for rule in rules:
        # check group_id should be 'tiflash'
        if rule['group_id'] != 'tiflash':
            print(rule['id'] + ' has wrong rule group, should be label_constraints')
            exit()

        constraints = rule['label_constraints']
        check_constraints_ok = True
        if len(constraints) != 1:
            check_constraints_ok = False
        else:
            if constraints[0]['key'] != 'engine' or constraints[0]['op'] != 'in':
                check_constraints_ok = False
            else:
                if len(constraints[0]['values']) != 1:
                    check_constraints_ok = False
                else:
                    if constraints[0]['values'][0] != 'tiflash':
                        check_constraints_ok = False

        if not check_constraints_ok:
            print("unexpect plancement rule: we expect constraints: <engine in tiflash> only")
            print(json.dumps(rule, indent=2))
            exit()

        disable_wn_rule = {'key': 'engine_role', 'op': 'notIn', 'values': ['write']}
        constraints.append(disable_wn_rule)
        new_rules.append(rule)
    print(json.dumps(new_rules, indent=2))


