"""Import the Hominin Hub posts from the live Wix site into src/content/blog/.

Wix server-renders each post at /post/<slug>, so the body is scraped from the
rendered HTML rather than an API (the blog API needs a signed app instance).
Slugs come from the two /blog-the-hominin-hub index pages; the RSS feed is
capped at 20 items and truncates bodies, so it is not used.

Requires: pip install beautifulsoup4 lxml
Usage:
    python3 scripts/import-wix-posts.py            # dry run
    python3 scripts/import-wix-posts.py --write    # write posts + images.json

Images are not fetched here; --write records them in images.json for download.
"""

import re, json, os, sys, glob, hashlib
from bs4 import BeautifulSoup, NavigableString, Tag

REPO = "/Users/yukiogawa/Downloads/sapient-website"
IMGDIR = os.path.join(REPO, "public/images/posts")
OUTDIR = os.path.join(REPO, "src/content/blog")
GENERIC_AUTHOR = "Sapient Editorial Board"

images = {}   # local filename -> remote url

# Wix media filenames vary: "id~mv2.png" but also "id~mv2_d_3024_4032_s_4_2.jpeg".
MEDIA_RE = re.compile(r"/media/([^/?]+\.(?:jpe?g|png|gif|webp|avif))", re.I)

def wix_url(uri, width):
    w = min(int(width or 1400), 1400)
    return f"https://static.wixstatic.com/media/{uri}/v1/fit/w_{w},h_{w*3},al_c,q_85/{uri}"

def register(uri, width, slug, idx):
    ext = os.path.splitext(uri)[1].lower() or ".jpg"
    if ext == ".png": ext = ".png"
    elif ext in (".jpeg", ".jpg"): ext = ".jpg"
    elif ext == ".gif": ext = ".gif"
    else: ext = ".jpg"
    name = f"{slug}{ext}" if idx == 0 else f"{slug}-{idx}{ext}"
    images[name] = wix_url(uri, width)
    return f"/images/posts/{name}"

def esc(t):
    return re.sub(r'([*_`\[\]])', r'\\\1', t)

def wrap(raw, pre, post):
    """Emphasis/link markers must hug the text, but surrounding spaces must survive."""
    core = raw.strip()
    if not core:
        return raw
    lead = raw[: len(raw) - len(raw.lstrip())]
    trail = raw[len(raw.rstrip()) :]
    return f"{lead}{pre}{core}{post}{trail}"

def inline(node):
    out = []
    for c in node.children:
        if isinstance(c, NavigableString):
            out.append(esc(str(c)))
        elif isinstance(c, Tag):
            n = c.name
            if n == "br":
                out.append("\n")
            elif n == "a" and c.get("href"):
                out.append(wrap(inline(c), "[", f"]({c['href']})"))
            elif n in ("em", "i"):
                out.append(wrap(inline(c), "*", "*"))
            elif n in ("strong", "b"):
                out.append(wrap(inline(c), "**", "**"))
            elif n == "code":
                out.append(f"`{c.get_text()}`")
            else:
                out.append(inline(c))
    return "".join(out)

def clean(s):
    s = s.replace(" ", " ")
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r" *\n *", "\n", s)
    return s.strip()

def figure_md(fig, slug, counter):
    wi = fig.select_one("wow-image[data-image-info]")
    if wi:
        d = json.loads(wi["data-image-info"]).get("imageData", {})
        uri, width = d.get("uri"), d.get("width")
    else:
        # Wix gallery cells render a plain <img> instead of a <wow-image>.
        img = fig.select_one("img[src]")
        m = MEDIA_RE.search(img["src"]) if img else None
        if not m: return None
        uri, width = m.group(1), img.get("width")
    if not uri: return None
    counter[0] += 1
    path = register(uri, width, slug, counter[0])
    cap = fig.select_one("figcaption")
    captxt = clean(inline(cap)) if cap else ""
    # alt must stay plain text: captions can contain links and bracketed citations.
    alt = re.sub(r"\s+", " ", cap.get_text(" ", strip=True)) if cap else ""
    alt = alt.replace("[", "(").replace("]", ")")
    if len(alt) > 120:
        alt = alt[:117].rsplit(" ", 1)[0] + "..."
    md = f"![{alt}]({path})"
    if captxt:
        md += f"\n*{captxt}*"
    return md

YT_RE = re.compile(r"(?:i\.ytimg\.com/vi|youtube\.com/(?:embed|watch\?v=)|youtu\.be)/([\w-]{11})")

def video_md(fig):
    m = YT_RE.search(str(fig))
    if not m: return None
    vid = m.group(1)
    return (f'<div class="video-embed"><iframe src="https://www.youtube.com/embed/{vid}" '
            f'title="YouTube video" loading="lazy" allowfullscreen '
            f'allow="accelerometer; clipboard-write; encrypted-media; picture-in-picture"></iframe></div>')

def convert(node, slug, counter, blocks):
    for c in node.children:
        if isinstance(c, NavigableString):
            continue
        if not isinstance(c, Tag):
            continue
        n = c.name
        if n == "figure":
            md = video_md(c) if c.get("data-hook") == "figure-VIDEO" else figure_md(c, slug, counter)
            if md: blocks.append(md)
        elif n == "p":
            t = clean(inline(c))
            if t: blocks.append(t)
        elif n in ("h1", "h2", "h3", "h4", "h5", "h6"):
            t = clean(inline(c))
            if t:
                lvl = max(2, int(n[1]))
                blocks.append("#" * lvl + " " + t)
        elif n == "blockquote":
            sub = []
            convert(c, slug, counter, sub)
            if sub:
                blocks.append("\n>\n".join("> " + b.replace("\n", "\n> ") for b in sub))
        elif n in ("ul", "ol") and c.select_one("figure"):
            convert(c, slug, counter, blocks)
        elif n in ("ul", "ol"):
            items = []
            for i, li in enumerate(c.find_all("li", recursive=False), 1):
                t = clean(inline(li))
                if t:
                    items.append((f"{i}. " if n == "ol" else "- ") + t.replace("\n", " "))
            if items: blocks.append("\n".join(items))
        elif n == "hr" or (c.get("data-hook") or "").startswith("divider"):
            blocks.append("---")
        else:
            convert(c, slug, counter, blocks)

def hook_text(soup, name):
    e = soup.select_one(f'[data-hook="{name}"]')
    return e.get_text(" ", strip=True) if e else None

NAME_RE = re.compile(r"^[A-Z][\w.'’-]*(?: [A-Z][\w.'’-]*){1,3}$")

def build(path):
    slug = os.path.basename(path)[:-5]
    h = open(path, encoding="utf-8").read()
    soup = BeautifulSoup(h, "lxml")
    ld = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', h, re.S).group(1))

    title = hook_text(soup, "post-title") or ld.get("headline")
    date = ld.get("datePublished", "")[:10]
    ttr = hook_text(soup, "time-to-read") or ""
    author = hook_text(soup, "user-name") or GENERIC_AUTHOR

    body = soup.select_one('[data-hook="post-description"]')
    counter = [0]
    blocks = []
    convert(body, slug, counter, blocks)

    # Wix pages often open/close with a decorative divider; a leading "---"
    # would also collide with the frontmatter fence.
    while blocks and blocks[0] == "---": blocks.pop(0)
    while blocks and blocks[-1] == "---": blocks.pop()

    # Byline handling: a standalone name as the first block.
    if blocks and NAME_RE.match(blocks[0]) and len(blocks[0]) <= 40:
        if author == GENERIC_AUTHOR:
            author = blocks[0]
        if blocks[0] == author:
            blocks.pop(0)
    # Some posts sign off at the end instead ("By Emma Gometz").
    if blocks and author == GENERIC_AUTHOR:
        mb = re.fullmatch(r"By ([A-Z][\w.'\u2019-]*(?: [A-Z][\w.'\u2019-]*){1,3})", blocks[-1])
        if mb:
            author = mb.group(1)
            blocks.pop()
    while blocks and blocks[-1] == "---": blocks.pop()

    # ld+json "image" is Wix's social/card thumbnail and is always one of the body
    # images. It fills `image:` for the index card; the body keeps every image in
    # its original position, so the post page reads exactly like the original.
    hero = None
    m = MEDIA_RE.search((ld.get("image") or {}).get("url", ""))
    if m:
        uri = m.group(1)
        existing = next((p for p, u in images.items() if uri in u), None)
        hero = f"/images/posts/{existing}" if existing else register(
            uri, (ld.get("image") or {}).get("width"), slug, 0)
    elif blocks:
        # No card image declared: fall back to the first body image.
        first_img = next((re.match(r"!\[[^\]]*\]\(([^)]+)\)", b) for b in blocks
                          if re.match(r"!\[[^\]]*\]\(([^)]+)\)", b)), None)
        if first_img:
            hero = first_img.group(1)



    # First real paragraph: skip images, dividers, embeds and short heading-ish lines.
    excerpt = ""
    for b in blocks:
        if b[0] in "!#-<":
            continue
        cand = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", b)
        cand = re.sub(r"[*\\]", "", cand).replace("\n", " ").strip()
        if len(cand) >= 60:
            excerpt = cand
            break
        excerpt = excerpt or cand
    if len(excerpt) > 180:
        cut = excerpt[:180]
        excerpt = cut[: cut.rfind(" ")] + "…"

    def y(s): return '"' + s.replace('"', '\\"') + '"'
    fm = ["---", f"title: {y(title)}", f"date: {date}", f"author: {y(author)}"]
    if ttr: fm.append(f"readingTime: {y(ttr)}")
    fm.append(f"excerpt: {y(excerpt)}")
    if hero: fm.append(f"image: {y(hero)}")
    fm += ["draft: false", "---", ""]
    return slug, "\n".join(fm) + "\n".join(b + "\n" for b in blocks)

if __name__ == "__main__":
    os.makedirs(OUTDIR, exist_ok=True)
    written = []
    for p in sorted(glob.glob("pages/*.html")):
        slug, md = build(p)
        written.append((slug, md))
    if "--write" in sys.argv:
        for slug, md in written:
            open(os.path.join(OUTDIR, slug + ".md"), "w", encoding="utf-8").write(md)
        json.dump(images, open("images.json", "w"), indent=1)
        print(f"wrote {len(written)} posts, {len(images)} images queued")
    else:
        for slug, md in written:
            if slug in sys.argv:
                print("=" * 70); print(slug); print("=" * 70); print(md)
        print(f"[dry run] {len(written)} posts, {len(images)} images")
