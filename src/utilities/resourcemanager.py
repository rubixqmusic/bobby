import os
import json
import base64
import zlib
from shutil import copytree, rmtree, move

from settings import *

'''this module is used to manage resource packing and reading. It handles all associated encoding/decoding and compression. it is used to both load and read resource files as well as generate the resource pack during the build process'''

def generate_resource_pack(resource_dirs, resource_file_name):
    resource_pack = {}

    for resource_dir in resource_dirs:
        for dirpath, dirnames, files in os.walk(resource_dir):
            for file in files:
                filepath = f"{dirpath}/{file}"
                resource_pack[filepath] = generate_encoded_resource(filepath)

    resource_pack[WORLD_DATA_PATH] = generate_encoded_resource(WORLD_DATA_PATH)
    resource_pack[RESOURCE_CONFIG_FILE] = generate_encoded_resource(RESOURCE_CONFIG_FILE)

    write_resource_file_to_disk(resource_file_name, resource_pack)


def write_resource_file_to_disk(resource_file_name, resource_file):
     with open(resource_file_name, 'wb') as save_file:
        encoded_resource_file = encode_resource_file_object_to_base64_bytes(resource_file)
        # compressed_resource_file = zlib.compress(encoded_resource_file)
        save_file.write(encoded_resource_file)


def generate_encoded_resource(filepath):
    with open(filepath, "rb") as file_data:
    
        data = file_data.read()
        encoded_data = encode_resource_data_to_base64_string(data)
        return encoded_data

def generate_decoded_resource(resource_pack_object, key):
    return base64.b64decode(resource_pack_object[key])


def encode_resource_data_to_base64_string(resource_data):
    encoded_data = base64.b64encode(resource_data).decode("ascii")
    return encoded_data


def encode_resource_file_object_to_base64_bytes(resource_file):
     resource_file_as_string = json.dumps(resource_file)
     compressed_resource_file_string = zlib.compress(resource_file_as_string.encode())
     return base64.b64encode(compressed_resource_file_string)

def decode_resource_file_to_object(resource_file):
    # decompressed_resource_file = zlib.decompress(resource_file.read())
    resource_pack_decoded = base64.b64decode(resource_file.read())
    resource_pack_decompressed_as_string = zlib.decompress(resource_pack_decoded)
    resource_pack_object = json.loads(resource_pack_decompressed_as_string)
    return resource_pack_object


