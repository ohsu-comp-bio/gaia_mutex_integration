from __future__ import print_function

import argparse
import json
import os
import requests

from . import parse_MRM
from . import create_matrix
from . import utils


def format_tes_message(mrm_pbo, storage_pre):
    cwd = os.path.dirname(os.path.realpath(__file__))
    task_message = {
        "name": "Mutex",
        "inputs": [],
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
                    "mutex.py"
                ],
                "workdir": "/mnt",
                "stdout": "stdout",
                "stderr": "stderr",
            },
            {
                "imageName": "mutex_agent:v0.1",
                "cmd": [
                    "create_AGM.py",
                    "--ranked-groups", "/mnt/ranked-groups.txt",
                    "--outfile", "/mnt/AGM.json"
                ],
                "Workdird": "/mnt",
                "stdout": "stdout",
                "stderr": "stderr",
            }

        ]
    }

    for k in mrm_pbo.DESCRIPTOR.fields_by_name:

        if k in ["data_file", "genes_file", "network_file"]:
            if k == "data_file":
                v = mrm_pbo.data_file
            if k == "genes_file":
                v = mrm_pbo.genes_file
            if k == "network_file":
                v = mrm_pbo.network_file
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
                "--{0}".format(k.replace("_", "-"))
            )
            task_message["docker"][0]["cmd"].append(
                "/mnt/{0}".format(os.path.basename(p))
            )
        else:
            task_message["docker"][0]["cmd"].append(
                "--{0}".format(k.replace("_", "-"))
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", "-m",
                        default="tes",
                        choices=["tes", "cwl"],
                        type=str,
                        help="engine selection")
    parser.add_argument("--endpoint", "-e",
                        default="localhost:8000",
                        type=str,
                        help="endpoint to submit mutex task to")
    parser.add_argument("--datapath", "-d",
                        default="./DataMatrix.txt",
                        type=str,
                        help="data file path; default = ./DataMatrix.txt")
    parser.add_argument("message",
                        help="MR JSON message")
    args = parser.parse_args()

    mrm_pbo = parse_MRM.message_to_pbo(args.message)
    mrm_dict = utils.pbo_to_dict(mrm_pbo)
    mrm_dict['datapath'] = args.datapath

    if not os.path.exists(args.datapath):

        matrix_json = create_matrix.get_matrix_from_gaia(mrm_pbo.matrix_url)
        matrix_pbo = create_matrix.convert_matrix_to_pb(matrix_json)
        create_matrix.build_matrix_outfile(args.datapath, matrix_pbo)

    if args.mode == "tes":
        tes_message = format_tes_message(mrm_dict, "file://")
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
