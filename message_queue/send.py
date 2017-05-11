#encoding=utf8
# !/usr/bin/env python
import pika
import sys
import time
def getCity():##返回城市二维列表[0]url [1]城市名字
    cityUrl_list=[]
    for line in open("123.txt"):
        list =[]  
        line=line.replace("\n","")
        lines=line.split("^") 
        list.append(lines[0])
        list.append(lines[1])
        cityUrl_list.append(list)
    return cityUrl_list
def send(message_list):
    '''
    message_list    :消息队列
    '''
    username = 'guest'   #指定远程rabbitmq的用户名密码
    pwd = 'guest' #远程密码
    user_pwd = pika.PlainCredentials(username, pwd)
    s_conn = pika.BlockingConnection(pika.ConnectionParameters('139.129.46.146',5672,'/', credentials=user_pwd))#创建连接
    channel = s_conn.channel()  #在连接上创建一个频道
    
    channel.queue_declare(queue='task_queue', durable=True) #创建一个新队列task_queue，设置队列持久化，注意不要跟已存在的队列重名，否则有报错
    for g in  range(len(message_list)):
        message = message_list[g][0]
        channel.basic_publish(exchange='',
                              routing_key='task_queue',#写明将消息发送给队列worker
                              body=message,    #要发送的消息
                              properties=pika.BasicProperties(delivery_mode=2,)#设置消息持久化，将要发送的消息的属性标记为2，表示该消息要持久化
                              )
        print g,':',(" [生产者] Send %r " % message)
        time.sleep(0.02)
    print g
if __name__ == '__main__':
    message_list = getCity()
    send(message_list)
 