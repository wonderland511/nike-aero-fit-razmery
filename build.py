#!/usr/bin/env python3
"""Генератор index.html: подборка Nike Aero-FIT + подбор размера по меркам.
Запуск: python3 build.py  (пишет index.html рядом)."""
import html, os
from decimal import Decimal, ROUND_HALF_UP
def r2(x, q="0.01"): return float(Decimal(str(x)).quantize(Decimal(q), ROUND_HALF_UP))

RATE = 0.17295          # 1 BRL -> USD, ЕЦБ через api.frankfurter.dev, курс на 17.11.2026
RATE_DATE = "17.11.2026"
RATE_URL = "https://api.frankfurter.dev/v1/latest?from=BRL&to=USD"

def usd(brl): return brl * RATE
def fbrl(x): x = r2(x); return "R$ " + f"{x:,.2f}".replace(",", " ").replace(".", ",").replace(" ", ".")
def fusd(x): x = r2(x); return "$" + f"{x:,.2f}".replace(",", " ").replace(".", ",").replace(" ", " ")
e = html.escape

# Мерки (см) — со схемы пользователя
ME = dict(neck=40, shoulders="44–45", chest=100.5, bicep=33.5, waist=78, sleeve=59, hips=96.5,
          back_glute=72, trouser_waist=84, thigh=56, trouser_len=96, back_knee=99)

# Официальная таблица Nike (Men's tops / Men's bottoms, nike.com/gb/size-fit), дюймы -> см
IN = 2.54
CH = {"P": (35*IN, 37.5*IN), "M": (37.5*IN, 41*IN), "G": (41*IN, 44*IN), "GG": (44*IN, 48.5*IN)}
WA = {"P": (29*IN, 32*IN), "M": (32*IN, 35*IN), "G": (35*IN, 38*IN), "GG": (38*IN, 43*IN)}
HI = {"P": (35*IN, 37.5*IN), "M": (37.5*IN, 41*IN), "G": (41*IN, 44*IN), "GG": (44*IN, 47*IN)}
EU = {"P": "S", "M": "M", "G": "L", "GG": "XL", "GGG": "XXL"}

def which(table, v):
    for k, (a, b) in table.items():
        if a <= v < b: return k
    return "—"

def c1(x): x = r2(x, "0.1"); return f"{x:.1f}".replace(".", ",").replace(",0", "")

def fitbar(label, value, table, rec, lo, hi, note=""):
    span = hi - lo
    segs = []
    for k, (a, b) in table.items():
        a2, b2 = max(a, lo), min(b, hi)
        if b2 <= a2: continue
        left = (a2 - lo) / span * 100; w = (b2 - a2) / span * 100
        cls = "seg pick" if k == rec else "seg"
        rng = f'<em>{c1(a)}–{c1(b)}</em>' if w >= 16 else ''
        segs.append(f'<div class="{cls}" style="left:{left:.2f}%;width:{w:.2f}%"><span>{k}</span>{rng}</div>')
    pos = (value - lo) / span * 100
    got = which(table, value)
    n = f'<p class="fb-note">{note}</p>' if note else ""
    return f'''<div class="fitbar">
  <div class="fb-head"><span>{e(label)}</span><b>{c1(value)} см → {got}</b></div>
  <div class="fb-track">{''.join(segs)}<i class="fb-mark" style="left:{pos:.2f}%"><span>{c1(value)}</span></i></div>{n}
</div>'''

ITEMS = [
 dict(id="tshirt", kind="Футболка беговая", name="T-shirt Performance Nike Aero-Fit Stride Masculina",
      code="IH0745-236", color="Bege (у Nike: Cream II/Sail)", store="Velocità",
      url="https://www.velocita.com.br/produto/t-shirt-performance-nike-aero-fit-stride-masculina-24200",
      nike="https://www.nike.com/gb/t/stride-mens-aero-fit-short-sleeve-running-top-9b5piMBN/IH0745-236",
      card=499.90, card_note="или 5× R$ 99,98 без процентов", pix=499.90*0.95, pix_note="≈ −5% по Pix (расчёт)", old=None,
      sizes=[("P",1),("M",1),("G",1),("GG",1)], rec="M", rec_eu="M",
      imgs=["tshirt-1","tshirt-2","tshirt-3","tshirt-4","tshirt-6","tshirt-5"],
      bars="top",
      verdict="Берите <b>M</b>. Грудь 100,5 см — в середине диапазона M, футболка сядет так, как задумано: свободно, но не мешком.",
      look=["<b>Корпус.</b> Посадка у Nike — «Standard fit: easy and traditional»: прямой силуэт без обтяжки. Грудь 100,5 — в середине M (95,3–104,1 см), запас ткани ровный.",
            "<b>Талия.</b> 78 см — это S по таблице, поэтому у пояса футболка будет висеть прямо, с небольшим запасом. Это нормально: Nike советует при расхождении груди и талии выбирать по груди.",
            "<b>Ткань.</b> Лёгкий трикотаж Aero-FIT с сетчатыми зонами спереди и сзади, разрезы по бокам низа — не липнет и не стесняет шаг (100% полиэстер).",
            "<b>Длина.</b> Nike не публикует длину изделия; на фото модель ростом 184 см — в M, низ закрывает пояс шорт.",
            "<b>G</b> не нужен: грудь 100,5 ниже диапазона G (104,1–111,8) — будет заметно мешковато в плечах и корпусе."]),
 dict(id="regata", kind="Майка беговая", name="Regata Performance Nike Aero-Fit Stride Masculina",
      code="IM5148-236", color="Bege", store="Velocità",
      url="https://www.velocita.com.br/produto/regata-performance-nike-aero-fit-stride-masculina-24241",
      nike="https://www.nike.com/gb/t/stride-aero-fit-mens-running-tank-top-hHmuPWP9/IM5148-702",
      card=449.90, card_note="или 4× R$ 112,48 без процентов", pix=449.90*0.95, pix_note="≈ −5% по Pix (расчёт)", old=None,
      sizes=[("P",0),("M",1),("G",1),("GG",1)], rec="M", rec_eu="M",
      imgs=["regata-1","regata-2"],
      bars="top",
      verdict="Берите <b>M</b> — та же логика, что и у футболки: по груди вы ровно в M.",
      look=["<b>Корпус.</b> Standard fit, как и футболка той же линейки Stride: прямой силуэт, без облегания. Грудь 100,5 — середина M.",
            "<b>Проймы.</b> По фото — глубокие проймы и открытые бока: плечи 44–45 см и бицепс 33,5 см ничем не стеснены (у майки нет рукава, таблица Nike эти мерки не учитывает).",
            "<b>Низ.</b> Разрезы по бокам — свобода движения на бегу; талия 78 (S) даст лёгкий запас у пояса.",
            "<b>Наличие.</b> На скриншоте у Velocità размер P недоступен — вам он и не нужен."]),
 dict(id="polo", kind="Поло теннисное", name="Camisa Polo Nike Court Air Force Slam U2 NY Masculina",
      code="IM6607-677", color="Team Red/Pale Ivory (бордовый)", store="Nike Brasil",
      url="https://www.nike.com.br/camisa-polo-nike-court-air-force-slam-u2-ny-masculina-105489.html?cor=P1",
      nike="https://www.nike.com/t/nikecourt-slam-mens-aero-fit-tennis-polo-4Hrut3kE/IM6607-677",
      card=147.36*4, card_note="4× R$ 147,36 без процентов (итого)", pix=560.00, pix_note="по Pix, −30% от R$ 799,99", old=799.99,
      sizes=[("P",1),("M",1),("G",1),("GG",1),("GGG",1)], rec="G", rec_eu="L",
      imgs=["polo-1","polo-4","polo-5","polo-2","polo-3"],
      bars="top",
      verdict="Берите <b>G</b>. По таблице вы M, но на странице именно этого поло Nike Brasil пишет: «Compre um tamanho maior que o usual» — берите на размер больше обычного.",
      look=["<b>Почему G, а не M.</b> По груди 100,5 вы в M (95,3–104,1). Но в блоке «Acerte o tamanho» на карточке этого поло nike.com.br советует брать размер больше обычного — значит, модель маломерит.",
            "<b>Как сядет G.</b> По таблице G рассчитан на грудь 104,1–111,8 см; учитывая, что поло маломерит, оно должно сесть как обычное M с небольшим запасом — свободно в плечах при подаче и замахе.",
            "<b>Конструкция.</b> Ластовица под мышкой и смещённый назад плечевой шов — для свободы руки; удлинённая спинка (drop-tail) не выбивается из шорт.",
            "<b>Если любите плотнее</b> — M, но тогда возможно облегание по груди и плечам (44–45 см).",
            "<b>Ткань.</b> Aero-FIT, 100% полиэстер."]),
 dict(id="court", kind="Шорты теннисные", name="Shorts Dri-FIT Nike Court Slam U2 NY Masculino",
      code="IM5776-677", color="Team Red/Pale Ivory (бордовый)", store="ATPSHOP",
      url="https://atpshop.com.br/produto/shorts-dri-fit-nike-court-slam-u2-ny-masculino/",
      nike="https://www.nike.com/t/nikecourt-slam-mens-dri-fit-tennis-shorts-htg3AQum/IM5776-677",
      card=569.90, card_note="или 10× R$ 56,99 без процентов", pix=512.91, pix_note="по Pix (−10%)", old=599.90,
      sizes=[("P",1),("M",1),("G",1),("GG",1)], rec="M", rec_eu="M",
      imgs=["court-2","court-3","court-1","court-6","court-4","court-5"],
      bars="bottom",
      verdict="Берите <b>M</b>: по бёдрам (96,5) и по талии брюк (84) вы в M — к поло G в комплекте их брать не нужно.",
      look=["<b>Бёдра.</b> 96,5 см — нижняя часть диапазона M (95,3–104,1): по бёдрам и ягодицам будет свободно, без натяжения.",
            "<b>Пояс.</b> Там, где сидят брюки, у вас 84 см — это M (81,3–88,9). Эластичный пояс; Nike описывает посадку на поясе как плотную («snug fit»).",
            "<b>Ткань.</b> Тянется в 4 стороны (89% полиэстер / 11% эластан), сетка 100% полиэстер; карманы расширяются под мячи.",
            "<b>Длина.</b> Шаговый шов Nike не публикует. По фото модели (191 см, размер M) — выше колена, заметно длиннее беговых Stride 12,5 см.",
            "<b>Посадка</b> — Standard fit."]),
 dict(id="bermuda", kind="Шорты беговые", name="Bermuda Nike Stride Men's Aero-FIT 5 Masculina",
      code="IM5132-010", color="Preto (чёрный)", store="Centauro",
      url="https://www.centauro.com.br/-bermud-nike-stride-mens-aero-fit-5-masculina-9976xc.html",
      nike="https://www.nike.com/bg/t/stride-aero-fit-mens-12-5cm-approx-brief-lined-running-shorts-bizoxOG3/IM5132-010",
      card=499.99, card_note="или 6× R$ 83,33 без процентов", pix=449.99, pix_note="по Pix (−10%)", old=None,
      sizes=[("P",1),("M",1),("G",1),("GG",0)], rec="M", rec_eu="M",
      imgs=["bermuda-1","bermuda-3","bermuda-2","bermuda-4","bermuda-5","bermuda-6"],
      bars="bottom", inseam=True,
      verdict="Берите <b>M</b>. Бёдра 96,5 и талия брюк 84 — обе мерки в M; шорты короткие (шаговый шов 12,5 см) с трусами-подкладкой.",
      look=["<b>Длина.</b> Шаговый шов ≈ 12,5 см (5″) — короткие беговые шорты. По вашим меркам низ будет примерно на 14–15 см выше колена (шкала и расчёт выше).",
            "<b>Бёдра и пояс.</b> Бёдра 96,5 → M, талия брюк 84 → M. Пояс со шнурком — подгоняется по талии.",
            "<b>Бедро ноги 56 см.</b> Ширину штанины Nike не публикует; по бокам есть разрезы (hem vents) — шаг не ограничен.",
            "<b>Внутри.</b> Трусы-подкладка (92% полиэстер / 8% эластан), задний карман на молнии под телефон, боковые карманы. Верх — жаккард Aero-FIT, 100% полиэстер.",
            "<b>Наличие.</b> На скриншоте у Centauro размер GG недоступен, «últimas unidades» — M стоит брать сразу."]),
]

def img_tag(src, alt, cls="", eager=False):
    return f'<img src="img/{src}.jpg" alt="{e(alt)}" class="{cls}" loading="{"eager" if eager else "lazy"}" decoding="async" referrerpolicy="no-referrer">'

def card(it, idx):
    gal = "".join(
        f'<button class="g-item" data-group="{it["id"]}" data-i="{i}" aria-label="Увеличить фото {i+1}">{img_tag(s, it["name"]+" — фото "+str(i+1), eager=(idx==0 and i==0))}</button>'
        for i, s in enumerate(it["imgs"]))
    sizes = "".join(
        f'<span class="sz{" on" if k==it["rec"] else ""}{"" if ok else " off"}" title="{"есть" if ok else "нет в наличии на скриншоте"}">{k}</span>'
        for k, ok in it["sizes"])
    if it["bars"] == "top":
        bars = (fitbar("Грудь", ME["chest"], CH, it["rec"] if it["rec"] in CH else "M", 86, 116,
                       "Главная мерка для верха (правило Nike)") +
                fitbar("Талия", ME["waist"], WA, it["rec"], 72, 98))
    else:
        bars = (fitbar("Бёдра", ME["hips"], HI, it["rec"], 86, 116, "Главная мерка для низа (правило Nike)") +
                fitbar("Талия брюк (где сидит пояс)", ME["trouser_waist"], WA, it["rec"], 72, 98) +
                fitbar("Талия (самое узкое место)", ME["waist"], WA, it["rec"], 72, 98))
    ins = ""
    if it.get("inseam"):
        fold_knee = ME["back_knee"] - ME["back_glute"]   # 27
        inseam = 12.5
        gap = fold_knee - inseam
        sw = inseam / fold_knee * 100
        ins = f'''<div class="inseam">
  <div class="fb-head"><span>Где закончатся шорты</span><b>≈ {c1(gap)} см выше колена</b></div>
  <div class="ins-track"><div class="ins-short" style="width:{sw:.1f}%">шорты 12,5</div><div class="ins-leg">открытое бедро ≈ {c1(gap)}</div><div class="ins-knee">колено</div></div>
  <p class="fb-note">Расчёт: «спина до колен» {ME["back_knee"]} − «спина до ягодиц» {ME["back_glute"]} = {fold_knee} см от ягодичной складки до колена; минус шаговый шов 12,5 см (данные Nike). Оценка приблизительная: принимаем, что шаговый шов шорт сидит на уровне ягодичной складки.</p>
</div>'''
    old = f'<s>{fbrl(it["old"])}</s> ' if it["old"] else ""
    return f'''
<article class="card" id="{it["id"]}">
  <div class="gwrap"><div class="gallery">{gal}</div><p class="ghint">{len(it["imgs"])} фото · листайте → · нажмите, чтобы увеличить</p></div>
  <div class="body">
    <p class="kicker">{e(it["kind"])} · {e(it["store"])}</p>
    <h3>{e(it["name"])}</h3>
    <p class="meta">Артикул {it["code"]} · {e(it["color"])}</p>
    <div class="rec-row">
      <div class="rec"><small>Заказать</small><strong>{it["rec"]}</strong><small>{"= " + it["rec_eu"] if it["rec_eu"]!=it["rec"] else "= M"} по EU/US</small></div>
      <p class="verdict">{it["verdict"]}</p>
    </div>
    <div class="price">
      <div><span class="usd">{fusd(usd(it["pix"]))}</span><span class="brl">{old}{fbrl(it["pix"])} · {e(it["pix_note"])}</span></div>
      <div><span class="usd sm">{fusd(usd(it["card"]))}</span><span class="brl">{fbrl(it["card"])} картой · {e(it["card_note"])}</span></div>
    </div>
    <div class="sizes"><span class="lbl">Размеры в магазине:</span>{sizes}</div>
    <h4>Как будет сидеть на вас</h4>
    <div class="bars">{bars}</div>
    {ins}
    <ul class="look">{"".join(f"<li>{l}</li>" for l in it["look"])}</ul>
    <div class="actions">
      <a class="btn primary" href="{it["url"]}" target="_blank" rel="noopener">Открыть в {e(it["store"])} ↗</a>
      <a class="btn" href="{it["nike"]}" target="_blank" rel="noopener">Характеристики на nike.com ↗</a>
    </div>
  </div>
</article>'''

def summary():
    rows = []
    tp = tc = 0
    for it in ITEMS:
        tp += r2(it["pix"]); tc += r2(it["card"])
        rows.append(f'''<a class="srow" href="#{it["id"]}">
  {img_tag(it["imgs"][0], it["name"], "sthumb", eager=True)}
  <span class="sname"><b>{e(it["kind"])}</b><small>{e(it["store"])} · {e(it["color"].split(" (")[0])}</small></span>
  <span class="ssize">{it["rec"]}</span>
  <span class="sprice"><b>{fusd(usd(it["pix"]))}</b><small>{fbrl(it["pix"])}</small></span>
</a>''')
    rows.append(f'''<div class="srow total"><span></span><span class="sname"><b>Итого по Pix</b><small>картой — {fusd(usd(tc))} ({fbrl(tc)})</small></span><span></span><span class="sprice"><b>{fusd(usd(tp))}</b><small>{fbrl(tp)}</small></span></div>''')
    return "".join(rows)

def chart():
    def row(name, table, v):
        tds = "".join(f'<td class="{"hit" if a <= v < b else ""}">{c1(a)}–{c1(b)}</td>' for k, (a, b) in table.items())
        return f'<tr><th>{name}<small>у вас {c1(v)}</small></th>{tds}</tr>'
    head = "".join(f'<th>{k}<small>{EU[k]}</small></th>' for k in CH)
    return f'''<div class="tablewrap"><table class="chart">
<thead><tr><th>Мерка тела, см</th>{head}</tr></thead>
<tbody>{row("Грудь", CH, ME["chest"])}{row("Талия", WA, ME["waist"])}{row("Талия брюк", WA, ME["trouser_waist"])}{row("Бёдра", HI, ME["hips"])}</tbody>
</table></div>'''

measures = [("Шея", "40"), ("Ширина плеч", "44–45"), ("Грудь", "100,5"), ("Бицепс", "33,5"), ("Талия", "78"),
            ("Длина рукава", "59"), ("Бёдра", "96,5"), ("Спина до ягодиц", "72"), ("Талия брюк", "84"),
            ("Бедро ноги", "56"), ("Длина брюк", "96"), ("Спина до колен", "99")]

CSS = open(os.path.join(os.path.dirname(__file__), "style.css"), encoding="utf-8").read()
JS = open(os.path.join(os.path.dirname(__file__), "app.js"), encoding="utf-8").read()

page = f'''<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex, nofollow, noarchive, nosnippet, noimageindex">
<meta name="googlebot" content="noindex, nofollow">
<meta name="color-scheme" content="dark light">
<title>Nike Aero-FIT: размеры</title>
<style>{CSS}</style>
</head>
<body>
<header class="hero">
  <p class="eyebrow">Nike Aero-FIT · Stride &amp; Court Slam U2 NY</p>
  <h1>Что заказать<br>и в каком размере</h1>
  <p class="lead">5 вещей из ваших вкладок: цены в долларах, ссылки на магазины, фото и как каждая вещь сядет по вашим меркам.</p>
</header>

<main>
<section class="sec">
  <h2>Коротко: размеры к заказу</h2>
  <div class="summary">{summary()}</div>
  <p class="fine">Курс: 1 R$ = ${str(RATE).replace(".", ",")} (ЕЦБ, <a href="{RATE_URL}" target="_blank" rel="noopener">Frankfurter API</a>, на {RATE_DATE}). Цены — со скриншотов и страниц магазинов на 18.11.2026; у Velocità цена по Pix не показана — посчитана как −5% (баннер «5% de desconto no Pix»).</p>
</section>

<section class="sec">
  <h2>Ваши мерки</h2>
  <div class="mgrid">{"".join(f'<div class="m"><small>{n}</small><b>{v}</b></div>' for n, v in measures)}</div>
</section>

<section class="sec chart-sec">
  <div class="sec-head">
    <h2>Таблица Nike и где вы в ней</h2>
    <figure class="sticker">{img_tag("cat-stretch", "Милый котик потягивается на траве — разминка перед примеркой", "")}</figure>
  </div>
  {chart()}
  <ul class="rules">
    <li>Это мерки <b>тела</b>, а не вещи (официальные таблицы Nike Men's tops и Men's bottoms, переведены из дюймов в см).</li>
    <li>Верх: если грудь и талия дают разные размеры — Nike советует брать <b>по груди</b>. У вас грудь → M, талия → P.</li>
    <li>Низ: если бёдра и талия расходятся — брать <b>по бёдрам</b>. У вас бёдра → M, талия брюк → M.</li>
    <li>P / M / G / GG в бразильских магазинах — это S / M / L / XL. Сайт nike.com.br не пускает автоматическую проверку — перед заказом можно сверить в «Tabela de medidas» на карточке.</li>
  </ul>
</section>

<section class="sec">
  <h2>Каждая вещь подробно</h2>
  <div class="cards">{"".join(card(it, i) for i, it in enumerate(ITEMS))}</div>
</section>

<footer class="sec foot">
  <h2>Источники</h2>
  <ul>
    <li>Таблицы размеров Nike: <a href="https://www.nike.com/gb/size-fit/mens-tops-alpha" target="_blank" rel="noopener">Men's tops</a>, <a href="https://www.nike.com/gb/size-fit/mens-bottoms-alpha" target="_blank" rel="noopener">Men's bottoms</a>.</li>
    <li>Посадка, состав, рост моделей, шаговый шов 12,5 см — официальные карточки nike.com (ссылки «Характеристики» в каждой карточке).</li>
    <li>Совет «на размер больше» для поло — карточка товара на nike.com.br (блок «Acerte o tamanho»).</li>
    <li>Фото товаров — Centauro, Velocità, ATPSHOP, Nike.</li>
    <li>Стикер: «<a href="https://commons.wikimedia.org/wiki/File:Cat_stretching_out.jpg" target="_blank" rel="noopener">Cat stretching out</a>», Clavecin, Wikimedia Commons, public domain.</li>
  </ul>
</footer>
</main>

<div class="lb" id="lb" hidden>
  <button class="lb-x" aria-label="Закрыть">×</button>
  <button class="lb-nav prev" aria-label="Предыдущее фото">‹</button>
  <img alt="" id="lb-img">
  <button class="lb-nav next" aria-label="Следующее фото">›</button>
  <p class="lb-count" id="lb-count"></p>
</div>
<script>{JS}</script>
<script type="module">
(async () => {{
  try {{
    if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    const {{ animate }} = await import('https://cdn.jsdelivr.net/npm/motion@11.18.2/+esm');
    const sp = {{ type: 'spring', stiffness: 380, damping: 26 }};
    document.querySelectorAll('.btn, .srow:not(.total), .rec, .sticker img').forEach(el => {{
      el.addEventListener('pointerenter', () => animate(el, {{ scale: 1.03 }}, sp));
      el.addEventListener('pointerleave', () => animate(el, {{ scale: 1 }}, sp));
      el.addEventListener('pointerdown', () => animate(el, {{ scale: 0.97 }}, sp));
      el.addEventListener('pointerup', () => animate(el, {{ scale: 1.03 }}, sp));
    }});
    const cat = document.querySelector('.sticker img');
    if (cat) cat.addEventListener('click', () => animate(cat, {{ rotate: [0, -10, 8, -4, 0] }}, {{ duration: 0.7 }}));
    document.querySelectorAll('.fb-mark').forEach((m, i) => animate(m, {{ y: [-6, 0] }}, {{ delay: 0.3 + i * 0.04, type: 'spring', stiffness: 300, damping: 12 }}));
  }} catch (e) {{ /* анимации — только украшение */ }}
}})();
</script>
</body>
</html>'''

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
open(out, "w", encoding="utf-8").write(page)
print("ok", out, len(page))
for it in ITEMS:
    print(it["id"], it["rec"], fbrl(it["pix"]), fusd(usd(it["pix"])), fbrl(it["card"]), fusd(usd(it["card"])))
