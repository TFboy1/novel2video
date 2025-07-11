import logging
import requests
import threading
from openai import OpenAI

client = OpenAI(
    api_key="fa957ca47ee74037874b03af14c5e3b4.wCJpHP08pS6XlY34",
    base_url="https://open.bigmodel.cn/api/paas/v4/"
)


def query_silicon_flow(input_text, sys_text,t):
    """
    获取模型生成的响应

    参数:
    prompt (str): 输入的提示文本

    返回:
    str: 模型生成的文本内容
    """
    messages=[]
    if sys_text:
        messages.append({"role": "system", "content": sys_text})
    messages.append({"role": "user", "content": input_text})
    try:
        response = client.chat.completions.create(
            model="GLM-4V-Flash",
            messages=messages,
            temperature=t,
            max_tokens=2048
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"



from backend.util.file import get_config

# List of models
silicon_flow_free_models = [
    "Qwen/Qwen2-7B-Instruct",
    "Qwen/Qwen2.5-7B-Instruct",
    "THUDM/glm-4-9b-chat",
    "01-ai/Yi-1.5-9B-Chat-16K",
    "internlm/internlm2_5-7b-chat",
    #"google/gemma-2-9b-it",
    #"meta-llama/Meta-Llama-3-8B-Instruct",
    #"meta-llama/Meta-Llama-3.1-8B-Instruct",
]

model_index = 0
model_index_lock = threading.Lock()

def get_next_model():
    global model_index
    with model_index_lock:
        model_index = (model_index + 1) % len(silicon_flow_free_models)
        return silicon_flow_free_models[model_index]
#
# def query_silicon_flow(input_text, sys_text, temperature):
#     url = "https://api.siliconflow.cn/v1/chat/completions"
#     key = get_config()['address2']
#     messages = []
#     if sys_text:
#         messages.append({"role": "system", "content": sys_text})
#     messages.append({"role": "user", "content": input_text})
#
#     sFModel = get_next_model()
#     logging.debug(f"query sfModel {sFModel}")
#     request_body = {
#         "temperature": temperature,
#         "messages": messages,
#         "model": sFModel,
#     }
#
#     headers = {
#         "Accept": "application/json",
#         "Content-Type": "application/json",
#         "Authorization": f"Bearer {key}",
#     }
#
#     response = requests.post(url, headers=headers, json=request_body)
#
#     if response.status_code != 200:
#         raise Exception(f"Unexpected response status: {response.status_code}, modelName {sFModel}")
#
#     response_data = response.json()
#     if 'choices' in response_data and len(response_data['choices']) > 0:
#         logging.debug(f"sfModel {sFModel}, response {response_data['choices'][0]['message']['content']}")
#         return response_data['choices'][0]['message']['content']
#     else:
#         raise Exception("No choices found in response.")
