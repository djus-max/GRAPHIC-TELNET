from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from eventdispatcher import EventDispatcherCLI, MainDevice

from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button

import sys

class CDATA(BoxLayout, MainDevice):
    search = ''
    list_button = []
    def __init__(self, **kwargs):
        super(CDATA, self).__init__(**kwargs)
        self.prompt = b"> "
        self.prompt_enable = b"# "
        self.build()
        CDATA_1.change_widget(self, self.mainbutton, self.mainbutton.text)


    def build(self):
        self.dropdown = CustomDropDownCDATA()
        self.mainbutton = Button(text='CDATA_1', background_normal= '',
                    background_color=self.black, size_hint_x=None, width=130) 
        self.mainbutton.bind(on_release=self.dropdown.open)
        self.dropdown.bind(on_select=self.change_device)
        self.list_button.append(self.mainbutton)
        self.ids.change_device.add_widget(self.mainbutton)


    def change_device(self, instance, text):
        cli_device = getattr(sys.modules[__name__], text)
        cli_device.change_widget(self, instance, text)

class CustomDropDownCDATA(DropDown ):
    pass


class Trafick:
    @classmethod
    def change_widget(cls, self, instance,  text):
        self.ids.DeviceCDATABox.clear_widgets()
        cls.TrafickCDATABox = TrafickCDATABox()
        self.ids.DeviceCDATABox.add_widget(cls.TrafickCDATABox)
        for item in self.list_button:
            item.background_color=self.grey
        instance.background_color=self.black

class TrafickCDATABox(BoxLayout, MainDevice):
    pass

class CDATA_1:
    @classmethod
    def change_widget(cls, self, instance, text):
        self.ids.DeviceCDATABox.clear_widgets()
        cls.CDATA_1Box = CDATA_1Box()
        self.ids.DeviceCDATABox.add_widget(cls.CDATA_1Box)

        for item in self.list_button:
            item.background_color=self.grey
        
        self.mainbutton.text = text
        self.mainbutton.background_color=self.black


class CDATA_3200:
    @classmethod
    def change_widget(cls, self, instance, text):
        self.ids.DeviceCDATABox.clear_widgets()
        cls.CDATA_3200Box = CDATA_3200Box()
        self.ids.DeviceCDATABox.add_widget(cls.CDATA_3200Box)

        for item in self.list_button:
            item.background_color=self.grey
        
        self.mainbutton.text = text
        self.mainbutton.background_color=self.black

class DeviceCDATABox(BoxLayout):
    pass


class CDATA_1Box(BoxLayout, MainDevice):
    pass


class CDATA_3200Box(BoxLayout, MainDevice):
    pass


Builder.load_string("""

<TrafickCDATABox>:
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
                text: 'CDATA'

    BoxLayout:


<CustomDropDownCDATA>:
    Button:
        text: 'CDATA_1'
        size_hint_y: None
        height: 30
        on_release: root.select(self.text)


<CDATA>:
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
                id: DeviceCDATABox
                padding: 5, 5, 5, 5
                orientation: 'vertical'
                spacing: 1
                size_hint_y: None
                height: self.minimum_height


<CDATA_1Box>:
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
        BoxLayout:
            Button:
                text: 'show system uptime'
                hint_text: 'show system uptime'
                size_hint_x: None
                width: self.texture_size[0] + 40
                on_release: root.commands_telnet(self, self.hint_text)

        BoxLayout:
            Button:
                text: 'show system log all'
                hint_text: 'show system log all'
                size_hint_x: None
                width: self.texture_size[0] + 40
                on_release: root.commands_telnet(self, self.hint_text)

    BoxLayout:
        size_hint_y: None
        height:  '30sp'
        BoxLayout:
            Button:
                text: 'show system log type onu-on-off-line'
                hint_text: 'show system log type onu-on-off-line'
                size_hint_x: None
                width: self.texture_size[0] + 40
                on_release: root.commands_telnet(self, self.hint_text)

    BoxLayout:
        spacing: 10
        size_hint_y: None
        height:  '35sp'
        padding: 0, 5, 0, 0
        BoxLayout:
            Button:
                text: 'show olt _X_ online'
                hint_text: 'show olt {add_text} online-onu '
                size_hint_x: None
                width: self.texture_size[0] + 30
                on_release: root.commands_telnet(self, self.hint_text, add_text=show_epon_active_onu.text )

            TextInput:
                id: show_epon_active_onu
                text: ''
                hint_text: 'xx'
                multiline: False
                halign: 'center'
                size_hint_x: None
                width:  str(len(self.hint_text)+2) + '0' + 'sp'
                on_text: root.validate(self, self.text, len(self.hint_text))

        BoxLayout:
            Button:
                text: 'show olt _X_ all-info'
                hint_text: 'show olt {add_text} all-onu-info '
                size_hint_x: None
                width: self.texture_size[0] + 30
                on_release: root.commands_telnet(self, self.hint_text, add_text=show_epon_onu_information.text )

            TextInput:
                id: show_epon_onu_information
                text: ''
                hint_text: 'xx'
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
                text: 'show onu-position '
                hint_text: 'show onu-position {add_text}'
                size_hint_x: None
                width: self.texture_size[0] + 40
                on_release: root.commands_telnet(self, self.hint_text, add_text=show_onu_position.text )

            TextInput:
                id: show_onu_position
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
                text: 'show mac-address-table mac'
                hint_text: 'show mac-address-table mac {add_text}'
                size_hint_x: None
                width: self.texture_size[0] + 40
                on_release: root.commands_telnet(self, self.hint_text, add_text=show_mac_address_table.text )

            TextInput:
                id: show_mac_address_table
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
                text: 'show olt _X_ mac-address _Y_'
                hint_text: 'show olt {add_text} mac-address {add_text_2} '
                size_hint_x: None
                width: self.texture_size[0] + 40
                on_release: root.commands_telnet(self, self.hint_text, add_text=show_olt_mac_address.text, add_text_2=show_olt_mac_address_onu.text )

            TextInput:
                id: show_olt_mac_address
                text: ''
                hint_text: 'xx'
                multiline: False
                halign: 'center'
                size_hint_x: None
                width:  str(len(self.hint_text)+2) + '0' + 'sp'
                on_text: root.validate(self, self.text, len(self.hint_text))

            TextInput:
                id: show_olt_mac_address_onu
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
                text: 'show olt _X_ mac-address-table _Y_ '
                hint_text: 'show olt {add_text} mac-address-table {add_text_2} '
                size_hint_x: None
                width: self.texture_size[0] + 40
                on_release: root.commands_telnet(self, self.hint_text, add_text=show_olt_mac_address_table.text, add_text_2=show_olt_mac_address_table_onu.text )

            TextInput:
                id: show_olt_mac_address_table
                text: ''
                hint_text: 'xx'
                multiline: False
                halign: 'center'
                size_hint_x: None
                width:  str(len(self.hint_text)+ 2) + '0' + 'sp'
                on_text: root.validate(self, self.text, len(self.hint_text))

            TextInput:
                id: show_olt_mac_address_table_onu
                text: ''
                hint_text: 'xx'
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
                text: 'show olt _X_ optical-online-onu'
                hint_text: 'show olt {add_text} optical-online-onu'
                size_hint_x: None
                width: self.texture_size[0] + 40
                on_release: root.commands_telnet(self, self.hint_text, add_text=show_olt_optical_online_onu.text )

            TextInput:
                id: show_olt_optical_online_onu
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
                text: 'show olt _X_ onu _Y_ ctc optical '
                hint_text: 'show olt {add_text} onu ctc optical  {add_text_2} '
                size_hint_x: None
                width: self.texture_size[0] + 40
                on_release: root.commands_telnet(self, self.hint_text, add_text=show_epon_optical_olt.text, add_text_2=show_epon_optical_interface.text )

            TextInput:
                id: show_epon_optical_olt
                text: ''
                hint_text: 'xx'
                multiline: False
                halign: 'center'
                size_hint_x: None
                width:  str(len(self.hint_text)+ 2) + '0' + 'sp'
                on_text: root.validate(self, self.text, len(self.hint_text))

            TextInput:
                id: show_epon_optical_interface
                text: ''
                hint_text: 'xx'
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
                text: 'show olt_X_ onu_Y_ uni _Z_ ctc attr'
                hint_text: 'show olt {add_text} onu {add_text_2} uni {add_text_3} ctc attribute'
                size_hint_x: None
                width: self.texture_size[0] + 35
                on_release: root.commands_telnet(self, self.hint_text, add_text=show_olt_attribute_ctc.text, add_text_2=show_olt_attribute_ctc_onu.text,  add_text_3=show_olt_attribute_ctc_onu_port.text)

            TextInput:
                id: show_olt_attribute_ctc
                text: ''
                hint_text: 'xx'
                multiline: False
                halign: 'center'
                size_hint_x: None
                width:  str(len(self.hint_text)+ 2) + '0' + 'sp'
                on_text: root.validate(self, self.text, len(self.hint_text))

            TextInput:
                id: show_olt_attribute_ctc_onu
                text: ''
                hint_text: 'xx'
                multiline: False
                halign: 'center'
                size_hint_x: None
                width:  str(len(self.hint_text)+2) + '0' + 'sp'
                on_text: root.validate(self, self.text, len(self.hint_text))
            
            TextInput:
                id: show_olt_attribute_ctc_onu_port
                text: '1'
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
                text: 'show olt_X_ onu_Y_ uni_Z_ ctc vlan-mode'
                hint_text: 'show olt {add_text} onu {add_text_2} uni {add_text_3} ctc vlan-mode'
                size_hint_x: None
                width: self.texture_size[0] + 35
                on_release: root.commands_telnet(self, self.hint_text, add_text=show_olt_attribute_vlan_mode.text, add_text_2=show_olt_attribute_ctc_vlan_mode_onu.text,  add_text_3=show_olt_attribute_ctc_onu_vlan_mode_port.text)

            TextInput:
                id: show_olt_attribute_vlan_mode
                text: ''
                hint_text: 'xx'
                multiline: False
                halign: 'center'
                size_hint_x: None
                width:  str(len(self.hint_text)+ 2) + '0' + 'sp'
                on_text: root.validate(self, self.text, len(self.hint_text))

            TextInput:
                id: show_olt_attribute_ctc_vlan_mode_onu
                text: ''
                hint_text: 'xx'
                multiline: False
                halign: 'center'
                size_hint_x: None
                width:  str(len(self.hint_text)+2) + '0' + 'sp'
                on_text: root.validate(self, self.text, len(self.hint_text))
            
            TextInput:
                id: show_olt_attribute_ctc_onu_vlan_mode_port
                text: '1'
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
                text: 'show olt_X_ onu_Y_ uni_Z_ ctc statist'
                hint_text: 'show olt {add_text} onu {add_text_2} uni {add_text_3} ctc current-period-statistics'
                size_hint_x: None
                width: self.texture_size[0] + 35
                on_release: root.commands_telnet(self, self.hint_text, add_text=show_olt_attribute_statistics.text, add_text_2=show_olt_attribute_ctc_statistics_onu.text,  add_text_3=show_olt_attribute_ctc_onu_statistics_port.text)

            TextInput:
                id: show_olt_attribute_statistics
                text: ''
                hint_text: 'xx'
                multiline: False
                halign: 'center'
                size_hint_x: None
                width:  str(len(self.hint_text)+ 2) + '0' + 'sp'
                on_text: root.validate(self, self.text, len(self.hint_text))

            TextInput:
                id: show_olt_attribute_ctc_statistics_onu
                text: ''
                hint_text: 'xx'
                multiline: False
                halign: 'center'
                size_hint_x: None
                width:  str(len(self.hint_text)+2) + '0' + 'sp'
                on_text: root.validate(self, self.text, len(self.hint_text))
            
            TextInput:
                id: show_olt_attribute_ctc_onu_statistics_port
                text: '1'
                hint_text: 'xx'
                multiline: False
                halign: 'center'
                size_hint_x: None
                width:  str(len(self.hint_text)+2) + '0' + 'sp'
                on_text: root.validate(self, self.text, len(self.hint_text))

    BoxLayout:
""")