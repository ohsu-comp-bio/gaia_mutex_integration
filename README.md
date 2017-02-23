# gaia_mutex_integration

## Synopsis
The files in this repository use python 3 and Google's protocol buffers to convert Mutex input and output into the format accepted by Gaia (JSON messages).

## Files for Mutex input:
The param_and_dm_tojson directory contains:  

| Filename        | Description           |
|:------------- |:------------- | -----:|
<<<<<<< ours
| MRM_Converter.py     | Converts MutexRun JSON messages into parameters.txt and DataMatrix.txt; Invokes Mutex |
| MR_pb2.py      | Python-translated protobuf schema used by MRM_Converter.py     |
| MRM_DEVEL.txt | Example Mutex run message (JSON format) to be converted with MRM_Converter.py      |
| param_and_dm_misc/ | Directory containing scripts and example files used to generate JSON messages for testing MRM_Converter.py |  
=======
| MutexRun_message_converter.py     | Converts MutexRun JSON messages into parameters.txt and DataMatrix.txt; Invokes Mutex |
| MutexRun_pb2.py      | Python-translated protobuf schema used by MutexRun_message_converter.py     |
| MutexRunMsg_DEVEL.txt | Example Mutex run message (JSON format) to be converted with MutexRun_message_converter.py      |
| param_and_dm_misc/ | Directory containing example files and scripts used to generate JSON messages for testing MutexRun_message_converter.py |  
>>>>>>> theirs

#### Notes on running MutexRun_message_converter.py:
It is intended to be run from the mutex directory containing:  
- mutex.jar  
<<<<<<< ours
- MR_pb2.py  
- MRM.txt or a substitute (like MRM_DEVEL.txt)  
=======
- MutexRun_pb2.py  
- MutexRunMsg.txt  
>>>>>>> theirs
- resources/PC2v8.sif  
- sample-input/  

Output will be deposited into sample-input/. If sample-input/ does not exist it will be created.

Example bash command:  
$ python MutexRun_message_converter.py -mrm MutexRunMsg_DEVEL.txt

## Files for Mutex output
The altgrp_tojson directory contains:

| Filename        | Description           |
|:------------- |:------------- | -----:|
| ranked-groups.txt   | Example Mutex output file |
| ranked_groups_converter.py      | Converts Mutex output (ranked-groups.txt) to JSON messages     |
| AlterationGroupSchema_pb2.py | Python-translated protobuf schema used by ranked_groups_converter.py      |
| altgrp_misc/ | Directory containing example ranked_groups_converter.py output and the protobuf schema used to generate AlterationGroupSchema_pb2.py |

Example bash command:  
$ python ranked_groups_converter.py -rg ranked-groups.txt -outfile rg_json_messages.txt
