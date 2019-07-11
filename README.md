# UiPath Workflows to Libs
## Inspiration
One of the best features we had in the latest version of UiPath was the ability to create customized libraries. Prior to this, we were using reusable components by invoking workflow files. 

Once we created our libraries, we had to update the existing code of all the robots to ensure that they were using our brand new and shiny libraries - and we didn't want to do this manually!

## What it does

We convert workflows calls to library calls.

## How we built it
We developed a Python script that reads the XML DOM of `.xaml` files and process it converting workflow calls to library calls. First, we find out which are the namespaces of the current workflow files along with their input and output arguments. Then, we replace the workflow call with the library call adding those arguments. Finally, the input `.xaml` is overwritten with the new XML DOM structure.

By default, it supports UiPath, SAP and ServiceNow libraries and namespaces. 
This script can be easily extended with your own libraries.  

## Video demo

## How to use it
### Requirements
- Python 3
### How to run it
Replace `PATH_TO_DIRECTORY_WITH_XAML_FILES` with your directory path where `.xaml` files are localised.
```bash
python replace_workflow_for_lib_calls.py -d PATH_TO_DIRECTORY_WITH_XAML_FILES
```
