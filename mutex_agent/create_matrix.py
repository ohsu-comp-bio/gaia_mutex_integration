from . import MR_pb2
import google.protobuf.json_format
import requests

def get_matrix_from_gaia(endpoint):
    if not endpoint.startswith("http"):
        endpoint = "http://" + endpoint

    if endpoint.endswith("/"):
        endpoint = endpoint[:-1]

    r = requests.get(endpoint)

    if r.status_code // 100 != 2:
        raise RuntimeError(
            "[STATUS CODE - {0}] Failed to acquire matrix from gaia: {1}".format(
                r.status_code, r.text
            )
        )
    return r.text

#i.e. r.text from above = mrm_json
def convert_matrix_to_pb(mrm_json):
    mrm = google.protobuf.json_format.Parse(mrm_json,MR_pb2.Matrix())
    return mrm

def build_matrix_outfile(file_location, mrm_pbo):
    m_outfh = open(file_location,"w")
    m_outfh.write(str('\t'.join(mrm_pbo.header)+'\n'))

    for row in mrm_pbo.rows:
        row = "{}\t{}{}".format(row.label, '\t'.join([str(i) for i in row.values]), '\n')
        m_outfh.write(row)

    m_outfh.close()