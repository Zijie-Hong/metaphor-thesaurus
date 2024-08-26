from ._anvil_designer import introductionTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from ..suggestion_list import suggestion_list

class introduction(introductionTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.panel_1.role="elevated-card"


  def reset_button_styles(self):
    self.panel_1.role = "default"
    self.panel_2.role = "default"
    self.panel_3.role = "default"

  def button_1_click(self, **event_args):
    self.reset_button_styles()
    self.panel_1.role = "elevated-card"

  def button_2_click(self, **event_args):
    self.reset_button_styles()
    self.panel_2.role = "elevated-card"
    
  def button_3_click(self, **event_args):
    self.reset_button_styles()
    self.panel_3.role = "elevated-card"


  def link_3_click(self, **event_args):
    open_form("main")

  def link_2_click(self, **event_args):
    from ..main import main
    main_form = main()
    main_form.add_map_to_content_panel()
    open_form(main_form)

  def link_1_click(self, **event_args):
    from ..main import main
    main_form = main()
    main_form.content_panel.clear()
    suggestion_list_form = suggestion_list()
    main_form.content_panel.add_component(suggestion_list_form, full_width_row=True)
    open_form(main_form)

