import telnetlib, socket
import time
import re
from eventdispatcher import EventDispatcherCLI


class TelnetConnect():
    username = None
    password = None
    port = 23
    timeout = 1
    time_sleep = 1

    def __init__(self, **kwargs):
        self.login_prompt = None
        self.password_prompt = None
        self.prompt = None
        self.prompt_enable = None
        self.tn = None
        self.command = None
        self.history = []


    def to_bytes(self, line):
        return f"{line}\r\n".encode("utf-8")


    def connect(self, HOST ):
        self.host = HOST
        text = ''
        try :
            self.tn = telnetlib.Telnet(self.host, self.port, self.timeout)
            tex = self.tn.read_until(self.login_prompt, self.timeout) 
            text += tex.decode('utf-8')
            self.tn.write(self.username.encode('utf-8') + b"\r\n")
            if self.password :
                tex = self.tn.read_until(self.password_prompt, self.timeout)
                text += tex.decode('utf-8')
                self.tn.write(self.password.encode('utf-8') + b"\r\n")
                tex = self.tn.read_until(self.prompt,self.timeout)
                text += tex.decode('utf-8')
                if self.prompt_enable:
                    self.tn.write('enable'.encode('utf-8') + b"\r\n")
                    tex = self.tn.read_until(self.prompt_enable, self.timeout)
                    text +=  tex.decode('utf-8') 
                flag = 1

        except socket.timeout :
            text += 'Not Connection' + '\r\n'   
            flag = 0

        except ConnectionRefusedError:
            text += 'Not Connection' + '\r\n'
            flag = 0

        except OSError:
            text += 'No route to host' + '\r\n'
            flag = 0

        else:
            self.text_split_login = text.split('\n')
            self.text_split_login = self.text_split_login[-1]
            self.text_split_login_bytes = self.text_split_login.encode('utf-8')

        return text, flag


    def write(self, msg, text, position_cursor, timeout=None ):
        if timeout == None:
            timeout = self.timeout

        self.tn.write(self.to_bytes(msg))
        output = self.tn.read_until(self.text_split_login_bytes, timeout)
        text, position_cursor_return = self.text_replace(output, text, position_cursor)
        return text, position_cursor_return


    def write_2(self, msg, text, position_cursor, timeout=None ):
        if timeout == None:
            timeout = self.timeout

        self.tn.write(msg.encode('utf-8'))
        time.sleep(timeout)
        output = self.tn.read_very_eager()

        text, position_cursor_return = self.text_replace(output, text, position_cursor)
        return text, position_cursor_return


    def text_replace(self, output, text, position_cursor):
        text_2 = output.decode()
        text_2_row_first = text_2.split('\n')[0]

        for c in text_2_row_first:
            if c == '\x08':
                position_cursor -= 1

            else:
                if position_cursor == len(text) and c!='\r':
                    text += c
                    position_cursor += 1

                elif c=='\r':
                    text += c
                    position_cursor = 0

                else:
                    text = ''.join((text[:position_cursor], c, text[position_cursor+1:]))
                    position_cursor += 1

        text += text_2[len(text_2_row_first):]
        return text, position_cursor


    def write_3(self, msg, timeout=None):
        if timeout == None:
            timeout = self.timeout

        self.tn.write(msg)
        time.sleep(timeout)
        output = self.tn.read_very_eager()
        text = self.text_replace(output)

        return text