# -*- coding: utf-8 -*-

try:
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
except ImportError:
    from http.server import BaseHTTPRequestHandler, HTTPServer

import threading
import sys
import os
import json
from markdown import markdown
import socket
from select import select
from websocket import WebSocket

MARKDOWN_OPTIONS = ['extra', 'codehilite']
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        if self.path == '/':
            f = open(CURRENT_DIR+'/index.html', 'r')
            data = f.read()
            self.wfile.write(data)
            f.close()
        try:
            f = open(self.path[1:], 'rb')
            self.wfile.write(f.read())
            f.close()
        except:
            pass


class InstantMarkdown():

    def __init__(self):
        self.port = 7000
        self.socket_list = set()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = False

    def server_main(self):
        s = HTTPServer(('', self.port), RequestHandler)
        s.serve_forever()

    def start_threads(self):
        self.running = True
        self.socket_thread = threading.Thread(target=self.socket_main)
        self.server_thread = threading.Thread(target=self.server_main)
        self.socket_thread.start()
        self.server_thread.start()

    def stop_threads(self):
        self.running = False
        self.socket_thread._Thread__stop()
        self.server_thread._Thread__stop()

    def start_browser(self):
        url = 'http://localhost:%s/' % self.port
        if sys.platform.startswith('darwin'):
            os.system('open -g '+url)
        elif sys.platform.startswith('win'):
            os.system('start '+url)
        else:
            os.system('xdg-open '+url)

    def send_markdown(self, data):
        html = markdown(
            '\n'.join(data).decode('utf-8'),
            MARKDOWN_OPTIONS
        )
        threading.Thread(
            target=self.socket_send_all,
            args=(json.dumps(html),)
        ).start()

    def socket_main(self):

        port = 7001
        try:
            self.server.bind(('', port))
            self.server.listen(100)
        except Exception as e:
            print(e)
            exit()
        self.socket_list.add(self.server)

        while True:
            r, w, e = select(self.socket_list, [], [])
            for sock in r:
                if sock == self.server:
                    conn, addr = sock.accept()
                    if WebSocket.handshake(conn):
                        self.socket_list.add(conn)
                else:
                    data = WebSocket.recv(sock)
                    if not data:
                        self.socket_list.remove(sock)
                    else:
                        WebSocket.send(conn, data)

    def socket_send_all(self, data):
        for sock in self.socket_list:
            if sock != self.server:
                WebSocket.send(sock, data)
