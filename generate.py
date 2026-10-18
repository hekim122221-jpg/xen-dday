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

INK, BLUE, CREAM, YEL, GREY = "#111", "#A8DCF8", "#FDE9A8", "#F2E27D", "#5E6366"
JP = "'Hiragino Sans','Noto Sans JP',sans-serif"
HEAVY = "'Arial Black',sans-serif"
MONO = "'IBM Plex Mono',Menlo,monospace"


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


STYLE = ("<style>text{font:400 6.5px " + MONO + ";letter-spacing:1.2px;fill:#5E6366}"
         ".s{font-size:5.5px}"
         ".v{font-weight:600;font-size:9px;fill:#111;letter-spacing:0}"
         ".b{font:900 20px " + HEAVY + ";fill:#111;letter-spacing:0}"
         ".j{font:800 11px " + JP + ";fill:#111;letter-spacing:2px}</style>")


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
    Y = 178
    mx = 9 + 311 * p
    label = f"{n}周年まで あと {left}日 ・ {nxt:%Y.%m.%d} ・ 記録は続く ・ "
    tw = round(len(label) * 11.6)
    px = 330 - (len(f"{pct}%") * 4.6 + 6)
    svg = (f"<svg xmlns='http://www.w3.org/2000/svg' width='330' height='200'>{STYLE}"
        "<defs><clipPath id='q'><rect x='48' y='114' width='278' height='28'/></clipPath></defs>"
        "<text y='8'>記録対象 — SUBJECT</text>"
        f"<text y='56' style='fill:#3A3E40'>SINCE {START:%Y.%m.%d}</text>"
        "<text x='330' y='8' text-anchor='end'>経過日数 · ELAPSED</text>"
        f"<text x='{px - 2:.0f}' y='60' text-anchor='end' style='fill:#3A3E40'>DAY {dayi:03d} / {cycle} · </text>"
        f"<circle cx='238' cy='5.6' r='2.6' fill='{BLUE}' stroke='{INK}'/>"
        f"<text class='j' y='42' style='font-size:26px;font-weight:900;letter-spacing:0'>{esc(NAME)}</text>"
        f"<text class='b' x='330' y='44' text-anchor='end' style='font-size:32px'>{num}</text>"
        f"<rect x='{px - 1:.0f}' y='53.5' width='{331 - px:.0f}' height='9' fill='{YEL}'/>"
        f"<text x='{px + 2:.0f}' y='60.3' style='fill:{INK}'>{pct}%</text>"
        f"<path d='M0 74H330' stroke='#8a8b8b'/><path d='M0 72H330' stroke='#999' stroke-width='3' stroke-dasharray='1 5'/>"
        f"<path d='M0 71H330' stroke='#999' stroke-width='5' stroke-dasharray='1 29'/>"
        f"<rect y='80' width='330' height='27.5' fill='{INK}'/><rect y='83.5' width='163' height='24' fill='{BLUE}'/><rect x='167' y='83.5' width='163' height='24' fill='{BLUE}'/>"
        "<text class='j' x='11' y='99.5'>◀ きのう</text><text class='j' x='319' y='99.5' text-anchor='end'>あした ▶</text>"
        f"<rect y='114' width='330' height='28' rx='3' fill='{INK}'/><path d='M3 114h41v28H3a3 3 0 0 1-3-3v-22a3 3 0 0 1 3-3z' fill='{CREAM}'/>"
        "<text class='j' x='22' y='126' text-anchor='middle' style='font-size:9px;letter-spacing:0'>次は</text>"
        "<text class='j' x='22' y='137' text-anchor='middle' style='font-size:9px;letter-spacing:0'>NEXT</text>"
        f"<g clip-path='url(#q)'><text class='j' x='48' y='132' textLength='{3 * tw}' style='fill:{CREAM};font-weight:700'>{label * 3}"
        f"<animateTransform attributeName='transform' type='translate' from='0 0' to='-{tw} 0' dur='{tw / 34:.2f}s' repeatCount='indefinite'/></text></g>"
        f"<path d='M9 {Y}H320' stroke='#DCDFE3' stroke-width='6'/><path d='M15 {Y}H{max(15, mx - 9):.0f}' stroke='{INK}' stroke-width='6'/>"
        f"<g fill='#fff' stroke='{INK}' stroke-width='3.2'><circle cx='9' cy='{Y}' r='6'/><circle cx='87' cy='{Y}' r='6'/><circle cx='165' cy='{Y}' r='6'/><circle cx='243' cy='{Y}' r='6'/>"
        f"<circle cx='320' cy='{Y}' r='8.5' stroke-width='2.6'/><circle cx='320' cy='{Y}' r='5' fill='{CREAM}' stroke-width='2'/></g>"
        f"<circle cx='{mx:.0f}' cy='{Y}' r='20' fill-opacity='0'><animate attributeName='fill-opacity' values='0;.1;0' dur='3.2s' repeatCount='indefinite'/></circle><rect x='{mx - 20:.0f}' y='146' width='40' height='15' fill='{INK}'/>"
        f"<text class='j' x='{mx:.0f}' y='157' text-anchor='middle' style='font-size:9px;letter-spacing:0;fill:#fff'>現在地</text>"
        f"<circle cx='{mx:.0f}' cy='{Y}' r='9' fill='{BLUE}' stroke='{INK}' stroke-width='4'/>"
        f"<text class='v' y='198' style='font-size:8.5px;letter-spacing:1.6px'>START</text>"
        f"<text class='v' x='330' y='198' text-anchor='end' style='font-size:8.5px;letter-spacing:1.6px'>{ordinal(n)}</text></svg>")
    return svg, f"{num} · {n}周年まで{left}日 · {pct}%"


def ticket_svg():
    """Main part (238 wide) and tear-off stub (92 wide); the stub is torn off on hover via CSS."""
    dash = "1 1 2 1 1 2 3 1 1 1 2 2 1 1 3 2 1 1 2 1 1 2 2 1 3 1 1 2 1 1 2 1 1 3"
    t = lambda x, y, c, txt, extra="": f"<text{f" class='{c}'" if c != 'm' else ''} x='{x}' y='{y}'{extra}>{txt}</text>"
    e = " text-anchor='end'"
    notch = lambda x: f"<circle cx='{x}' r='9' fill='#F3F4F3'/><circle cx='{x}' cy='204' r='9' fill='#F3F4F3'/>"
    main = (f"<svg xmlns='http://www.w3.org/2000/svg' width='238' height='204'>{STYLE}"
        f"<rect width='238' height='24' fill='{INK}'/><circle cx='17.5' cy='12' r='4.7' fill='none' stroke='#fff' stroke-width='1.6'/><circle cx='17.5' cy='12' r='2' fill='#fff'/>"
        + t(29, 15.5, "b", "SERAPHIX", " textLength='66' style='font-size:10px;letter-spacing:1.8px;fill:#fff'")
        + t(112, 14.5, "m", "BOARDING PASS · 搭乗券", " style='font-size:6px;fill:#A9AFB2'")
        + f"<rect y='78' width='238' height='3' fill='{YEL}'/>"
        + t(74, 91, "s", "PASSENGER")
        + t(12, 144, "b", "XEN", " textLength='44'") + t(226, 144, "b", "DINE", e + " textLength='52'")
        + t(12, 152, "s", "SERAPHIX") + t(226, 152, "s", "ARCHIVE B2", e)
        + f"<path d='M64 137H166' stroke='#777' stroke-width='1.2' stroke-dasharray='3 2.5'/><rect x='108' y='128' width='14' height='16' fill='#FBFBFB'/>"
        + "<path transform='translate(122.2 129) rotate(90) scale(.6)' d='M21 16v-2l-8-5V3.5a1.5 1.5 0 0 0-3 0V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5z'/>"
        + "".join(t(x, 166, "s", a) + t(x, 177, "v", b)
                  for x, a, b in ((12, "FLIGHT", "VX-01"), (66, "GATE", "31F"), (120, "SEAT", "0808A"), (174, "DATE", "08AUG26")))
        + "<path d='M237 30V194' stroke='#aaa' stroke-width='1.5' stroke-dasharray='4 3'/>"
        + notch(238) + "</svg>")
    stub = (f"<svg xmlns='http://www.w3.org/2000/svg' width='92' height='204'>{STYLE}"
        f"<rect width='92' height='24' fill='{INK}'/>"
        + t(12, 40, "s", "BOARDING") + t(12, 53, "b", "XEN → DINE", " style='font-size:9.5px'")
        + t(12, 66, "s", "SEAT") + t(12, 83, "b", "0808A", " style='font-size:17px'")
        + t(12, 96, "s", "GATE") + t(12, 113, "b", "31F", " style='font-size:17px'")
        + f"<path d='M12 170H80' stroke='{INK}' stroke-width='20' stroke-dasharray='{dash}'/>"
        + t(12, 192, "s", "NO.0001 · XEN")
        + "<path d='M0 30V194' stroke='#F3F4F3' stroke-width='3' stroke-dasharray='0 7' stroke-linecap='round'/>"
        + notch(0) + "</svg>")
    return main, stub


if __name__ == "__main__":
    today = datetime.now(TZ).date()
    svg, info = dday_svg(today)
    open("dday.svg", "w", encoding="utf-8").write(svg)
    main, stub = ticket_svg()
    open("ticket.svg", "w", encoding="utf-8").write(main)
    open("stub.svg", "w", encoding="utf-8").write(stub)
    print(today, info)
