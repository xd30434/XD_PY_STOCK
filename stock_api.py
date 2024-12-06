from common import http_request
from config_base import license_code

url_prefix = 'http://v.mairui.club/'

def get_stock_hs_list():
    """
    获取沪深两市股票列表
    :return: 沪深两市股票列表
    """
    url = url_prefix + 'hslt/list/' + license_code

    return http_request(url, 'get')

def get_stock_company_introduction(stock_code):
    """
    获取股票公司简介
    :return: 股票公司简介信息
    """
    url = url_prefix + 'hscp/gsjj/' + stock_code + '/' +license_code

    return http_request(url, 'get')

def get_stock_fsjj_info(stock_code, time_level, start_time, end_time):
    """
    自选时段历史分时交易
    :return: 分时交易信息
    """
    url = url_prefix + 'hszbc/fsjy/' + stock_code + '/' + time_level + '/' + start_time + '/' + end_time + '/' + license_code

    return http_request(url, 'get')