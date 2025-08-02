import re

def analyze_text(full_text):
    analyzed_list = []

    text_line = full_text.splitlines()

    for line in text_line:
        line = line.strip()
        if not line:
            continue

        if line.startswith('\\'):
            analyzed_list.append({'type': 'command', 'text': line})

            # 正規表現でコマンド名と引数を抽出
            match = re.match(r'\\(\w+)(?:\{(.*)\})?', line)
            if match:
                command = match.group(1)
                raw_arg = match.group(2) if match.group(2) else ""
                print(f"コマンド名: {command}, 引数: {raw_arg}")

                # 引数文字列を辞書に変換
                kwargs = parse_kwargs(raw_arg)

                # コマンド名で関数呼び出し
                if command == 'section':
                    section(**kwargs)
                elif command == 'setSubtitleScale':
                    set_subtitle_scale(**kwargs)
                elif command == 'setTalkSpeed':
                    set_talk_speed(**kwargs)
                elif command == 'delay':
                    delay(**kwargs)

        else:
            analyzed_list.append({'type': 'text', 'text': line})
            print(f"テキスト: {line}")

    return analyzed_list

def parse_kwargs(arg_str):
    kwargs = {}
    if not arg_str:
        return kwargs
    for part in arg_str.split(','):
        if '=' in part:
            key, value = part.split('=', 1)
            kwargs[key.strip()] = value.strip()
        else:
            kwargs[part.strip()] = ""  # キーのみ（値なし）の場合
    return kwargs

def section(**kwargs):
    print(f"  → section関数: {kwargs}")

def image(**kwargs):
    print(f"  → image関数: {kwargs}")

def delay(**kwargs):
    print(f"  → delay関数: {kwargs}")
