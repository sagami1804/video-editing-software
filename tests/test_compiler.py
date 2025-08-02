import re

def analyze_text(full_text):
    analyzed_list = []

    text_line = full_text.splitlines() 

    for line in text_line:
        #空白の行がないかの確認
        line = line.strip()
        if not line:
            continue
        #その行がコマンドかテキスト文かの判別
        if line[0] =='\\':
            analyzed_list.append({'type': 'command','text': line })
            #if line[1:]
        else:
            analyzed_list.append({'type': 'text', 'text': line})
            print(f"テキスト: {line}")
        
    return analyzed_list