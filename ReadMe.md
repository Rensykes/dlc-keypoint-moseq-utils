# Installation Instructions

The scope of this repository is to provide utilities to have a complete DeepLabCut + Keypoint-MoSeq workflow.

## First Time Usage
- Clone the repository and move into it
- [Create a virtual environment](#create-a-virtual-environment)
- [Activate the virtual environment](#activate-the-virtual-environment)
- [Install dependencies](#install-dependencies)

## Next Usages
- Move to the repository
- [Activate the virtual environment](#activate-the-virtual-environment)
- Do your work
- [Deactivate](#deactivate)

## How to use h5 Converter

Assuming you used DeepLabCut's ModelZoo TopViewMouse model to label your videos, you might want to adjust the h5 files and export them as CSV for faster analysis and manipulation. 

First of all, add to the repository's root directory your Keypoint-MoSeq config.yaml file.

The main goal of h5 Converter is to:
- Rename some bodyparts to fit your config.yaml.
  - In the h5_converter.py file, update the bodyparts_to_rename list, adding new tuples where the first item of the tuple is the name of the bodypart in the h5 file and the second item of the tuple is the new name that you want to give to that bodypart.
    - For example ('neck', 'spine1') will rename the neck bodypart into spine1.
- Delete bodyparts from the h5 that do not belong to the ones explicited in your conifg.yaml file bodyparts list.
- Reoder the data so that the order of the bodyparts will follow the order of the bodyparts explicited in your conifg.yaml file bodyparts list (this is crucial in order to have a correct trajectory plot).

### Usage Instructions
Given that you must have followed the steps in [First Time Usage](#first-time-usage) and [Next Usages](#next-usages) and that you have added to the repository's root directory your Keypoint-MoSeq config.yaml file, your next step will be to drop the h5 files that you want to manipulate into the h5 folder.
Now you are free to launch the script.

For the time being h5-converter is not included in the fat client but it's still usable as a script by running:

```
python h5_converter.py
```

**IMPORTANT:** the output CSV folder will be emptied everytime you launch the script - *remember to save your converted csv files!*

## Cheatsheet for python, virtual environments and pip
### Create a virtual environment
```
python -m venv dev
```
### Activate the virtual environment

Linux
```
source dev/bin/activate
```
Windows
```
.\dev\Scripts\activate
```
### Deactivate

```
deactivate
```

### Generate Requirements
```
pip freeze > requirements.txt
```

### Install dependencies

```
pip install -r requirements.txt
```