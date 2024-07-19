from anvil import *
import anvil.server

def populate_content_panel(content_panel, lexical_items, open_item_function):
    for index, item in enumerate(lexical_items, start=1):
        content_link = Link(text=f"{index}. {item}", role='text-link')
        content_link.tag.main_heading = item
        content_link.set_event_handler('click', open_item_function)
        content_panel.add_component(content_link)
    content_panel.tag.loaded = True

def open_lexical_item(sender, **event_args):
    user_input = sender.tag.main_heading
    results = anvil.server.call('get_lexical_item_details', user_input)
    open_form('LexicalItem', item_panel_role='elevated-card', item_panel_visibility=True, data=results)
