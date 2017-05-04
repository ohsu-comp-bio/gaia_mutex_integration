# gaia_mutex_integration

## Synopsis
The files in this repository employ python and Google's protocol buffers to convert Mutex input and output into the format accepted by Gaia (JSON messages).

## Motivation
Gaia is a Tinkerpop-based engine for gathering and analyzing biomedical data as graphs. It receives and outputs information organized into JSON messages. The Mutex algorithm utilizes mutual exclusivity of genomic alterations to identify signaling pathways involved in carcinogenesis. The goal of this project is to provide resources to automatically convert Mutex input and output into JSON messages for the purpose of communication with the Gaia platform.

Gaia: https://github.com/bmeg/gaia  
Mutex: https://github.com/PathwayAndDataAnalysis/mutex  
Mutex publication: https://genomebiology.biomedcentral.com/articles/10.1186/s13059-015-0612-6

## Mutex Agent Overview

A user (or a trigger) will instruct Gaia to find mutually exclusive groups of genes on a given dataset. Gaia will submit a Mutex Run Message to an Apache Kafka queue. The agent will then:

1. Consume this JSON message from the queue
2. Request the desired Data Matrix (Mutex input) from Gaia
3. Convert DataMatrix.json into DataMatrix.txt
4. Submit an API call to either a TES or WES compliant service.

The service will initiate a docker process that causes a mutex wrapper to construct parameters.txt (Mutex input) and invoke Mutex. Mutex will output ranked-groups.txt. The agent will then:

5. Convert ranked-groups.txt into a JSON message
6. Post it to Kafka for storage

## Protobuf schema:
These files have the .proto extension are contained in the schema directory.

For more information on protocol buffers, see: https://developers.google.com/protocol-buffers/docs/pythontutorial

To compile the schema run:

`bash bin/build-proto`

## Creating A Mutex Run Message (MRM) for MRM_Converter.py testing purposes:
An example MRM is provided: tests/resources/MRM_DEVEL.json
  
Or use src/create-MRM.py to generate a MRM from a new parameters.txt and a data matrix url. The data matrix url will be used to query Gaia which will return a data matrix JSON file.
  
`python src/create-MRM.py --ip tests/resources/parameters.txt --im tests/resources/DataMatrix.txt -mro MRM.json -mto MatM.json`

## Running the Mutex Agent
Example bash command:

`./bin/mutex-agent --mode tes --endpoint localhost:8000/v1/jobs tests/resources/MRM_DEVEL.json`

  
Relevant files:

| Filename        | Description   |
|:--------------- |:------------- |
| mutex-agent     | Runs mutex_agent.py |
| mutex_agent.py  | Calls on parse_MRM.py, create_matrix.py and other scripts |
| parse-MRM.py    | Defines functions which convert MutexRun JSON messages into messages compatible with the TES or WES APIs |
| create_matrix.py| Defines functions which request JSON matrix from Gaia and convert it to .txt |
| MR_pb2.py       | Python-translated protobuf schema used by MRM_Converter.py |
| MRM_DEVEL.json  | Example Mutex run message (JSON format) to be converted with parse-MRM.py |


#### Notes on running MutexRun_message_converter.py:

The directory containing mutex.jar must also contain:
- MR_pb2.py
- MRM.json or a substitute (like MRM_DEVEL.json)
- resources/PC2v8.sif

DataMatrix.txt, parameters.txt, and (after Mutex concludes) ranked-groups.txt will be placed in sample-input/. If sample-input/ does not yet exist it will be created.

## Converting Mutex output file (ranked-groups.txt) to Alteration Group Message (AGM):
Example bash command:

`./bin/create-AGM --ranked-groups tests/resources/ranked-groups.txt --outfile AGM.json`
  
Relevant files:
  
| Filename                     | Description       |
|:---------------------------- |:----------------- |
| create-AGM                   | Runs create-AGM.py|
| create-AGM.py                | Converts Mutex output (ranked-groups.txt) to JSON messages |
| ranked-groups.txt            | Mutex output file (an example is provided in tests/resources)|
| AlterationGroupSchema_pb2.py | Python-translated protobuf schema used by ranked_groups_converter.py |

## Testing
Testing is in development (see tests directory). Tests may be run and the coverage of those tests (# of statements tested) may be assessed with the following nosetests command:

`nosetests --with-coverage --cover-package=mutex_agent/ tests/`
