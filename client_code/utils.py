from anvil import *
import anvil.server
import re

def populate_content_panel(content_panel, items, open_item_function, theme=False, source=False, word_class=False, is_grid=False, num_columns=3, width_xs=4.5):
    content_panel.clear()
    seen = set()
    display_index = 1  # 新增：用于显示的连续索引

    for index, item in enumerate(items):
        if word_class:
            main_heading = item[0]
            if main_heading in seen:
                continue  # 如果已经处理过，跳过当前项目
            seen.add(main_heading)  # 记录这个词头已经添加过
        elif source:
            main_heading = ','.join(item)
        else:
            main_heading = item

        # 使用 display_index 而不是 index+1
        display_text = f"{display_index}. {main_heading}" if word_class or source else f"{display_index}. {item}"
        content_link = Link(text=display_text, role='text-link')
        
        content_link.tag.main_heading = item
        if theme:
            content_link.set_event_handler('click', lambda sender, source=source, **event_args: open_theme(sender, source=source, **event_args))
        else:
            content_link.set_event_handler('click', lambda sender, word_class=word_class, **event_args: open_item_function(sender, word_class=word_class, **event_args))
        
        if is_grid:
            row = f"row_{(display_index-1) // num_columns}"
            col_xs = (display_index-1) % num_columns
            content_panel.add_component(content_link, row=row, col_xs=col_xs, width_xs=width_xs)
        else:
            content_panel.add_component(content_link)
        
        display_index += 1  # 增加显示索引
    
    content_panel.tag.loaded = True

def open_lexical_item(sender, word_class=False, **event_args):
    if not word_class:
        user_input = sender.tag.main_heading
        results = anvil.server.call('get_lexical_entries', user_input)
    else:
        user_input = sender.tag.main_heading[0]
        results = anvil.server.call('get_lexical_entries', user_input)
      
    open_form('LexicalItem', item_panel_role='elevated-card', item_panel_visibility=True, data=results)

def open_theme(sender, source=False, **event_args):
    if not source:
        user_input = sender.tag.main_heading
        result = anvil.server.call('get_main_heading_data_by_heading', user_input)
        open_form('LexicalItem', theme_panel_role='elevated-card', item_panel_visibility=False, data=result)
    else:
        user_input = sender.tag.main_heading
        result = anvil.server.call('get_main_heading_data_by_vague_source', user_input)
        open_form('LexicalItem', theme_panel_role='elevated-card', item_panel_visibility=False, data=result)

def check_password():
      password_box = TextBox(placeholder="Enter password", role="outlined", hide_text=True)
      result = alert(
          content=password_box,
          title="Password Required",
          buttons=[("OK", True), ("Cancel", False)],
      )
      if result:
          if anvil.server.call('verify_password', password_box.text):
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
            if search_key == 'idi':
                matching_items = [item for item in self.data_lexis if search_key in item[1]]
            else:
                matching_items = [item for item in self.data_lexis if search_key == item[1]]
            populate_content_panel(panel, matching_items, open_lexical_item, word_class=True, is_grid=True)
          else:
            populate_content_panel(panel, self.data_lexis, open_lexical_item, word_class=True, is_grid=True)

def search_lexical_item(user_input):
      if user_input:
          results = anvil.server.call('search_lexical_items', user_input)
          print
          if results:
              open_form('main')
              main_form = get_open_form()
              main_form.search_lexical_item(results)
          else:
              alert(
                  f"No results found for '{user_input}'",
                  title="Search Result"
              )
      else:
          alert("Please input the search field")


