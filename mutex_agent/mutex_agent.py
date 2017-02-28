#!/usr/bin/env python

from __future__ import print_function

import argparse
import json
import os
import requests

import parse_MRM


def formatTESMessage(params, storage_pre):
    cwd = os.path.dirname(os.path.realpath(__file__))
    task_message = {
        "name": "Mutex",
        "inputs": [
            {
                "location": storage_pre + os.path.join(cwd, "create_AGM.py"),
                "class": "File",
                "path": "/mnt/create_AGM.py"
            }
        ],
        "outputs": [
            {
                "location": storage_pre + os.path.join(cwd, "tests", "ranked_groups.txt"),
                "class": "File",
                "path": "/mnt/ranked-groups.txt"
            },
            {
                "location": storage_pre + os.path.join(cwd, "tests", "AGM.json"),
                "class": "File",
                "path": "/mnt/AGM.json"
            }
        ],
        "resources": {
            "minimumCpuCores": 1,
            "minimumRamGb": 8,
            "volumes": [{
                "name": "work-dir",
                "sizeGb": 5,
                "mountPoint": "/mnt"
            }]
        },
        "docker": [
            {
                "imageName": "opengenomics/mutex:v1.0",
                "cmd": [
                    "python",
                    "/home/mutex.py"
                ],
                "workdir": "/mnt",
                "stdout": "stdout",
                "stderr": "stderr",
            },
            {
                "imageName": "opengenomics/mutex:v1.0",
                "cmd": [
                    "python",
                    "/mnt/create-AGM.py",
                    "--ranked-groups", "/mnt/ranked-groups.txt",
                    "--outfile", "/mnt/AGM.json"
                ],
                "Workdird": "/mnt",
                "stdout": "stdout",
                "stderr": "stderr",
            }

        ]
    }

    filtered_params = dict((k, v) for k, v in params.iteritems() if v)

    for k, v in filtered_params.items():
        if k in ["data_file", "genes_file", "network_file"]:
            p = os.path.abspath(v)
            task_message["inputs"].append(
                {
                    "name": k,
                    "location": storage_pre + p,
                    "class": "File",
                    "path": "/mnt/{0}".format(os.path.basename(p))
                }
            )
            task_message["docker"][0]["cmd"].append(
                ("--{0}").format(k.replace("_", "-"))
            )
            task_message["docker"][0]["cmd"].append(
                ("/mnt/{0}").format(os.path.basename(p))
            )
        else:
            task_message["docker"][0]["cmd"].append(
                ("--{0}").format(k.replace("_", "-"))
            )
            task_message["docker"][0]["cmd"].append(str(v))

    return task_message


def post_task(message, endpoint):
    if not endpoint.startswith("http"):
        endpoint = "http://" + endpoint

    if endpoint.endswith("/"):
        endpoint = endpoint[:-1]

    response = requests.post(endpoint, data=json.dumps(message))
    return response


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", "-m",
                        default="tes",
                        choices=["tes", "cwl"],
                        type=str,
                        help="engine selection")
    parser.add_argument("--endpoint", "-e",
                        type=str,
                        help="endpoint to submit mutex task to")
    parser.add_argument("message")
    args = parser.parse_args()

    msg = parse_MRM.loadMessage(args.message)
    if parse_MRM.validateMessage(msg):

        if args.mode == "tes":
            tes_message = formatTESMessage(msg, "file://")
            r = post_task(tes_message, args.endpoint)
        elif args.mode == "cwl":
            # cwl_inputs = formatCWLInputs(msg)
            # r = post_task(cwl_desc, cwl_inputs)
            raise NotImplementedError

        if r.status_code // 100 != 2:
            raise RuntimeError(
                "[STATUS CODE - {0}] Failed to start Mutex: {1}".format(
                    r.status_code, r.text
                )
            )
        print(r.text)
    else:
        raise RuntimeError(
            "Error parsing message; check the message format against schema"
        )
