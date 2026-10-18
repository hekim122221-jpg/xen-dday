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
    tw = round(len(label.rstrip(' ・')) * 11.6)
    px = 330 - (len(f"{pct}%") * 4.6 + 6)
    # entry motion (SMIL, timed from image load so it lines up with the page's intro)
    B = 2.1
    E = "calcMode='spline' keyTimes='0;1' keySplines='.16 1 .3 1'"
    def at(x):
        return f"{B + x:.2f}s"
    # The entry motion now lives in the page CSS (a mask wipe per row), because an SVG
    # background's own timeline can start before the page is shown (or be reused from cache).
    def rise(body, x, dy=8):
        return body
    def grow(attrs, w, x, d=.7, x0=None, x1=None):
        return f"<rect {attrs} width='{w}'{f' x={chr(39)}{x1}{chr(39)}' if x1 is not None else ''}/>"
    def pop(cx, r, x, extra=""):
        return f"<circle cx='{cx}' cy='{Y}' r='{r}'{extra}/>"
    def ripple(b):
        return (f"<circle cx='{mx:.0f}' cy='{Y}' r='9' fill-opacity='0'><animate attributeName='r' values='9;20' keyTimes='0;1' calcMode='spline' "
                f"keySplines='.2 .7 .3 1' dur='3.6s' begin='{b - 1.9:.1f}s' repeatCount='indefinite'/><animate attributeName='fill-opacity' values='.13;0' "
                f"dur='3.6s' begin='{b - 1.9:.1f}s' repeatCount='indefinite'/></circle>")
    svg = (f"<svg xmlns='http://www.w3.org/2000/svg' width='330' height='200'>{STYLE}"
        "<defs><clipPath id='q'><rect x='48' y='114' width='278' height='28'/></clipPath>"
        "<clipPath id='r'><rect y='60' height='20' width='330'/></clipPath>"
        "<clipPath id='t'><rect y='160' height='40' width='330'/></clipPath></defs>"
        + rise("<text y='8'>記録対象 — SUBJECT</text>"
               f"<text class='j' y='42' style='font-size:26px;font-weight:900;letter-spacing:0'>{esc(NAME)}</text>"
               f"<text y='56' style='fill:#3A3E40'>SINCE {START:%Y.%m.%d}</text>", 0)
        + rise("<text x='330' y='8' text-anchor='end'>経過日数 · ELAPSED</text>"
               f"<circle cx='238' cy='5.6' r='2.6' fill='{BLUE}' stroke='{INK}'/>"
               f"<text class='b' x='330' y='44' text-anchor='end' style='font-size:32px'>{num}</text>", .08, 12)
        + rise(f"<text x='{px - 2:.0f}' y='60' text-anchor='end' style='fill:#3A3E40'>DAY {dayi:03d} / {cycle} · </text>", .22, 4)
        + grow(f"y='53.5' height='9' fill='{YEL}'", f"{331 - px:.0f}", .3, .5, f"{px - 1:.0f}", f"{px - 1:.0f}")
        + rise(f"<text x='{px + 2:.0f}' y='60.3' style='fill:{INK}'>{pct}%</text>", .45, 0)
        + "<g clip-path='url(#r)'><path d='M0 74H330' stroke='#8a8b8b'/><path d='M0 72H330' stroke='#999' stroke-width='3' stroke-dasharray='1 5'/>"
          "<path d='M0 71H330' stroke='#999' stroke-width='5' stroke-dasharray='1 29'/></g>"
        + grow(f"y='80' height='27.5' fill='{INK}'", 330, .35, .7)
        + grow(f"y='83.5' height='24' fill='{BLUE}'", 163, .45, .7)
        + grow(f"y='83.5' height='24' fill='{BLUE}'", 163, .45, .7, 330, 167)
        + rise("<text class='j' x='11' y='99.5'>◀ きのう</text>", .75, 0)
        + rise("<text class='j' x='319' y='99.5' text-anchor='end'>あした ▶</text>", .8, 0)
        + grow(f"y='114' height='28' rx='3' fill='{INK}'", 330, .6, .7)
        + rise(f"<path d='M3 114h41v28H3a3 3 0 0 1-3-3v-22a3 3 0 0 1 3-3z' fill='{CREAM}'/>"
               "<text class='j' x='22' y='126' text-anchor='middle' style='font-size:9px;letter-spacing:0'>次は</text>"
               "<text class='j' x='22' y='137' text-anchor='middle' style='font-size:9px;letter-spacing:0'>NEXT</text>", .85, 6)
        + f"<g clip-path='url(#q)'><text class='j' x='326' y='132' textLength='{tw}' style='fill:{CREAM};font-weight:700'>{label.rstrip(' ・')}"
          f"<animateTransform attributeName='transform' type='translate' from='0 0' to='-{tw + 278} 0' dur='{(tw + 278) / 36:.2f}s' repeatCount='indefinite'/></text></g>"
        + f"<g clip-path='url(#t)'><path d='M9 {Y}H320' stroke='#DCDFE3' stroke-width='6'/><path d='M15 {Y}H{max(15, mx - 9):.0f}' stroke='{INK}' stroke-width='6'/></g>"
        + f"<g fill='#fff' stroke='{INK}' stroke-width='3.2'>"
        + "".join(pop(cx, 6, .9 + k * .09) for k, cx in enumerate((9, 87, 165, 243)))
        + pop(320, 8.5, 1.26, " stroke-width='2.6'") + pop(320, 5, 1.32, f" fill='{CREAM}' stroke-width='2'") + "</g>"
        + rise(ripple(1.9) + ripple(3.7)
               + f"<rect x='{mx - 20:.0f}' y='146' width='40' height='15' fill='{INK}'/>"
               f"<text class='j' x='{mx:.0f}' y='157' text-anchor='middle' style='font-size:9px;letter-spacing:0;fill:#fff'>現在地</text>"
               f"<circle cx='{mx:.0f}' cy='{Y}' r='9' fill='{BLUE}' stroke='{INK}' stroke-width='4'/>", 1.35, -14)
        + rise(f"<text class='v' y='198' style='font-size:8.5px;letter-spacing:1.6px'>START</text>"
               f"<text class='v' x='330' y='198' text-anchor='end' style='font-size:8.5px;letter-spacing:1.6px'>{ordinal(n)}</text>", 1.0, 4)
        + "</svg>")
    return svg, f"{num} · {n}周年まで{left}日 · {pct}%"


def ticket_svg():
    """Design A "ARCHIVE PASS": light main part (238 wide) + inverse black stub (92 wide).
    Photo, avatar, name, handle and share button are page elements placed over these by the CSS."""
    dash = "1 1 2 1 1 2 3 1 1 1 2 2 1 1 3 2 1 1 2 1 1 2 2 1 3 1 1 2 1 1 2 1 1 3"
    t = lambda x, y, c, txt, extra="": f"<text{f" class='{c}'" if c != 'm' else ''} x='{x}' y='{y}'{extra}>{txt}</text>"
    e = " text-anchor='end'"
    notch = lambda x: f"<circle cx='{x}' r='9' fill='#F3F4F3'/><circle cx='{x}' cy='204' r='9' fill='#F3F4F3'/>"
    lab = " style='font-size:5px;letter-spacing:1.3px'"
    plane = "M21 16v-2l-8-5V3.5a1.5 1.5 0 0 0-3 0V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5z"
    slash = "".join(f"M{x} 17l3-10h2.2l-3 10z" for x in (207, 212.5, 218, 223.5))
    main = (f"<svg xmlns='http://www.w3.org/2000/svg' width='238' height='204'>{STYLE}"
        f"<rect width='238' height='204' fill='#FCFCFB'/>"
        f"<rect width='238' height='24' fill='{INK}'/><circle cx='17.5' cy='12' r='4.7' fill='none' stroke='#fff' stroke-width='1.6'/><circle cx='17.5' cy='12' r='2' fill='#fff'/>"
        + t(29, 15.5, "b", "SERAPHIX", " textLength='66' style='font-size:10px;letter-spacing:1.8px;fill:#fff'")
        + t(104, 14.5, "m", "BOARDING PASS · 搭乗券", " textLength='92' style='font-size:5.5px;fill:#8F9497'")
        + f"<path d='{slash}' fill='{YEL}'/>"
        + f"<rect y='80' width='202' height='3' fill='{YEL}'/><rect x='202' y='80' width='36' height='3' fill='{INK}'/>"
        + f"<rect x='18' y='111' width='40' height='9' fill='{INK}'/>"
        + t(38, 117.3, "m", "ID·0808", " text-anchor='middle' style='font-size:4.5px;letter-spacing:1px;fill:#fff'")
        + t(74, 91, "m", "PASSENGER · 乗客", lab)
        + t(12, 146, "b", "XEN", " textLength='46' style='font-size:22px'") + t(226, 146, "b", "DINE", e + " textLength='54' style='font-size:22px'")
        + t(12, 155, "m", "SERAPHIX", lab) + t(226, 155, "m", "EXITUS", e + lab)
        + "<path d='M68 139.5H164' stroke='#14151673'/><path d='M68 141.5H164' stroke='#14151673' stroke-width='3' stroke-dasharray='1 5'/>"
        + f"<circle cx='116' cy='139' r='9' fill='{INK}'/><path transform='translate(122 133.2) rotate(90) scale(.5)' d='{plane}' fill='{YEL}'/>"
        + "<path d='M66 162V182M120 162V182M174 162V182' stroke='#14151624'/>"
        + "".join(t(x, 169, "m", a, lab) + t(x, 180, "v", b)
                  for x, a, b in ((12, "FLIGHT", "VX-01"), (73, "GATE", "31F"), (127, "SEAT", "0808A"), (181, "DATE", "08AUG26")))
        + t(12, 198, "m", "LINK ARCHIVE — ACCESS PASS · 記録保管所", " style='font-size:4.5px;letter-spacing:1.1px;fill:#8F9497'")
        + f"<rect x='212' y='193' width='4' height='4' fill='{INK}'/><rect x='217' y='193' width='4' height='4' fill='{YEL}'/><rect x='222' y='195' width='4' height='4' fill='#8F9497'/>"
        + "<path d='M237 30V190' stroke='#14151650' stroke-width='1.5' stroke-dasharray='4 3'/>"
        + notch(238) + "</svg>")
    g = " style='fill:#8F9497;font-size:5px;letter-spacing:1.3px'"
    stub = (f"<svg xmlns='http://www.w3.org/2000/svg' width='92' height='204'>{STYLE}"
        f"<rect width='92' height='204' fill='{INK}'/><path d='M0 24.5H92' stroke='#ffffff1f'/>"
        + t(12, 40, "m", "BOARDING", g) + t(12, 53, "b", "XEN → DINE", " style='font-size:9.5px;fill:#fff'")
        + t(12, 68, "m", "SEAT", g) + t(12, 85, "b", "0808A", " textLength='58' style='font-size:18px;fill:#fff'")
        + t(12, 100, "m", "GATE", g) + t(12, 117, "b", "31F", f" style='font-size:18px;fill:{YEL}'")
        + "<text transform='translate(84 40) rotate(90)' style='font-size:4.5px;letter-spacing:1.8px;fill:#5E6366'>PASS · 搭乗券</text>"
        + f"<path d='M12 169H80' stroke='#fff' stroke-width='18' stroke-dasharray='{dash}'/>"
        + t(12, 194, "m", "NO.0001 · XEN", g)
        + "<path d='M0 30V194' stroke='#F3F4F3' stroke-width='3' stroke-dasharray='0 7' stroke-linecap='round'/>"
        + notch(0) + "</svg>")
    return main, stub


def calendar_svg(today):
    """Month calendar popup (hover on きのう). Regenerated hourly, Asia/Seoul date."""
    import calendar
    W, H = 210, 214
    JPM = "一二三四五六七八九十"
    jm = ("十" + JPM[today.month - 11] if today.month > 10 else JPM[today.month - 1]) + "月"
    first_wd = (date(today.year, today.month, 1).weekday() + 1) % 7   # 0 = Sunday
    days = calendar.monthrange(today.year, today.month)[1]
    out = [f"<svg xmlns='http://www.w3.org/2000/svg' width='{W}' height='{H}'>{STYLE}",
           f"<rect x='.5' y='.5' width='{W - 1}' height='{H - 1}' rx='6' fill='#FCFCFB' stroke='#14151633'/>",
           f"<path d='M6 .5h{W - 12}a5.5 5.5 0 0 1 5.5 5.5V24H.5V6A5.5 5.5 0 0 1 6 .5z' fill='{INK}'/>",
           "<text x='12' y='15' style='font-size:5.5px;letter-spacing:1.6px;fill:#8F9497'>◇ CALENDAR · 暦</text>",
           f"<text x='{W - 12}' y='15' text-anchor='end' style='font-size:5.5px;letter-spacing:1.6px;fill:#8F9497'>KST</text>",
           f"<rect x='{W - 40}' y='9' width='8' height='8' fill='{YEL}'/>",
           f"<text class='b' x='12' y='60' style='font-size:30px'>{today.month:02d}</text>",
           f"<text x='60' y='47' style='font-size:7px;letter-spacing:1.6px;fill:{INK}'>{today.strftime('%B').upper()}</text>",
           f"<text x='60' y='58' style='font-size:6px;letter-spacing:1.4px'>{today.year} · {jm}</text>",
           f"<path d='M12 68H{W - 12}' stroke='{INK}'/>"]
    cw, ch, x0, y0 = 26.6, 19, 12, 90
    for i, wd in enumerate("日月火水木金土"):
        out.append(f"<text class='j' x='{x0 + cw * i + cw / 2:.1f}' y='81' text-anchor='middle' style='font-size:6px;letter-spacing:0;fill:{'#8F9497' if i == 0 else INK}'>{wd}</text>")
    for dnum in range(1, days + 1):
        k = first_wd + dnum - 1
        cx, cy = x0 + cw * (k % 7) + cw / 2, y0 + ch * (k // 7) + 12
        d = date(today.year, today.month, dnum)
        if d == today:
            out.append(f"<rect x='{cx - 10:.1f}' y='{cy - 9.5:.1f}' width='20' height='14' fill='{YEL}'/><rect x='{cx - 10:.1f}' y='{cy + 4.5:.1f}' width='20' height='1.5' fill='{INK}'/>")
            fill = INK
        elif d < today:
            fill = "#A9AFB2"
        else:
            fill = "#8F9497" if k % 7 == 0 else INK
        out.append(f"<text class='v' x='{cx:.1f}' y='{cy:.1f}' text-anchor='middle' style='font-size:8px;fill:{fill}'>{dnum}</text>")
        if d == START or (d.month == START.month and d.day == START.day and d > START):
            out.append(f"<circle cx='{cx + 8:.1f}' cy='{cy - 8:.1f}' r='1.6' fill='{BLUE}' stroke='{INK}' stroke-width='.6'/>")
    dnum_today = (today - START).days + 1
    out += [f"<path d='M12 {H - 22}H{W - 12}' stroke='#14151624'/>",
            f"<text x='12' y='{H - 11}' style='font-size:5.5px;letter-spacing:1.4px'>TODAY {today:%m.%d} {today.strftime('%a').upper()}</text>",
            f"<text x='{W - 12}' y='{H - 11}' text-anchor='end' style='font-size:5.5px;letter-spacing:1.4px;fill:{INK}'>D+{dnum_today} · 記録中</text>",
            "</svg>"]
    return "".join(out)


def clock_svg(now):
    """Current-hour popup (hover on あした). GitHub regenerates it hourly, so it shows the hour, not minutes."""
    W, H = 210, 128
    h = now.hour
    out = [f"<svg xmlns='http://www.w3.org/2000/svg' width='{W}' height='{H}'>{STYLE}",
           f"<rect width='{W}' height='{H}' rx='6' fill='{INK}'/>",
           "<text x='12' y='17' style='font-size:5.5px;letter-spacing:1.6px;fill:#8F9497'>◷ 現在時刻 · NOW</text>",
           f"<text x='{W - 12}' y='17' text-anchor='end' style='font-size:5.5px;letter-spacing:1.6px;fill:#8F9497'>KST · UTC+9</text>",
           "<path d='M12 24.5H198' stroke='#ffffff1f'/>",
           f"<text class='b' x='10' y='70' style='font-size:44px;fill:#fff'>{h:02d}</text>",
           f"<text class='j' x='70' y='70' style='font-size:14px;letter-spacing:1px;fill:{YEL}'>時台</text>",
           f"<text x='{W - 12}' y='48' text-anchor='end' style='font-size:7px;letter-spacing:1.4px;fill:#A9AFB2'>{h:02d}:00 — {h:02d}:59</text>",
           f"<text x='{W - 12}' y='62' text-anchor='end' style='font-size:7px;letter-spacing:1.4px;fill:#fff'>{now:%Y.%m.%d} · {now:%a}</text>".replace(now.strftime('%a'), now.strftime('%a').upper())]
    sw = 186 / 24
    for i in range(24):
        fill = YEL if i == h else ("#5E6366" if i < h else "#2B2E30")
        out.append(f"<rect x='{12 + sw * i:.2f}' y='86' width='{sw - 1.5:.2f}' height='{12 if i == h else 8}' fill='{fill}'/>")
    for i in (0, 6, 12, 18, 24):
        out.append(f"<text x='{12 + sw * i:.1f}' y='108' text-anchor='{'start' if i == 0 else ('end' if i == 24 else 'middle')}' style='font-size:5px;letter-spacing:1px;fill:#8F9497'>{i:02d}</text>")
    out += [f"<text x='12' y='{H - 8}' style='font-size:4.5px;letter-spacing:1.4px;fill:#5E6366'>HOURLY SYNC — 1時間ごとに更新</text>", "</svg>"]
    return "".join(out)


if __name__ == "__main__":
    today = datetime.now(TZ).date()
    svg, info = dday_svg(today)
    open("dday.svg", "w", encoding="utf-8").write(svg)
    main, stub = ticket_svg()
    open("ticket.svg", "w", encoding="utf-8").write(main)
    open("stub.svg", "w", encoding="utf-8").write(stub)
    now = datetime.now(TZ)
    open("calendar.svg", "w", encoding="utf-8").write(calendar_svg(today))
    open("clock.svg", "w", encoding="utf-8").write(clock_svg(now))
    print(today, info, f"{now:%H}時台")
