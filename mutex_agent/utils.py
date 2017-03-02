import google.protobuf.json_format
import json


def pbo_to_json(pbo):
    return google.protobuf.json_format.MessageToJson(pbo).replace('\n','')


def pbo_to_dict(pbo):
    return json.loads(pbo_to_json(pbo))