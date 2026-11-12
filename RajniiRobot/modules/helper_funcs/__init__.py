from typing import Optional, Tuple

# Setting Message

def get_text(event) -> Optional[str]:
    """Extract Text From Commands"""
    text_to_return = getattr(event, "raw_text", None)
    if text_to_return is None:
        return None
    if " " not in text_to_return:
        return None

    try:
        return text_to_return.split(None, 1)[1]
    except IndexError:
        return None