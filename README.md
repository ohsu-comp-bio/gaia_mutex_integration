# gaia_mutex_integration

## Synopsis
The files in this repository use python 3 and Google's protocol buffers to convert Mutex input and output into the format accepted by Gaia (JSON messages).

## Motivation
Gaia is a Tinkerpop-based engine for gathering and analyzing biomedical data as graphs. It receives and outputs information organized into JSON messages. The Mutex algorithm utilizes mutual exclusivity of genomic alterations to identify signaling pathways involved in carcinogenesis. The goal of this project is to provide resources to automatically convert Mutex input and output into JSON messages for the purpose of communication with the Gaia platform.

Gaia: https://github.com/bmeg/gaia  
Mutex: https://github.com/PathwayAndDataAnalysis/mutex  
Mutex publication: https://genomebiology.biomedcentral.com/articles/10.1186/s13059-015-0612-6

## Mutex Input and Output
Mutex takes as input two files with the names:
  - parameters.txt  
  - DataMatrix.txt  
  
Mutex outputs one file with the name:
  - ranked-groups.txt

Verbosely:  

1. Gaia will provide a 1-line file containing a JSON message (called a Mutex Run Message) to MRM_Converter.py.  
2. MRM_Converter.py will output parameters.txt and DataMatrix.txt and invoke Mutex.  
3. Mutex will output ranked-groups.txt.  
4. ranked_groups_converter.py will read-in ranked-groups.txt and output a multi-line ranked-groups JSON message.
5. Gaia will receive this JSON message.

## Creating A Mutex Run Message (MRM) for MRM_Converter.py testing purposes:
An example MRM is provided: test/MRM_DEVEL.txt.  
  
Or use MRM_Maker.py to generate a MRM from new parameters.txt and DataMatrix.txt files with the bash command:  
  
$ python3 MRM_Maker.py -inparam parameters.txt -inmat DataMatrix.txt -outf MRM.txt

## Converting a MRM to be received by Mutex:
Example bash command:  
  
$ python3 MRM_Converter.py -mrm MRM.txt
  
Relevant files:  

| Filename        | Description           |
|:------------- |:------------- |
| MRM_Converter.py     | Converts MutexRun JSON messages into parameters.txt and DataMatrix.txt; Invokes Mutex |
| MR_pb2.py      | Python-translated protobuf schema used by MRM_Converter.py     |
| MRM_DEVEL.txt | Example Mutex run message (JSON format) to be converted with MRM_Converter.py      |
| mutex.jar     | Mutex |

#### Notes on running MutexRun_message_converter.py:
The directory containing mutex.jar must also contain:  
- MR_pb2.py  
- MRM.txt or a substitute (like MRM_DEVEL.txt)  
- resources/PC2v8.sif  

DataMatrix.txt, parameters.txt, and (after Mutex concludes) ranked-groups.txt will be placed in sample-input/. If sample-input/ does not yet exist it will be created.

## Converting Mutex output file (ranked-groups.txt):
Example bash command:  
  
$ python3 ranked_groups_converter.py -rg ranked-groups.txt -outfile ranked-groups.json  
  
Relevant files:  
  
| Filename        | Description           |
|:------------- |:------------- |
| ranked-groups.txt   | Mutex output file |
| ranked_groups_converter.py      | Converts Mutex output (ranked-groups.txt) to JSON messages     |
| AlterationGroupSchema_pb2.py | Python-translated protobuf schema used by ranked_groups_converter.py      |

## Protobuf schema
These files have the .proto extension are contained in the schema directory. They have been translated into python (see scripts ending in pb2.py) for use in the conversion scripts.  
  
For more information on protocol buffers, see: https://developers.google.com/protocol-buffers/docs/pythontutorial

## Testing
Testing is in development. For now, the test directory contains a preliminary structure appropriate for a not-yet-created test script. It also contains a subdirectory ("pretest") that holds example input and output files for the conversion scripts. 
