from ._anvil_designer import mainTemplate
from anvil import *
import plotly.graph_objects as go
from ..homepage import homepage
from ..map import map
import anvil.server
from ..LexicalItem_List import LexicalItem_List
from ..word import word
from ..suggestion_list import suggestion_list
from ..entry_edit import entry_edit
from ..about_us import about_us
from ..introduction import introduction

class main(mainTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.content_panel.add_component(homepage(), full_width_row=True)
        self.add_letter_links()
      
    def link_3_click(self, **event_args):
      open_form('main')

    def link_2_click(self, **event_args):
      self.add_map_to_content_panel()

    def add_map_to_content_panel(self):
      self.content_panel.clear()
      self.content_panel.add_component(map(), full_width_row=True)

    def add_letter_links(self):
        self.letter_links = {}
        # Add links for each letter
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for index, letter in enumerate(letters):
            link = Link(text=letter, align="center")
            link.set_event_handler('click', self.on_letter_click)
            self.letter_links[letter] = link
            
            if index % 2 == 0:
                self.column_1.add_component(link)
            else:
                self.column_2.add_component(link)
        
    def on_letter_click(self, sender, **event_args):
        if (self.link_lexis.role != "bordered" and
            self.link_theme.role != "bordered" and
            self.link_source.role != "bordered"):
            alert('Please select one list')
        else:
            letter = sender.text
            self.content_panel.clear()

            if self.link_lexis.role == "bordered":
                lexical_item_list = LexicalItem_List()
                lexical_item_list.explore_letter_list(letter)
            elif self.link_theme.role == "bordered":
                lexical_item_list = LexicalItem_List(lexis=False, theme=True)
                lexical_item_list.explore_theme_list(letter)
            elif self.link_source.role == "bordered":
                lexical_item_list = LexicalItem_List(lexis=False, theme=False, source=True)
                lexical_item_list.explore_source_list(letter)
            self.content_panel.add_component(lexical_item_list, full_width_row=True)
              
      
    def search_lexical_item(self, data):
        self.content_panel.clear()
        lexical_item_list = LexicalItem_List()
        self.content_panel.add_component(lexical_item_list, full_width_row=True)
        lexical_item_list.search_list(data)

    def link_suggest_click(self, **event_args):
        new_entry = {}
  
        while True:
            entry_form = entry_edit(item=new_entry)
            save_clicked = alert(
                content=entry_form,
                title="Add Entry",
                large=True,
                buttons=[("Submit", True), ("Cancel", False)]
            )
            
            if save_clicked:
                if entry_form.theme_box.selected_value:
                    entry_form.item['theme'] = anvil.server.call('get_main_heading_data_by_id', entry_form.theme_box.selected_value)
                if entry_form.section_heading_box.selected_value:
                    entry_form.item['subtheme'] = anvil.server.call('get_section_heading_data', entry_form.section_heading_box.selected_value)
                required_fields = ['english_headword', 'literal_meaning', 'metaphor_meaning', 'literal_word_class', 'metaphorical_word_class','english_example_sentence','dictionary', 'theme', 'subtheme']  # 添加所有必填字段
                empty_fields = [field for field in required_fields if not new_entry.get(field)]
                
                if empty_fields:
                    error_message = f"Please fill in these required fields: {', '.join(empty_fields)}"
                    alert(error_message)
                    continue 
                else:
                    result = anvil.server.call('add_new_lexical_item', new_entry)
                    if result['status'] == 'success':
                        alert('Suggestion submitted successfully!')                  
                        break  
                    else:
                        alert(f"Error adding entry: {result['message']}")
            else:
                break


    def reset_link_styles(self):
        self.link_lexis.role = "default"
        self.link_theme.role = "default"
        self.link_source.role = "default"
    
    def link_1_click(self, **event_args):
        self.content_panel.clear()
        suggestion_list_form = suggestion_list()
        self.content_panel.add_component(suggestion_list_form, full_width_row=True)

    def link_lexis_click(self, **event_args):
        self.reset_link_styles()
        self.link_lexis.role = "bordered"

    def link_theme_click(self, **event_args):
        self.reset_link_styles()
        self.link_theme.role = "bordered"

    def link_source_click(self, **event_args):
        self.reset_link_styles()
        self.link_source.role = "bordered"

    def bottom_about_link_click(self, **event_args):
      self.content_panel.clear()
      
      self.content_panel.add_component(about_us(), full_width_row=True)

    def link_4_click(self, **event_args):
      open_form('introduction')

    
        
