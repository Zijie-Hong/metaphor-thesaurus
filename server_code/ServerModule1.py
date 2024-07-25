import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime

@anvil.server.callable
def search_lexical_items(input):
    query1 = f'% {input} %'  # 单词在中间
    query2 = f'{input} %'    # 单词在开头
    query3 = f'% {input}'    # 单词在结尾
    query4 = f'{input}'      # 精确匹配

    matching_rows = app_tables.lexical_items.search(
    english_headword=q.any_of(
        q.like(query1),
        q.like(query2),
        q.like(query3),
        q.like(query4)
        )
    )
    return list(set(row['english_headword'] for row in matching_rows)) or None
  
@anvil.server.callable
def get_lexical_item_details(headword):
    matching_rows = app_tables.lexical_items.search(english_headword=headword)
    results = []
    
    for row in matching_rows:
        results.append({
            "lexical_item_id": row['lexical_item_id'],
            "section_heading_id": row['section_heading_id'],
            "english_headword": row['english_headword'],
            "literal_word_class": row['literal_word_class'],
            "metaphorical_word_class": row['metaphorical_word_class'],
            "literal_meaning": row['literal_meaning'],
            "metaphor_meaning": row['metaphor_meaning'],
            "english_example_sentence": row['english_example_sentence'],
        })
    return results if results else None

@anvil.server.callable
def search_by_theme(input1, input2):
    connectors = ['IS', 'ARE']
    results = []
    for connector in connectors:
        query = f'%{input1}% {connector} %{input2}%'
        matching_rows = app_tables.main_headings.search(main_heading=q.like(query))
        results.extend([row['main_heading'] for row in matching_rows]) 
    if results:
        return results
    return None

@anvil.server.callable
def search_themes_by_target(input):
    connectors = ['IS', 'ARE']
    results = []
    for connector in connectors:
        query = f'%{input}% {connector}%'
        matching_rows = app_tables.main_headings.search(main_heading=q.like(query))
        results.extend([row['main_heading'] for row in matching_rows]) 
    if results:
        return results
    return None

@anvil.server.callable
def search_themes_by_source(input):
    connectors = ['IS', 'ARE']
    results = []
    for connector in connectors:
        query = f'%{connector} %{input}%'
        matching_rows = app_tables.main_headings.search(main_heading=q.like(query))
        results.extend([row['main_heading'] for row in matching_rows]) 
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
        record["literal_word_class"]= new_data['literal_word_class']
        record["metaphorical_word_class"]= new_data['metaphorical_word_class']
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
            seen.add(headword)
    unique_headwords = sorted(seen)
    return unique_headwords

@anvil.server.callable
def get_matching_headings(source_text, target_text):
    source_row = app_tables.category_sources.get(category_source=source_text)
    target_row = app_tables.category_targets.get(category_target=target_text)

    source_id = source_row['category_source_id'] if source_row else None
    target_id = target_row['category_target_id'] if target_row else None
  
    if source_id and target_id:
        matching_rows = app_tables.main_headings.search(
            q.all_of(category_source_id=source_id, category_target_id=target_id)
        )
    elif source_id:
        matching_rows = app_tables.main_headings.search(
            q.any_of(category_source_id=source_id)
        )
    elif target_id:
        matching_rows = app_tables.main_headings.search(
            q.any_of(category_target_id=target_id)
        )
    else:
        return []
    result = [{'main_heading_id': row['main_heading_id'], 'main_heading': row['main_heading']} for row in matching_rows]
    return result
 

@anvil.server.callable
def get_relationships_by_main_heading_id(main_heading_id):
    matching_rows = app_tables.relationships.search(main_heading_id=main_heading_id)
    return [{'relationship': row['relationship'], 'related_heading': row['related_heading']} for row in matching_rows]


@anvil.server.callable
def add_new_lexical_item(entry_dict):
    max_id_entry = app_tables.suggestion.search(tables.order_by("id", ascending=False))
    if max_id_entry and len(max_id_entry) > 0:
      max_id = max_id_entry[0]['id']
      new_id = max_id + 1
    else:
      new_id = 1
    entry_dict['id'] = new_id
    now = datetime.now().replace(microsecond=0)
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
    try:
        app_tables.suggestion.add_row(
        added_time=formatted_time,
        **entry_dict
    )
        return {'status': 'success', 'message': 'Item added successfully.'}
    except Exception as e:
        # 发生错误时返回错误消息
        return {'status': 'error', 'message': str(e)}
      
@anvil.server.callable
def get_entries():
    # Get a list of entries from the Data Table, sorted by 'created' column, in descending order
    return app_tables.suggestion.search(
      tables.order_by("added_time", ascending=False)
    )

@anvil.server.callable
def update_entry(entry, entry_dict):
  existing_entry = app_tables.lexical_items.get(lexical_item_id=entry['lexical_item_id'])
  if existing_entry:
      existing_entry.update(**entry_dict)
  else:
      raise Exception("Entry does not exist in either tables")
    
@anvil.server.callable
def delete_entry(entry):
  # check that the entry being deleted exists in the Data Table
  if app_tables.suggestion.has_row(entry):
    entry.delete()
  else:
    raise Exception("Entry does not exist")


@anvil.server.callable
def accept_entry(entry, section_heading_id):
    max_id_entry = app_tables.lexical_items.search(tables.order_by("lexical_item_id", ascending=False))
    if max_id_entry and len(max_id_entry) > 0:
      max_id = max_id_entry[0]['lexical_item_id']
      new_id = max_id + 1
    else:
      new_id = 1

    try:
        app_tables.lexical_items.add_row(
            lexical_item_id=new_id,
            section_heading_id=section_heading_id,
            **entry
        )
        return {'status': 'success', 'message': 'Item added successfully.'}
    except Exception as e:
        # 发生错误时返回错误消息
        return {'status': 'error', 'message': str(e)}