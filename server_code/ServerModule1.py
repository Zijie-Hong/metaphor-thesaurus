import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable
def search_lexical_items(headword):
    headword = headword.strip() 
    matching_rows = app_tables.lexical_items.search(english_headword=headword)
    results = []
    for row in matching_rows:
        results.append({
            "lexical_item_id": row['lexical_item_id'],
            "section_heading_id": row['section_heading_id'],
            "english_headword": row['english_headword'],
            "word_class": row['word_class'],
            "literal_meaning": row['literal_meaning'],
            "metaphor_meaning": row['metaphor_meaning'],
            "english_example_sentence": row['english_example_sentence'],
        })
    if results:
        return results
    else:
        return None

@anvil.server.callable
def get_lexical_item_details(headword):
    row = app_tables.lexical_items.get(english_headword=headword)
    results = []
    results.append({
        "lexical_item_id": row['lexical_item_id'],
        "section_heading_id": row['section_heading_id'],
        "english_headword": row['english_headword'],
        "word_class": row['word_class'],
        "literal_meaning": row['literal_meaning'],
        "metaphor_meaning": row['metaphor_meaning'],
        "english_example_sentence": row['english_example_sentence'],
    })
    if results:
        return results
    else:
        return None

@anvil.server.callable
def search_main_headings(input1, input2):
    connectors = ['IS', 'ARE']
    if input1 and input2:
      for connector in connectors:
          row = app_tables.main_headings.get(main_heading=f"{input1} {connector} {input2}")
          if row:
              return {
                  "main_heading_id": row['main_heading_id'],
                  "main_heading": row['main_heading'],
                  "target_id": row['target_id'],
                  "source_id": row['source_id'],
                  "category_source_id": row['category_source_id'],
                  "category_target_id": row['category_target_id']
              }
    elif input1 or input2:
        query = f'{input1} % %' if input1 else f'% % {input2}'
        matching_rows = app_tables.main_headings.search(main_heading=q.like(query))
        results = [row['main_heading'] for row in matching_rows]
        if results:
          return results     
    return None
  
@anvil.server.callable
def get_main_heading_data(section_heading_id):
    section_heading_row = app_tables.section_headings.get(section_heading_id=section_heading_id)
    if not section_heading_row:
        return None
    
    section_heading = section_heading_row['section_heading']
    main_heading_id = section_heading_row['main_heading_id']
    
    main_heading_row = app_tables.main_headings.get(main_heading_id=main_heading_id)
    if not main_heading_row:
        return None
    
    main_heading_data = {
        "main_heading_id": main_heading_row['main_heading_id'],
        "main_heading": main_heading_row['main_heading'],
        "target_id": main_heading_row['target_id'],
        "source_id": main_heading_row['source_id'],
        "category_source_id": main_heading_row['category_source_id'],
        "category_target_id": main_heading_row['category_target_id']
    }
    
    return main_heading_data, section_heading

@anvil.server.callable
def get_main_heading_data_by_heading(main_heading):
    row = app_tables.main_headings.get(main_heading=main_heading)
    if row:
        return {
            "main_heading_id": row['main_heading_id'],
            "main_heading": row['main_heading'],
            "target_id": row['target_id'],
            "source_id": row['source_id'],
            "category_source_id": row['category_source_id'],
            "category_target_id": row['category_target_id']
        }
    return None
  
@anvil.server.callable
def get_category_descriptions(source_id, target_id):
    source_description = app_tables.category_sources.get(category_source_id=source_id)['category_source']
    target_description = app_tables.category_targets.get(category_target_id=target_id)['category_target']
    return source_description, target_description


@anvil.server.callable
def get_section_heading(main_heading_id):
    section_headings = app_tables.section_headings.search(main_heading_id=main_heading_id)
    return [{'section_heading_id': row['section_heading_id'], 'section_heading': row['section_heading']} for row in section_headings]

@anvil.server.callable
def get_lexical_items(section_heading_id):
    rows = app_tables.lexical_items.search(section_heading_id=section_heading_id)
    return [row['english_headword'] for row in rows]

@anvil.server.callable
def update_data_in_database(record_id, new_data):
    record = app_tables.lexical_items.get(lexical_item_id=record_id)
    
    if record:
        # Update the record with the new data
        record['english_headword'] = new_data['english_headword']
        record['literal_meaning'] = new_data['literal_meaning']
        record['word_class'] = new_data['word_class']
        record['metaphor_meaning'] = new_data['metaphor_meaning']
        record['english_example_sentence'] = new_data['english_example_sentence']
        
        # Optionally return a success message or updated record
        return {"status": "success", "message": "Record updated successfully"}
    else:
        return None


@anvil.server.callable
def get_lexical_items_by_letter(letter):
    items = app_tables.lexical_items.search(english_headword=q.like(letter.lower() + '%'))
    unique_headwords = []
    seen = set()
    for item in items:
        headword = item['english_headword']
        if headword not in seen:
            unique_headwords.append(headword)
            seen.add(headword)
    return unique_headwords

