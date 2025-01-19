#!/usr/bin/env python3

import selectors
import socket
import sys
import traceback

import libclient as libclient


class ClientSocket:
    def __init__(self):
        self.sel = selectors.DefaultSelector()
        self.host = 'localhost'
        self.port = 12345


    def create_request(self, action, value):
        match action:
            case "set horizontal motors":
                return dict(
                    type="text/json",
                    encoding="utf-8",
                    content=dict(action=action, value=value),
                )
            case "set vertical motors":
                return dict(
                    type="text/json",
                    encoding="utf-8",
                    content=dict(action=action, value=value),
                )
            case "shutdown":
                return dict(
                    type="text/json",
                    encoding="utf-8",
                    content=dict(action=action),
                )
            case _:
                raise ValueError(f"Unknown action: {action!r}")
            


    def start_connection(self, host, port, request):
        addr = (host, port)
        print(f"Starting connection to {addr}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        message = libclient.Message(self.sel, sock, addr, request)
        self.sel.register(sock, events, data=message)
        
    def run(self):
        try:
            while True:
                events = self.sel.select(timeout=1)
                for key, mask in events:
                    message = key.data
                    try:
                        message.process_events(mask)
                    except Exception:
                        print(
                            f"Main: Error: Exception for {message.addr}:\n"
                            f"{traceback.format_exc()}"
                        )
                        message.close()
                # Check for a socket being monitored to continue. I think this exists to exit if there are no active connections
                '''if not self.sel.get_map():
                    break'''
        except KeyboardInterrupt:
            print("Caught keyboard interrupt, exiting")
        finally:
            self.sel.close()
