import re

# Define the allowed ban code prefixes
prefixes = ['UX', 'SRS', 'SXS', 'SYS', 'OZ', 'T7']

# Define the regex pattern for a single ban code
bancode_pattern = ban_code_pattern = r'{(' + '|'.join(prefixes) + r')x(0[0-9]|1[0-9]|2[0-4])}'

# Define the regex pattern for a single URL
url_pattern = r'^(https?://)?(?:(?:t\.me|telegram\.me|telegram\.dog)/(?:c/(\d{10,})|([a-zA-Z0-9_]{5,})|([a-zA-Z0-9_]+))/(\d+)|(?:te\.legra\.ph|telegra\.ph|graph\.org)\/file\/[^\s\/]+\.[a-zA-Z0-9-]+)$'

def validate_url(input_string) -> bool:
    """Validate URL in entire input string"""
    return bool(re.match(url_pattern, input_string))

def validate_gban_codes(input_string) -> bool:
    """Checks if given string checks the following conditions:
    {(Prefix)x(Bancode Number)}
    Telegram or Telegraph URL

    Example:
    {SXSx21} {UXx15} {OZx12}
    t.me/c/1375161034/4
    t.me/chatusername/4
    telegram.me/c/1375161034/4
    telegram.me/chatusername/4
    telegram.dog/c/1375161034/4
    telegram.dog/chatusername/4
    graph.org/file/d7a4a7f2f0f6d1d
    te.legra.ph/file/d7a4a7f2f0f6d1d
    telegra.ph/file/d7a4a7f2f0f6d1d
    https://t.me/c/1375161034/4
    https://t.me/chatusername/4
    https://telegram.me/c/1375161034/4
    https://telegram.me/chatusername/4
    https://telegram.dog/c/1375161034/4
    https://telegram.dog/chatusername/4
    https://graph.org/file/d7a4a7f2f0f6d1d
    https://te.legra.ph/file/d7a4a7f2f0f6d1d
    https://telegra.ph/file/d7a4a7f2f0f6d1d
    """
    input_pattern = r'^(' + bancode_pattern + r' ?)*$'
    return bool(re.match(input_pattern, input_string))

def validate_gban_format(input_string) -> bool:
    "Checks if Bancodes and provided URL are correct"
    # Split the input string into lines
    lines = input_string.strip().split("\n")
    # Validate each line
    for line in lines:
        line = line.strip()
        if not validate_url(line) and not validate_gban_codes(line):
            return False
    return True