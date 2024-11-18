import urllib.parse

def double_url_encode(text):
    # 进行第一次URL编码
    encoded_text = urllib.parse.quote(text)
    # 进行第二次URL编码
    encoded_text = urllib.parse.quote(encoded_text)
    return encoded_text

def generate_urls(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in lines:
            # 去除行尾的换行符
            line = line.strip()
            # 进行两次URL编码
            encoded_line = double_url_encode(line)
            # 生成完整的URL
            url = f"https://www.xiaohongshu.com/search_result?keyword={encoded_line}&source=web_search_result_notes"
            # 写入到输出文件
            f.write(url + '\n')