from argparse import ArgumentParser
from xml.dom.minidom import parse
import os
from glob import glob


def run_replace(filepath):
    dom = parse(filepath)
    namespaces = set()
    for wf_node in dom.getElementsByTagName('ui:InvokeWorkflowFile'):
        keys = []
        values = []
        parent = wf_node.parentNode
        full_wf_filename = wf_node.getAttribute('WorkflowFileName')
        wf_file = full_wf_filename[full_wf_filename.find("\"") + 1:full_wf_filename.find(".xaml")].replace(" ", "")
        lib_separator_index = full_wf_filename.find("+")
        if lib_separator_index > -1:
            wf_lib = full_wf_filename[1:lib_separator_index].lower()
            ns = 'unk'
            if 'uipath' in wf_lib:
                ns = 'uilib'
            elif 'sap' in wf_lib:
                ns = 'saplib'
            elif 'servicenow' in wf_lib:
                ns = 'snlib'
            namespaces.add(ns)
            if ns is 'unk':
                continue
        else:
            continue

        arguments_node = wf_node.getElementsByTagName('ui:InvokeWorkflowFile.Arguments')[0]
        for in_out_node in arguments_node.childNodes:
            if in_out_node.nodeType == in_out_node.ELEMENT_NODE and (
                    in_out_node.tagName == 'OutArgument' or in_out_node.tagName == 'InArgument'):
                key = in_out_node.getAttribute('x:Key')
                keys.append(key)
                value = in_out_node.lastChild.data if in_out_node.lastChild is not None else '{x:Null}'
                values.append(value)
        new_element = dom.createElement('{}:{}'.format(ns, wf_file))
        for key, val in zip(keys, values):
            new_element.setAttribute(key, val)
        parent.replaceChild(new_element, wf_node)

    root_node = dom.getElementsByTagName('Activity')[0]
    for ns in namespaces:
        if ns is 'uilib':
            root_node.setAttribute('xmlns:uilib', 'clr-namespace:UiPathLibrary;assembly=UiPathLibrary')
        elif ns is 'saplib':
            root_node.setAttribute('xmlns:saplib', 'clr-namespace:SAP_Library;assembly=SAP_Library')
        elif ns is 'snlib':
            root_node.setAttribute('xmlns:snlib', 'clr-namespace:ServiceNow_Library;assembly=ServiceNow_Library')

    with open(filepath, 'w') as f:
        dom.writexml(f)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-d", "--dir_path", dest="dir_path",
                        help="Root dir where pdf files are located")

    args = parser.parse_args()
    dir_path = args.dir_path

    file_paths = glob(os.path.join(dir_path, '*.xaml'), recursive=True)
    for file_path in file_paths:
        try:
            print('Processing file {}'.format(file_path))
            run_replace(file_path)
        except Exception as e:
            print(e)
            print('Error processing file {}'.format(file_path))
            continue
