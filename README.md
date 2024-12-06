# XD_PY_STOCK
This is a Python project for obtaining and processing stock data!

这是一个股票数据获取、处理的python项目！

# 环境说明
在windows下开发运行

# 2024年度最新整理的免费股票数据接口--沪深A股历史交易数据API接口

口说明：

麦蕊智数的所有接口都是标准的Json格式，使用Get方式即可请求，或者直接在浏览器打开就可以看到返回的数据，下方的API接口Url链接中000001均为股票代码，Url链接结尾的b997d4403688d5e65a，均为请求证书的秘钥，股票代码和证书秘钥可以自行更换，返回的字段说明可以查看API说明文档：https://www.mairui.club/hsdata.html

注意：如果更换股票代码后返回的数据仍为000001的数据的话，自己申请个免费的证书更换一下就好了，麦蕊智数的秘钥申请很简单，不需要注册用户，打开证书申请页面：https://www.mairui.club/getlicence.html

实时交易数据接口

API接口：http://api.mairui.club/hsrl/ssjy/000001/b997d4403688d5e65a

字段说明：fm_五分钟涨跌幅;h_最高价;hs_换手;lb_量比;l_最低价;lt_流通市值;o_开盘价;pe_市盈率;pc_涨跌幅;p_当前价格;sz_总市值;cje_成交额;ud_涨跌额;v_成交量（手）;yc_昨日收盘价;zf_振幅;zs_涨速;sjl_市净率;zdf60_60日涨跌幅;zdfnc_年初至今涨跌幅;t_更新时间

买卖五档盘口数据接口

API接口：http://api.mairui.club/hsrl/mmwp/000001/b997d4403688d5e65a

字段说明：t_更新时间;vc_委差;vb_委比;pb1_买1价;vb1_买1量;pb2_买2价;vb2_买2量;pb3_买3价;vb3_买3量;pb4_买4价;vb4_买4量;pb5_买5价;vb5_买5量;ps1_卖1价;vs1_卖1量;ps2_卖2价;vs2_卖2量;ps3_卖3价;vs3_卖3量;ps4_卖4价;vs4_卖4量;ps5_卖5价;vs5_卖5量

当天逐笔交易数据接口

API接口：http://api.mairui.club/hsrl/zbjy/000001/b997d4403688d5e65a

字段说明：d_数据归属日期;t_时间;v_成交量;p_成交价;ts_交易方向（0：中性盘，1：买入，2：卖出）

当天分时成交数据接口

API接口：http://api.mairui.club/hsrl/fscj/000001/b997d4403688d5e65a

字段说明：d_数据归属日期;t_时间;v_成交量;p_成交价

当天分价成交占比数据接口

API接口：http://api.mairui.club/hsrl/fjcj/000001/b997d4403688d5e65a

字段说明：d_数据归属日期;v_成交量;p_成交价;b_占比

当天逐笔大单交易数据接口

API接口：http://api.mairui.club/hsrl/zbdd/000001/b997d4403688d5e65a

字段说明：d_数据归属日期;t_时间;v_成交量;p_成交价;ts_交易方向（0：中性盘，1：买入，2：卖出）

最新分时交易数据接口

API接口：http://api.mairui.club/hszb/fsjy/000001/dn/b997d4403688d5e65a

字段说明：d_交易时间;o_开盘价;h_最高价;l_最低价;c_收盘价;v_成交量;e_成交额;zf_振幅;hs_换手率;zd_涨跌幅;zde_涨跌额

最新分时KDJ数据接口

API接口：http://api.mairui.club/hszb/kdj/000001/dn/b997d4403688d5e65a

字段说明：t_交易时间;k_K值;d_D值;j_J值

最新分时MACD数据接口

API接口：http://api.mairui.club/hszb/macd/000001/dn/b997d4403688d5e65a

字段说明：t_交易时间;diff_DIFF值;dea_DEA值;macd_MACD值;ema12_EMA（12）值;ema26_EMA（26）值

最新分时MA数据接口

API接口：http://api.mairui.club/hszb/macd/000001/dn/b997d4403688d5e65a

字段说明：t_交易时间;ma3_MA3，没有则为null;ma5_MA5，没有则为null;ma10_MA10，没有则为null;ma15_MA20，没有则为null;ma20_MA20，没有则为null;ma30_MA30，没有则为null;ma60_MA60，没有则为null;ma120_MA120，没有则为null;ma200_MA200，没有则为null;ma250_MA250，没有则为null

最新分时BOLL数据接口

API接口：http://api.mairui.club/hszb/boll/000001/dn/b997d4403688d5e65a
————————————————
                        
原文链接：https://blog.csdn.net/u012940698/article/details/135359174