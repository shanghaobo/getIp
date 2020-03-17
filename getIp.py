from flask import Flask,request,make_response,redirect
import requests as r
import json
import time
import base64

app = Flask(__name__)

#app_path='E:Git/getIp'
app_path='/root/getIp'

@app.route('/')
def hello_world():
    ip=request.remote_addr
    return ip

@app.route('/get_ip_city')
def get_ip_city():
    ip=request.args.get('ip')
    if ip:
        #查询ip信息

        try:
            res = r.get('http://ip.ws.126.net/ipquery?ip=%s' % ip)
            text = res.text
            text = text[text.find('localAddress=') + len('localAddress='):]
            text = text.replace('city', '"city"').replace('province', '"province"')
            jsondata = json.loads(text)
            region = jsondata['province']
            city = jsondata['city']
            return (region + '-' + city).encode('gbk')
        except:
            return 'error'

    else:
        return 'request error'

def get_ip_address(ip):
    try:
        res = r.get('http://ip.ws.126.net/ipquery?ip=%s' % ip)
        text = res.text
        text = text[text.find('localAddress=') + len('localAddress='):]
        text = text.replace('city', '"city"').replace('province', '"province"')
        jsondata = json.loads(text)
        region = jsondata['province']
        city = jsondata['city']
        return region + '-' + city
    except:
        return 'error'


@app.route('/get_info')
def get_info():
    #resp=make_response('true')
    #resp.headers['Location']='http://q.qlogo.cn/headimg_dl?dst_uin=1186156343&spec=100'
    url=request.args.get('amp;url')
    if url:
        url=base64.b64decode(url).decode('utf-8')
        print('【url=%s】'%url)
        resp = redirect(url)
    else:
        resp=''
    timestamp = request.args.get('timestamp')
    ip = str(request.remote_addr)
    address = get_ip_address(ip)
    ip = ip.replace(ip.split('.')[3], '***')
    print(request.user_agent)
    sys = request.user_agent.platform  # 系统
    if not sys:
        return 'true'
    eq_info=request.user_agent.string
    if eq_info:
        try:
            eq_info = eq_info[eq_info.find('(') + 1:eq_info.find(')')]
            eq_info = eq_info.split(';')[3].split('/')[0].replace('Build', '').replace(' ', '')
        except:
            eq_info=''
    now_timestamp=int(time.time()*1000)
    if (now_timestamp-int(timestamp))>30*1000:#超过30秒的不处理
        return resp
    if timestamp:
        text = '%s %s(%s)\n' % (ip, address,eq_info)
        try:
            with open('%s/info/%s.txt' % (app_path, timestamp), 'r', encoding='utf-8') as f:
                if f.read().find(text) != -1:
                    return resp
        except:
            pass
        with open('%s/info/%s.txt' % (app_path, timestamp), 'a+', encoding='utf-8') as f:
            f.write(text)
    else:
        return 'args error'
    return resp



@app.route('/get_info_text')
def get_info_text():
    try:
        timestamp = request.args.get('timestamp')
        if timestamp:
            text = ''
            with open('%s/info/%s.txt' % (app_path, timestamp), 'r+', encoding='utf-8') as f:
                text = f.read()[:-1]
                lines=len(text.split('\n'))
                text='有来自以下地区的%s个小伙伴正在窥屏\n'%lines+text
            return text.encode('gbk')
        else:
            return 'args error'
    except:
        return 'error'


if __name__ == '__main__':
    app.run(host='0.0.0.0',port='9999')
