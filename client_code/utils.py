from anvil import *
import anvil.server
import re

def populate_content_panel(content_panel, lexical_items, open_item_function, word_class=False, is_grid=False, num_columns=3):
    content_panel.clear()
    for index, item in enumerate(lexical_items):
        if word_class:
            content_link = Link(text=f"{index+1}. {item[0]}", role='text-link')
        else:
            content_link = Link(text=f"{index+1}. {item}", role='text-link')
        
        content_link.tag.main_heading = item
        content_link.set_event_handler('click', lambda sender, word_class=word_class, **event_args: open_item_function(sender, word_class=word_class, **event_args))
        
        if is_grid:
            row = f"row_{index // num_columns}"
            col_xs = index % num_columns
            content_panel.add_component(content_link, row=row, col_xs=col_xs, width_xs=4.5)
        else:
            content_panel.add_component(content_link)
    
    content_panel.tag.loaded = True

def open_lexical_item(sender, word_class=False, **event_args):
    if not word_class:
        user_input = sender.tag.main_heading
        results = anvil.server.call('get_lexical_item_details', user_input)
        
    else:
        user_input = sender.tag.main_heading[0]
        results = anvil.server.call('get_lexical_item_details', user_input)
      
    open_form('LexicalItem', item_panel_role='elevated-card', item_panel_visibility=True, data=results)

def check_password():
      password_box = TextBox(placeholder="Enter password", role="outlined", hide_text=True)
      result = alert(
          content=password_box,
          title="Password Required",
          buttons=[("OK", True), ("Cancel", False)],
      )
      if result:
          if password_box.text == '123':
            return True
          else:
            return 'wrong'
      else:
          return False


def drop_down_change(self, panel, **event_args):      #filter by word class
        selected_value = self.drop_down.selected_value
        
        if selected_value:
          if selected_value !='All':
            search_key = re.split(r'\s+', selected_value)[0]
            matching_items = [item for item in self.headwords if search_key == item[1]]
            print(f"Selected value: {search_key}")
            print(f"Headwords: {self.headwords}")
            print(f"Matching items: {matching_items}")
            populate_content_panel(panel, matching_items, open_lexical_item, word_class=True, is_grid=True)
          else:
            populate_content_panel(panel, self.headwords, open_lexical_item, word_class=False, is_grid=True)


