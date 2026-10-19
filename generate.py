"""XEN · luvlinks widgets.
Writes:
  dday_w.svg – WHITE LAB record panel (updates daily)
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
    """W3 "FLASHBACK" LED board (330 x 210): dark board with LED panels + light route track below."""
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
    Y = 186
    mx = 9 + 311 * p
    label = f"※{n}周年まで あと {left}日 ・ {nxt:%Y.%m.%d} ・ 記録は続く"
    tw = round(len(label) * 10.6)
    J = "font-family:" + JP.replace("'", "&apos;")
    def panel(x, y, w, h, body):
        return (f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='1.5' fill='#0E0F10' stroke='#000'/>{body}"
                f"<rect x='{x}' y='{y}' width='{w}' height='{h}' fill='url(#L)'/>"
                f"<path d='M{x} {y + h + 1}H{x + w}' stroke='#5E6366' stroke-width='1.5'/>")
    nw = len(NAME) * 22 + 8
    svg = (f"<svg xmlns='http://www.w3.org/2000/svg' width='330' height='210'>{STYLE}"
        "<defs><linearGradient id='g' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#232526'/><stop offset='1' stop-color='#1A1C1D'/></linearGradient>"
        "<pattern id='L' width='1.5' height='1.5' patternUnits='userSpaceOnUse'><path d='M0 0h1.5v1.5H0zM.75 .2a.55 .55 0 1 0 .001 0z' fill='#111213' fill-opacity='.62' fill-rule='evenodd'/></pattern>"
        "<clipPath id='q'><rect x='9' y='128' width='312' height='20'/></clipPath></defs>"
        "<rect x='.5' y='.5' width='329' height='151' rx='4' fill='url(#g)' stroke='#000'/>"
        "<text x='10' y='14' style='font-size:5.5px;letter-spacing:1.6px;fill:#8F9497'>記録対象 · SUBJECT</text>"
        f"<text x='10' y='24' style='font-size:5.5px;letter-spacing:1.6px'>SINCE {START:%Y.%m.%d}</text>"
        f"<rect x='261' y='7' width='14' height='30' fill='{YEL}'/>"
        f"<text x='282' y='27' style='{J};font-size:18px;font-weight:500;letter-spacing:0;fill:#fff'>記録</text>"
        "<text x='282' y='35' style='font-family:Arial,sans-serif;font-size:5.5px;letter-spacing:.4px;fill:#A9AFB2'>record</text>"
        + panel(8, 42, 314, 34,
                f"<rect x='14' y='46' width='{nw}' height='26' fill='{BLUE}'/>"
                f"<text class='j' x='18' y='67' style='font-size:22px;font-weight:900;letter-spacing:0;fill:#10283A'>{esc(NAME)}</text>"
                f"<text class='b' x='312' y='70' text-anchor='end' style='font-size:26px;fill:{YEL}'>{num}</text>")
        + panel(8, 80, 314, 20, f"<text class='j' x='165' y='93.5' text-anchor='middle' style='font-size:9px;font-weight:700;letter-spacing:2.2px;fill:#F3F4F3'>{dayi}日目 ・ DAY {dayi:03d} / {cycle} ・ {pct}%</text>")
        + panel(8, 104, 314, 20, f"<text class='j' x='165' y='117.5' text-anchor='middle' style='font-size:9px;font-weight:700;letter-spacing:2.2px;fill:{YEL}'>◀ きのう ・ きょう ・ あした ▶</text>")
        + panel(8, 128, 314, 20,
                f"<g clip-path='url(#q)'><text class='j' x='322' y='141.5' textLength='{tw}' style='font-size:9px;font-weight:700;letter-spacing:1.4px;fill:{CREAM}'>{label}"
                f"<animateTransform attributeName='transform' type='translate' from='0 0' to='-{tw + 314} 0' dur='{(tw + 314) / 36:.2f}s' repeatCount='indefinite'/></text></g>")
        + f"<path d='M9 {Y}H320' stroke='#DCDFE3' stroke-width='5'/><path d='M0 {Y}H{max(9, mx - 8):.0f}' stroke='{BLUE}' stroke-width='5'/>"
        + f"<g fill='#fff' stroke='{INK}' stroke-width='2.8'>" + "".join(f"<circle cx='{x}' cy='{Y}' r='5'/>" for x in (9, 87, 165, 243)) + "</g>"
        + f"<circle cx='320' cy='{Y}' r='7.5' fill='#fff' stroke='{INK}' stroke-width='2.4'/><circle cx='320' cy='{Y}' r='4.2' fill='{CREAM}'/>"
        + "".join(f"<circle cx='{mx:.0f}' cy='{Y}' r='9' fill-opacity='0'><animate attributeName='r' values='9;20' keyTimes='0;1' calcMode='spline' keySplines='.2 .7 .3 1' dur='3.6s' begin='{b}s' repeatCount='indefinite'/><animate attributeName='fill-opacity' values='.13;0' dur='3.6s' begin='{b}s' repeatCount='indefinite'/></circle>" for b in (0, 1.8))
        + f"<rect x='{mx - 18:.0f}' y='157' width='36' height='13' fill='{INK}'/><text class='j' x='{mx:.0f}' y='166.6' text-anchor='middle' style='font-size:8px;letter-spacing:0;fill:#fff'>現在地</text>"
        + f"<circle cx='{mx:.0f}' cy='{Y}' r='8' fill='{BLUE}' stroke='{INK}' stroke-width='3.4'/>"
        + f"<text class='v' y='205' style='font-size:7.5px;letter-spacing:1.4px'>START</text>"
        + f"<text class='v' x='330' y='205' text-anchor='end' style='font-size:7.5px;letter-spacing:1.4px'>{ordinal(n)}</text></svg>")
    return svg, f"{num} · {n}周年まで{left}日 · {pct}%"


def dday_w_svg(today):
    """WHITE LAB record panel (142 x 98) — content only; the glass panel itself is drawn by the page CSS."""
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
    sign, num = ("D+", dnum) if dnum > 0 else ("D-", 1 - dnum)
    K, M, Yd = "#2B333B", "#8A939B", "#EDCC55"
    MO = "font-family:ui-monospace,Menlo,Consolas,monospace"
    SA = "font-family:Pretendard,&apos;Helvetica Neue&apos;,Arial,sans-serif"
    JJ = "font-family:" + JP.replace("'", "&apos;")
    tx, ty, tw = 10, 68, 122
    mx = tx + tw * p
    msg = esc(f"※ {n}周年まで あと {left}日 · {nxt:%Y.%m.%d} · 記録は続く")
    mw = round(len(msg) * 5.2)
    o = [f"<svg xmlns='http://www.w3.org/2000/svg' width='284' height='196' viewBox='0 0 142 98'>",
         "<defs><linearGradient id='pl' x1='0' x2='1'><stop offset='0' stop-color='#E3F1FA'/><stop offset='1' stop-color='#FBF3D2'/></linearGradient>",
         "<linearGradient id='pr' x1='0' x2='1'><stop offset='0' stop-color='#C8E6F7'/><stop offset='1' stop-color='#8CC6EC'/></linearGradient>",
         f"<clipPath id='mq'><rect x='{tx}' y='82' width='{tw}' height='10'/></clipPath></defs>",
         f"<text x='10' y='14.5' style='{MO};font-size:5.2px;font-weight:700;letter-spacing:.6px;fill:{M}'>◇ RECORD · 記録</text>",
         f"<rect x='98' y='7' width='34' height='11' rx='5.5' fill='url(#pl)'/>",
         f"<text x='115' y='14.6' text-anchor='middle' style='{JJ};font-size:5.6px;font-weight:700;fill:{K}'>{NAME}</text>",
         f"<text x='9' y='47' style='{SA};font-size:30px;letter-spacing:-1.2px;fill:{K}'><tspan style='font-weight:200'>{sign}</tspan><tspan style='font-weight:800'>{num}</tspan></text>",
         f"<text x='10' y='58' style='{MO};font-size:4.8px;font-weight:600;letter-spacing:.4px;fill:{K}'>{dayi}日目 · DAY {dayi:03d} / {cycle} · {pct}%</text>",
         f"<rect x='{tx}' y='{ty}' width='{tw}' height='.6' fill='{K}' opacity='.25'/>",
         f"<rect x='{tx}' y='{ty - .7}' width='{tw * p:.1f}' height='2' fill='url(#pr)'/>"]
    o += [f"<rect x='{tx + tw * f - .3:.1f}' y='{ty - 2}' width='.6' height='5' fill='{K}' opacity='.35'/>" for f in (0, .25, .5, .75, 1)]
    o += [f"<circle cx='{mx:.1f}' cy='{ty + .3}' r='2.6' fill='{Yd}'/>",
          f"<circle cx='{mx:.1f}' cy='{ty + .3}' r='2.6' fill='none' stroke='{Yd}' stroke-width='.8'><animate attributeName='r' values='2.6;7' dur='2.4s' repeatCount='indefinite'/><animate attributeName='opacity' values='.9;0' dur='2.4s' repeatCount='indefinite'/></circle>",
          f"<text x='{tx}' y='{ty + 8}' style='{MO};font-size:4px;font-weight:600;fill:{M}'>START</text>",
          f"<text x='{mx:.1f}' y='{ty - 5}' text-anchor='middle' style='{JJ};font-size:4px;font-weight:700;fill:{K}'>現在地</text>",
          f"<text x='{tx + tw}' y='{ty + 8}' text-anchor='end' style='{MO};font-size:4px;font-weight:600;fill:{M}'>{ordinal(n)}</text>",
          f"<rect x='{tx}' y='82' width='{tw}' height='.6' fill='{K}' opacity='.1'/>",
          f"<g clip-path='url(#mq)'><text x='0' y='89.5' style='{JJ};font-size:5.4px;letter-spacing:.3px;fill:{M}'>{msg}"
          f"<animateTransform attributeName='transform' type='translate' values='{tx + tw} 0;{tx - mw} 0' dur='{(tw + mw) / 16:.1f}s' repeatCount='indefinite'/></text></g>",
          "</svg>"]
    return "".join(o)


def ticket_svg():
    """Design Q+ "RESERVED": light main part (238 wide) with train formation + seat map, black stub (92 wide).
    Photo, avatar, name, handle and share button are page elements placed over these by the CSS."""
    dash = "1 1 2 1 1 2 3 1 1 1 2 2 1 1 3 2 1 1 2 1 1 2 2 1 3 1 1 2 1 1 2 1 1 3"
    t = lambda x, y, c, txt, extra="": f"<text{f" class='{c}'" if c != 'm' else ''} x='{x}' y='{y}'{extra}>{txt}</text>"
    e = " text-anchor='end'"
    notch = lambda x: f"<circle cx='{x}' r='9' fill='#F3F4F3'/><circle cx='{x}' cy='204' r='9' fill='#F3F4F3'/>"
    lab = " style='font-size:5.5px;letter-spacing:1.3px'"
    G = "#E6E8E8"
    # formation: 8 cars, car 8 highlighted
    cw = (214 - 7 * 3) / 8
    cars = ""
    for k in range(8):
        x = 12 + k * (cw + 3)
        last = k == 7
        cars += f"<rect x='{x:.2f}' y='131' width='{cw:.2f}' height='15' rx='{6 if k in (0, 7) else 2}' fill='{INK if last else G}'/>"
        if k == 0:
            cars += f"<rect x='{x + 8:.2f}' y='131' width='{cw - 8:.2f}' height='15' rx='2' fill='{G}'/>"
        if last:
            cars += f"<rect x='{x:.2f}' y='131' width='{cw - 8:.2f}' height='15' rx='2' fill='{INK}'/>"
        cars += t(f"{x + cw / 2:.2f}", 141.5 if not last else 142, "b", str(k + 1), f" text-anchor='middle' style='font-size:{8 if last else 6.5}px;fill:{YEL if last else '#8F9497'}'")
    # seat map of car 8: rows A/B x 12 seats, seat A-08 highlighted
    sx0, sw = 48, (222 - 48 - 11 * 2) / 12
    seats = ""
    for r, y in (("A", 159.5), ("B", 172.5)):
        for k in range(12):
            x = sx0 + k * (sw + 2)
            hit = r == "A" and k == 7
            seats += f"<rect x='{x:.2f}' y='{y}' width='{sw:.2f}' height='11' rx='1.5' fill='{YEL if hit else G}'{' stroke=' + chr(39) + INK + chr(39) + ' stroke-width=' + chr(39) + '1.2' + chr(39) if hit else ''}/>"
            if hit:
                seats += t(f"{x + sw / 2:.2f}", y + 7.6, "b", "08", " text-anchor='middle' style='font-size:4.5px'")
    main = (f"<svg xmlns='http://www.w3.org/2000/svg' width='238' height='204'>{STYLE}"
        f"<rect width='238' height='204' fill='#FCFCFB'/>"
        f"<rect width='238' height='24' fill='{INK}'/><circle cx='17.5' cy='12' r='4.7' fill='none' stroke='#fff' stroke-width='1.6'/><circle cx='17.5' cy='12' r='2' fill='#fff'/>"
        + t(29, 15.5, "b", "SERAPHIX", " textLength='66' style='font-size:10px;letter-spacing:1.8px;fill:#fff'")
        + f"<rect x='148' y='6.5' width='31' height='11' fill='{BLUE}'/>"
        + t(163.5, 14.6, "j", "指定席", " text-anchor='middle' style='font-size:6.5px;font-weight:900;letter-spacing:1.2px'")
        + t(184, 14.5, "m", "RESERVED", " textLength='42' style='font-size:5.5px;fill:#A9AFB2'")
        + f"<rect y='80' width='238' height='3' fill='{YEL}'/>"
        + t(74, 92, "m", "PASSENGER · 乗客", lab)
        + t(12, 126, "b", "XEN", " textLength='28' style='font-size:13px'") + t(43, 126, "m", "発", lab)
        + t(119, 125, "m", "◀ 進行方向 ▶", " text-anchor='middle' style='font-size:5.5px;letter-spacing:1px'")
        + t(190, 126, "m", "着", e + lab) + t(226, 126, "b", "DINE", e + " textLength='34' style='font-size:13px'")
        + cars
        + f"<rect x='12.6' y='156.6' width='212.8' height='28.8' rx='4' fill='#fff' stroke='{INK}' stroke-width='1.2'/>"
        + f"<path d='M16.6 156.6H34V185.4H16.6a4 4 0 0 1-4-4V160.6a4 4 0 0 1 4-4z' fill='{INK}'/>"
        + t(23.3, 172, "b", "8", f" text-anchor='middle' style='font-size:9px;fill:{YEL}'")
        + t(23.3, 180.5, "j", "号車", " text-anchor='middle' style='font-size:4.5px;font-weight:700;letter-spacing:0;fill:#fff'")
        + t(40, 167.5, "b", "A", " style='font-size:5px'") + t(40, 180.5, "b", "B", " style='font-size:5px;fill:#8F9497'")
        + seats
        + t(12, 198, "m", "A席 = 窓側 WINDOW", " style='font-size:5.5px;letter-spacing:1px'")
        + t(226, 198, "m", "列車 <tspan style='fill:#111;font-weight:600'>VX-01 · 26.08.08</tspan>", e + " style='font-size:5.5px;letter-spacing:1px'")
        + "<path d='M237 30V190' stroke='#14151650' stroke-width='1.5' stroke-dasharray='4 3'/>"
        + notch(238) + "</svg>")
    g = " style='fill:#8F9497;font-size:5px;letter-spacing:1.3px'"
    stub = (f"<svg xmlns='http://www.w3.org/2000/svg' width='92' height='204'>{STYLE}"
        f"<rect width='92' height='204' fill='{INK}'/><path d='M0 24.5H92' stroke='#ffffff1f'/>"
        + t(12, 40, "m", "発車 · DEPARTS", g)
        + t(12, 62, "b", "08:08", f" textLength='62' style='font-size:22px;fill:{YEL}'")
        + t(12, 77, "m", "番線 TRACK", g) + t(12, 93, "b", "31F", " style='font-size:16px;fill:#fff'")
        + t(12, 106, "m", "号車 CAR", g) + t(12, 120, "b", "8A", " style='font-size:13px;fill:#fff'")
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
    open("dday_w.svg", "w", encoding="utf-8").write(dday_w_svg(today))
    main, stub = ticket_svg()
    open("ticket.svg", "w", encoding="utf-8").write(main)
    open("stub.svg", "w", encoding="utf-8").write(stub)
    now = datetime.now(TZ)
    open("calendar.svg", "w", encoding="utf-8").write(calendar_svg(today))
    open("clock.svg", "w", encoding="utf-8").write(clock_svg(now))
    print(today, info, f"{now:%H}時台")
