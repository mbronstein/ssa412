import sys
import getopt
import csv
from os.path import dirname
import simplejson

def csvtofixture(input_file, model_name):
    """
    params:
    input_file_name
    output_model_name
    """

    in_file = dirname(__file__) + input_file
    out_file = dirname(__file__) + model_name + ".json"

    print("Converting %s from CSV to JSON as %s" % (input_file, model_name))

    f = open(input_file, 'r' )
    fo = open(out_file, 'w')

    reader = csv.reader( f )

    header_row = []
    entries = []
    for row in reader:
        if not header_row:
            header_row = row
            continue

        pk = row[0]
        model = model_name
        fields = {}
        for i in range(len(row)-1):
            active_field = row[i+1]
            if active_field.isdigit():
                try:
                    new_number = int(active_field)
                except ValueError:
                    new_number = float(active_field)
                fields[header_row[i+1]] = new_number
            else:
                fields[header_row[i+1]] = active_field.strip()

        row_dict = {}
        row_dict["pk"] = int(pk)
        row_dict["model"] = model_name

        row_dict["fields"] = fields
        entries.append(row_dict)

    fo.write("%s" % simplejson.dumps(entries, indent=4))
    f.close()
    fo.close()

