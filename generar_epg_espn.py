import urllib.request
import urllib.error
import re
import gzip
import shutil
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from html import unescape

OUTPUT_XML = "epg_espn.xml"
OUTPUT_GZ = "epg_espn.xml.gz"
OUTPUT_DEFAULT = "epg.xml"
TIMEZONE_OFFSET = "-0500"

CHANNELS_CONFIG = [
    # === ESPN LATINOAMÉRICA ===
    {
        "id": "espn-lat.tv",
        "name": "LAT ®| ESPN",
        "streams": ["LAT ®| ESPN HD", "LAT ®| ESPN FHD"],
        "icon": "https://cdn.mitvstatic.com/channels/pe_espn_m.png",
        "source": "mitv",
        "country": "pe",
        "slug": "espn",
        "utc_offset": "-300",
        "category": "Deportes",
    },
    {
        "id": "espn2-lat.tv",
        "name": "LAT ®| ESPN 2",
        "streams": ["LAT ®| ESPN 2 HD", "LAT ®| ESPN 2 FHD"],
        "icon": "https://cdn.mitvstatic.com/channels/pe_espn-2_m.png",
        "source": "mitv",
        "country": "pe",
        "slug": "espn-2",
        "utc_offset": "-300",
        "category": "Deportes",
    },
    {
        "id": "espn3-lat.tv",
        "name": "LAT ®| ESPN 3",
        "streams": ["LAT ®| ESPN 3 HD", "LAT ®| ESPN 3 FHD"],
        "icon": "https://cdn.mitvstatic.com/channels/pe_espn-3_m.png",
        "source": "mitv",
        "country": "pe",
        "slug": "espn-3",
        "utc_offset": "-300",
        "category": "Deportes",
    },
    {
        "id": "espn4-lat.tv",
        "name": "LAT ®| ESPN 4",
        "streams": ["LAT ®| ESPN 4 HD", "LAT ®| ESPN 4 FHD"],
        "icon": "",
        "source": "gatotv",
        "slug": "espn_4_peru",
        "category": "Deportes",
    },
    {
        "id": "espn5-lat.tv",
        "name": "LAT ®| ESPN 5",
        "streams": ["LAT ®| ESPN 5 HD", "LAT ®| ESPN 5 FHD"],
        "icon": "",
        "source": "gatotv",
        "slug": "espn_5_peru",
        "category": "Deportes",
    },
    {
        "id": "espn6-lat.tv",
        "name": "LAT ®| ESPN 6",
        "streams": ["LAT ®| ESPN 6 HD", "LAT ®| ESPN 6 FHD"],
        "icon": "",
        "source": "gatotv",
        "slug": "espn_6_peru",
        "category": "Deportes",
    },
    {
        "id": "espn7-lat.tv",
        "name": "LAT ®| ESPN 7",
        "streams": ["LAT ®| ESPN 7 HD", "LAT ®| ESPN 7 FHD"],
        "icon": "",
        "source": "gatotv",
        "slug": "espn_7_peru",
        "category": "Deportes",
    },

    # === ESPN MÉXICO ===
    {
        "id": "espn-mx.tv",
        "name": "MX ®| ESPN",
        "streams": ["MX ®| ESPN HD", "MX ®| ESPN FHD"],
        "icon": "https://cdn.mitvstatic.com/channels/mx_espn_m.png",
        "source": "mitv",
        "country": "mx",
        "slug": "espn",
        "utc_offset": "-360",
        "category": "Deportes",
    },
    {
        "id": "espn2-mx.tv",
        "name": "MX ®| ESPN 2",
        "streams": ["MX ®| ESPN 2 HD", "MX ®| ESPN 2 FHD"],
        "icon": "https://cdn.mitvstatic.com/channels/mx_espn-2_m.png",
        "source": "mitv",
        "country": "mx",
        "slug": "espn-2",
        "utc_offset": "-360",
        "category": "Deportes",
    },
    {
        "id": "espn3-mx.tv",
        "name": "MX ®| ESPN 3",
        "streams": ["MX ®| ESPN 3 HD", "MX ®| ESPN 3 FHD"],
        "icon": "https://cdn.mitvstatic.com/channels/mx_espn-3_m.png",
        "source": "mitv",
        "country": "mx",
        "slug": "espn-3",
        "utc_offset": "-360",
        "category": "Deportes",
    },
    {
        "id": "espn4-mx.tv",
        "name": "MX ®| ESPN 4",
        "streams": ["MX ®| ESPN 4 HD", "MX ®| ESPN 4 FHD"],
        "icon": "",
        "source": "gatotv",
        "slug": "espn_4_peru",
        "category": "Deportes",
    },
    {
        "id": "espn5-mx.tv",
        "name": "MX ®| ESPN 5",
        "streams": ["MX ®| ESPN 5 HD", "MX ®| ESPN 5 FHD"],
        "icon": "",
        "source": "gatotv",
        "slug": "espn_5_peru",
        "category": "Deportes",
    },
    {
        "id": "espn6-mx.tv",
        "name": "MX ®| ESPN 6",
        "streams": ["MX ®| ESPN 6 HD", "MX ®| ESPN 6 FHD"],
        "icon": "",
        "source": "gatotv",
        "slug": "espn_6_peru",
        "category": "Deportes",
    },

    # === ESPN ARGENTINA ===
    {
        "id": "espn-arg.tv",
        "name": "ARG ®| ESPN",
        "streams": ["ARG ®| ESPN HD"],
        "icon": "https://cdn.mitvstatic.com/channels/ar_espn_m.png",
        "source": "mitv",
        "country": "ar",
        "slug": "espn",
        "utc_offset": "-180",
        "category": "Deportes",
    },
    {
        "id": "espn2-arg.tv",
        "name": "ARG ®| ESPN 2",
        "streams": ["ARG ®| ESPN 2 HD"],
        "icon": "https://cdn.mitvstatic.com/channels/ar_espn-2_m.png",
        "source": "mitv",
        "country": "ar",
        "slug": "espn-2",
        "utc_offset": "-180",
        "category": "Deportes",
    },
    {
        "id": "espn3-arg.tv",
        "name": "ARG ®| ESPN 3",
        "streams": ["ARG ®| ESPN 3 HD"],
        "icon": "https://cdn.mitvstatic.com/channels/ar_espn-3_m.png",
        "source": "mitv",
        "country": "ar",
        "slug": "espn-3",
        "utc_offset": "-180",
        "category": "Deportes",
    },
    {
        "id": "espn4-arg.tv",
        "name": "ARG ®| ESPN 4",
        "streams": ["ARG ®| ESPN 4 HD"],
        "icon": "",
        "source": "gatotv",
        "slug": "espn_4_peru",
        "category": "Deportes",
    },
    {
        "id": "espn-premium-arg.tv",
        "name": "ARG ®| ESPN PREMIUM",
        "streams": ["ARG ®| ESPN PREMIUM FHD"],
        "icon": "",
        "source": "gatotv",
        "slug": "espn_premium",
        "category": "Deportes",
    },

    # === ESPN COLOMBIA ===
    {
        "id": "espn-col.tv",
        "name": "COL ®| ESPN",
        "streams": ["COL ®| ESPN HD"],
        "icon": "https://cdn.mitvstatic.com/channels/co_espn_m.png",
        "source": "mitv",
        "country": "co",
        "slug": "espn",
        "utc_offset": "-300",
        "category": "Deportes",
    },
    {
        "id": "espn2-col.tv",
        "name": "COL ®| ESPN 2",
        "streams": ["COL ®| ESPN 2 HD"],
        "icon": "https://cdn.mitvstatic.com/channels/co_espn-2_m.png",
        "source": "mitv",
        "country": "co",
        "slug": "espn-2",
        "utc_offset": "-300",
        "category": "Deportes",
    },
    {
        "id": "espn3-col.tv",
        "name": "COL ®| ESPN 3",
        "streams": ["COL ®| ESPN 3 HD"],
        "icon": "https://cdn.mitvstatic.com/channels/co_espn-3_m.png",
        "source": "mitv",
        "country": "co",
        "slug": "espn-3",
        "utc_offset": "-300",
        "category": "Deportes",
    },
    {
        "id": "espn4-col.tv",
        "name": "COL ®| ESPN 4",
        "streams": ["COL ®| ESPN 4 HD"],
        "icon": "",
        "source": "gatotv",
        "slug": "espn_4_peru",
        "category": "Deportes",
    },
    {
        "id": "espn5-col.tv",
        "name": "COL ®| ESPN 5",
        "streams": ["COL ®| ESPN 5 HD"],
        "icon": "",
        "source": "gatotv",
        "slug": "espn_5_peru",
        "category": "Deportes",
    },
    {
        "id": "espn6-col.tv",
        "name": "COL ®| ESPN 6",
        "streams": ["COL ®| ESPN 6 HD"],
        "icon": "",
        "source": "gatotv",
        "slug": "espn_6_peru",
        "category": "Deportes",
    },
    {
        "id": "espn7-col.tv",
        "name": "COL ®| ESPN 7",
        "streams": ["COL ®| ESPN 7 HD"],
        "icon": "",
        "source": "gatotv",
        "slug": "espn_7_peru",
        "category": "Deportes",
    },

    # === ESPN CHILE ===
    {
        "id": "espn-chi.tv",
        "name": "CHI ®| ESPN",
        "streams": ["CHI ®| ESPN HD"],
        "icon": "https://cdn.mitvstatic.com/channels/cl_espn_m.png",
        "source": "mitv",
        "country": "cl",
        "slug": "espn",
        "utc_offset": "-180",
        "category": "Deportes",
    },
    {
        "id": "espn2-chi.tv",
        "name": "CHI ®| ESPN 2",
        "streams": ["CHI ®| ESPN 2 HD"],
        "icon": "https://cdn.mitvstatic.com/channels/cl_espn-2_m.png",
        "source": "mitv",
        "country": "cl",
        "slug": "espn-2",
        "utc_offset": "-180",
        "category": "Deportes",
    },
    {
        "id": "espn3-chi.tv",
        "name": "CHI ®| ESPN 3",
        "streams": ["CHI ®| ESPN 3 HD"],
        "icon": "https://cdn.mitvstatic.com/channels/cl_espn-3_m.png",
        "source": "mitv",
        "country": "cl",
        "slug": "espn-3",
        "utc_offset": "-180",
        "category": "Deportes",
    },
    {
        "id": "espn4-chi.tv",
        "name": "CHI ®| ESPN 4",
        "streams": ["CHI ®| ESPN 4 HD"],
        "icon": "https://cdn.mitvstatic.com/channels/cl_espn-4_m.png",
        "source": "mitv",
        "country": "cl",
        "slug": "espn-4",
        "utc_offset": "-180",
        "category": "Deportes",
    },
    {
        "id": "espn5-chi.tv",
        "name": "CHI ®| ESPN 5",
        "streams": ["CHI ®| ESPN 5 HD"],
        "icon": "",
        "source": "gatotv",
        "slug": "espn_5_peru",
        "category": "Deportes",
    },
    {
        "id": "espn6-chi.tv",
        "name": "CHI ®| ESPN 6",
        "streams": ["CHI ®| ESPN 6 HD"],
        "icon": "",
        "source": "gatotv",
        "slug": "espn_6_peru",
        "category": "Deportes",
    },
    {
        "id": "espn7-chi.tv",
        "name": "CHI ®| ESPN 7",
        "streams": ["CHI ®| ESPN 7 HD"],
        "icon": "",
        "source": "gatotv",
        "slug": "espn_7_peru",
        "category": "Deportes",
    },
    {
        "id": "espn-premium-chi.tv",
        "name": "CHI ®| ESPN PREMIUM",
        "streams": ["CHI ®| ESPN PREMIUM HD"],
        "icon": "",
        "source": "gatotv",
        "slug": "espn_premium_chile",
        "category": "Deportes",
    },

    # === ESPN USA (DEPORTES) ===
    {
        "id": "espn-deportes-usa.tv",
        "name": "USA ®| ESPN DEPORTES",
        "streams": ["USA ®| ESPN DEPORTES SD", "USA ®| ESPN DEPORTES HD"],
        "icon": "",
        "source": "gatotv",
        "slug": "espn_deportes",
        "category": "Deportes",
    },
]

SPORTS_DEFAULT_TEMPLATE = [
    ("00:00", "03:00", "SportsCenter - Edición Medianoche", "Resumen de las noticias y jugadas más destacadas del deporte mundial.", "Deportes"),
    ("03:00", "06:00", "Lo Mejor de ESPN", "Repetición de los eventos deportivos y partidos más destacados.", "Deportes"),
    ("06:00", "08:30", "SportsCenter - Primera Edición", "Toda la actualidad deportiva matinal, goles y resultados internacionales.", "Deportes"),
    ("08:30", "11:00", "ESPN FShow / Magazine Deportivo", "Debate, notas de color y la previa de los grandes eventos del día.", "Deportes"),
    ("11:00", "13:00", "SportsCenter - Mediodía", "Edición en vivo con análisis y conexiones desde los estadios.", "Deportes"),
    ("13:00", "15:00", "ESPN F90 / F360", "Mesa de debate sobre fútbol internacional, Champions League, ligas y torneos.", "Deportes"),
    ("15:00", "18:00", "Fútbol / Evento Deportivo en Vivo", "Transmisión en directo del evento estelar de la jornada.", "Deportes"),
    ("18:00", "20:00", "SportsCenter - Tarde", "Todos los goles, tablas de posiciones y entrevistas post-partido.", "Deportes"),
    ("20:00", "22:00", "ESPN Equipo F / Debate Estelar", "Análisis a fondo y polémica de la fecha con los mejores especialistas.", "Deportes"),
    ("22:00", "24:00", "SportsCenter - Noche", "Cierre de la jornada con los mejores momentos del deporte.", "Deportes"),
]

def clean_html_text(text):
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", "", text)
    text = unescape(text)
    return re.sub(r"\s+", " ", text).strip()

def fetch_url(url, timeout=12):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept-Language": "es-PE,es;q=0.9",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")

def scrape_mitv_channel(slug, base_date, country="pe", utc_offset="-300"):
    day_configs = [
        ("ayer", base_date - timedelta(days=1)),
        ("", base_date),
        ("manana", base_date + timedelta(days=1)),
    ]

    raw_items = []
    for day_slug, day_dt in day_configs:
        if day_slug:
            url = f"https://mi.tv/{country}/async/channel/{slug}/{day_slug}/{utc_offset}"
        else:
            url = f"https://mi.tv/{country}/async/channel/{slug}/{utc_offset}"

        try:
            html = fetch_url(url)
        except Exception as e:
            continue

        li_blocks = re.findall(r"<li[^>]*>(.*?)</li>", html, re.DOTALL)
        current_day_date = day_dt.date()
        last_hour = -1

        for block in li_blocks:
            time_m = re.search(r'<span class="time">\s*(\d{1,2}):(\d{2})\s*</span>', block)
            title_m = re.search(r"<h2>(.*?)</h2>", block, re.DOTALL)
            if not time_m or not title_m:
                continue

            hh = int(time_m.group(1))
            mm = int(time_m.group(2))
            title = clean_html_text(title_m.group(1))

            sub_m = re.search(r'<span class="sub-title">(.*?)</span>', block, re.DOTALL)
            cat = clean_html_text(sub_m.group(1)) if sub_m else "Deportes"

            syn_m = re.search(r'<p class="synopsis">(.*?)</p>', block, re.DOTALL)
            desc = clean_html_text(syn_m.group(1)) if syn_m else f"Transmisión de {title} por ESPN."

            if last_hour >= 18 and hh < 6:
                current_day_date = current_day_date + timedelta(days=1)
            last_hour = hh

            start_dt = datetime(
                current_day_date.year,
                current_day_date.month,
                current_day_date.day,
                hh,
                mm,
                0,
            )
            raw_items.append(
                {
                    "start": start_dt,
                    "title": title,
                    "desc": desc,
                    "category": cat,
                }
            )

    if not raw_items:
        return []

    raw_items.sort(key=lambda x: x["start"])
    dedup = []
    for item in raw_items:
        if dedup and dedup[-1]["start"] == item["start"]:
            continue
        dedup.append(item)

    programs = []
    for i, item in enumerate(dedup):
        start_dt = item["start"]
        if i + 1 < len(dedup):
            stop_dt = dedup[i + 1]["start"]
            if (stop_dt - start_dt) > timedelta(hours=6):
                stop_dt = start_dt + timedelta(hours=2)
        else:
            stop_dt = start_dt + timedelta(hours=2)

        if stop_dt > start_dt:
            programs.append(
                {
                    "start": start_dt,
                    "stop": stop_dt,
                    "title": item["title"],
                    "desc": item["desc"],
                    "category": item["category"],
                }
            )

    return programs

def scrape_gatotv_channel(slug, base_date, ch_name="ESPN"):
    url = f"https://www.gatotv.com/canal/{slug}"
    try:
        html = fetch_url(url)
    except Exception as e:
        return []

    rows = re.findall(
        r'<tr class="tbl_EPG_row[^"]*">(.*?)</tr>', html, re.DOTALL
    )
    daily_slots = []
    for row in rows:
        times = re.findall(r'<time datetime="(\d{2}:\d{2})">', row)
        title_m = re.search(
            r'<div class="div_program_title_on_channel">\s*<span[^>]*>(.*?)</span>',
            row,
            re.DOTALL,
        )
        if not title_m:
            title_m = re.search(
                r'<div class="div_program_title_on_channel">.*?<span>(.*?)</span>',
                row,
                re.DOTALL,
            )
        if len(times) >= 2 and title_m:
            t_start, t_end = times[0], times[1]
            title = clean_html_text(title_m.group(1))
            daily_slots.append((t_start, t_end, title))

    if not daily_slots:
        return []

    programs = []
    for day_offset in (-1, 0, 1):
        d = (base_date + timedelta(days=day_offset)).date()
        for t_start, t_end, title in daily_slots:
            sh, sm = map(int, t_start.split(":"))
            eh, em = map(int, t_end.split(":"))
            start_dt = datetime(d.year, d.month, d.day, sh, sm, 0)
            if (eh, em) <= (sh, sm):
                stop_dt = datetime(d.year, d.month, d.day, eh, em, 0) + timedelta(days=1)
            else:
                stop_dt = datetime(d.year, d.month, d.day, eh, em, 0)

            programs.append(
                {
                    "start": start_dt,
                    "stop": stop_dt,
                    "title": title,
                    "desc": f"Transmisión de {title} por {ch_name}.",
                    "category": "Deportes",
                }
            )

    return programs

def generate_template_programs(ch_conf, base_date):
    ch_name = ch_conf["name"]
    programs = []
    for day_offset in (-1, 0, 1, 2):
        d = (base_date + timedelta(days=day_offset)).date()
        for start_str, end_str, title_tpl, desc_tpl, cat in SPORTS_DEFAULT_TEMPLATE:
            sh, sm = map(int, start_str.split(":"))
            start_dt = datetime(d.year, d.month, d.day, sh, sm, 0)
            if end_str == "24:00":
                stop_dt = datetime(d.year, d.month, d.day, 0, 0, 0) + timedelta(days=1)
            else:
                eh, em = map(int, end_str.split(":"))
                stop_dt = datetime(d.year, d.month, d.day, eh, em, 0)

            programs.append(
                {
                    "start": start_dt,
                    "stop": stop_dt,
                    "title": f"{title_tpl}",
                    "desc": f"{desc_tpl} Señal en vivo de {ch_name}.",
                    "category": cat,
                }
            )
    return programs

def format_xmltv_time(dt):
    return dt.strftime(f"%Y%m%d%H%M%S {TIMEZONE_OFFSET}")

def main():
    peru_tz = timezone(timedelta(hours=-5))
    now = datetime.now(peru_tz).replace(tzinfo=None)
    print(f"=== Generador EPG ESPN / Deportes - Fecha base (Perú): {now.strftime('%Y-%m-%d %H:%M')} ===")

    tv = ET.Element(
        "tv",
        {
            "source-info-name": "EPG ESPN AkyHay",
            "generator-info-name": "EPG_ESPN_XUI_Generator",
        },
    )

    all_programs = []
    total_channels = 0

    for ch in CHANNELS_CONFIG:
        ch_id = ch["id"]
        ch_name = ch["name"]
        streams = ch["streams"]
        icon = ch.get("icon", "")

        ch_elem = ET.SubElement(tv, "channel", {"id": ch_id})
        dn_main = ET.SubElement(ch_elem, "display-name", {"lang": "es"})
        dn_main.text = ch_name

        for st_name in streams:
            dn_st = ET.SubElement(ch_elem, "display-name", {"lang": "es"})
            dn_st.text = st_name

        if icon:
            ET.SubElement(ch_elem, "icon", {"src": icon})

        total_channels += 1

        source = ch.get("source")
        country = ch.get("country", "pe")
        utc_offset = ch.get("utc_offset", "-300")
        progs = []

        if source == "mitv":
            print(f"[*] Extrayendo guía en vivo de mi.tv ({country}) para: {ch_name} ({ch['slug']})...")
            progs = scrape_mitv_channel(ch["slug"], now, country=country, utc_offset=utc_offset)
        elif source == "gatotv":
            print(f"[*] Extrayendo guía en vivo de GatoTV para: {ch_name} ({ch['slug']})...")
            progs = scrape_gatotv_channel(ch["slug"], now, ch_name=ch_name)

        if not progs:
            print(f"    -> Usando parrilla deportiva estructurada para: {ch_name}")
            progs = generate_template_programs(ch, now)

        for p in progs:
            all_programs.append((ch_id, p))

    for ch_id, p in all_programs:
        prog_elem = ET.SubElement(
            tv,
            "programme",
            {
                "start": format_xmltv_time(p["start"]),
                "stop": format_xmltv_time(p["stop"]),
                "channel": ch_id,
            },
        )
        t_el = ET.SubElement(prog_elem, "title", {"lang": "es"})
        t_el.text = p["title"]

        d_el = ET.SubElement(prog_elem, "desc", {"lang": "es"})
        d_el.text = p["desc"]

        c_el = ET.SubElement(prog_elem, "category", {"lang": "es"})
        c_el.text = p.get("category", "Deportes")

    tree = ET.ElementTree(tv)
    if hasattr(ET, "indent"):
        ET.indent(tree, space="  ", level=0)

    tree.write(OUTPUT_XML, encoding="utf-8", xml_declaration=True)
    shutil.copyfile(OUTPUT_XML, OUTPUT_DEFAULT)

    with open(OUTPUT_XML, "rb") as f_in:
        with gzip.open(OUTPUT_GZ, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)

    print("\n========================================================")
    print(f"¡EPG ESPN / Deportes generado con éxito!")
    print(f" - Canales únicos configurados : {total_channels} (cubriendo todos tus streams de ESPN)")
    print(f" - Programas totales generados : {len(all_programs)}")
    print(f" - Archivo XML                 : {OUTPUT_XML} (y {OUTPUT_DEFAULT})")
    print(f" - Archivo comprimido GZ       : {OUTPUT_GZ}")
    print("========================================================")

if __name__ == "__main__":
    main()
