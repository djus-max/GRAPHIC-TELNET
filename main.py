#!.telnet_lib_py_3.7.5/bin/python
# -*- coding: utf-8 -*-

import kivy  
kivy.require('1.11.1')
from kivy.app import App
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.uix.widget import Widget

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from kivy.uix.popup import Popup
from kivy.uix.bubble import Bubble

from kivy.event import EventDispatcher
from kivy.properties import  ListProperty

from kivy.core.window import Window
from kivy.cache import Cache
from functools import partial

import re
import sys

from telnet_connect import TelnetConnect

from eventdispatcher import EventDispatcherCLI, show_status_popup, DispatcherColor, EmacsBehavior

from DeviceClass.QTech import QTech
from DeviceClass.SNR import SNR
from DeviceClass.DLink import DLink
from DeviceClass.BDCOM import BDCOM
from DeviceClass.CDATA import CDATA
from DeviceClass.EdgeCore import EdgeCore

from kivy.lang import Builder
import os


class LeftWidget(FloatLayout):
    def __init__(self, **kwargs):
        super(LeftWidget, self).__init__(**kwargs)
        pass


class RightWidget(BoxLayout):
    DispatcherColor = DispatcherColor()
    grey = DispatcherColor.color_grey
    black = DispatcherColor.color_black
    color_canvas = DispatcherColor.color_canvas


    def __init__(self, **kwargs):
        super(RightWidget, self).__init__(**kwargs)
        EventDispatcherCLI.right_widget = self


    def choice_device(self, obj=None, value=None):
        curent = EventDispatcherCLI.current_btn_cli

        if EventDispatcherCLI.cli[curent]['device'] != None:
            EventDispatcherCLI.cli[curent]['device'].background_color = self.grey
            self.ids.CLIDevice.remove_widget(EventDispatcherCLI.cli[curent]['cli_device'])

        cli_device = getattr(sys.modules[__name__], value)
        cli_device = cli_device(size_hint=(1, 1), pos=self.pos)
        self.ids.CLIDevice.add_widget(cli_device,  0)

        obj.background_color = self.black
        EventDispatcherCLI.install_cli(btn=EventDispatcherCLI.current_btn_cli, device=obj, cli_device=cli_device)

        # параметры логина и пароля
        cli_device.install_arg_curent_connect()  


    def choice_device_with_main(self, old_obj, obj):
        current_old = EventDispatcherCLI.cli[old_obj]['device']
        if current_old != None:
            current_old.background_color = self.grey
            EventDispatcherCLI.cli[old_obj]['cli_device'].size_hint = (0, 0)
            Cache.register(EventDispatcherCLI.cli[old_obj]['cli_device'])
            len_children = len( EventDispatcherCLI.cli[old_obj]['cli_device'].ids.change_device.children)
            
            for item in range(len_children):
                Cache.append(EventDispatcherCLI.cli[old_obj]['cli_device'], item, EventDispatcherCLI.cli[old_obj]['cli_device'].ids.change_device.children[item-1])

            EventDispatcherCLI.cli[old_obj]['cli_device'].ids.change_device.clear_widgets()

        cli_device = EventDispatcherCLI.cli[obj]['cli_device']
        if cli_device == None:
            return

        current = EventDispatcherCLI.cli[obj]['device']
        current.background_color = self.black
        EventDispatcherCLI.cli[obj]['cli_device'].size_hint = (1, 1)

        for item in range(0,3):
            button = Cache.get(EventDispatcherCLI.cli[obj]['cli_device'], item)
            if button != None:
                EventDispatcherCLI.cli[obj]['cli_device'].ids.change_device.add_widget(button)


    def change_curent_cli(self, current_btn):
        EventDispatcherCLI.cli[current_btn]['device'].background_color = self.grey
        self.ids.CLIDevice.remove_widget(EventDispatcherCLI.cli[current_btn]['cli_device'])



class RowLogin(BoxLayout):

    def __init__(self, **kwargs):
        super(RowLogin, self).__init__(**kwargs)
        self.check_len_value = 0


    def validate(self, obj, value):
        if self.check_len_value < len(value):
            self.check_len_value = len(value)
            if len(value) > 10:
                obj.text = value[:10]
                return
            else:
                if value[0] == ' ':
                    obj.text = value.lstrip()
                    return
        else:
            self.check_len_value = len(value)
            return


    def focus(self, obj, value):
        if obj.focus == False:
            if len(value) > 0:
                if self.ids.id_username == obj:
                    TelnetConnect.username = value                  # TODO
                if self.ids.id_password == obj:
                    TelnetConnect.password = value                   # TODO


class WorkComands(BoxLayout):
    DispatcherColor = DispatcherColor()
    grey = DispatcherColor.color_grey

    
    def __init__(self, **kwargs):
        super(WorkComands, self).__init__(**kwargs)


    def commands_telnet_2(self, obj, value):                #! РЕФАКТОРИТЬ
        command = value
        current_connect = EventDispatcherCLI.cli[EventDispatcherCLI.current_btn_cli]['connect']
        try:
            text = current_connect.write_2(command, timeout=0.3)

        except AttributeError:
            show_status_popup('NO CONNECTION')
            return

        #except BrokenPipeError:
            #show_status_popup('NO CONNECTION')
            #return

        if EventDispatcherCLI.cli[EventDispatcherCLI.current_btn_cli]['btn_label'].text == 'text':
            text = EventDispatcherCLI.change_text_replace(text)
        else:
            text = EventDispatcherCLI.change_label_replace(text)

        EventDispatcherCLI.cli[EventDispatcherCLI.current_btn_cli]['box_cli'].ids.textinput_cli.text +=  text


    def clear_cpi(self):
        text_obj = EventDispatcherCLI.cli[EventDispatcherCLI.current_btn_cli]['box_cli'].ids.textinput_cli
        text_split = text_obj.text.split('\n')
        text_obj.text = text_split[-1]


    def refresh(self):
        """перезагружает соединение и все данные"""
        curent = EventDispatcherCLI.current_btn_cli

        try:
            EventDispatcherCLI.cli[EventDispatcherCLI.current_btn_cli]['box_cli'].ids.textinput_cli.text = ''
            if EventDispatcherCLI.cli[curent]['connect'].tn != None:
                EventDispatcherCLI.main_widget.show_bubble(EventDispatcherCLI.cli[curent]['box_cli'])

            for key in EventDispatcherCLI.cli[curent]['connect'].__dict__.keys():
                EventDispatcherCLI.cli[curent]['connect'].__dict__[key] = None
            
            EventDispatcherCLI.right_widget.change_curent_cli(curent)
            curent.text = ''

            EventDispatcherCLI.install_cli(btn=curent, device=None, cli_device=None )

            curent = EventDispatcherCLI.current_btn_cli

        except AttributeError:
            return

        except KeyError:
            return


class DeviceType(BoxLayout):
        pass


class AddWidgetTelnet( BoxLayout):
    pass


class CLI(FloatLayout):
    pass


class CLIDevice(FloatLayout):
    """ add new window device with button """
    pass


class BoxTab(FloatLayout):
    """ add BOX with button for new window CLI """
    pass


class BoxCliLabel(FloatLayout):
    """ new window CLI """
    pass


class TerminalConsole(EmacsBehavior, TextInput ):
    key_bindings = 'emacs'


class BoxCliTextInput(BoxLayout):
    """ new window CLI """
    pass


class BoxCliText(FloatLayout):
    """ new window CLI """
    pass
    

class ErorrPopup(BoxLayout):
    pass


class ShowBubble(Bubble): 
    """ add bubble-connect for new window CLI """
    DispatcherColor = DispatcherColor()
    black = DispatcherColor.color_black
    red = DispatcherColor.color_red
    color_canvas = DispatcherColor.color_grey


    def validate(self, obj, value):
        if len(value) > 15:
            obj.text = value[:15]
            return
        else:
            obj.text = value.strip()
            status = re.search(r'[^\d\.]', value)

            if  status :
                obj.foreground_color = self.red
                return
            elif not  status:
                obj.foreground_color = self.black



class MainWidget(BoxLayout):
    """ MAIN WIDGET"""                                             
    DispatcherColor = DispatcherColor()
    color_canvas = DispatcherColor.color_canvas
    grey = DispatcherColor.color_grey
    black = DispatcherColor.color_black


    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        EventDispatcherCLI.main_widget = self
        self.add_tab()


    def add_tab(self):
        """ """                                          
        box_text = BoxTab(pos_hint={"right":1}, size_hint_x=None, width=75, )
        self.btn_text = Button(text="text", size_hint=(1, 0.8), 
                    pos_hint={"right":1.5, "top":0.8},
                    background_color = self.grey, 
                    background_normal= '', on_release=self.change_label )
        box_text.add_widget(self.btn_text)

        box_label = BoxTab(pos_hint={"right":1}, size_hint_x=None, width=75, )
        self.btn_label = Button(text="label", size_hint=(1, 0.8), 
                    pos_hint={"right":1.5, "top":0.8},
                    background_color = self.black, 
                    background_normal= '', on_release=self.change_label )
        box_label.add_widget(self.btn_label)

        for i in range(5):
            box = BoxTab(pos_hint={"left":1}, size_hint_x=None, width=140)

            btn = Button(text="", size_hint=(1,1), 
                        pos_hint={"right":1, "top":0.9},
                        background_color = self.grey, 
                        background_normal= '', on_release=self.cli_current )

            box.add_widget(btn)
            self.ids.AddWidgetTelnet.add_widget(box)

            # add new work screen
            box_cli, box_cli_text = self.add_cli(btn)
            
            connect = TelnetConnect()

            # параметры для диспетчера
            EventDispatcherCLI.install_cli(btn=btn, btn_main=btn, btn_label=self.btn_label,
                                            box_cli=box_cli, box_cli_text=box_cli_text, connect=connect,  
                                            device=None, cli_device=None) 

            EventDispatcherCLI.current_btn_cli = btn

        btn.background_color = self.black
        self.ids.AddWidgetTelnet.add_widget(box_text)
        self.ids.AddWidgetTelnet.add_widget(box_label)
        EventDispatcherCLI.current_btn_cli = btn


    def add_cli(self, obj):
        """ """                                                  
        curent = EventDispatcherCLI.current_btn_cli
        if curent != None:
            EventDispatcherCLI.cli[curent]['box_cli'].size_hint=(0, 0)

        box_cli = BoxCliLabel(size_hint=(1, 0.98),  )
        self.ids.CLI.add_widget(box_cli,  0)
        box_cli_text = BoxCliTextInput(size_hint=(1, 0.08) )
        self.ids.CLI.add_widget(box_cli_text,  0)
        self.show_bubble(box_cli)
        return box_cli, box_cli_text


    def cli_current(self, obj):
        """ """                                     
        old_obj = EventDispatcherCLI.current_btn_cli

        if old_obj == obj:
            return
        elif old_obj != obj:
            EventDispatcherCLI.cli[old_obj]['box_cli'].size_hint=(0, 0)
            EventDispatcherCLI.cli[old_obj]['box_cli_text'].size_hint=(0, 0)
            old_obj.background_color = self.grey
            EventDispatcherCLI.cli[obj]['box_cli'].size_hint=(1, 0.98)
            EventDispatcherCLI.cli[obj]['box_cli_text'].size_hint=(1, 0.08)
            self.change_label_color(obj)
            EventDispatcherCLI.right_widget.choice_device_with_main(old_obj, obj)
            EventDispatcherCLI.current_btn_cli = obj 
            obj.background_color = self.black


    def change_label_color(self, obj):
        if EventDispatcherCLI.cli[obj]['btn_label'] == self.btn_label:
            self.btn_text.background_color = self.grey
        else:
            self.btn_label.background_color = self.grey
        
        EventDispatcherCLI.cli[obj]['btn_label'].background_color = self.black


    def change_label(self, obj):
        current = EventDispatcherCLI.current_btn_cli

        if EventDispatcherCLI.cli[current]['btn_label'] == obj or (len(EventDispatcherCLI.cli[current]['box_cli'].children) > 1):
            return

        else:
            text = EventDispatcherCLI.cli[current]['box_cli'].ids.textinput_cli.text
            self.ids.CLI.remove_widget(EventDispatcherCLI.cli[current]['box_cli'])
            self.ids.CLI.remove_widget(EventDispatcherCLI.cli[current]['box_cli_text'])
            if obj.text == 'text':
                box_cli = BoxCliText(size_hint=(1, 0.98),  )
                text = EventDispatcherCLI.change_text_replace(text, global_change=True)

            else: 
                box_cli = BoxCliLabel(size_hint=(1, 0.98),  )
                text = EventDispatcherCLI.change_label_replace(text, global_change=True)

            self.ids.CLI.add_widget(box_cli,)
            box_cli_text = BoxCliTextInput(size_hint=(1, 0.08) )
            self.ids.CLI.add_widget(box_cli_text,  0)
            box_cli_text.ids.text_input.text = EventDispatcherCLI.cli[current]['box_cli_text'].ids.text_input.text

            EventDispatcherCLI.cli[current]['btn_label'].background_color = self.grey
            obj.background_color = self.black

            box_cli.ids.textinput_cli.text = text
            EventDispatcherCLI.install_cli(btn=current, box_cli=box_cli, box_cli_text=box_cli_text, btn_label=obj)


    def connect(self, obj, bubble):
        ip = bubble.ids.ip_text.text.rstrip()
        pat = re.compile('^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
        status = pat.match(ip)
        if not status:
            status = 'ip address not correct'
            show_status_popup(status)
            return
        elif  status:
            ip_split = ip.split('.')
            for item in ip_split:
                if int(item) > 255:
                    status = 'ip address not correct'
                    show_status_popup(status)
                    return

            connect = EventDispatcherCLI.cli[EventDispatcherCLI.current_btn_cli]['connect']

            if connect.username == None:
                status = 'username not found'
                show_status_popup(status)
                return

            elif connect.password == None:
                status = 'password not found'
                show_status_popup(status)
                return

            elif connect.login_prompt == None:
                status = 'device not found'
                show_status_popup(status)
                return

            current = EventDispatcherCLI.current_btn_cli
            current.text = bubble.ids.ip_text.text
            text, flag = connect.connect(HOST =str(bubble.ids.ip_text.text))

            if flag == 1:
                if EventDispatcherCLI.cli[EventDispatcherCLI.current_btn_cli]['btn_label'].text == 'text':
                    text = EventDispatcherCLI.change_text_replace(text)
                else:
                    text = EventDispatcherCLI.change_label_replace(text)

                EventDispatcherCLI.cli[current]['box_cli'].remove_widget(bubble)

            EventDispatcherCLI.cli[current]['box_cli'].ids.textinput_cli.text += text 


    def show_bubble(self, box_cli):
        bubble = ShowBubble(size_hint=(0.4, 0.2), show_arrow=False, 
                        border = [5, 5, 5, 5],
                        pos_hint={'center_x': .5, 'center_y': .5}) 
        box_cli.add_widget(bubble)
        bubble.ids.ip_btn.bind(on_release=lambda btn: self.connect(btn, bubble))


class FirstScreen(Screen):
    def __init__(self, **kwargs):
        super(FirstScreen, self).__init__(**kwargs)
        self.widget = MainWidget()
        self.widget.size = (Window.width, Window.height)
        self.add_widget(self.widget)


class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)
        self.add_widget(FirstScreen(name='FirstScreen'))
        self.current = 'FirstScreen'


class TelnetSwitch(App):
    def config_file_get( *args):
        arg = args
        return Config.get(arg[0], arg[1])


    def config_file_set( *args):
        arg = args
        Config.set(arg[0], arg[1], arg[2])
        Config.write()


    def build(self):
        Cache.register('cli_table')
        Cache.register('cli_device')
        sm = ScreenManagement()
        return sm


if __name__ in ('__main__'):
    Window.size = (1366, 680)
    TelnetSwitch().run()