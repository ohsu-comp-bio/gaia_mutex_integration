from __future__ import print_function

import argparse
import json
import os
import requests

from . import parse_MRM
from . import create_matrix
from . import utils


def format_tes_message(mrm_dict, storage_pre):
    cwd = os.path.dirname(os.path.realpath(__file__))
    task_message = {
        "name": "Mutex",
        "inputs": [],
        "outputs": [
            {
                "url": storage_pre + os.path.join(cwd, "tests", "ranked_groups.txt"),
                "path": "/mnt/ranked-groups.txt"
            },
            {
                "url": storage_pre + os.path.join(cwd, "tests", "AGM.json"),
                "path": "/mnt/AGM.json"
            }
        ],
        "resources": {
            "cpu_cores": 1,
            "ram_gb": 8
        },
        "executors": [
            {
                "image_name": "opengenomics/mutex:latest",
                "cmd": [
                    "mutex.py"
                ],
                "workdir": "/mnt",
                "stdout": "stdout",
                "stderr": "stderr"
            },
            {
                "image_name": "mutex_agent:v0.1",
                "cmd": [
                    "create_AGM.py",
                    "--ranked-groups", "/mnt/ranked-groups.txt",
                    "--outfile", "/mnt/AGM.json"
                ],
                "workdir": "/mnt",
                "stdout": "stdout",
                "stderr": "stderr"
            }

        ]
    }

    for k in mrm_dict:
        v = mrm_dict[k]
        if k in ["data_file", "genes_file", "network_file"]:
            p = os.path.abspath(v)
            task_message["inputs"].append(
                {
                    "name": k,
                    "url": storage_pre + p,
                    "path": "/mnt/{0}".format(os.path.basename(p))
                }
            )
            task_message["executors"][0]["cmd"].append(
                "--{0}".format(k.replace("_", "-"))
            )
            task_message["executors"][0]["cmd"].append(
                "/mnt/{0}".format(os.path.basename(p))
            )
        else:
            task_message["executors"][0]["cmd"].append(
                "--{0}".format(k.replace("_", "-"))
            )
            task_message["executors"][0]["cmd"].append(str(v))

    return task_message

# post the task to TES
def post_task(message, endpoint):
    if not endpoint.startswith("http"):
        endpoint = "http://" + endpoint

    if endpoint.endswith("/"):
        endpoint = endpoint[:-1]

    response = requests.post(endpoint, data=json.dumps(message))
    #response.raise_for_status()

    return response


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", "-m",
                        default="tes",
                        choices=["tes", "cwl"],
                        type=str,
                        help="engine selection")
    parser.add_argument("--endpoint", "-e",
                        default="localhost:8000/v1/tasks",
                        type=str,
                        help="endpoint to submit mutex task to")
    parser.add_argument("--data-file", "-d",
                        default="./DataMatrix.txt",
                        type=str,
                        help="data file path; default = ./DataMatrix.txt")
    parser.add_argument("message",
                        help="MR JSON message")
    args = parser.parse_args()

    # convert json message to pbo, to dict, add path to datamatrix if available
    mrm_pbo = parse_MRM.message_to_pbo(args.message)
    mrm_dict = utils.pbo_to_dict(mrm_pbo)
    mrm_dict['data_file'] = args.data_file

    # if there isn't a DataMatrix.txt in this file, get it as a message from mock_gaia
    # compose the matrix
    if not os.path.exists(args.data_file):

        matrix_json = create_matrix.get_matrix_from_gaia(mrm_dict['matrix_url'])
        matrix_pbo = create_matrix.convert_matrix_to_pb(matrix_json)
        create_matrix.build_matrix_outfile(args.data_file, matrix_pbo)

    # remove this later
    del mrm_dict['matrix_url']

    # post message to TES, TES should initiate docker process that starts Mutex
    # Mutex should output ranked-groups.txt in sample-input
    if args.mode == "tes":
        tes_message = format_tes_message(mrm_dict, "file://")
        r = post_task(tes_message, args.endpoint)
    elif args.mode == "cwl":
        # cwl_inputs = formatCWLInputs(msg)
        # r = post_task(cwl_desc, cwl_inputs)
        raise NotImplementedError

    # TODO: "monkey business"
    if r.status_code // 100 != 2:
        raise RuntimeError(
            "[STATUS CODE - {0}] Failed to start Mutex: {1}".format(
                r.status_code, r.text
            )
        )
    print(r.text)
