from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from eventdispatcher import EventDispatcherCLI, MainDevice

from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button

import sys


class SNR(BoxLayout, MainDevice):
    search = ''
    list_button = []
    def __init__(self, **kwargs):
        super(SNR, self).__init__(**kwargs)
        self.prompt = b"# "
        self.build()
        SNR_2800.change_widget(self, self.mainbutton, self.mainbutton.text)


    def build(self):
        self.dropdown = CustomDropDownSNR()
        self.mainbutton = Button(text='SNR_2800', background_normal= '',
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


class CustomDropDownSNR(DropDown ):
    pass


class Trafick:
    @classmethod
    def change_widget(cls, self, instance,  text):
        self.ids.DeviceSNRBox.clear_widgets()
        cls.TrafickSNRBox = TrafickSNRBox()
        self.ids.DeviceSNRBox.add_widget(cls.TrafickSNRBox)

        for item in self.list_button:
            item.background_color=self.grey

        instance.background_color=self.black


class TrafickSNRBox(BoxLayout, MainDevice):
    pass

class SNR_2800:
    @classmethod
    def change_widget(cls, self, instance, text):
        self.ids.DeviceSNRBox.clear_widgets()
        cls.SNRBox2800 = SNRBox2800()
        self.ids.DeviceSNRBox.add_widget(cls.SNRBox2800)

        for item in self.list_button:
            item.background_color=self.grey
        
        self.mainbutton.text = text
        self.mainbutton.background_color=self.black


class DeviceSNRBox(BoxLayout):
    pass


class SNRBox2800(BoxLayout, MainDevice):
    pass


Builder.load_string("""
<TrafickSNRBox>:
    orientation: 'vertical'
    size_hint_y: None
    height: self.minimum_height
    BoxLayout:
        size_hint_y: None
        height:  '35sp'
        padding: 0, 5, 0, 0
        spacing: 10
        BoxLayout:
            Label:
                text: 'SNR'


<CustomDropDownSNR>:
    Button:
        text: 'SNR_2800'
        size_hint_y: None
        height: 30
        on_release: root.select(self.text)


<SNR>:
    size_hint: None, None
    size_hint: (1, 1)
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            id: change_device
            padding: 5, 5, 5, 5
            size_hint_y: None
            height: '40sp'
            spacing: 10

        ScrollView:
            bar_width: 8
            size_hint_y: 0.98
            BoxLayout:
                id: DeviceSNRBox
                padding: 5, 5, 5, 5
                orientation: 'vertical'
                spacing: 1
                size_hint_y: None
                height: self.minimum_height


<SNRBox2800>:
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
                on_release: root.commands_telnet(self, self.hint_text, add_text=virtual_cable_test.text )

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