from URL import URL

def show(body:str) -> None: # Update the return type at the end of the function
    in_tag: bool = False
    for char in body: # Loop over character by character
        if char == "<":
            in_tag = True
        elif char == ">":
            in_tag = False
        elif not in_tag:
            print(char, end="")

def load(url: URL) -> None:
    body: str = url.request()
    show(body)

if __name__ == "__main__":
    import sys
    load(URL(sys.argv[1]))