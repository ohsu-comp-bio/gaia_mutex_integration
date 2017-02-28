#!/usr/bin/env python3

#Not yet finished (obvi)

import subprocess
import os
import MR_pb2
import AlterationGroupSchema_pb2
import google.protobuf.json_format


def test_mrm_maker():
    print("Testing MRM_Maker.py")
    subprocess.run(["python3", "../src/MRM_Maker.py", "-inparam", "pretest/parameters.txt",
                    "-inmat", "pretest/DataMatllrix.txt", "-outf", "testout_MRM.json"])

    def mrm_file_exists():
        if os.path.isfile("testout_MRM.json"):
            print("Mutex run message successfully created")
            return True
        else:
            print("Error: Failed to generate mutex run message")
            return False

    def open_mrm_file():
        mrm = open("testout_MRM.json", "r")
        mrmlist = mrm.readlines()
        mrm.close()
        return mrmlist

    def mrm_file_is_right_length(mrmlist):
        if len(mrmlist) == 1:
            print("Mutex run message is correct length (1 line)")
            return True
        else:
            print("Mutex run message is incorrect length")
            print("{}{}{}".format("Expected length: 1 line. Actual length: ", len(mrmlist), " lines."))
            return False

    def mrm_has_matrix_info(mrm_pbo):

        def check_header(mrm_pbo):
            if len(mrm_pbo.matrix.header) > 0:
                print("MRM matrix has header")
                if mrm_pbo.matrix.header[0] != '':
                    print("Header lacks initial blank space. Column titles may be offset.")

                header_comment = "Column titles exist"
                for i in mrm_protobuf_object.matrix.header[1:]:
                    if len(i) == 0:
                        header_comment = "Error: At least one column title (sample) is of length 0."
                print(header_comment)

            else:
                print("MRM matrix lacks header")

        def check_rows(mrm_pbo):
            if len(mrm_pbo.matrix.rows) > 0:
                print("MRM matrix has rows")
                labellist = []
                valuelist = []
                for i in mrm_pbo.rows:
                    labellist.append(i.label)
                    valuelist.append(i.values)
                if len()

            else:
                print("MRM matrix does not have rows")



        def check_labels(mrmlist):
            if "label" in mrmlist:
                print("MRM matrix rows have labels")
            else:
                print("MRM lacks matrix labels")

        def check_values(mrmlist):
            if "values" in mrmlist:
                print("MRM matrix rows have values")
            else:
                print("MRM lacks matrix values")

        def matrix_values_are_integers(mrmlist):

        def all_matrix_rows_have_labels():

        def matrix_header_right_format():

        #commands for just matrix having right info
        check_header(mrm_pbo)
        check_rows(mrm_pbo)
        check_labels(mrm_pbo)
        check_values(mrm_pbo)

    #OVERARCHING MRM MATRIX COMMANDS
    if mrm_file_exists():
        mrmlist = open_mrm_file()
        if mrm_file_is_right_length(mrmlist):
            mrmlist = mrmlist[0]
            mrm_protobuf_object = google.protobuf.json_format.Parse(mrmlist[0], MR_pb2.MutexRun())
            mrm_has_matrix_info(mrm_protobuf_object)

    def mrm_has_parameters_info():

        def parameters_correct_format():





    if mrm_file_exists():
        mrm_rdlines = open_mrm_file()
        mrm_file_is_right_length(mrm_rdlines)
        mrm_has_matrix_info(mrm_rdlines)
        mrm_has_parameters_info(mrm_rdlines)

    if mrm_file_exists() & mrm_file_is_right_length() & mrm_has_matrix_info() & mrm_has_parameters_info():
        print("MRM_Maker.py looks good")
    else:
        print("There were one or more errors with the mutex run message")
        #and exit?

















def test_mrm_conv():
    print("Testing MRM_Converter.py")
    print("This may take a few minutes as it invokes Mutex")
    subprocess.run(["python3", "../src/MRM_Converter.py", "-mrm", "testout_MRM.json"])

    def test_dm():
        if os.path.isfile("sample-input/DataMatrix.txt"):
            print("DataMatrix.txt successfully created")
        else:
            print("Error: Failed to generate DataMatrix.txt")

    def test_param():
        if os.path.isfile("sample-input/parameters.txt"):
            print("parameters.txt successfully created")
            #   parameters.txt
            #       has equal signs on every line
            #       contains necessary pointers
        else:
            print("Error: Failed to generate parameters.txt")

    def test_rg():
        if os.path.isfile("sample-input/ranked-groups.txt"):
            print("ranked-groups.txt successfully created")
        else:
            print("Error: Failed to generate ranked-groups.txt")

    test_dm()
    test_param()
    test_rg()

    #if no issues, print this; otherwise print something sad.
    print("MRM_Converter.py looks good")

def test_rg_conv():
    print("Testing ranked_groups_converter.py")
    subprocess.run(["python3", "../src/ranked_groups_converter.py", "-rg", "sample-input/ranked-groups.txt",
                    "-outfile", "ranked-groups.json"])

    def test_rg_json():
        if os.path.isfile("ranked-groups.json"):
            print("JSON message for ranked-groups successfully created")
        else:
            print("Failed to convert ranked-groups.txt to JSON")

    test_rg_json()
    print("ranked_groups_converter.py looks good")

if __name__ == '__main__':
    test_mrm_maker()
    test_mrm_conv()
    test_rg_conv()

# write code to clean up after itself (maybe prompt the user to proceed with this step?)