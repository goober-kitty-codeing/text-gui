import os
import type_helper as th
from typing import Union

GUIparent = ( Union['GUIgui', 'GUIbase'] )

class GUIbase:
    x: int = None
    y: int = None
    func: callable = None
    enabeld: bool = None
    parent: GUIparent = None
    image: str = None
    def __init__(s, x: int, y: int, func: callable = None, enabeld: bool = True):
        s.x = th.to_int(x)
        s.y = th.to_int(y)
        s.enabeld = th.to_bool(enabeld)
        if th.is_callable(func): s.func = func
    def make_image(s):
        print("[Error 0] | Make this method yourself please")
        return "DEFAULT"
    def on_interact(s, *args):
        s.func(s)

class GUIbutton(GUIbase):
    label: str = None
    def __init__(s, x: int, y: int, label: str, func: callable = None):
        super().__init__(x, y, func)
        s.label = label
        s.make_image()
    def make_image(s):
        s.image = f"[{["#",""][th.to_int(s.enabeld)]}{s.label}]"
        return s.image

class GUIentry(GUIbase):
    placeholder: str = None
    value: str = None
    def __init__(s, x: int, y: int, placeholder: str, func: callable = None):
        super().__init__(x, y, func)
        s.placeholder = th.to_str(placeholder)
        s.value = ""
    def make_image(s):
        display = s.value if s.value != "" else s.placeholder
        return f"<{display}>"
    def on_interact(s, *args):
        s.parent.erase_item(s)
        s.value = input(f"[Entry: {s.parent.get_id(s)}]Enter input: ")
        super().on_interact(s) # super refrences the parent. In this case GUIbase, pretty cool.

class GUIlabel(GUIbase):
    value: str = None
    def __init__(s, x: int, y: int, value: str, func: callable = None):
        super().__init__(x, y, func)
        s.value = value
    def make_image(s):
        display = s.value
        return f"'{display}'"
    def on_interact(s, *args): ... # Dosent do anything

class GUIgui:
    width: int = None
    hight: int = None
    bg_char: str = None
    objects: list[list[GUIbase]] = None
    boreds: list[str] = None
    current_bored: int = None
    def __init__(s, widht: int, height: int, bg_char: str):
        s.width   = th.to_int(widht)
        s.hight   = th.to_int(height)
        s.bg_char = bg_char[0]
        s.objects = [[]]
        s.current_bored = 0
        s.boreds = [ f"{f"{s.bg_char}"*s.width}\n"*s.hight ]
        if len(bg_char) != 1:
            print("[Error 0] | fyi: bg_char is supposed to be one symbel.")
    def make_image(s):
        for i in s.objects[s.current_bored]:
            s.imprent(i)
    def imprent(s, object: GUIbase):
        if (object.x<0) or (object.y<0):
            print("[Error 2] | x or y < 0")
            return
        
        pos = object.x + object.y * (s.width + 1)
        obj = th.to_list(object.make_image())
        bored = th.to_list(s.boreds[s.current_bored])

        for i in range(len(obj)):
            if pos + i >= len(bored): break
            if obj[i] == "\n":
                pos += s.width - ((pos + i) % (s.width + 1)) + 1 # Skips ahead to next line if we run into a newline
                continue
            if bored[pos + i] == "\n": pos += 1
            if pos + i >= len(bored): break
            bored[pos + i] = obj[i]

        s.boreds[s.current_bored] = ''.join(bored)

    def adjoin(s, object: GUIbase):
        s.objects[s.current_bored].append(object)
        object.parent = s
    def update(s):
        print(f"{s.current_bored}:")
        print(s.boreds[s.current_bored])
        option = input("Type item #: ")
        os.system('cls' if os.name == 'nt' else 'clear') # clears screen
        if option == '-1':
            print("Exiting")
            exit()
        elif option == '>':
            s.current_bored += 1
            if s.current_bored > len(s.boreds) - 1: s.current_bored = 0
            return
        elif option == '<':
            s.current_bored -= 1
            if s.current_bored < len(s.boreds): s.current_bored = len(s.boreds) - 1
            return
        if len( s.objects[s.current_bored] ) - 1 < th.to_int(option):
            print(f"Object ID {option} dosent exist on screen {s.current_bored}")
            return
        s.objects[s.current_bored][ th.to_int(option) ].on_interact()
    def get_id(s, object: GUIbase):
        try:
            return s.objects[s.current_bored].index(object)
        except ValueError:
            print("[Error 1] | Object is not in gui.")
            return -1
    def erase_item(s, object: GUIbase):
        x = object.x - 1
        y = object.y - 1
        if (x < 0) or (y < 0):
            print("[Error 2] | x or y < 0")
            return
        pos = x + y * (s.width + 1)
        obj = th.to_list(object.make_image())
        bored = th.to_list(s.boreds[s.current_bored])
        for i in range(len(obj)):
            if pos + i >= len(bored):
                print("[Error ?] How did you do this? GUIgui.erase_item")
                break
            if obj[i] == "\n":
                rem = s.width - ((pos + i) % (s.width + 1))
                pos += rem + 1
                continue
            if bored[pos + i] == "\n": pos += 1
            if pos + i >= len(bored):
                print("[Error ?] How did you do this? GUIgui.erase_item")
                break
            bored[pos + i] = s.bg_char
        s.boreds[s.current_bored] = ''.join(bored)
    def add_bored(s):
        s.boreds.append( f"{f"{s.bg_char}"*s.width}\n"*s.hight )
        s.objects.append( [] )
        return len(s.boreds) - 1

if __name__ == "__main__":
    
    GUItentry = GUIentry(0, 0, "ClickMe", lambda x: print(x.value))

    GUItest = GUIgui(25, 14, "#")
    GUItest.make_image()
    GUItest.adjoin(GUItentry)

    exampelBored = GUItest.add_bored()
    GUItest.current_bored = exampelBored
    GUItest.adjoin( GUIlabel(0, 0, "Made by Luke", lambda: ...) )
    GUItest.current_bored = 0

    while True:
        GUItest.make_image()
        GUItest.update()