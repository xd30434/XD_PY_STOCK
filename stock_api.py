import os

from common import http_request, tempfile_path
from config_base import license_code

url_prefix = 'http://api.mairui.club/'

def get_stock_hs_list():
    """
    获取沪深两市股票列表
    :return: 沪深两市股票列表
    """
    filename = 'hs_list.json'
    if tempfile_path is not None:
        if not os.path.exists(tempfile_path):
            os.mkdir(tempfile_path)
        if os.path.exists(tempfile_path + filename):
            return open(tempfile_path + filename, 'r').read()
    url = url_prefix + 'hslt/list/' + license_code
    ret = http_request(url, 'get')
    if ret == None:
        return None
    open(tempfile_path + filename, 'w').write(ret)
    return ret

def get_stock_company_introduction(stock_code):
    """
    获取股票公司简介
    :return: 股票公司简介信息
    """
    filename = 'company_introduction_' + stock_code + '.json'
    if tempfile_path is not None:
        if not os.path.exists(tempfile_path):
            os.mkdir(tempfile_path)
        if os.path.exists(tempfile_path + filename):
            return open(tempfile_path + filename, 'r').read()
    url = url_prefix + 'hscp/gsjj/' + stock_code + '/' +license_code
    ret = http_request(url, 'get')
    if ret == None:
        return None
    open(tempfile_path + filename, 'w').write(ret)
    return ret

def get_stock_fsjj_info(stock_code, time_level, start_time, end_time):
    """
    自选时段历史分时交易
    :return: 分时交易信息
    """
    filename = 'stock_fsjj_' + stock_code + '_' + time_level + '_' + start_time + '_' + end_time + '.json'
    if tempfile_path is not None:
        if not os.path.exists(tempfile_path):
            os.mkdir(tempfile_path)
        if os.path.exists(tempfile_path + filename):
            return open(tempfile_path + filename, 'r').read()

    url = url_prefix + 'hszbc/fsjy/' + stock_code + '/' + time_level + '/' + start_time + '/' + end_time + '/' + license_code

    ret = http_request(url, 'get')
    if ret == None:
        return None
    open(tempfile_path + filename, 'w').write(ret)
    return ret

def get_stock_hszg_list():
    """
    接口说明：获取指数、行业、概念（包括基金，债券，美股，外汇，期货，黄金等的代码），
    其中isleaf为1（叶子节点）的记录的code（代码）可以作为下方接口的参数传入，
    从而得到某个指数、行业、概念下的相关股票。
    :return: 指数、行业、概念信息
    """
    filename = 'hszg_list.json'
    if tempfile_path is not None:
        if not os.path.exists(tempfile_path):
            os.mkdir(tempfile_path)
        if os.path.exists(tempfile_path + filename):
            return open(tempfile_path + filename, 'r').read()

    url = url_prefix + 'hszg/list/' + license_code
    ret = http_request(url, 'get')
    if ret == None:
        return None
    open(tempfile_path + filename, 'w').write(ret)
    return ret

def get_stock_hszg_gg(hszg_code):
    """
    根据“指数、行业、概念树”接口得到的代码作为参数，得到相关的股票。
    :return: 指数、行业、概念相关的股票
    """
    filename = 'hszg_gg_' + hszg_code + '.json'
    if tempfile_path is not None:
        if not os.path.exists(tempfile_path):
            os.mkdir(tempfile_path)
        if os.path.exists(tempfile_path + filename):
            return open(tempfile_path + filename, 'r').read()

    url = url_prefix + 'hszg/gg/' + hszg_code + '/' + license_code
    ret = http_request(url, 'get')
    if ret == None:
        return None
    open(tempfile_path + filename, 'w').write(ret)
    return ret