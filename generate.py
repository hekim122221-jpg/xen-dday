"""XEN · luvlinks widgets.
Writes:
  dday.svg   – D-DAY widget (updates daily, Asia/Seoul date)
  ticket.svg – boarding-pass background for the ID card (static)
Run by .github/workflows/dday.yml every hour; only commits when the files change."""
from datetime import date, datetime
from zoneinfo import ZoneInfo

START = date(2026, 8, 8)      # this day = D+1
NAME = "しれん"
TZ = ZoneInfo("Asia/Seoul")

INK, BLUE, CREAM, YEL, GREY = "#141516", "#A8DCF8", "#FDE9A8", "#F2E27D", "#5E6366"
JP = "'Noto Sans JP','Hiragino Sans','Hiragino Kaku Gothic ProN','Yu Gothic','Meiryo',sans-serif"
HEAVY = "'Archivo Black','Arial Black','Helvetica Neue',Arial,sans-serif"
MONO = "'IBM Plex Mono','SFMono-Regular',Menlo,Consolas,monospace"


def anniv(n):
    try:
        return START.replace(year=START.year + n)
    except ValueError:
        return date(START.year + n, 2, 28)


def ordinal(n):
    if 10 <= n % 100 <= 20:
        return f"{n}TH"
    return f"{n}{ {1: 'ST', 2: 'ND', 3: 'RD'}.get(n % 10, 'TH') }"


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;")


def dday_svg(today):
    dnum = (today - START).days + 1
    n = 1
    while anniv(n) <= today:
        n += 1
    prev, nxt = anniv(n - 1), anniv(n)
    cycle = (nxt - prev).days
    dayi = (today - prev).days + 1 if today >= START else 0
    left = (nxt - today).days
    p = max(0.0, min(1.0, dayi / cycle))
    pct = round(p * 100)
    num = f"D+{dnum}" if dnum > 0 else f"D-{1 - dnum}"

    X0, X1, Y = 9, 320, 196
    mx = X0 + (X1 - X0) * p
    stations = [9, 87, 165, 243]
    passed = "".join(f"<circle cx='{x}' cy='{Y}' r='6'/>" for x in stations)
    label = f"{n}周年まで あと {left}日 ・ {nxt:%Y.%m.%d} ・ 記録は続く ・ "
    tw = len(label) * 11.6
    pct_txt = f"DAY {dayi:03d} / {cycle} · "
    pct_x = 330 - (len(f"{pct}%") * 4.6 + 6)

    ticks = "".join(f"M{x} 74v{-4 if x % 30 == 0 else -2.5}" for x in range(0, 331, 6))
    return f"""<svg xmlns='http://www.w3.org/2000/svg' width='330' height='218' viewBox='0 0 330 218'>
<defs><clipPath id='mq'><rect x='48' y='124' width='278' height='28'/></clipPath></defs>
<g font-family="{MONO}" fill='{GREY}' font-size='6.5' letter-spacing='1.3'>
<text x='0' y='8'>記録対象 — SUBJECT</text>
<text x='0' y='56' fill='#3A3E40' font-size='7' letter-spacing='1.1'>SINCE {START:%Y.%m.%d}</text>
<text x='330' y='8' text-anchor='end'>経過日数 · ELAPSED</text>
<text x='{pct_x - 2:.1f}' y='60' text-anchor='end' fill='#3A3E40' letter-spacing='1'>{pct_txt}</text>
</g>
<circle cx='{330 - 92}' cy='5.6' r='2.6' fill='{BLUE}' stroke='{INK}' stroke-width='1'/>
<text x='0' y='42' font-family="{JP}" font-weight='900' font-size='26' fill='{INK}'>{esc(NAME)}</text>
<text x='330' y='44' text-anchor='end' font-family="{HEAVY}" font-weight='900' font-size='32' fill='{INK}'>{num}</text>
<rect x='{pct_x - 1:.1f}' y='53.5' width='{330 - pct_x + 1:.1f}' height='9' fill='{YEL}'/>
<text x='{pct_x + 2:.1f}' y='60.3' font-family="{MONO}" font-size='6.5' letter-spacing='1' fill='{INK}'>{pct}%</text>
<path d='M0 74H330' stroke='{INK}' stroke-opacity='.5'/><path d='{ticks}' stroke='{INK}' stroke-opacity='.45'/>
<rect y='84' width='330' height='3.5' fill='{INK}'/>
<rect y='87.5' width='163' height='24' fill='{BLUE}'/><rect x='167' y='87.5' width='163' height='24' fill='{BLUE}'/><rect x='163' y='84' width='4' height='27.5' fill='{INK}'/>
<g font-family="{JP}" font-weight='800' font-size='11' letter-spacing='2' fill='{INK}'>
<text x='11' y='103.5'>◀ きのう</text><text x='319' y='103.5' text-anchor='end'>あした ▶</text></g>
<rect y='124' width='330' height='28' rx='3' fill='{INK}'/>
<path d='M3 124h41v28H3a3 3 0 0 1-3-3v-22a3 3 0 0 1 3-3z' fill='{CREAM}'/>
<g font-family="{JP}" font-weight='800' font-size='9' text-anchor='middle' fill='{INK}'><text x='22' y='136'>次は</text><text x='22' y='147'>NEXT</text></g>
<g clip-path='url(#mq)'><g><text x='330' y='142' font-family="{JP}" font-weight='700' font-size='11' letter-spacing='2' fill='{CREAM}'>{label}{label}{label}</text>
<animateTransform attributeName='transform' type='translate' from='0 0' to='-{tw:.1f} 0' dur='{tw / 34:.1f}s' repeatCount='indefinite'/></g></g>
<path d='M{X0} {Y}H{X1}' stroke='#DCDFE3' stroke-width='6'/>
<path d='M15 {Y}H{max(15, mx - 9):.1f}' stroke='{INK}' stroke-width='6'/>
<g fill='#fff' stroke='{INK}' stroke-width='3.2'>{passed}<circle cx='320' cy='{Y}' r='8.5' stroke-width='2.6'/><circle cx='320' cy='{Y}' r='5' fill='{CREAM}' stroke-width='2'/></g>
<circle cx='{mx:.1f}' cy='{Y}' r='20' fill='#000' fill-opacity='.05'/>
<rect x='{mx - 20:.1f}' y='164' width='40' height='15' fill='{INK}'/>
<text x='{mx:.1f}' y='175' text-anchor='middle' font-family="{JP}" font-weight='800' font-size='9' fill='#fff'>現在地</text>
<circle cx='{mx:.1f}' cy='{Y}' r='9' fill='{BLUE}' stroke='{INK}' stroke-width='4'/>
<g font-family="{MONO}" font-weight='600' font-size='8.5' letter-spacing='1.6' fill='{INK}'>
<text x='0' y='216'>START</text><text x='330' y='216' text-anchor='end'>{ordinal(n)}</text></g>
</svg>
""", f"{num} · {n}周年まで{left}日 · {pct}%"


def ticket_svg():
    bars, x, seed = "", 0, 7
    while x < 68:
        seed = (seed * 9301 + 49297) % 233280
        w = 1 + seed % 3
        bars += f"<rect x='{250 + x}' y='160' width='{w}' height='20'/>"
        seed = (seed * 9301 + 49297) % 233280
        x += w + 1 + seed % 2
    lab = f"font-family=\"{MONO}\" font-size='5.5' letter-spacing='1' fill='{GREY}'"
    val = f"font-family=\"{MONO}\" font-weight='600' font-size='9' fill='{INK}'"
    big = f"font-family=\"{HEAVY}\" font-weight='900' fill='{INK}'"
    plane = "<path transform='translate(111 126) rotate(90 8 8) scale(.67)' d='M21 16v-2l-8-5V3.5a1.5 1.5 0 0 0-3 0V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5z' fill='#141516'/>"
    return f"""<svg xmlns='http://www.w3.org/2000/svg' width='330' height='204' viewBox='0 0 330 204'>
<rect width='330' height='24' fill='{INK}'/>
<circle cx='17.5' cy='12' r='4.7' fill='none' stroke='#fff' stroke-width='1.6'/><circle cx='17.5' cy='12' r='2' fill='#fff'/>
<text x='29' y='15.5' font-family="{HEAVY}" font-weight='900' font-size='10' letter-spacing='1.8' fill='#fff'>SERAPIX</text>
<text x='112' y='14.5' font-family="{MONO}" font-size='6' letter-spacing='1.4' fill='#A9AFB2'>BOARDING PASS · 搭乗券</text>
<rect y='78' width='238' height='3' fill='{YEL}'/>
<text x='74' y='91' {lab}>PASSENGER</text>
<text x='12' y='144' {big} font-size='20'>XEN</text><text x='226' y='144' text-anchor='end' {big} font-size='20'>DINE</text>
<text x='12' y='152' {lab}>SERAPIX</text><text x='226' y='152' text-anchor='end' {lab}>ARCHIVE B2</text>
<path d='M64 137H180' stroke='{INK}' stroke-opacity='.5' stroke-width='1.2' stroke-dasharray='3 2.5'/>
<rect x='113' y='128' width='14' height='16' fill='#FBFBFB'/>{plane}
<g><text x='12' y='166' {lab}>FLIGHT</text><text x='12' y='177' {val}>VX-01</text>
<text x='66' y='166' {lab}>GATE</text><text x='66' y='177' {val}>31F</text>
<text x='120' y='166' {lab}>SEAT</text><text x='120' y='177' {val}>0808A</text>
<text x='174' y='166' {lab}>DATE</text><text x='174' y='177' {val}>08AUG26</text></g>
<text x='12' y='197' font-family="{MONO}" font-size='5' letter-spacing='1' fill='#8F9497'>LINK ARCHIVE — ACCESS PASS · 記録保管所</text>
<path d='M238 30V194' stroke='{INK}' stroke-opacity='.35' stroke-width='1.5' stroke-dasharray='4 3'/>
<text x='250' y='40' {lab}>BOARDING</text>
<text x='250' y='53' {big} font-size='9.5' letter-spacing='.4'>XEN → DINE</text>
<text x='250' y='66' {lab}>SEAT</text><text x='250' y='83' {big} font-size='17'>0808A</text>
<text x='250' y='96' {lab}>GATE</text><text x='250' y='113' {big} font-size='17'>31F</text>
<g fill='{INK}'>{bars}</g>
<text x='250' y='192' font-family="{MONO}" font-size='5.5' letter-spacing='1.1' fill='{GREY}'>NO.0001 · XEN</text>
<circle cx='238' cy='0' r='9' fill='#F3F4F3'/><circle cx='238' cy='204' r='9' fill='#F3F4F3'/>
</svg>
"""


if __name__ == "__main__":
    today = datetime.now(TZ).date()
    svg, info = dday_svg(today)
    open("dday.svg", "w", encoding="utf-8").write(svg)
    open("ticket.svg", "w", encoding="utf-8").write(ticket_svg())
    print(today, info)
