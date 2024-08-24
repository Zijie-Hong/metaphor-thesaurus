from ._anvil_designer import ItemTemplate1Template
from anvil import *
import anvil.server
from ...entry_edit import entry_edit
from ...utils import check_password
class ItemTemplate1(ItemTemplate1Template):
  def __init__(self, **properties):
      # Set Form properties and Data Bindings.
      self.init_components(**properties)
      self.english_headword_label.visible = bool(self.item['english_headword'])
      self.literal_meaning_label.visible = bool(self.item['literal_meaning'])
      self.metaphor_meaning_label.visible = bool(self.item['metaphor_meaning'])
      self.english_example_sentence_label.visible = bool(self.item['english_example_sentence'])


  def delete_entry_button_click(self, **event_args):
      result = check_password()
      if result is True:
        if confirm(f"Are you sure you want to delete {self.item['english_headword']}?"):
            self.parent.raise_event('x-delete-entry', entry=self.item)
      elif result == 'wrong':
        alert("Incorrect password.")

  def edit_entry_button_click(self, **event_args):
      result = check_password()
      if result is True:
          entry_copy = dict(self.item)
          entry_form = entry_edit(item=entry_copy)
          save_clicked = alert(
            content=entry_form,
            title="Reiew Entry",
            large=True,
            buttons=[("Accept", True), ("Cancel", False)]
          )
          # Update the entry if the user clicks save
          if save_clicked:
            if entry_form.are_fields_filled():
                entry_accept, section_heading_id = entry_form.get_data()
                entry_accept_copy = dict(entry_accept)
                del entry_accept_copy['added_time']
                del entry_accept_copy['id']
                del entry_accept_copy['dictionary']
                result = anvil.server.call('accept_entry', entry_accept_copy, section_heading_id)
                if result == 'success':
                    alert('Item approved successfully')
                else:
                    alert(result['message'])
                # Now refresh the page
                self.refresh_data_bindings()
            else:
                alert("Please fill in all required fields.")
      elif result == 'wrong':
            alert("Incorrect password.")
