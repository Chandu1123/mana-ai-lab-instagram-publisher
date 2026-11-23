from datetime import date
from fractions import Fraction
from PIL import Image, ImageDraw, ImageFont

START = date(2026, 12, 22)
END = date(2030, 11, 22)


def lesson(day):
    index = (day - START).days
    if not START <= day <= END:
        raise ValueError("Date outside the campaign")
    n, topic = divmod(index, 10)
    a, b = 4 + n % 13, 2 + n // 13
    dist = a * b
    price = 100 + 5 * n
    rate = 5 * (1 + n % 6)
    items = [
        ("Shop maths", f"Rs {price} at {rate}% off. Final bill?", f"Rs {price*(100-rate)/100:,.2f}", f"Discount = {price} x {rate}/100. Subtract it from the original price.", "Offer chusaka final bill lekka veyyandi."),
        ("Map skills", f"On a map, 1 cm means {b} km. What does {a} cm mean?", f"{dist} kilometres", f"Each centimetre covers {b} km. Multiply the measured length, {a}, by {b}.", "Map scale tho dooram kanukkovachu."),
        ("Data literacy", f"{a} votes for A and {b} for B. What share chose A?", f"{100*a/(a+b):.1f}%", f"Count all {a+b} votes first. Divide {a} by {a+b}, then multiply by 100. Rounded to one decimal.", "Percentage chuste total entho kuda adagandi."),
        ("Digital images", f"A {120*a} px wide photo is scaled to 50%. New width?", f"{60*a} pixels", f"Half the width means {120*a} / 2. If height also halves, the new pixel count is one quarter.", "Width sagam aithe pixel count em avutundo try cheyyandi."),
        ("Travel planning", f"Cover {dist} km in {b} hours. Average speed?", f"{a} km/h", f"Divide total distance, {dist} km, by the full elapsed time, {b} hours, including stops.", "Aagina samayam kuda total time lo untundi."),
        ("Kitchen ratios", f"{a} cups serve {2*a} people. How much for {2*b}?", f"{b} cups", f"One person gets half a cup. Multiply {2*b} portions by 0.5 cup per portion.", "Guests maarite portions kuda ila marchandi."),
        ("Time zones", f"Meeting at {n%17:02}:{(n//17)*5:02} UTC. India time?", f"{n%17+5+(30+(n//17)*5)//60:02}:{(30+(n//17)*5)%60:02} IST", "Add 5 hours and 30 minutes. When minutes reach 60, carry one hour.", "Meeting invite lo time zone chudandi."),
        ("Spreadsheet lab", f"Cells A1 and A2 hold {a} and {b}. What does =A1*A2 give?", str(dist), f"The asterisk multiplies. Change A2 to {b+1} and the result becomes {a*(b+1)}.", "Formula petti okka cell marchi chudandi."),
        ("Design geometry", f"A {a} by {b} cm card needs a border. How much trim?", f"{2*(a+b)} cm", f"Add all four sides: {a} + {b} + {a} + {b}. For covering the face you would use {dist} square cm.", "Border kosam perimeter kavali."),
        ("Chance puzzle", f"A bag has {a} blue and {b} red counters. Chance of blue?", str(Fraction(a,a+b)), f"Assume a random draw. There are {a} blue outcomes among {a+b} counters. Reduce the fraction if possible.", "Chance lekka vesetappudu anni outcomes lekkinchandi."),
    ]
    return items[topic]


def render(day, path):
    topic, question, answer, detail, telugu = lesson(day)
    im = Image.new("RGB", (1080,1350), "#fcf6e9")
    draw = ImageDraw.Draw(im)
    def block(value, y, size, bold=False, color="#172337"):
        font = ImageFont.truetype("DejaVuSans" + ("-Bold" if bold else "") + ".ttf",size)
        line = ""
        for word in value.split():
            joined = (line+" "+word).strip()
            if draw.textlength(joined,font=font)>920 and line:
                draw.text((78,y),line,font=font,fill=color)
                y += int(size*1.3)
                line = word
            else:
                line = joined
        draw.text((78,y),line,font=font,fill=color)
        return y+int(size*1.3)
    blue = "#1c5086"
    block("MANA AI LAB",65,34,True,blue)
    draw.line((78,148,1000,148),fill=blue,width=3)
    block(topic.upper(),194,36,True,blue)
    y = block(question,284,60,True)
    y = block(answer,y+44,65,True,blue)
    y = block(detail,y+42,42)
    y = block(telugu,y+40,36,False,blue)
    if y>1185: raise ValueError("Text overflow")
    block("Follow @__all_in__onee for daily Telugu-English learning.",1250,27,True)
    im.save(path,quality=91)
    return f"{question}\n\n{telugu}\n\n{answer}. {detail}\n\nMana AI Lab | {day.isoformat()}\n#TeluguLearning #ManaAILab"
