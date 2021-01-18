from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from eventdispatcher import EventDispatcherCLI, MainDevice

from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button

import sys
import re

from kivy.clock import Clock

import threading
from functools import partial

from telnet_connect import TelnetConnect


class QTech(BoxLayout, MainDevice):
    list_button = []


    def __init__(self, **kwargs):
        super(QTech, self).__init__(**kwargs)
        self.prompt = b"# "
        self.search = ''
        self.build()
        QTech_2800.change_widget(self, self.mainbutton, self.mainbutton.text)


    def build(self):
        self.dropdown = CustomDropDownQTech()
        self.mainbutton = Button(text='QTech_2800', background_normal= '',
                    background_color=self.black, size_hint_x=None, width=130) 
        self.mainbutton.bind(on_release=self.dropdown.open)
        self.dropdown.bind(on_select=self.change_device)
        self.list_button.append(self.mainbutton)
        self.ids.change_device.add_widget(self.mainbutton)

        button = Button(text='Trafick', background_normal= '',
                    background_color= self.grey,  size_hint_x=None, width=130)
        button.bind(on_release=lambda button: self.change_device(button, button.text))
        self.list_button.append(button)
        self.ids.change_device.add_widget(button)


    def change_device(self, instance, text):
        cli_device = getattr(sys.modules[__name__], text)
        cli_device.change_widget(self, instance, text)


class CustomDropDownQTech(DropDown ):
    pass


class Trafick:
    @classmethod
    def change_widget(cls, self, instance,  text):
        self.ids.DeviceQTechBox.clear_widgets()
        cls.TrafickQTechBox = TrafickQTechBox()
        self.ids.DeviceQTechBox.add_widget(cls.TrafickQTechBox)

        for item in self.list_button:
            item.background_color=self.grey

        instance.background_color=self.black

class TrafickQTechBox(BoxLayout, MainDevice):


    def counter(self, instance, text):
        self.flag = True
        Clock.schedule_interval(partial(self.counter_inteval, instance, text), 5)


    def counter_inteval(self, instance, text, dt):
        command = f'show interface ethernet {text} | include last 5'
        connect = EventDispatcherCLI.cli[EventDispatcherCLI.current_btn_cli]['connect']
        text = connect.write(command)
        def split_text(rate):
            text = re.search(r'rate\s\d+', rate )[0].split(' ')
            text = str(int(text[1]) // 1000 )
            text = text[::-1]
            value = ','
            number =  3
            text = f"{value}".join(text[i:i+number] for i in range(0, len(text), number))
            text = text[::-1]

            return text

        text = text.split('\n')
        input_rate = text[1]
        output_rate = text[2]
        input_rate = split_text(input_rate)
        output_rate = split_text(output_rate)
        self.ids.input_rate.text = f'{input_rate} KBits/sec'
        self.ids.output_rate.text = f'{output_rate} KBits/sec'

        return self.flag


    def stop(self, instance):
        self.flag = False


class QTech_2800:
    @classmethod
    def change_widget(cls, self, instance, text):
        self.ids.DeviceQTechBox.clear_widgets()
        cls.QTechBox2800 = QTechBox2800()
        self.ids.DeviceQTechBox.add_widget(cls.QTechBox2800)

        for item in self.list_button:
            item.background_color=self.grey
        
        self.mainbutton.text = text
        self.mainbutton.background_color=self.black


class DeviceQTechBox(BoxLayout):
    pass


class QTechBox2800(BoxLayout, MainDevice):
    pass



Builder.load_string("""
<TrafickQTechBox>:
    orientation: 'vertical'
    size_hint_y: None
    height: self.height
    BoxLayout:
        size_hint_y: None
        height:  '35sp'
        padding: 0, 5, 0, 0
        spacing: 10
        Button:
            text: 'counter'
            size_hint_x: None
            width: self.texture_size[0] + 30
            on_release: root.counter(self, counter.text)

        TextInput:
            id: counter
            text: ''
            hint_text: 'x/x/xx'
            multiline: False
            halign: 'center'
            size_hint_x: None
            width:  str(len(self.hint_text)+2) + '0' + 'sp'

        BoxLayout:
            size_hint_y: None
            height:  '35sp'
            padding: 20, 5, 0, 0
            spacing: 10
            Button:
                text: 'stop'
                size_hint_x: None
                width: self.texture_size[0] + 30
                on_release: root.stop(self)
        
    BoxLayout:
        size_hint_y: None
        height:  '35sp'
        padding: 0, 5, 0, 0
        spacing: 10
        canvas:
            Color:
                rgba: 0.6, 0.6, 0.53, 1
            Rectangle:    
                size: self.size
                pos: self.pos

        Label:
            text: 'input rate'

        Label:
            id: input_rate
            text: '0.0 Kbits/sec'

    BoxLayout:
        size_hint_y: None
        height:  '35sp'
        padding: 0, 5, 0, 0
        spacing: 10
        canvas:
            Color:
                rgba: 0.6, 0.6, 0.53, 1
            Rectangle:    
                size: self.size
                pos: self.pos

        Label:
            text: 'output rate'

        Label:
            id: output_rate
            text: '0.0 Kbits/sec'

    BoxLayout:


<CustomDropDownQTech>:
    Button:
        text: 'QTech_2800'
        size_hint_y: None
        height: 30
        on_release: root.select(self.text)


<QTech>:
    size_hint: None, None
    size_hint: (1, 1)
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            id: change_device
            padding: 5, 5, 5, 15
            size_hint_y: None
            height: '50sp'
            spacing: 10

        ScrollView:
            bar_width: 8
            size_hint_y: 0.9
            padding: 5, 20, 5, 5
            BoxLayout:
                id: DeviceQTechBox
                padding: 5, 5, 5, 5
                orientation: 'vertical'
                spacing: 10
                size_hint_y: None
                height: self.minimum_height


<QTechBox2800>:
    orientation: 'vertical'
    size_hint_y: None
    height: self.minimum_height
    BoxLayout:
        size_hint_y: None
        height:  '35sp'
        padding: 0, 5, 0, 0
        spacing: 10
        TextInput:
            id: search
            text: ''
            hint_text: 'search'
            multiline: False
            halign: 'center'
            size_hint_x: None
            width: str(len(self.hint_text)+14) + '0' + 'sp'
            on_text: root.validate_search(self, self.text, 18)
            on_focus: root.focus_search(self, self.text)

    BoxLayout:
        size_hint_y: None
        height:  '35sp'
        padding: 0, 5, 0, 0
        spacing: 10
        Button:
            text: 'show version'
            hint_text: 'show version'
            size_hint_x: None
            width: self.texture_size[0] + 30
            on_release: root.commands_telnet(self, self.hint_text)

        Button:
            text: 'show vlan'
            hint_text: 'show vlan'
            size_hint_x: None
            width: self.texture_size[0] + 30
            on_release: root.commands_telnet(self, self.hint_text)

        Button:
            text: 'sh log bu level warn'
            hint_text: 'sh log bu le wa'
            size_hint_x: None
            width: self.texture_size[0] + 30
            on_release: root.commands_telnet(self, self.hint_text)

    BoxLayout:
        size_hint_y: None
        height:  '30sp'
        BoxLayout:
            Button:
                text: 'sh log bu level warning'
                hint_text: 'sh log bu le wa | include {add_text}'
                size_hint_x: None
                width: self.texture_size[0] + 40
                on_release: root.commands_telnet(self, self.hint_text, add_text=sh_log.text )

            TextInput:
                id: sh_log
                text: ''
                hint_text: 'x/x/xx'
                multiline: False
                halign: 'center'
                size_hint_x: None
                width:  str(len(self.hint_text)+2) + '0' + 'sp'
                on_text: root.validate(self, self.text, len(self.hint_text))

    BoxLayout:
        size_hint_y: None
        height:  '35sp'
        padding: 0, 5, 0, 0
        spacing: 10
        Button:
            text: 'show running-config'
            hint_text: 'show running-config'
            size_hint_x: None
            width: self.texture_size[0] + 40
            on_release: root.commands_telnet(self, self.hint_text)

    BoxLayout:
        size_hint_y: None
        height:  '30sp'
        spacing: 10
        Button:
            text: 'sh int eth status'
            hint_text: 'sh int eth st'
            size_hint_x: None
            width: self.texture_size[0] + 40
            on_release: root.commands_telnet(self, self.hint_text)

        Button:
            text: 'sh mac-address-table'
            hint_text: 'sh mac-address-table'
            size_hint_x: None
            width: self.texture_size[0] + 40
            on_release: root.commands_telnet(self, self.hint_text)

    BoxLayout:
        size_hint_y: None
        height:  '35sp'
        padding: 0, 5, 0, 0
        BoxLayout:
            Button:
                text: 'show interface ethernet '
                hint_text: 'sh interface ethernet {add_text}'
                size_hint_x: None
                width: self.texture_size[0] + 40
                on_release: root.commands_telnet(self, self.hint_text, add_text=sh_int_eth.text )

            TextInput:
                id: sh_int_eth
                text: ''
                hint_text: 'x/x/xx'
                multiline: False
                halign: 'center'
                size_hint_x: None
                width:  str(len(self.hint_text)+2) + '0' + 'sp'
                on_text: root.validate(self, self.text, len(self.hint_text))

    BoxLayout:
        size_hint_y: None
        height:  '30sp'
        BoxLayout:
            Button:
                text: 'sh mac-address-table interface ethernet '
                hint_text: 'sh mac-address-table interface ethernet {add_text}'
                size_hint_x: None
                width: self.texture_size[0] + 40
                on_release: root.commands_telnet(self, self.hint_text, add_text=sh_mac_int_eth.text )

            TextInput:
                id: sh_mac_int_eth
                text: ''
                hint_text: 'x/x/xx'
                multiline: False
                halign: 'center'
                size_hint_x: None
                width:  str(len(self.hint_text)+2) + '0' + 'sp'
                on_text: root.validate(self, self.text, len(self.hint_text))

    BoxLayout:
        size_hint_y: None
        height:  '30sp'
        BoxLayout:
            Button:
                text: 'sh mac-address-table address '
                hint_text: 'sh mac-address-table address {add_text}'
                size_hint_x: None
                width: self.texture_size[0] + 40
                on_release: root.commands_telnet(self, self.hint_text, add_text=sh_mac_address.text )

            TextInput:
                id: sh_mac_address
                text: ''
                hint_text: 'xx-xx-xx-xx-xx-xx'
                multiline: False
                halign: 'center'
                size_hint_x: None
                width:  str(len(self.hint_text)) + '0' + 'sp'
                on_text: root.validate_mac(self, self.text, len(self.hint_text), value='-', number=2)

    BoxLayout:
        size_hint_y: None
        height:  '30sp'
        BoxLayout:
            Button:
                text: 'sh mac-address-table vlan '
                hint_text: 'sh mac-address-table vlan {add_text}'
                size_hint_x: None
                width: self.texture_size[0] + 40
                on_release: root.commands_telnet(self, self.hint_text, add_text=sh_mac_vlan.text )

            TextInput:
                id: sh_mac_vlan
                text: ''
                hint_text: 'xxxx'
                multiline: False
                halign: 'center'
                size_hint_x: None
                width:  str(len(self.hint_text)+2) + '0' + 'sp'
                on_text: root.validate(self, self.text, len(self.hint_text))

    BoxLayout:
        size_hint_y: None
        height:  '30sp'
        BoxLayout:
            Button:
                text: 'virtual-cable-test int eth '
                hint_text: 'virtual-cable-test int eth {add_text}'
                size_hint_x: None
                width: self.texture_size[0] + 40
                on_release: root.commands_telnet(self, self.hint_text, add_text=virtual_cable_test.text, timeout=3 )

            TextInput:
                id: virtual_cable_test
                text: ''
                hint_text: 'x/x/xx'
                multiline: False
                halign: 'center'
                size_hint_x: None
                width:  str(len(self.hint_text)+2) + '0' + 'sp'
                on_text: root.validate(self, self.text, len(self.hint_text))

    BoxLayout:
        size_hint_y: None
        height:  '35sp'
        padding: 0, 5, 0, 0
        BoxLayout:
            Button:
                text: 'clear counters '
                hint_text: 'clear counters'
                size_hint_x: None
                width: self.texture_size[0] + 40
                on_release: root.commands_telnet(self, self.hint_text )

    BoxLayout:
        size_hint_y: None
        height:  '30sp'
        Button:
            text: 'clear counters int eth '
            hint_text: 'clear counters int eth  {add_text}'
            size_hint_x: None
            width: self.texture_size[0] + 40
            on_release: root.commands_telnet(self, self.hint_text, add_text=clear_counters.text )

        TextInput:
            id: clear_counters
            text: ''
            hint_text: 'x/x/xx'
            multiline: False
            halign: 'center'
            size_hint_x: None
            width:  str(len(self.hint_text)+2) + '0' + 'sp'
            on_text: root.validate(self, self.text, len(self.hint_text))

    BoxLayout:
        size_hint_y: None
        height:  '30sp'
        BoxLayout:
            Button:
                text: 'clear mac-address-table dynamic int eth '
                hint_text: 'clear mac-address-table dynamic interface ethernet {add_text}'
                size_hint_x: None
                width: self.texture_size[0] + 40
                on_release: root.commands_telnet(self, self.hint_text, add_text=clear_mac.text )

            TextInput:
                id: clear_mac
                text: ''
                hint_text: 'x/x/xx'
                multiline: False
                halign: 'center'
                size_hint_x: None
                width:  str(len(self.hint_text)+2) + '0' + 'sp'
                on_text: root.validate(self, self.text, len(self.hint_text))

    BoxLayout:
        size_hint_y: None
        height:  '35sp'
        padding: 0, 5, 0, 0
        BoxLayout:
            Button:
                text: 'show ip dhcp snooping binding all'
                hint_text: 'show ip dhcp snooping binding all'
                size_hint_x: None
                width: self.texture_size[0] + 40
                on_release: root.commands_telnet(self, self.hint_text )

    BoxLayout:
        size_hint_y: None
        height:  '30sp'
        BoxLayout:
            Button:
                text: 'show ip dhcp snooping interface ethernet '
                hint_text: 'show ip dhcp snooping interface ethernet {add_text}'
                size_hint_x: None
                width: self.texture_size[0] + 40
                on_release: root.commands_telnet(self, self.hint_text, add_text=show_ip_dhcp.text )

            TextInput:
                id: show_ip_dhcp
                text: ''
                hint_text: 'x/x/xx'
                multiline: False
                halign: 'center'
                size_hint_x: None
                width:  str(len(self.hint_text)+2) + '0' + 'sp'
                on_text: root.validate(self, self.text, len(self.hint_text))

    BoxLayout:
        size_hint_y: None
        height:  '35sp'
        padding: 0, 5, 0, 0
        BoxLayout:
            Button:
                text: 'show int eth counter packet'
                hint_text: 'show interface ethernet counter packet'
                size_hint_x: None
                width: self.texture_size[0] + 40
                on_release: root.commands_telnet(self, self.hint_text )

    BoxLayout:
        size_hint_y: None
        height:  '30sp'
        BoxLayout:
            Button:
                text: 'show int eth counter rate'
                hint_text: 'show interface ethernet counter rate'
                size_hint_x: None
                width: self.texture_size[0] + 40
                on_release: root.commands_telnet(self, self.hint_text )

    BoxLayout:
""")