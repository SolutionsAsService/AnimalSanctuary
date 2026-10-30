"""Build the static site: wraps each _src/pages/*.html in _src/layout.html.

Each page starts with a header block, then a line with three dashes:

    title: Page title
    description: Meta description
    nav: adopt           (current nav item; optional)
    ---
    <page html>

{{pet:cat:#C8643B}} (species cat, dog or rabbit, then a coat colour) is
replaced by a drawn portrait of that animal, so no stock photos are needed.

Run:  python _src/build.py   (writes index.html, adopt.html, ... into site/)
"""
import pathlib
import re

SRC = pathlib.Path(__file__).resolve().parent
ROOT = SRC.parent / "site"
NAV = ["adopt", "foster", "volunteer", "give", "about", "contact"]

EARS = {
    "cat": '<path d="M27 40 31 14 47 31Z M93 40 89 14 73 31Z" fill="{c}"/><path d="M31 33 33 21 41 30Z M89 33 87 21 79 30Z" fill="#F2C7B5"/>',
    "dog": '<path d="M25 34c-9 4-12 26-4 36 6 2 9-10 12-22Z M95 34c9 4 12 26 4 36-6 2-9-10-12-22Z" fill="{d}"/>',
    "rabbit": '<path d="M44 34C38 14 40 2 47 2s9 14 6 32Z M76 34c6-20 4-32-3-32s-9 14-6 32Z" fill="{c}"/><path d="M47 30c-3-12-2-22 1-22s4 10 2 22Z M73 30c3-12 2-22-1-22s-4 10-2 22Z" fill="#F2C7B5"/>',
}


def darker(hex_colour, f=0.72):
    r, g, b = (int(hex_colour[i:i + 2], 16) for i in (1, 3, 5))
    return "#%02X%02X%02X" % (int(r * f), int(g * f), int(b * f))


def pet(species, colour):
    d = darker(colour)
    ears = EARS[species].format(c=colour, d=d)
    whiskers = (
        '<path d="M44 74H28M44 79l-15 4M76 74h16M76 79l15 4" stroke="#3B2A20" stroke-width="1.6" stroke-linecap="round" opacity=".55"/>'
        if species != "dog" else ""
    )
    return (
        f'<svg class="pet-art" viewBox="0 0 120 120" aria-hidden="true">'
        f'<circle cx="60" cy="66" r="52" class="pet-bg"/>{ears}'
        f'<ellipse cx="60" cy="64" rx="33" ry="30" fill="{colour}"/>'
        f'<ellipse cx="60" cy="78" rx="17" ry="12" fill="#F7E8DA"/>'
        f'<circle cx="48" cy="60" r="4.2" fill="#2A1D16"/><circle cx="72" cy="60" r="4.2" fill="#2A1D16"/>'
        f'<circle cx="49.4" cy="58.6" r="1.4" fill="#fff"/><circle cx="73.4" cy="58.6" r="1.4" fill="#fff"/>'
        f'<path d="M55 71h10l-5 5Z" fill="#3B2A20"/><path d="M60 76v4m0 0c-2 3-6 3-8 1m8-1c2 3 6 3 8 1" fill="none" stroke="#3B2A20" stroke-width="1.8" stroke-linecap="round"/>'
        f'{whiskers}</svg>'
    )


layout = (SRC / "layout.html").read_text(encoding="utf-8")

for page in sorted((SRC / "pages").glob("*.html")):
    head, body = page.read_text(encoding="utf-8").split("\n---\n", 1)
    meta = dict(line.split(": ", 1) for line in head.strip().splitlines())
    body = re.sub(r"\{\{pet:(cat|dog|rabbit):(#[0-9A-Fa-f]{6})\}\}", lambda m: pet(m[1], m[2].upper()), body)
    html = layout.replace("{{title}}", meta["title"]).replace("{{description}}", meta["description"])
    for key in NAV:
        html = html.replace("{{cur:%s}}" % key, ' aria-current="page"' if meta.get("nav") == key else "")
    html = html.replace("{{content}}", body.rstrip())
    assert not re.search(r"\{\{.*?\}\}", html), f"unfilled placeholder in {page.name}"
    for ref in re.findall(r'(?:href|src)="(?![a-z]+:)([^"#?]+)', html):
        assert (ROOT / ref).exists() or (SRC / "pages" / ref).exists(), f"{page.name} links to missing {ref}"
    (ROOT / page.name).write_text(html, encoding="utf-8", newline="\n")
    print("built", page.name)
