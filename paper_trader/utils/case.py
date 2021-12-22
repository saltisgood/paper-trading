def camel_to_snake(s: str):
    if not s:
        return ""
    chars = [s[0].lower()]
    for c in s[1:]:
        if c.isupper():
            chars.append("_")
            c = c.lower()
        chars.append(c)
    return "".join(chars)
