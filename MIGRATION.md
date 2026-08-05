# Migration checklist

The site currently shows labelled grey placeholders wherever a real image or
PDF belongs, so it builds and lays out correctly before any assets arrive.

## 1. Run the download script

**Do this while the Wix site is still live.** Once the subscription lapses
these URLs stop resolving and the files are gone.

```bash
bash scripts/fetch-assets.sh
```

It pulls 36 files — all six PDFs, both logos, every board and alumni
headshot, the Volume 13 cover, and all four blog images — at original
resolution, straight into the right filenames. Anything that fails is printed
so you can grab it by hand.

## 2. Five things the script can't get

Wix renders these as CSS backgrounds, so there's no URL to extract. Open the
live site, right-click each one, Save Image As:

| Save to | What it is |
| --- | --- |
| `public/images/monkey-portrait-1.jpg` | left round photo by the sa·pi·ent definition |
| `public/images/monkey-portrait-2.jpg` | right round photo, same section |
| `public/images/topics/topic-1.jpg` … `topic-4.jpg` | the four Research Topics circles |
| `public/images/covers/vol-9.png` … `vol-12.png` | older covers — not on the site at all |

For the older covers, export page 1 of each PDF:

```bash
pdftoppm -png -r 150 -f 1 -l 1 public/files/sapient-vol-12.pdf public/images/covers/vol-12
```

## 3. Check the volume numbering

Wix lists the four older PDFs unlabelled, so `journal.json` assumes they run
12, 11, 10, 9 in the order they appear. The last one is named `Vol.9.png` on
Wix, which supports that. Open each PDF, confirm, and correct
`src/data/journal.json` if needed.

## 4. Blog post bodies

The four posts are in `src/content/blog/` with correct titles, authors, dates,
reading times and slugs. Only the body text is missing — each file names the
Wix URL to copy from. Paste below the `---` block.

## 5. Domain

Check the registrar at https://lookup.icann.org before cancelling anything.
Full sequence is in `LAUNCH.md`, Step 1 and Step 6.

## 6. Before you cancel Wix

Archive everything downloaded above into a shared Drive folder the board owns
collectively — not a personal laptop that graduates.
