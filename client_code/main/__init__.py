from ._anvil_designer import mainTemplate
from anvil import *
import plotly.graph_objects as go
from ..homepage import homepage
from ..LexicalItem import LexicalItem
import anvil.server
from ..LexicalItem_List import LexicalItem_List

class main(mainTemplate):
    def __init__(self, **properties):
        # 初始化组件
        self.init_components(**properties)
        self.content_panel.add_component(homepage(), full_width_row=True)
        self.add_letter_links()
       

    def link_3_click(self, **event_args):
      open_form('main')

    def link_2_click(self, **event_args):
      """This method is called when the link is clicked"""
      pass

    def add_letter_links(self):
        self.letter_links = {}
      
        # Add links for each letter
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for index, letter in enumerate(letters):
            link = Link(text=letter, align="center")
            link.set_event_handler('click', self.on_letter_click)
            self.letter_links[letter] = link
            
            # Alternate links between the two columns
            if index % 2 == 0:
                self.column_1.add_component(link)
            else:
                self.column_2.add_component(link)
        

    def on_letter_click(self, sender, **event_args):
        letter = sender.text
        self.content_panel.clear()
        lexical_item_list = LexicalItem_List()
        self.content_panel.add_component(lexical_item_list, full_width_row=True)
        lexical_item_list.setup_list(letter)
 
