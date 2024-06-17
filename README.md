# Flowchart Editor

This project, flowchart editor, aims to convert an image of flowchart into a slide (powerpoint) format. With this product, when people saw a flowchart, they don't need to rewrite the flowchart from scratch, 
but use this to facilitate the process. Flowchart editor not only captures the flow of every block but also identify the feature of each block. e.g., the shpae, color, etc.

## work flow 

<img width="216" alt="image" src="https://github.com/ryanrwei/nvidia_ai_agent_contest_flowchart_editor/assets/55873378/9657bbd9-264c-4b82-abeb-022628862c58">

## Demo Video: https://www.youtube.com/watch?v=W_8QV3NMXmA

## How to run 

### First, enter you API key in flowchart_editor.py:
- <font color=#808080> os.environ["NVIDIA_API_KEY"] = "your nvidia key" </font>

### Secondly, execute flowchart editor and input your image path:
- python3 flowchart_editor.py

### requirement:
- python-pptx
- langchain
- FlagEmbedding
