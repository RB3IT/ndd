from PIL import Image, ImageDraw, ImageFont
import json
import pathlib

VERIFICATION = (pathlib.Path(__file__).parent / "Bristol Order Verification Form.jpg").resolve()
VERIFICATIONJSON = (pathlib.Path(__file__).parent / "Bristol Order Verification Form.json").resolve()
with open(VERIFICATIONJSON,'r') as f:
    VERIFICATIONJSON = json.load(f)

def shop_drawing(door, order, additional_notes = ""):
    """ Generate a Shop Drawing for the given door """
    pos = VERIFICATIONJSON
    img = Image.open(VERIFICATION)
    context = ImageDraw.Draw(img)

    for text in pos:
        fntname = "times"
        font = text['font']
        if font['weight'] == "bold": fntname+= "b"
        if font['slant']=="italic": fntname += "i"
        fnt = ImageFont.truetype(f"{fntname}.ttf", size = font['size'])

        if text == "notes":
            width = text['bbox'][2] - text['bbox'][0]
            output = ""
            for line in additional_notes.split("\n"):
                while line:
                    cut = ""
                    lwidth = context.textsize(line, font = fnt)[0]
                    while lwidth > width:
                        cut = line[-1] + cut
                        line = line[:-1]
                        lwidth = context.textsize(line, font = fnt)[0]
                    out += line+"\n"
                    line = cut
            context.multiline_text((text['x'],text['y']), output, font = fnt, spacing = font['linespacing'])
        else:
            if text['name'] == "locking":
                val = " & ".join([access['kind'] for access in door.accessories if "locking" in access['kind']])
            else:
                heirarchy = text['name'].split(".")
                first = heirarchy.pop(0)
                if first == "door": val = door
                elif first == "order": val = order
                for attr in heirarchy:
                    val = getattr(val,attr)

            context.text((text['x'],text['y']), str(val), font = fnt)
    
    return img