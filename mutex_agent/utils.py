import google.protobuf.json_format
import json


def pbo_to_json(pbo):
    assert len(pbo.ListFields()) != 0
    return google.protobuf.json_format.MessageToJson(pbo, preserving_proto_field_name=True).replace('\n','')


def pbo_to_dict(pbo):
    # return json.loads(pbo_to_json(pbo))
    return google.protobuf.json_format.MessageToDict(
        pbo,
        including_default_value_fields=False,
        preserving_proto_field_name=True
    )

