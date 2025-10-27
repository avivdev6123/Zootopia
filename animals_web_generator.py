import requests, textwrap
from html import escape
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')
API_URL = "https://api.api-ninjas.com/v1/animals"
PLACEHOLDER = "{{ANIMAL_RESULTS}}"

def get_animals(name):
    headers = {"X-Api-Key": API_KEY}
    params = {"name": name}
    resp = requests.get(API_URL, headers=headers, params=params, timeout=20)
    resp.raise_for_status()
    return resp.json()

def render_animals_html(data, search_key):
    if not data:
        return f'<div class="animal-results"><p>The Animal "{search_key}" doesnt exist.</p></div>'
    cards = []
    #cards.append(f"{PLACEHOLDER}")
    for item in data:
        name = escape(item.get("name", "Unknown"))
        taxonomy = item.get("taxonomy") or {}
        characteristics = item.get("characteristics") or {}
        locations = item.get("locations") or []
        def dict_to_dl(d):
            if not d:
                return "<p><em>None</em></p>"
            rows = []
            for k, v in d.items():
                val = ", ".join(v) if isinstance(v, list) else str(v)
                rows.append(f"<div class='row'><dt>{escape(str(k))}</dt><dd>{escape(val)}</dd></div>")
            return "<dl class='kv'>" + "".join(rows) + "</dl>"
        loc_html = (
            "<ul class='locations'>" +
            "".join(f"<li>{escape(str(loc))}</li>" for loc in locations) +
            "</ul>" if locations else "<p><em>None listed</em></p>"
        )
        cards.append(f"""
        <article class="animal-card">
          <header><h2 class="animal-name">{name}</h2></header>
          <section><h3>Taxonomy</h3>{dict_to_dl(taxonomy)}</section>
          <section><h3>Locations</h3>{loc_html}</section>
          <section><details><summary><strong>Characteristics</strong></summary>{dict_to_dl(characteristics)}</details></section>
        </article>
        """)
    css = textwrap.dedent("""
    <style>
      .animal-results { display: grid; gap: 1rem; }
      .animal-card { border: 1px solid #ddd; border-radius: 12px; padding: 1rem; }
      .animal-name { margin: 0 0 .5rem 0; }
      .kv { display: grid; grid-template-columns: max-content 1fr; column-gap: .75rem; row-gap: .25rem; }
      .kv .row { display: contents; }
      .kv dt { font-weight: 600; }
      .kv dd { margin: 0; }
      .locations { margin: .25rem 0 0 1rem; }
    </style>
    """).strip()
    return f"<div class='animal-results'>{''.join(cards)}</div>\n{css}"

def inject_into_html(template_path, output_path, html_snippet):
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()
    if PLACEHOLDER in template:
        result_html = template.replace(PLACEHOLDER, html_snippet)
    else:
        tl = template.lower()
        if "</body>" in tl:
            idx = tl.rfind("</body>")
            result_html = template[:idx] + html_snippet + template[idx:]
        else:
            result_html = template + "\n" + html_snippet
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result_html)



