import platform
import re
import socket
import sys
import time
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread

setting = {
    'linux': '/etc/hosts',
    'darwin': '/etc/hosts',
    'windows': 'C:/Windows/System32/drivers/etc/hosts'
}


class MyHttpServer(BaseHTTPRequestHandler):
    def do_GET(self):
        """Serve a GET request."""
        self.send_response(HTTPStatus.OK)
        self.end_headers()
        self.wfile.write(b'SUCCESS')  # 此处修改返回标识
        print('本地服务器启动')


def change_hosts(sys_type):
    host_path = setting[sys_type]
    with open(host_path, 'r') as f:
        txt = f.read()
    try:
        if 'iristech.co' in txt:
            txt = re.sub('.+?iristech.co.*?', '127.0.0.1 iristech.co', txt)
            with open(host_path, 'w') as f:
                f.write(txt)
        else:
            with open(host_path, 'a') as f:
                f.writelines('\n127.0.0.1 iristech.co\n')
    except PermissionError as err:
        print('权限不足，请以管理员或root权限运行')
        sys.exit(1)


def get_ip():
    addr_info = socket.getaddrinfo('iristech.co', 'http')
    return addr_info[0][4][0]


if __name__ == '__main__':
    print('''###############################
       Iris Pro 本地激活
###############################''')
    sys_type = platform.system()
    print('1 ==> 系统类型： ', sys_type)
    iris_ip = get_ip()
    print('2 ==> iristech.co 指向 ', iris_ip)
    if iris_ip != '127.0.0.1':
        is_true = input('此 %s ip是否为激活服务器IP? (y/N)' % iris_ip)
        if is_true.lower() != 'y':
            change_hosts(sys_type.lower())
            for try_count in range(5):
                # todo: 刷新dns缓存
                iris_ip = get_ip()
                print('iristech.co ==> ', iris_ip)
                if iris_ip == '127.0.0.1':
                    print('IP已指向本地服务器')
                    break
                time.sleep(1)
            else:
                print('ERROR: IP指向仍然错误，程序终止，请手动设置 iristech.co 指向 127.0.0.1')
                print('提示： 百度 "[所用系统] 修改 hosts"')
                print('提示： 百度 "[所用系统] 刷新dns"')
                sys.exit(1)

    http_server = HTTPServer(('', int(80)), MyHttpServer)
    thread = Thread(target=http_server.serve_forever)
    thread.start()
    print('服务已启动')
    print('3 ==> 打开软件输入任意激活码激活')
