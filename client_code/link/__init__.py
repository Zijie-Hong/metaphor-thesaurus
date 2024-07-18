from ._anvil_designer import linkTemplate
from anvil import *
import anvil.server

class link(linkTemplate):
    def __init__(self, data=None, **properties):
        self.init_components(**properties)
        self.data = data
        self.related_headings_panel.clear()
        self.label_1.visible = False
        self.label_2.visible = False
        self.update_display()
        
    def update_display(self):
        if self.data:
            self.label_1.visible = True
            self.label_2.visible = True
            self.main_heading.text = self.data['main_heading']
            self.display_relationships()
 
    def display_relationships(self):
        self.results_panel.clear()
        relationships = anvil.server.call('get_relationships_by_main_heading_id', self.data['main_heading_id'])
        unique_relationships = {}
        for relationship in relationships:
            if relationship['relationship'] not in unique_relationships:
                unique_relationships[relationship['relationship']] = []
            unique_relationships[relationship['relationship']].append(relationship['related_heading'])

        for relationship, related_headings in unique_relationships.items():
            button = Button(text=relationship)
            button.tag.related_headings = related_headings
            button.set_event_handler('click', self.show_related_heading_list)
            self.results_panel.add_component(button)

    def show_related_heading_list(self, **event_args):
        button = event_args['sender']
        related_headings = button.tag.related_headings
        self.related_headings_panel.clear()
        for index, heading in enumerate(related_headings, start=1):
            link = Link(text=f"{index}. {heading}")
            link.tag.main_heading = heading
            link.set_event_handler('click', self.main_heading_click)
            self.related_headings_panel.add_component(link)

    def main_heading_click(self, sender, **event_args):
        main_heading = sender.tag.main_heading
        main_heading_data = anvil.server.call('get_main_heading_data_by_heading', main_heading)
        print(main_heading_data)
        if main_heading_data:
            open_form('LexicalItem', theme_panel_role='elevated-card', item_panel_visibility=False, data=main_heading_data)
            
