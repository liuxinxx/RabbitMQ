#encoding=utf8
import pika
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import HTMLParser
def downloader_html(url):##利用PhantomJS获取网页数据
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    #伪造浏览器UA标识，该条UA为百度爬虫
    baidu_ua = 'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html）'
    dcap["phantomjs.page.settings.userAgent"] = (baidu_ua)
    driver = webdriver.PhantomJS(desired_capabilities=dcap)
    #print driver.service
    print '浏览器打开完成，开始下拉页面加载！'
    driver.get(url)    
    time.sleep(2)
    ##下拉浏览器页面使，页面完全加载 
    dian = ''
    print '网页下拉中',     
    for i in range(4): 
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        ##进程休眠一秒等待网页加载完成    
        time.sleep(1) 
        dian =dian +'.'
        print '.', 
    print '页面获取完成，开始解析页面'
    data = driver.page_source
    # 解决页面转义
    html_parser = HTMLParser.HTMLParser()
    data = html_parser.unescape(data)   
    return data
def fenlei(soup):##获取全国各个地区链接
    list_fenlei = []    
    div_list = soup.find_all("div",class_="J-nav-item")
    for v in div_list:
        for k in v.find_all('li'):
            list =[]
            k = k.find('a')        
            fenlei_url =k.get('href')
            fenlei_name =k.get_text()
            list.append(fenlei_name)
            list.append(fenlei_url)
            list_fenlei.append(list)           
    return list_fenlei
def callback(ch, method, properties, body):
    print(" [消费者] Received %r" % body)
    soup = BeautifulSoup(downloader_html(body),'lxml')
    listfenlei = fenlei(soup)
    for g in range(len(listfenlei)):
        print '分类为：',listfenlei[g][0],'链接为：',listfenlei[g][1]
        time.sleep(1)
    print(" [消费者] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)#  接收到消息后会给rabbitmq发送一个确认
def accept_list():
    '''
            接收任务
    callback    :回调函数
    '''
    username = '*****'   #指定远程rabbitmq的用户名密码
    pwd = '*****'
    user_pwd = pika.PlainCredentials(username, pwd)
    s_conn = pika.BlockingConnection(pika.ConnectionParameters('192.168.1.1',5672,'/', credentials=user_pwd))#创建连接
    channel = s_conn.channel()  #在连接上创建一个频道
    
    channel.queue_declare(queue='task_queue', durable=True) #创建一个新队列task_queue，设置队列持久化，注意不要跟已存在的队列重名，否则有报错  
    
    channel.basic_qos(prefetch_count=1)   # 消费者给rabbitmq发送一个信息：在消费者处理完消息之前不要再给消费者发送消息
    
    channel.basic_consume(callback,        #回调函数,具体执行任务
                          queue='task_queue',                #这里就不用再写no_ack=False了
                          )
    channel.start_consuming()
if __name__ == '__main__':
    accept_list()