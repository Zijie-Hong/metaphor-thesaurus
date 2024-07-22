from anvil import *
import anvil.server

def populate_content_panel(content_panel, lexical_items, open_item_function, is_grid=False, num_columns=4):
    content_panel.clear()
    
    for index, item in enumerate(lexical_items):
        content_link = Link(text=f"{index+1}. {item}", role='text-link')
        content_link.tag.main_heading = item
        content_link.set_event_handler('click', open_item_function)
        
        if is_grid:
            row = f"row_{index // num_columns}"
            col_xs = index % num_columns
            content_panel.add_component(content_link, row=row, col_xs=col_xs, width_xs=3)
        else:
            content_panel.add_component(content_link)
            
    content_panel.tag.loaded = True

def open_lexical_item(sender, **event_args):
    user_input = sender.tag.main_heading
    results = anvil.server.call('get_lexical_item_details', user_input)
    open_form('LexicalItem', item_panel_role='elevated-card', item_panel_visibility=True, data=results)

def check_password():
      password_box = TextBox(placeholder="Enter password", hide_text=True)
      result = alert(
          content=password_box,
          title="Password Required",
          buttons=[("OK", True), ("Cancel", False)],
      )
      if result:
          if password_box.text == '123':
            return True
          else:
            return False

