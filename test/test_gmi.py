#!/usr/bin/env python3

#Not yet finished!

import subprocess
import os
import sys
src_path = os.path.abspath(os.path.join('..', 'src'))
sys.path.append(src_path)
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
            print("Error: Mutex run message is incorrect length")
            print("{}{}{}".format("Expected length: 1 line. Actual length: ", len(mrmlist), " lines."))
            return False

    def mrm_has_matrix_info(mrm_pbo):

        def check_header(mrm_pbo):
            if len(mrm_pbo.matrix.header) > 0:
                print("MRM matrix has header")
                passed_test = True

                if mrm_pbo.matrix.header[0] != '':
                    print("Error: Header lacks initial blank space. Column titles may be offset.")
                    passed_test = False
                header_comment = "Column titles exist"

                for i in mrm_pbo.matrix.header[1:]:
                    if len(i) == 0:
                        header_comment = "Error: At least one column title (sample) is of length 0."
                        passed_test = False
                print(header_comment)

            else:
                print("Error: MRM matrix lacks header")
                passed_test = False

            return passed_test

        def check_rows(mrm_pbo):
            if len(mrm_pbo.matrix.rows) > 0:
                print("MRM matrix has rows")
                passed_test = True
            else:
                print("Error: MRM matrix does not have rows")
                passed_test = False

            return passed_test

        def check_row_labels(mrm_pbo):

            count = 0
            unlabeled_count = 0

            for i in mrm_pbo.matrix.rows:
                if len(i.label) == 0:
                    unlabeled_count += 1
                count += 1
            if count > 0 and unlabeled_count == 0:
                print("All MRM matrix rows have labels")
                passed_test = True
            elif count > 0 and unlabeled_count > 0:
                print("Error", unlabeled_count, "out of", count, "rows lack labels")
                passed_test = False
            elif count == 0:
                print("Error: Failed to iterate through matrix rows")
                passed_test = False

            return passed_test

        def check_row_values(mrm_pbo):

            count = 0
            non_integers_count = 0

            for i in mrm_pbo.matrix.rows:
                for value in i.values:
                    if type(value) != int:
                        non_integers_count += 1
                    count += 1

            if count > 0 and non_integers_count == 0:
                print("All MRM matrix values are integers")
                passed_test = True
            elif count > 0 and non_integers_count > 0:
                print("Error:", non_integers_count, "MRM matrix values are not integer type")
                passed_test = False
            elif count == 0:
                print("Error: Failed to iterate through MRM matrix values")
                passed_test = False

        #commands for just matrix having right info
        header_looks_good = check_header(mrm_pbo)
        rows_look_good = check_rows(mrm_pbo)
        labels_look_good = check_row_labels(mrm_pbo)
        values_look_good = check_row_values(mrm_pbo)

        if header_looks_good & rows_look_good & labels_look_good & values_look_good:
            return True
        else:
            return False

    def mrm_has_parameters_info(mrm_pbo):

        count = 0
        nonstring_count = 0
        key_contains_equal_sign = 0
        value_contains_equal_sign = 0

        for key in mrm_pbo.parameters:
            if type(key) or type(mrm_pbo.parameters[key]) != str:
                nonstring_count += 1
            count += 1
            if "=" in key:
                key_contains_equal_sign += 1
            if "=" in mrm_pbo.parameters[key]:
                value_contains_equal_sign += 1

        if count > 0 and nonstring_count == 0:
            print("All MRM parameters key and value objects are strings")
            passed_test = True
            if key_contains_equal_sign or value_contains_equal_sign > 0:
                print("Error: MRM parameters message incorporated '=' instead of key or value")
                print(key_contains_equal_sign, "'=' error(s) out of", count, "parameters keys")
                print(value_contains_equal_sign, "'=' error(s) out of", count, "parameters values")
                passed_test = False

        elif count > 0 and nonstring_count > 0:
            print("Error:", nonstring_count, "MRM parameters key-value pairs contain non-strings")
            passed_test = False

        elif count == 0:
            print("Error: Failed to iterate through MRM parameters key-value pairs")
            passed_test = False

        return passed_test

    if mrm_file_exists():
        mrmfe = True
        mrmlist = open_mrm_file()
        if mrm_file_is_right_length(mrmlist):
            mrmfrl = True
            mrmlist = mrmlist[0]
            mrm_protobuf_object = google.protobuf.json_format.Parse(mrmlist[0], MR_pb2.MutexRun())

            matrix_looks_good = mrm_has_matrix_info(mrm_protobuf_object)
            parameters_look_good = mrm_has_parameters_info(mrm_protobuf_object)

    if mrmfe & mrmfrl & matrix_looks_good & parameters_look_good:
        print("No errors were detected in the mutex run message generated by MRM_Maker.py")
    else:
        print("There were one or more errors in the mutex run message generated by MRM_Maker.py")

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

    # if no issues, print this; otherwise print something sad.
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

'''
def cleanup():
    while True:
        try:
            x = str(input("Would you like me to clean up this mess? [y/n]"))
            break
        except ValueError:
            print("Try entering y or n")
'''

















