# gaia_mutex_integration

## Synopsis
The files in this repository use python 3 and Google's protocol buffers to convert Mutex input and output into the format accepted by Gaia (JSON messages).

## Motivation
Gaia is a Tinkerpop-based engine for gathering and analyzing biomedical data as graphs. It receives and outputs information organized into JSON messages. The Mutex algorithm utilizes mutual exclusivity of genomic alterations to identify signaling pathways involved in carcinogenesis. The goal of this project is to provide resources to automatically convert Mutex input and output into JSON messages for the purpose of communication with the Gaia platform.

Gaia: https://github.com/bmeg/gaia  
Mutex: https://github.com/PathwayAndDataAnalysis/mutex  
Mutex publication: https://genomebiology.biomedcentral.com/articles/10.1186/s13059-015-0612-6

## Mutex Agent Overview

1. Gaia will provide a JSON message (called a Mutex Run Message) to parse-MRM.py.  
2. parse-MRM.py will invoke a Mutex run via an API call to either a TES or WES compliant service.
3. Mutex will output ranked-groups.txt.  
4. post-message.py will read-in ranked-groups.txt and output a multi-line ranked-groups JSON message.
5. Gaia will receive this JSON message.

## Protobuf schema:
These files have the .proto extension are contained in the schema directory.

For more information on protocol buffers, see: https://developers.google.com/protocol-buffers/docs/pythontutorial

To compile the schema run:

`bash bin/build-proto`

## Creating A Mutex Run Message (MRM) for MRM_Converter.py testing purposes:
An example MRM is provided: tests/resources/MRM_DEVEL.json
  
Or use src/create-MRM.py to generate a MRM from a new parameters.txt and a data matrix url. The data matrix url will be used to query Gaia which will return a data matrix .json file.
  
`python src/create-MRM.py --ip tests/resources/parameters.txt --im tests/resources/DataMatrix.txt -mro MRM.json -mto MatM.json`

## Converting a MRM to be received by the Mutex agent:
Example bash command:
  
`python parse-MRM.py --mode tes --endpoint http://someurl:8000/v1/jobs MRM.txt`
  
Relevant files:

| Filename      | Description   |
|:------------- |:------------- |
| parse-MRM.py  | Converts MutexRun JSON messages into messages compatible with the TES or WES APIs |
| MR_pb2.py     | Python-translated protobuf schema used by MRM_Converter.py |
| MRM_DEVEL.txt | Example Mutex run message (JSON format) to be converted with parse-MRM.py |


#### Notes on running MutexRun_message_converter.py:

The directory containing mutex.jar must also contain:
- MR_pb2.py
- MRM.json or a substitute (like MRM_DEVEL.json)
- resources/PC2v8.sif

DataMatrix.txt, parameters.txt, and (after Mutex concludes) ranked-groups.txt will be placed in sample-input/. If sample-input/ does not yet exist it will be created.

## Converting Mutex output file (ranked-groups.txt) to Alteration Group Message (AGM):
Example bash command:
  
`python create_AGM.py --ranked-groups ranked-groups.txt --outfile ranked_groups.json`
  
Relevant files:
  
| Filename                     | Description       |
|:---------------------------- |:----------------- |
| ranked-groups.txt            | Mutex output file |
| create-AGM.py                | Converts Mutex output (ranked-groups.txt) to JSON messages |
| AlterationGroupSchema_pb2.py | Python-translated protobuf schema used by ranked_groups_converter.py |

## Testing
Testing is in development. For now, the test directory contains a preliminary structure appropriate for a not-yet-created test script. It also contains a subdirectory ("pretest") that holds example input and output files for the conversion scripts. 
