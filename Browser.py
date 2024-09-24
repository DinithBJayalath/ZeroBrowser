from URL import URL
import tkinter

WIDTH: int = 800
HEIGHT: int = 600
HSTEP: int = 13
VSTEP: int = 18
SCROLL_STEP: int = 50

class Browser:

    def __init__(self) -> None:
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(
            self.window,
            width=WIDTH,
            height=HEIGHT
        )
        self.scroll = 0
        self.window.bind("<Down>", self.scroll_down)
        self.canvas.pack()

    def scroll_down(self, e) -> None:
        """This is a event listener function to make the window scroll  

        The takes the event as an argument and update the value of the instance variable scroll  
        and redraw the body of the page"""
        self.scroll += SCROLL_STEP
        self.draw()

    def load(self, url: URL) -> None:
        body: str = url.request()
        text = Browser.lex(body)
        self.display_list = Browser.layout(text)
        self.draw()

    def draw(self) -> None:
        self.canvas.delete("all")
        for x, y, char in self.display_list:
            self.canvas.create_text(x, y-self.scroll, text=char)

    @staticmethod
    def lex(self, body:str) -> str:
        """This function receives the webpage body as an argument and parses it.

        It looks for HTML tags and remove them and looks for special characters and  
        converts them to the respective expected characters"""
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
                    # If ";" doesn't exist in the body then the find method will return "-1"
                    if semicolon_pos != -1:
                        entry = body[i+1:semicolon_pos]
                        if entry in Special_characters:
                            text += Special_characters.get(entry)
                            # When a special character is added to the text,
                            # the position of the current letter needs to be updated to be the position after the ";"
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
    
    @staticmethod
    def layout(text: str) -> list[tuple[int, int, str]]:
        display_list = []
        cursor_x, cursor_y = HSTEP, VSTEP
        for char in text:
            display_list.append((cursor_x, cursor_y, char))
            cursor_x += HSTEP
            # The position  of the character needs to be updated to be in the next row if the character is going of the screen from the side
            if cursor_x >= WIDTH - HSTEP:
                cursor_x = HSTEP
                cursor_y += VSTEP
        return display_list

if __name__ == "__main__":
    import sys
    Browser().load(URL(sys.argv[1]))
    tkinter.mainloop()