import base64
import json
import os
import re
from slides_maker import creating_slides
from langchain_openai import ChatOpenAI
from getpass import getpass
import os
from langchain_nvidia_ai_endpoints import ChatNVIDIA
import base64
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.messages import SystemMessage

'''key setting'''
os.environ["NVIDIA_API_KEY"] = "your nvidia key"
if not os.environ.get("NVIDIA_API_KEY", "").startswith("nvapi-"):
    nvapi_key = getpass.getpass("Enter your NVIDIA API key: ")
    assert nvapi_key.startswith("nvapi-"), f"{nvapi_key[:5]}... is not a valid key"
    os.environ["NVIDIA_API_KEY"] = nvapi_key

os.environ["OPENAI_API_KEY"] = "your openai key"

def image_object_detection(image_b64):

    ### ------------------------------- flowchart object detection: input: image, description, output: block info of flowchart -------------------------------
    llm = ChatOpenAI(model="gpt-4o",
                    temperature=1,
                    max_retries=2,
                )
    
    ''' prompt setting '''
    prompt = [
            SystemMessage(
                content=("You're good at doing Image Segmentation, and strictly follow the user's instruction")
            ),
            HumanMessage(content=[
                {
                "type": "text", 
                "text": f"You will be provided with a flowchart and its desription. Your task is to perform detailed image segmentation on the given flowchart and desription and respond with detailed information, following these guidelines:\
                        1. Must utilize that information from the flowchart and desription to help answer the questions.\
                        2. For each block in the flowchart, specify its position by providing the coordinates of the block's center (in pixels), assuming the top-left corner of the image is (0, 0).\
                        3. For each block in the flowchart, identify its width and length (in pixels), and provide details about each block, including its text content, font family, font size, text color (in RGB format), block fill color (in RGB format), and block shape, related with its function, (e.g., rectangle, diamond, oval, start, process, decision, end).\
                        4. Describe the connections between blocks (e.g., the starting/ending block), the shape (e.g., arrows or lines), color and their positions (in pixels).\
                        5. Ensure that you do not miss any information or elements present in the image or flowchart. \
                        6. Pay special attention to blocks that have the same information (e.g., shape, content, etc.), and report on each instance of such blocks separately.\
                        The information from your response will be used to create a PowerPoint slide (.pptx), so ensure that the details you provide (e.g., font families, sizes, colors) are compatible with slide formatting conventions.\
                        "
                },
                {
                "type": "image_url", 
                "image_url": {"url": f"data:image/png;base64,{image_b64}"}
                },
                {
                    "type": "text", 
                    "text": r'''Please response as the following format, which is JSON format:\
                        {
                            "flowchart_title": list( str(the_flowchart_title) ),
                            "blocks":
                                list(
                                    {
                                        "text content": list( str(the_content_in_block) ), 
                                        "font size": list( str(the_font_size) ),  #(in pixels)
                                        "text color": list( str(R), str(B), str(G) ), #(in RGBColor format)
                                        "block color": list( str(R), str(B), str(G) ), #(in RGBColor format)
                                        "Block center coordinates": list( str(x-coordinate), str(y-coordinate) ), #(in pixels)
                                        "block size" list( str(block_width), str(block_length) ), #(in pixels)
                                        "block description": list( str(describe what shape the block is and what its function in the flowchart))
                                    },
                                ),
                            "arrows":
                                list(
                                    {
                                        "starting block": list( str(text_content_of_starting_block) ),
                                        "ending block": list( str(text_content_of_ending_block) ),
                                        "start position": list( str(x-coordinate_of_the_arrow's_starting_point), str(y-coordinate_of_the_arrow's_starting_point) ),  #(in pixels)
                                        "end position": list( str(x-coordinate_of_the_arrow's_ending_point), str(y-coordinate_of_the_arrow's_ending_point) ),  #(in pixels)
                                        "color": list( str(R), str(B), str(G) ), # (in RGBColor format)
                                        "type": list( str(the_type_of_arrow) ), # e.g., solid, dash or others
                                        "arrow boolean": list( str(the text neighbor to the arrow from starting block to ending block. the text MUST be "Yes"/"No", and if there is no text, respense "None") ), # # e.g., you're only allowed answer "Yes", "No", or "None"
                                    },                           
                                ),                                
                        }
                        '''
                },
            ]
            ),
        ]

    chain = llm | StrOutputParser()
    flowchart_block_info = chain.invoke(prompt)

    print()
    print("-" * 30)
    print()
    print(f"flowchart_block_info: {flowchart_block_info}")
    print()
    print("-" * 30)
    print()

    ### ------------------------------- formatter: input: info, output: JSON info -------------------------------
    
    ''' define model'''
    llm = ChatNVIDIA(model="meta/llama3-70b-instruct", 
                    temperature = 1,
                    top_p = 0.7,
                    )

    ''' prompt setting '''
    prompt = [
            SystemMessage(
                content=(f"{flowchart_block_info}, please turn this input into the following format. i.e., JSON format")
            ),
            HumanMessage(content=[
                {
                    "type": "text", 
                    "text": r'''Here is the JSON format requirement:\
                        {
                        "flowchart_title": list( str(the_flowchart_title) ),
                        "blocks":
                            list(
                                {
                                    "text content": list( str(the_content_in_block) ), 
                                    "font size": list( str(the_font_size) ),  
                                    "text color": list( str(R), str(B), str(G) ), 
                                    "block color": list( str(R), str(B), str(G) ), 
                                    "Block center coordinates": list( str(x-coordinate), str(y-coordinate) ), 
                                    "block size" list( str(block_width), str(block_length) ),
                                    "block description": list( str(describe what shape the block is and what its function in the flowchart))
                                },
                            ),
                        "arrows":
                            list(
                                {
                                    "starting block": list( str(text_content_of_starting_block) ),
                                    "ending block": list( str(text_content_of_ending_block) ),
                                    "start position": list( str(x-coordinate_of_the_arrow's_starting_point), str(y-coordinate_of_the_arrow's_starting_point) ),  
                                    "end position": list( str(x-coordinate_of_the_arrow's_ending_point), str(y-coordinate_of_the_arrow's_ending_point) ),  
                                    "color": list( str(R), str(B), str(G) ), 
                                    "type": list( str(the_type_of_arrow) ), 
                                    "arrow boolean": list( str(the text neighbor to the arrow from starting block to ending block. the text MUST be "Yes"/"No", and if there is no text, respense "None") ),
                                },                           
                            ),
                        }
                    '''
                }
            ]
            ),
        ]

    chain = llm | StrOutputParser()
    draft_info = chain.invoke(prompt)

    print()
    print("-" * 30)
    print()
    print(f"draft_info: {draft_info}")
    print()
    print("-" * 30)
    print()

    pattern = re.compile(r'```(.*?)```', re.DOTALL)
    draft_info = pattern.findall(draft_info)[0]

    print()
    print("-" * 30)
    print()
    print(f"draft_info2: {draft_info}")
    print()
    print("-" * 30)
    print()


    JSON_info = json.loads(draft_info)

    print()
    print("-" * 30)
    print()
    print(f"JSON_info: {JSON_info}")
    print()
    print("-" * 30)
    print()
    return JSON_info


if __name__ == '__main__':
    
    def encode_image(image_path: str) -> str:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    image_path = input("enter the image path:  ")
    image_b64 = encode_image(f"{image_path}")

    ### ------------------------------- object detection -------------------------------
    JSON_info = image_object_detection(image_b64)


    ### ------------------------------- save & load model output -------------------------------
    ''' save temp model output '''
    save_file = open("where you save model output", "w")  
    json.dump(JSON_info, save_file, indent = 4)  
    save_file.close()
    print()
    print("-" * 30)
    print()
    print(f"JSON_info: {JSON_info}")
    print()
    print("-" * 30)
    print()

    ''' load model output '''
    # json_file_path = '/workspaces/gstudio/src/studio_lite/my_test/data_model_output.json'
    # with open(json_file_path, 'r') as file:
    #     JSON_info = json.load(file)
    # print()
    # print("-"*30)
    # print()
    # print(f"load model output:")
    # print(f"{JSON_info}")
    # print()
    # print("-"*30)
    # print()


    ### ------------------------------- convert model output into slides -------------------------------
    creating_slides(JSON_info, resize_block = False)



