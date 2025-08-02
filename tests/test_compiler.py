import re

def analyze_text(full_text):
    analyzed_list = []

    text_line = full_text.splitlines() 

    for line in text_line:
        if line[0] =='\\':
            analyzed_list.append({'type': 'command','text': line })
        else:
            analyzed_list.append({'type': 'text', 'text': line})
        
    return analyzed_list