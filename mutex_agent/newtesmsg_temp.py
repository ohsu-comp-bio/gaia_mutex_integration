#old
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