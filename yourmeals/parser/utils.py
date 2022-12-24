def norm_text(text: str) -> str:
    text = text.replace('\n', ' ')
    text = text.replace('\r', ' ')
    text = text.replace('\t', ' ')
    text = text.replace('\xa0', ' ')
    text = text.replace('!!!', '')
    text = text.strip(' ')
    return text
