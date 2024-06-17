# Flowchart Editor

This project, Flowchart Editor, aims to transform an image of a flowchart into a slide (PowerPoint) format seamlessly. With this tool, users can avoid the tedious task of redrawing flowcharts from scratch by simply uploading an image of the flowchart. Flowchart Editor not only captures the structure of each block but also identifies specific features such as shape, color, and text.

## Features
- Automatic Flowchart Recognition: Easily convert flowchart images to editable PowerPoint slides.
- Detail Preservation: Maintains the original shapes, colors, and text from the image.
- Editable Output: The generated PowerPoint slides are fully editable, allowing further customization.
- User-Friendly Interface: Simple and intuitive interface for easy navigation and operation.


## Workflow 
- Upload Flowchart Image:
Upload the image of the flowchart that you wish to convert.

- Flowchart Analysis:
The editor analyzes the flowchart, identifying and preserving the structure and features.

- Generate Editable Slide:
The tool generates an editable PowerPoint slide, retaining the original details.

<img width="216" alt="image" src="https://github.com/ryanrwei/nvidia_ai_agent_contest_flowchart_editor/assets/55873378/9657bbd9-264c-4b82-abeb-022628862c58">

## Demo Video: https://www.youtube.com/watch?v=W_8QV3NMXmA

## How to run 

### First, enter you API key in flowchart_editor.py:
<pre style="background-color: #f0f0f0; padding: 10px;">
os.environ["NVIDIA_API_KEY"] = "your nvidia key"
</pre>

### Secondly, execute flowchart editor and input your image path:
<pre style="background-color: #f0f0f0; padding: 10px;">
python3 flowchart_editor.py
</pre>

### Requirements (using poetry):
- Python==3.10.8
- Poetry==1.8.3
- python-pptx==0.6.23     
- langchain==0.2.3  
- FlagEmbedding=1.2.10
