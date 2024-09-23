from URL import URL
import tkinter

WIDTH: int = 800
HEIGHT: int = 600

class Browser:

    def __init__(self) -> None:
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(
            self.window,
            width=WIDTH,
            height=HEIGHT
        )
        self.canvas.pack()

    def lex(self, body:str) -> str: # Update the return type at the end of the function
        in_tag: bool = False
        Special_characters: dict[str, str] = {
            "lt": "<",
            "gt": ">",
            "amp": "&",
            "quot": '"',
            "apos": "'"
        }
        i = 0
        text: str = ""
        while i < len(body): # Loop over character by character
            if body[i] == "<":
                in_tag = True
                i += 1
            elif body[i] == ">":
                in_tag = False
                i += 1
            elif not in_tag:
                if body[i] == "&":
                    semicolon_pos = body.find(";", i)
                    if semicolon_pos != -1:
                        entry = body[i+1:semicolon_pos]
                        if entry in Special_characters:
                            text += Special_characters.get(entry)
                            i = semicolon_pos + 1
                        else:
                            text += body[i]
                            i += 1
                    else:
                        text += body[i]
                        i += 1
                else:
                    text += body[i]
                    i += 1
            else:
                i += 1
        return text
        
    def load(self, url: URL) -> None:
        HSTEP, VSTEP = 13, 18
        cursor_x, cursor_y = HSTEP, VSTEP
        body: str = url.request()
        text = self.lex(body)
        for char in text:
            self.canvas.create_text(cursor_x, cursor_y, text=char)
            cursor_x += HSTEP
            if cursor_x >= WIDTH - HSTEP:
                cursor_x = HSTEP
                cursor_y += VSTEP

if __name__ == "__main__":
    import sys
    Browser().load(URL(sys.argv[1]))
    tkinter.mainloop()