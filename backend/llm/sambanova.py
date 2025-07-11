import logging
import requests
from openai import OpenAI
from backend.util.file import get_config
client = OpenAI(
    api_key="fa957ca47ee74037874b03af14c5e3b4.wCJpHP08pS6XlY34",
    base_url="https://open.bigmodel.cn/api/paas/v4/"
)

def query_samba_nova(input_text, sys_text,t):
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
#
# LLAMA_405B = "Meta-Llama-3.1-405B-Instruct"
#
# def query_samba_nova(input_text: str, sys: str, model_name: str, temperature: float) -> str:
#     model = get_config()['model']
#     try:
#         url = "https://api.sambanova.ai/v1/chat/completions"
#         messages = []
#         if sys:
#             messages.append({"role": "system", "content": sys})
#         messages.append({"role": "user", "content": input_text})
#
#         request_body = {
#             "temperature": temperature,
#             "messages": messages,
#             "model": model,  # Assuming model_name is passed correctly
#         }
#         key = get_config()['apikey']
#         headers = {
#             "Content-Type": "application/json",
#             "Authorization": f"Bearer {key}",
#         }
#         response = requests.post(url, headers=headers, json=request_body)
#         response.raise_for_status()  # Raises an HTTPError for bad responses
#
#         response_data = response.json()
#         if 'choices' in response_data and len(response_data['choices']) > 0:
#             return response_data['choices'][0]['message']['content']
#         else:
#             error_message = f"No choices found in response: {response_data}"
#             logging.error(error_message)
#             raise ValueError(error_message)
#     except requests.exceptions.HTTPError as http_err:
#         error_message = f"HTTP error occurred: {http_err} - Response: {http_err.response.text}"
#         logging.error(error_message)
#         raise
#     except requests.exceptions.ConnectionError as conn_err:
#         error_message = f"Connection error occurred: {conn_err}"
#         logging.error(error_message)
#         raise
#     except requests.exceptions.Timeout as timeout_err:
#         error_message = f"Timeout error occurred: {timeout_err}"
#         logging.error(error_message)
#         raise
#     except requests.exceptions.RequestException as req_err:
#         error_message = f"Request error occurred: {req_err}"
#         logging.error(error_message)
#         raise
