# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: AlterationGroupSchema.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='AlterationGroupSchema.proto',
  package='',
  syntax='proto3',
  serialized_pb=_b('\n\x1b\x41lterationGroupSchema.proto\"<\n\x0f\x41lterationGroup\x12\r\n\x05score\x18\x01 \x01(\x02\x12\t\n\x01q\x18\x02 \x01(\x02\x12\x0f\n\x07members\x18\x03 \x03(\tb\x06proto3')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_ALTERATIONGROUP = _descriptor.Descriptor(
  name='AlterationGroup',
  full_name='AlterationGroup',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='score', full_name='AlterationGroup.score', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='q', full_name='AlterationGroup.q', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='members', full_name='AlterationGroup.members', index=2,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=31,
  serialized_end=91,
)

DESCRIPTOR.message_types_by_name['AlterationGroup'] = _ALTERATIONGROUP

AlterationGroup = _reflection.GeneratedProtocolMessageType('AlterationGroup', (_message.Message,), dict(
  DESCRIPTOR = _ALTERATIONGROUP,
  __module__ = 'AlterationGroupSchema_pb2'
  # @@protoc_insertion_point(class_scope:AlterationGroup)
  ))
_sym_db.RegisterMessage(AlterationGroup)


# @@protoc_insertion_point(module_scope)
