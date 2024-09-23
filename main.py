from URL import URL

def show(body:str) -> None: # Update the return type at the end of the function
    in_tag: bool = False
    Special_characters: dict[str, str] = {
        "lt": "<",
        "gt": ">",
        "amp": "&",
        "quot": '"',
        "apos": "'"
    }
    i = 0
    while i < len(body): # Loop over character by character
        if body[i] == "<":
            in_tag = True
        elif body[i] == ">":
            in_tag = False
        elif not in_tag:
            if body[i] == "&":
                semicolon_pos = body.find(";", i)
                if semicolon_pos != 1:
                    entry = body[i+1:semicolon_pos]
                    if entry in Special_characters:
                        print(Special_characters.get(entry), end="")
                        i = semicolon_pos + 1
                    else:
                        print(body[i], end="")
                        i += 1
                else:
                    print(body[i], end="")
                    i+=1
            else:
                print(body[i], end="")
                i+=1

def load(url: URL) -> None:
    body: str = url.request()
    show(body)

if __name__ == "__main__":
    import sys
    load(URL(sys.argv[1]))