#!/usr/bin/env python3

#Not yet finished (obvi)

import subprocess

def test_mrm_maker():
    print("Testing MRM_Maker.py")
    subprocess.run(["python3", "../src/MRM_Maker.py", "-inparam", "pretest/parameters.txt", "-inmat", "pretest/DataMatrix.txt", "-outf", "testout_MRM.json"])


    def test_mrm():
        if os.path.isfile("testout_MRM.json"):
            print("Mutex run message successfully created")
            mrm = open("testout_MRM.json","r").readlines()
            #close it. might have to change to old school format
            if len(mrm) == 1:
                print("Mutex run message is correct length (1line)")
                #contains
                #parameters and matrix
                #values, headers, etc.
            else:
                print("Mutex run message is wrong length")
                print("{}{}{}".format("Expected length: 1 line. Actual length: ", len(myfilelisty), " lines."))

        else:
            print("Error: Failed to generate mutex run message")

    test_mrm()
    print("MRM_Maker.py looks good")

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
    subprocess.run(["python3", "../src/ranked_groups_converter.py", "-rg", "sample-input/ranked-groups.txt", "-outfile", "ranked-groups.json"])

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