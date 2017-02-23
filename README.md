# gaia_mutex_integration

## Synopsis
The files in this repository use python 3 and Google's protocol buffers to convert Mutex input and output into the format accepted by Gaia (JSON messages).

## Files for Mutex input:
The MutexInConversion directory contains:  

| Filename        | Description           |
|:------------- |:------------- | -----:|
| MRM_Converter.py     | Converts MutexRun JSON messages into parameters.txt and DataMatrix.txt; Invokes Mutex |
| MR_pb2.py      | Python-translated protobuf schema used by MRM_Converter.py     |
| MRM_DEVEL.txt | Example Mutex run message (JSON format) to be converted with MRM_Converter.py      |
| MutexIn_Misc/ | Directory containing scripts and example files used to generate JSON messages for testing MRM_Converter.py |

#### Notes on running MutexRun_message_converter.py:
It is intended to be run from the mutex directory containing:  
- mutex.jar  
- MR_pb2.py  
- MRM.txt or a substitute (like MRM_DEVEL.txt)  
- MutexRun_pb2.py  
- MutexRunMsg.txt  
- resources/PC2v8.sif  
- sample-input/  

Output will be deposited into sample-input/. If sample-input/ does not exist it will be created.

Example bash command:  
$ python MutexRun_message_converter.py -mrm MutexRunMsg_DEVEL.txt

## Files for Mutex output
The MutexOutConversion directory contains:

| Filename        | Description           |
|:------------- |:------------- | -----:|
| ranked-groups.txt   | Example Mutex output file |
| ranked_groups_converter.py      | Converts Mutex output (ranked-groups.txt) to JSON messages     |
| AlterationGroupSchema_pb2.py | Python-translated protobuf schema used by ranked_groups_converter.py      |
| MutexOut_Misc/ | Directory containing example ranked_groups_converter.py output and the protobuf schema used to generate AlterationGroupSchema_pb2.py |

Example bash command:  
$ python ranked_groups_converter.py -rg ranked-groups.txt -outfile rg_json_messages.txt
