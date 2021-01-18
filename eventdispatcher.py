#from telnet_connect import TelnetConnect
from kivy.core.window import Window
from kivy.event import EventDispatcher

from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import  ListProperty

from kivy.uix.behaviors.emacs import EmacsBehavior
import re



class DispatcherColor(EventDispatcher):
    """ """                                     
    color_grey = ListProperty([0.6, 0.6, 0.53, 1])
    color_black = ListProperty([0, 0, 0, 1])
    color_red = ListProperty([1, 0, 0, 1])
    color_canvas = ListProperty([0.7, 0.7, 0.7, 1]) 


class ErorrPopup(BoxLayout):
    pass


def show_status_popup( status, *args):
    content = ErorrPopup()
    content.ids.label_erorr.text = status            
    Window._popup = Popup(title="", content=content, separator_height = 0,
                                background =  './data/f.png', opacity = 1, size_hint=(0.3, 0.2))
    Window._popup.open()


class MainDevice():
    EventDispatcher = DispatcherColor()
    grey = EventDispatcher.color_grey
    black = EventDispatcher.color_black

    def __init__(self, **kwargs):
        self.login_prompt = b"login: "
        self.password_prompt = b"Password: "
        self.prompt = b"# "
        self.prompt_enable = None


    def install_arg_curent_connect(self):
        current_connect = EventDispatcherCLI.cli[EventDispatcherCLI.current_btn_cli]['connect']
        current_connect.login_prompt = self.login_prompt
        current_connect.password_prompt = self.password_prompt 
        current_connect.prompt = self.prompt
        current_connect.prompt_enable = self.prompt_enable


    def commands_telnet(self, obj, value, add_text=None, add_text_2=None, add_text_3=None, timeout=None ):
        """                                                
        отправка команд из биндинных кнопок
        """

        if add_text_3 != None:
            value = value.format( add_text=add_text, add_text_2=add_text_2, add_text_3=add_text_3)
        if add_text_2 != None:
            value = value.format( add_text=add_text, add_text_2=add_text_2)
        if add_text != None:
            value = value.format( add_text=add_text)
        
        command = value
        current = EventDispatcherCLI.cli[EventDispatcherCLI.current_btn_cli]
        row_last = EventDispatcherCLI.cli[EventDispatcherCLI.current_btn_cli]['box_cli'].ids.textinput_cli.text.split('\n')
        text = row_last[-1]
        text = EventDispatcherCLI.change_text_replace(text)
        position_cursor = current['box_cli_text'].ids.text_input.position_cursor
        
        if position_cursor == 0:
            position_cursor = len(text)

        try:
            text_return, position_cursor = current['connect'].write(command, text, position_cursor, timeout )
            
            current['box_cli'].ids.textinput_cli.text += command
        
        except AttributeError:
            show_status_popup('NO CONNECTION')
            return

        except BrokenPipeError:
            show_status_popup('NO CONNECTION')
            return

        search_end_row = current['box_cli'].ids.textinput_cli.text.split('\n')[-1]

        if current['btn_label'].text == 'text':
            text_return = EventDispatcherCLI.change_text_replace(text_return)

        else:
            text_return = EventDispatcherCLI.change_label_replace(text_return)

        current['box_cli'].ids.textinput_cli.text = current['box_cli'].ids.textinput_cli.text[:-len(search_end_row)] + text_return
        current['box_cli_text'].ids.text_input.position_cursor = 0
        current['box_cli_text'].ids.text_input.cursor = (0, 0)


    def commands_telnet_2(self, obj, value, add_text=None, add_text_2=None, add_text_3=None, timeout=None ):
        """                                                 # TODO refactoring
        отправка команд из биндинных кнопок
        """

        if add_text_3 != None:
            value = value.format( add_text=add_text, add_text_2=add_text_2, add_text_3=add_text_3)
        if add_text_2 != None:
            value = value.format( add_text=add_text, add_text_2=add_text_2)
        if add_text != None:
            value = value.format( add_text=add_text)
        
        command = value
        current = EventDispatcherCLI.cli[EventDispatcherCLI.current_btn_cli]
        current['connect'].command = command
        

        try:
            text = current['connect'].write(command, timeout)
            current['box_cli'].ids.textinput_cli.text += command

        except AttributeError:
            show_status_popup('NO CONNECTION')
            return
        except BrokenPipeError:
            show_status_popup('NO CONNECTION')
            return

        if current['btn_label'].text == 'text':
            text = EventDispatcherCLI.change_text_replace(text)
        else:
            text = EventDispatcherCLI.change_label_replace(text)

        current['box_cli'].ids.textinput_cli.text += text


    def validate(self, obj, value, len_hint_text):
        if len(value) > len_hint_text:
            obj.text = value[:len_hint_text]
            return
        else:
            obj.text = value.strip()


    def validate_search(self, obj, value, len_hint_text):
        if len(value) > len_hint_text:
            obj.text = value[:len_hint_text]
            return
        else:
            obj.text = value.lstrip()


    def focus_search(self, obj, value):
        if obj.focus == False:
            EventDispatcherCLI.cli[EventDispatcherCLI.current_btn_cli]['cli_device'].search = value


    def validate_mac(self, obj, subline, len_hint_text, value=None, number=None):
        sub_line = re.sub(r'\W', '', subline)
        if len(sub_line) > 12:
            obj.text = subline[:len_hint_text]
            return
        else:
            obj.text = subline.strip()

        if len(subline) >= 12:
            subline = re.sub(r'\W', '', subline)
            text = f"{value}".join(subline[i:i+number] for i in range(0, len(subline), number))
            obj.text = text
            return


class EventDispatcherCLI():
    """ """                                     
    cli = {}
    current_btn_cli = None

    def __init__(self, **kwargs):
        pass

    @classmethod
    def install_cli(cls, btn, **kwargs):
        try:
            cls.cli[btn]
        except KeyError:
            cls.cli[btn] = {}
        for key , val in kwargs.items():
            cls.cli[btn][key] = val


    @classmethod
    def change_text_replace(cls, text, global_change=False):
        current = cls.current_btn_cli
        if cls.cli[current]['connect'].command != None and global_change==False:
            text = text.replace( str(cls.cli[current]['connect'].command), '' )

        text = re.sub(r'\[color=[0-9a-f]{6}\]|\[/color\]', '', text  )
        return text


    @classmethod
    def change_label_replace(cls, text, global_change=False):
        current = cls.current_btn_cli

        if cls.cli[current]['connect'].command != None and global_change==False:
            text = text.replace( str(cls.cli[current]['connect'].command), '' )

        search = cls.cli[current]['cli_device'].search
        text_split_login = cls.cli[current]['connect'].text_split_login

        text_split = ''
        if '$' in text_split_login:
            for item in text_split_login:
                if item == '$':
                    text_split += '\$'
                else:
                    text_split += item
        if text_split == '':
            text_split = text_split_login

        login_search_color = re.findall(fr'{text_split}',   text )

        if  login_search_color:
            text = re.sub(fr'{text_split}', f'[color=00ffff]{text_split_login}[/color]', text)

        text = re.sub(r'\bup\b', str(' [color=00ff00]UP[/color] '), text , flags=re.IGNORECASE)
        text = re.sub(r'\bdown\b', str(' [color=ff0000]DOWN[/color] '), text , flags=re.IGNORECASE)
        if search != '':
            text = re.sub(r'{search}\b'.format(search=str(search)), str('[color=ff00ff]{search}[/color]'.format(search=str(search))), text , flags=re.IGNORECASE)

        return text


class  EmacsBehavior():

    def __init__(self, **kwargs):
        super(EmacsBehavior, self).__init__(**kwargs)
        self.position_cursor = 0

        self.bindings = {
            'number': {
                'tab': lambda: self.write_command('\t', timeout=0.3,  key='tab'),
                'enter': lambda: self.write_command('\r', timeout=0.8, key='enter'),

                'up': lambda: self.write_command('\x1b\x5b\x41', timeout=0.1),
                'down': lambda: self.write_command('\x1b\x5b\x42', timeout=0.1),

                'left': lambda: self.write_command('\x1b\x5b\x44', timeout=0.1, key='left', com='cursor_left' ),
                'right': lambda: self.write_command('\x1b\x5b\x43', timeout=0.1, key='right', com='cursor_right'),

                'backspace': lambda: self.write_command('\b',timeout=0.1, ),
                'spacebar': lambda: self.write_command(' ', timeout=0.3, key='spacebar'),
                    },
            'ctrl': {
                'a': lambda: self.write_command('\x01', timeout=0.1, key='home', com='cursor_home' ),
                'e': lambda: self.write_command('\x05', timeout=0.1, key='end', com='cursor_end' ),
                'x': lambda: self._cut(self.selection_text),
                'v': self.paste,
                'b': lambda: self.do_cursor_movement('cursor_left'),
                'f': lambda: self.do_cursor_movement('cursor_right'),
            },
            'alt': {
                'b': lambda: self.do_cursor_movement('cursor_left',
                                                    control=True ),
                'f': lambda: self.do_cursor_movement('cursor_right',
                                                    control=True ),
            },
            'shift': {
                '/': lambda: self.write_command('?'),
            },
        }


    def keyboard_on_key_down(self, window,  keycode, text, modifiers):
        keycode, key =  keycode
        if len(self.text) == 0 and key=='backspace':
            return

        # join the modifiers e.g. ['alt', 'ctrl']
        mod = '+'.join(modifiers) if modifiers else None
        is_emacs_shortcut = False

        if keycode in range(286) and self.key_bindings == 'emacs':
            if mod == None and key in self.bindings['number'].keys():
                is_emacs_shortcut = True
            elif mod == 'ctrl' and key in self.bindings['ctrl'].keys():
                is_emacs_shortcut = True
            elif mod == 'alt' and key in self.bindings['alt'].keys():
                is_emacs_shortcut = True
            elif mod == 'shift' and key in self.bindings['shift'].keys():
                is_emacs_shortcut = True
            else:  # e.g. ctrl+alt or alt+ctrl (alt-gr key)
                is_emacs_shortcut = False

        if is_emacs_shortcut and mod:
            # Look up mod and key
            emacs_shortcut = self.bindings[mod][key]
            emacs_shortcut()
        elif is_emacs_shortcut and  mod == None:
            emacs_shortcut = self.bindings['number'][key]
            emacs_shortcut()
        elif mod == None:
            self.write_command(chr(keycode), timeout=0.1)
            pass


    def write_command(self, value, timeout=None, key=None, com=None):
        current_connect = EventDispatcherCLI.cli[EventDispatcherCLI.current_btn_cli]

        row_last = EventDispatcherCLI.cli[EventDispatcherCLI.current_btn_cli]['box_cli'].ids.textinput_cli.text.split('\n')
        text = row_last[-1]
        text = EventDispatcherCLI.change_text_replace(text)

        if self.position_cursor == 0:
            self.position_cursor = len(text)

        try:
            text_return, position_cur = current_connect['connect'].write_2(value,  text, self.position_cursor, timeout )

        except AttributeError:
            show_status_popup('NO CONNECTION')
            return

        self.position_cursor = position_cur
        search_end_row = current_connect['box_cli'].ids.textinput_cli.text.split('\n')[-1]

        if current_connect['btn_label'].text == 'text':
            text_return_change = EventDispatcherCLI.change_text_replace(text_return)
        else:
            text_return_change = EventDispatcherCLI.change_label_replace(text_return)

        current_connect['box_cli'].ids.textinput_cli.text = current_connect['box_cli'].ids.textinput_cli.text[:-len(search_end_row)] + text_return_change

        text_split_login = current_connect['connect'].text_split_login
        row_login = text_return.split('\n')[-1]
        login = re.search(text_split_login, row_login)
        if login:
            self.text = row_login[login.end():]

        elif not login:
            self.text = ''

        if (key == 'enter' and re.search('\r\n', text_return)) or (key!='tab' and re.search('\r\n', text_return)) :
            self.position_cursor = 0
        self.cursor = ((self.position_cursor - len(text_split_login)) , 0)

        return