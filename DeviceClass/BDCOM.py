from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from eventdispatcher import EventDispatcherCLI, MainDevice

from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button

import sys

class BDCOM(BoxLayout, MainDevice):
    search = ''
    list_button = []

    def __init__(self, **kwargs):
        super(BDCOM, self).__init__(**kwargs)
        self.prompt = b"> "
        self.prompt_enable = b"# "
        self.build()
        BDCOM_1.change_widget(self, self.mainbutton, self.mainbutton.text)


    def build(self):
        self.dropdown = CustomDropDownBDCOM()
        self.mainbutton = Button(text='BDCOM_1', background_normal= '',
                    background_color=self.black, size_hint_x=None, width=130) 
        self.mainbutton.bind(on_release=self.dropdown.open)
        self.dropdown.bind(on_select=self.change_device)
        self.list_button.append(self.mainbutton)
        self.ids.change_device.add_widget(self.mainbutton)


    def change_device(self, instance, text):
        cli_device = getattr(sys.modules[__name__], text)
        cli_device.change_widget(self, instance, text)


class CustomDropDownBDCOM(DropDown ):
    pass


class Trafick:
    @classmethod
    def change_widget(cls, self, instance,  text):
        self.ids.DeviceBDCOMBox.clear_widgets()
        cls.TrafickBDCOMBox = TrafickBDCOMBox()
        self.ids.DeviceBDCOMBox.add_widget(cls.TrafickBDCOMBox)
        for item in self.list_button:
            item.background_color=self.grey
        instance.background_color=self.black


class TrafickBDCOMBox(BoxLayout, MainDevice):
    pass

class BDCOM_1:
    @classmethod
    def change_widget(cls, self, instance, text):
        self.ids.DeviceBDCOMBox.clear_widgets()
        cls.BDCOM_1Box = BDCOM_1Box()
        self.ids.DeviceBDCOMBox.add_widget(cls.BDCOM_1Box)

        for item in self.list_button:
            item.background_color=self.grey
        
        self.mainbutton.text = text
        self.mainbutton.background_color=self.black


class DeviceBDCOMBox(BoxLayout):
    pass

class BDCOM_1Box(BoxLayout, MainDevice):
    pass


Builder.load_string("""

<TrafickBDCOMBox>:
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
                text: 'BDCOM'

    BoxLayout:


<CustomDropDownBDCOM>:
    Button:
        text: 'BDCOM_1'
        size_hint_y: None
        height: 30
        on_release: root.select(self.text)


<BDCOM>:
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
                id: DeviceBDCOMBox
                padding: 5, 5, 5, 5
                orientation: 'vertical'
                spacing: 1
                size_hint_y: None
                height: self.minimum_height

<BDCOM_1Box>:
    orientation: 'vertical'
    spacing: 1
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
            size_hint_y: None
            height:  '30sp'
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
            width: self.texture_size[0] + 40
            on_release: root.commands_telnet(self, self.hint_text)

        Button:
            text: 'show logging'
            hint_text: 'show logging'
            size_hint_x: None
            width: self.texture_size[0] + 40
            on_release: root.commands_telnet(self, self.hint_text)

    BoxLayout:
        size_hint_y: None
        height:  '35sp'
        padding: 0, 5, 0, 0
        BoxLayout:
            Button:
                text: 'show epon active-onu interface EPON '
                hint_text: 'show epon active-onu interface EPON {add_text}'
                size_hint_x: None
                width: self.texture_size[0] + 40
                on_release: root.commands_telnet(self, self.hint_text, add_text=show_epon_active_onu.text )

            TextInput:
                id: show_epon_active_onu
                text: ''
                hint_text: 'x/xx'
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
                text: 'show epon onu-information interface EPON '
                hint_text: 'show epon onu-information interface EPON {add_text}'
                size_hint_x: None
                width: self.texture_size[0] + 40
                on_release: root.commands_telnet(self, self.hint_text, add_text=show_epon_onu_information.text )

            TextInput:
                id: show_epon_onu_information
                text: ''
                hint_text: 'x/xx'
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
                text: 'show mac address-table interface EPON'
                hint_text: 'show mac address-table interface EPON{add_text}'
                size_hint_x: None
                width: self.texture_size[0] + 40
                on_release: root.commands_telnet(self, self.hint_text, add_text=show_mac_address_table.text )

            TextInput:
                id: show_mac_address_table
                text: ''
                hint_text: 'x/xx:xx'
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
                text: 'show mac address-table '
                hint_text: 'show mac address-table {add_text}'
                size_hint_x: None
                width: self.texture_size[0] + 40
                on_release: root.commands_telnet(self, self.hint_text, add_text=show_mac_address.text )

            TextInput:
                id: show_mac_address
                text: ''
                hint_text: 'xxxx.xxxx.xxxx'
                multiline: False
                halign: 'center'
                size_hint_x: None
                width:  str(len(self.hint_text)) + '0' + 'sp'
                on_text: root.validate_mac(self, self.text, len(self.hint_text), value='.', number=4)

    BoxLayout:
        size_hint_y: None
        height:  '35sp'
        padding: 0, 5, 0, 0
        BoxLayout:
            Button:
                text: 'show epon optical-transc-diagnosis int EPON '
                hint_text: 'show epon optical-transceiver-diagnosis interface EPON {add_text}'
                size_hint_x: None
                width: self.texture_size[0] + 40
                on_release: root.commands_telnet(self, self.hint_text, add_text=show_epon_optical_interface.text )

            TextInput:
                id: show_epon_optical_interface
                text: ''
                hint_text: 'x/x:xx'
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
                text: 'sh epon int EPON_X_ onu ctc opt-transc-diag'
                hint_text: 'show epon interface EPON {add_text} onu ctc optical-transceiver-diagnosis'
                size_hint_x: None
                width: self.texture_size[0] + 40
                on_release: root.commands_telnet(self, self.hint_text, add_text=show_epon_int_optical.text )

            TextInput:
                id: show_epon_int_optical
                text: ''
                hint_text: 'x/x:xx'
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
                text: 'show epon interface EPON _X_ onu port 1 state '
                hint_text: 'show epon interface EPON {add_text} onu port 1 state '
                size_hint_x: None
                width: self.texture_size[0] + 40
                on_release: root.commands_telnet(self, self.hint_text, add_text=show_port_state.text )

            TextInput:
                id: show_port_state
                text: ''
                hint_text: 'x/x:xx'
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
                text: 'show logging | include '
                hint_text: 'show logging | include {add_text} '
                size_hint_x: None
                width: self.texture_size[0] + 40
                on_release: root.commands_telnet(self, self.hint_text, add_text=show_logging_include.text )

            TextInput:
                id: show_logging_include
                text: ''
                hint_text: 'epon0/x:xx__'
                multiline: False
                halign: 'center'
                size_hint_x: None
                width:  str(len(self.hint_text)+2) + '0' + 'sp'
                on_text: root.validate(self, self.text, len(self.hint_text))

    BoxLayout:
""")