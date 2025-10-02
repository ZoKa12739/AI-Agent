# test_deepseek.py
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()


def test_deepseek_directly():
    """直接测试DeepSeek API"""
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("未找到API密钥")
        return

    url = "https://api.siliconflow.cn/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # 尝试不同的模型
    models = [
        "deepseek-ai/DeepSeek-V3.1-Terminus",
        "deepseek-ai/DeepSeek-R1",
        "deepseek-ai/DeepSeek-V3.1"
    ]

    for model in models:
        print(f"\n测试模型: {model}")

        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": "请回复'测试成功'"}
            ],
            "max_tokens": 10,
            "temperature": 0.1
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            print(f"状态码: {response.status_code}")

            if response.status_code == 200:
                result = response.json()
                print(f"成功: {result}")
                return True
            else:
                print(f"错误: {response.text}")

        except Exception as e:
            print(f"异常: {e}")

    return False


if __name__ == "__main__":
    test_deepseek_directly()