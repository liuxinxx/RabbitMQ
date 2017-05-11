#encoding=utf8
from xtls.activemqwraps import consumer
# mq_uri 是你的MQ的连接地址
# queue_name 是queue的名字
# param_type 是你入库时yield出去的对象的类型，对应的你task接受的param的类型
mq_uri=''
queue_name =''
param_type =''
@consumer(mq_uri, queue_name, param_type=str)
def task(param):
    pass  # crawl target
