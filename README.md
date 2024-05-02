# Deep-Learning-Project
UI Evaluation of Mobile Application Screens

# Code Setup
1. Download semantic annotations and image files
    - https://storage.cloud.google.com/crowdstf-rico-uiuc-4540/rico_dataset_v0.1/semantic_annotations.zip
    - https://storage.googleapis.com/crowdstf-rico-uiuc-4540/rico_dataset_v0.1/unique_uis.tar.gz 

2. Extract files from the downloaded files and move the `combined` and `semantic_annotations` folder to the project root
3. Run the `MakeDataset.ipynb` file

The Data Sample Includes:
1. Screenshot images, in JPG format
2. Semantic wireframe images
3. Semantic annotations, in JSON format, with all the UI components, text buttons, and icons encoded in the wireframes.
4. View hierarchies, or DOM-like tree structure, in JSON format.
5. App metadata, in JSON format. Scrapped from Google Play as of August 2020. 


