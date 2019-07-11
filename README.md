# UiPath Workflows to Libs
## Inspiration
One of the best features we had in the latest version of UiPath was the ability to create customized libraries. Prior to this, we were using reusable components by invoking workflow files. 

Once we created our libraries, we had to update the existing code of all the robots to ensure that they were using our brand new and shiny libraries - and we didn't want to do this manually!

## What it does

We convert workflows calls to library calls.

### Before
```xml
<ui:InvokeWorkflowFile ContinueOnError="{x:Null}" sap2010:Annotation.AnnotationText="Precondition: ME52N Transacion visible.&#xA;&#xA;Actions:&#xA;1.Converting JSON to DataTable to obtain the whole data from the PR - coming from reports&#xA;&#xA;" DisplayName="Deserialize object from Queue" sap2010:WorkflowViewState.IdRef="InvokeWorkflowFile_3" UnSafe="False" WorkflowFileName="[assetUiPathLibraryPath+&quot;DeserializeObjectDataTable.xaml&quot;]">
  <ui:InvokeWorkflowFile.Arguments>
    <InArgument x:TypeArguments="x:String" x:Key="argJSONComing">[argTransactionItem.SpecificContent("DtPR").ToString]</InArgument>
    <OutArgument x:TypeArguments="sd:DataTable" x:Key="argObjectOutput">[DtPRLines]</OutArgument>
  </ui:InvokeWorkflowFile.Arguments>
</ui:InvokeWorkflowFile>
```

### After
```xml
<uilib:DeserializeObjectDataTable argJSONComing="[argTransactionItem.SpecificContent(&quot;DtPR&quot;).ToString]" argObjectOutput="[DtPRLines]"/>
```

## How we built it
We developed a Python script that reads the XML DOM of `.xaml` files and process it converting workflow calls to library calls. First, we find out which are the namespaces of the current workflow files along with their input and output arguments. Then, we replace the workflow call with the library call adding those arguments. Finally, the input `.xaml` is overwritten with the new XML DOM structure.

In our case, we had three different libraries to interact with different systems. UiPath, SAP and ServiceNow. However, this script can be easily extended with your own libraries.

## Video demo
[![UiPath Worfklows to Libs Video Demo](https://img.youtube.com/vi/hcV-x6a_1xw/0.jpg)](https://www.youtube.com/watch?v=hcV-x6a_1xw "UiPath Worfklows to Libs Video Demo")
## How to use it
### Requirements
- Python 3
### How to run it
Replace `PATH_TO_DIRECTORY_WITH_XAML_FILES` with your directory path where `.xaml` files are localised.
```bash
python replace_workflow_for_lib_calls.py -d PATH_TO_DIRECTORY_WITH_XAML_FILES
```
