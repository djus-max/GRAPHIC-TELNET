from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from eventdispatcher import EventDispatcherCLI, MainDevice

from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button

import sys

class DLink(BoxLayout, MainDevice):
    search = ''
    list_button = []
    def __init__(self, **kwargs):
        super(DLink, self).__init__(**kwargs)
        self.prompt = b"# "
        self.build()
        DLink_3100.change_widget(self, self.mainbutton, self.mainbutton.text)


    def build(self):
        self.dropdown = CustomDropDownDLink()
        self.mainbutton = Button(text='DLink_3100', background_normal= '',
                    background_color=self.black, size_hint_x=None, width=130) 
        self.mainbutton.bind(on_release=self.dropdown.open)
        self.dropdown.bind(on_select=self.change_device)
        self.list_button.append(self.mainbutton)
        self.ids.change_device.add_widget(self.mainbutton)
    

    def change_device(self, instance, text):
        cli_device = getattr(sys.modules[__name__], text)
        cli_device.change_widget(self, instance, text)


class CustomDropDownDLink(DropDown ):
    pass


class Trafick:
    @classmethod
    def change_widget(cls, self, instance,  text):
        self.ids.DeviceDLinkBox.clear_widgets()
        cls.TrafickDLinkBox = TrafickDLinkBox()
        self.ids.DeviceDLinkBox.add_widget(cls.TrafickDLinkBox)

        for item in self.list_button:
            item.background_color=self.grey
        instance.background_color=self.black


class TrafickDLinkBox(BoxLayout, MainDevice):
    pass

class DLink_3100:
    @classmethod
    def change_widget(cls, self, instance, text):
        self.ids.DeviceDLinkBox.clear_widgets()
        cls.DLink_3100Box = DLink_3100Box()
        self.ids.DeviceDLinkBox.add_widget(cls.DLink_3100Box)

        for item in self.list_button:
            item.background_color=self.grey
        
        self.mainbutton.text = text
        self.mainbutton.background_color=self.black


class DLink_3200:
    @classmethod
    def change_widget(cls, self, instance, text):
        self.ids.DeviceDLinkBox.clear_widgets()
        cls.DLink_3200Box = DLink_3200Box()
        self.ids.DeviceDLinkBox.add_widget(cls.DLink_3200Box)

        for item in self.list_button:
            item.background_color=self.grey
        
        self.mainbutton.text = text
        self.mainbutton.background_color=self.black


class DeviceDLinkBox(BoxLayout):
    pass


class DLink_3100Box(BoxLayout, MainDevice):
    pass


class DLink_3200Box(BoxLayout, MainDevice):
    pass


Builder.load_string("""
<TrafickDLinkBox>:
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
                text: 'DLink'

    BoxLayout:



<CustomDropDownDLink>:
    Button:
        text: 'DLink_3100'
        size_hint_y: None
        height: 30
        on_release: root.select(self.text)

    Button:
        text: 'DLink_3200'
        size_hint_y: None
        height: 30
        on_release: root.select(self.text)


<DLink>:
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
                id: DeviceDLinkBox
                padding: 5, 5, 5, 5
                orientation: 'vertical'
                spacing: 1
                size_hint_y: None
                height: self.minimum_height


<DLink_3100Box>:
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
        padding: (0, 5, 0, 0)
        spacing: 10
        Button:
            text: 'show switch'
            hint_text: 'show switch'
            size_hint_x: None
            width: self.texture_size[0] + 40
            on_release: root.commands_telnet(self, self.hint_text)

        Button:
            text: 'show time'
            hint_text: 'show time'
            size_hint_x: None
            width: self.texture_size[0] + 30
            on_release: root.commands_telnet(self, self.hint_text)

        Button:
            text: 'show fdb'
            hint_text: 'show fdb'
            size_hint_x: None
            width: self.texture_size[0] + 40
            on_release: root.commands_telnet(self, self.hint_text)

    BoxLayout:
        size_hint_y: None
        height:  '35sp'
        padding: 0, 5, 0, 0
        spacing: 5
        Button:
            text: 'show log'
            hint_text: 'show log'
            size_hint_x: None
            width: self.texture_size[0] + 40
            on_release: root.commands_telnet(self, self.hint_text)

    BoxLayout:
        size_hint_y: None
        height:  '30sp'
        Button:
            text: 'show ports'
            hint_text: 'show ports'
            size_hint_x: None
            width: self.texture_size[0] + 40
            on_release: root.commands_telnet(self, self.hint_text)

    BoxLayout:
        padding: 0, 5, 0, 0
        size_hint_y: None
        height:  '35sp'
        BoxLayout:
            Button:
                text: 'show ports '
                hint_text: 'show ports {add_text}'
                size_hint_x: None
                width: self.texture_size[0] + 40
                on_release: root.commands_telnet(self, self.hint_text, add_text=show_ports.text )

            TextInput:
                id: show_ports
                text: ''
                hint_text: 'xx'
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
                text: 'show fdb port '
                hint_text: 'show fdb port {add_text}'
                size_hint_x: None
                width: self.texture_size[0] + 40
                on_release: root.commands_telnet(self, self.hint_text, add_text=show_fdb_port.text )

            TextInput:
                id: show_fdb_port
                text: ''
                hint_text: 'xx'
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
                text: 'show fdb mac_address '
                hint_text: 'show fdb mac_address {add_text}'
                size_hint_x: None
                width: self.texture_size[0] + 40
                on_release: root.commands_telnet(self, self.hint_text, add_text=show_fdb_mac_address.text )

            TextInput:
                id: show_fdb_mac_address
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
                text: 'show fdb vlanid '
                hint_text: 'show fdb vlanid {add_text}'
                size_hint_x: None
                width: self.texture_size[0] + 40
                on_release: root.commands_telnet(self, self.hint_text, add_text=show_fdb_vlanid.text )

            TextInput:
                id: show_fdb_vlanid
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

        Button:
            text: 'cable_diag ports '
            hint_text: 'cable_diag ports {add_text}'
            size_hint_x: None
            width: self.texture_size[0] + 30
            on_release: root.commands_telnet(self, self.hint_text, add_text=cable_diag_ports.text )

        TextInput:
            id: cable_diag_ports
            text: ''
            hint_text: 'xx'
            multiline: False
            halign: 'center'
            size_hint_x: None
            width:  str(len(self.hint_text)+2) + '0' + 'sp'
            on_text: root.validate(self, self.text, len(self.hint_text))

    BoxLayout:
        padding: 0, 5, 0, 0
        size_hint_y: None
        height:  '35sp'
        BoxLayout:
            Button:
                text: 'show error ports '
                hint_text: 'show error ports {add_text}'
                size_hint_x: None
                width: self.texture_size[0] + 40
                on_release: root.commands_telnet(self, self.hint_text, add_text=show_error_ports.text )

            TextInput:
                id: show_error_ports
                text: ''
                hint_text: 'xx'
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
                text: 'show packet ports '
                hint_text: 'show packet ports {add_text}'
                size_hint_x: None
                width: self.texture_size[0] + 40
                on_release: root.commands_telnet(self, self.hint_text, add_text=show_packet_ports.text )

            TextInput:
                id: show_packet_ports
                text: ''
                hint_text: 'xx'
                multiline: False
                halign: 'center'
                size_hint_x: None
                width:  str(len(self.hint_text)+2) + '0' + 'sp'
                on_text: root.validate(self, self.text, len(self.hint_text))

    BoxLayout:
        padding: 0, 5, 0, 0
        size_hint_y: None
        height:  '35sp'
        BoxLayout:
            Button:
                text: 'clear counters ports '
                hint_text: 'clear counters ports  {add_text}'
                size_hint_x: None
                width: self.texture_size[0] + 40
                on_release: root.commands_telnet(self, self.hint_text, add_text=clear_counters_ports.text )

            TextInput:
                id: clear_counters_ports
                text: ''
                hint_text: 'xx'
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
                text: 'clear fdb port '
                hint_text: 'clear fdb port {add_text}'
                size_hint_x: None
                width: self.texture_size[0] + 40
                on_release: root.commands_telnet(self, self.hint_text, add_text=clear_fdb_port.text )

            TextInput:
                id: clear_fdb_port
                text: ''
                hint_text: 'xx'
                multiline: False
                halign: 'center'
                size_hint_x: None
                width:  str(len(self.hint_text)+2) + '0' + 'sp'
                on_text: root.validate(self, self.text, len(self.hint_text))

    BoxLayout:
        padding: 0, 5, 0, 0
        size_hint_y: None
        height:  '35sp'
        BoxLayout:
            Button:
                text: 'show lldp remote_ports'
                hint_text: 'show lldp remote_ports'
                size_hint_x: None
                width: self.texture_size[0] + 40
                on_release: root.commands_telnet(self, self.hint_text )

    BoxLayout:


<DLink_3200Box>:
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
        padding: (0, 5, 0, 0)
        spacing: 10
        Button:
            text: 'show switch'
            hint_text: 'show switch'
            size_hint_x: None
            width: self.texture_size[0] + 40
            on_release: root.commands_telnet(self, self.hint_text)

        Button:
            text: 'show time'
            hint_text: 'show time'
            size_hint_x: None
            width: self.texture_size[0] + 30
            on_release: root.commands_telnet(self, self.hint_text)

        Button:
            text: 'show fdb'
            hint_text: 'show fdb'
            size_hint_x: None
            width: self.texture_size[0] + 40
            on_release: root.commands_telnet(self, self.hint_text)

    BoxLayout:
        size_hint_y: None
        height:  '35sp'
        padding: 0, 5, 0, 0
        spacing: 5
        Button:
            text: 'show log'
            hint_text: 'show log'
            size_hint_x: None
            width: self.texture_size[0] + 40
            on_release: root.commands_telnet(self, self.hint_text)

    BoxLayout:
        size_hint_y: None
        height:  '30sp'
        Button:
            text: 'show ports'
            hint_text: 'show ports'
            size_hint_x: None
            width: self.texture_size[0] + 40
            on_release: root.commands_telnet(self, self.hint_text)

    BoxLayout:
        padding: 0, 5, 0, 0
        size_hint_y: None
        height:  '35sp'
        BoxLayout:
            Button:
                text: 'show ports '
                hint_text: 'show ports {add_text}'
                size_hint_x: None
                width: self.texture_size[0] + 40
                on_release: root.commands_telnet(self, self.hint_text, add_text=show_ports.text )

            TextInput:
                id: show_ports
                text: ''
                hint_text: 'xx'
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
                text: 'show fdb port '
                hint_text: 'show fdb port {add_text}'
                size_hint_x: None
                width: self.texture_size[0] + 40
                on_release: root.commands_telnet(self, self.hint_text, add_text=show_fdb_port.text )

            TextInput:
                id: show_fdb_port
                text: ''
                hint_text: 'xx'
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
                text: 'show fdb mac_address '
                hint_text: 'show fdb mac_address {add_text}'
                size_hint_x: None
                width: self.texture_size[0] + 40
                on_release: root.commands_telnet(self, self.hint_text, add_text=show_fdb_mac_address.text )

            TextInput:
                id: show_fdb_mac_address
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
                text: 'show fdb vlanid '
                hint_text: 'show fdb vlanid {add_text}'
                size_hint_x: None
                width: self.texture_size[0] + 40
                on_release: root.commands_telnet(self, self.hint_text, add_text=show_fdb_vlanid.text )

            TextInput:
                id: show_fdb_vlanid
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
        Button:
            text: 'cable diag ports '
            hint_text: 'cable diag port {add_text}'
            size_hint_x: None
            width: self.texture_size[0] + 30
            on_release: root.commands_telnet(self, self.hint_text, add_text=cable_diag_port.text )

        TextInput:
            id: cable_diag_port
            text: ''
            hint_text: 'xx'
            multiline: False
            halign: 'center'
            size_hint_x: None
            width:  str(len(self.hint_text)+2) + '0' + 'sp'
            on_text: root.validate(self, self.text, len(self.hint_text))

    BoxLayout:
        padding: 0, 5, 0, 0
        size_hint_y: None
        height:  '35sp'
        BoxLayout:
            Button:
                text: 'show error ports '
                hint_text: 'show error ports {add_text}'
                size_hint_x: None
                width: self.texture_size[0] + 40
                on_release: root.commands_telnet(self, self.hint_text, add_text=show_error_ports.text )

            TextInput:
                id: show_error_ports
                text: ''
                hint_text: 'xx'
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
                text: 'show packet ports '
                hint_text: 'show packet ports {add_text}'
                size_hint_x: None
                width: self.texture_size[0] + 40
                on_release: root.commands_telnet(self, self.hint_text, add_text=show_packet_ports.text )

            TextInput:
                id: show_packet_ports
                text: ''
                hint_text: 'xx'
                multiline: False
                halign: 'center'
                size_hint_x: None
                width:  str(len(self.hint_text)+2) + '0' + 'sp'
                on_text: root.validate(self, self.text, len(self.hint_text))

    BoxLayout:
        padding: 0, 5, 0, 0
        size_hint_y: None
        height:  '35sp'
        BoxLayout:
            Button:
                text: 'clear counters ports '
                hint_text: 'clear counters ports  {add_text}'
                size_hint_x: None
                width: self.texture_size[0] + 40
                on_release: root.commands_telnet(self, self.hint_text, add_text=clear_counters_ports.text )

            TextInput:
                id: clear_counters_ports
                text: ''
                hint_text: 'xx'
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
                text: 'clear fdb port '
                hint_text: 'clear fdb port {add_text}'
                size_hint_x: None
                width: self.texture_size[0] + 40
                on_release: root.commands_telnet(self, self.hint_text, add_text=clear_fdb_port.text )

            TextInput:
                id: clear_fdb_port
                text: ''
                hint_text: 'xx'
                multiline: False
                halign: 'center'
                size_hint_x: None
                width:  str(len(self.hint_text)+2) + '0' + 'sp'
                on_text: root.validate(self, self.text, len(self.hint_text))

    BoxLayout:
        padding: 0, 5, 0, 0
        size_hint_y: None
        height:  '35sp'
        BoxLayout:
            Button:
                text: 'show lldp remote_ports'
                hint_text: 'show lldp remote_ports'
                size_hint_x: None
                width: self.texture_size[0] + 40
                on_release: root.commands_telnet(self, self.hint_text )

    BoxLayout:
""")