import requests
from matplotlib.font_manager import FontProperties


def http_request(url, method='GET', data=None):
    """
    发送 HTTP 请求并返回响应数据。

    :param url: 目标 URL
    :param method: 请求方法，默认为 'GET'
    :param data: POST 请求时的数据，默认为 None
    :return: 服务器返回的数据
    """
    try:
        if method.lower() == 'get':
            response = requests.get(url)
        elif method.lower() == 'post':
            response = requests.post(url, data=data)
        else:
            raise ValueError("Unsupported HTTP method")

        response.raise_for_status()  # 检查请求是否成功
        return response.text  # 返回文本形式的响应内容
    except requests.RequestException as e:
        print(f"请求错误: {e}")
        return None

# 定义一个支持中文的字体
chinese_font = FontProperties(fname='C:/Windows/Fonts/simhei.ttf') # 对应你系统的字体路径