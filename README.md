# Sapient Journal — website

The website for Sapient, Columbia University's undergraduate journal of
biological anthropology. Built with [Astro](https://astro.build), hosted free
on Cloudflare Pages, and edited through a browser-based CMS at `/admin/`.

**Nothing here costs money except the domain name.**

---

## For editors (no code required)

Go to **https://www.sapientjournal.com/admin/** and sign in with GitHub. From
there you can:

| Task | Where |
| --- | --- |
| Write or edit a Hominin Hub post | *Hominin Hub posts* |
| Open or close submissions | *Journal & board → Volumes & submissions* |
| Publish a new volume PDF | *Journal & board → Volumes & submissions* |
| Update the board for a new year | *Journal & board → Editorial board* |

Saving publishes a change to GitHub; the site rebuilds itself in about a
minute. Nothing you do in the editor can break the site permanently — every
change is a commit, and anything can be undone.

**Handing over to next year's board:** add their GitHub accounts as
collaborators on the repository (Settings → Collaborators). That is the whole
handover. Do not let the repository live on a personal account that graduates
with you — use a GitHub organization owned by the journal.

---

## For whoever maintains the code

```bash
npm install     # once
npm run dev     # http://localhost:4321
npm run build   # output in dist/
```

### Where things live

```
src/
  pages/            one file per page; the URL matches the filename
  content/blog/     one Markdown file per Hominin Hub post
  data/site.ts      nav, contact address, research areas
  data/journal.json volumes + submission status   (CMS-editable)
  data/board.json   editorial board roster        (CMS-editable)
  components/       header, footer, section rail
  layouts/Base.astro  <head>, fonts, page shell
  styles/global.css   the whole design system, tokens at the top
public/
  volumes/          volume PDFs
  images/           covers, board photos, post images
  admin/            the CMS (config.yml defines the editing fields)
  _redirects        old Wix URLs → new ones
```

### Design tokens

Colours and type are defined once, at the top of `src/styles/global.css`.
Change `--ink`, `--bone`, `--columbia` and the whole site follows.

---

## First-time deployment

1. **Create a GitHub organization** for the journal and push this folder to a
   repository inside it (e.g. `sapient-journal/website`).
2. **Cloudflare Pages** → Create project → connect the repository.
   Framework preset: **Astro**. Build command `npm run build`, output
   directory `dist`. Deploy.
3. **Point the domain.** In Cloudflare Pages → Custom domains, add
   `sapientjournal.com` and `www.sapientjournal.com`. If the domain is still
   registered with Wix, transfer it out *before* cancelling the Wix plan.
4. **Set the repo in the CMS.** Edit `public/admin/config.yml` and replace
   `YOUR-GITHUB-USERNAME/sapient-journal` with the real repository.
5. **Enable CMS sign-in.** Deploy the one-click
   [sveltia-cms-auth](https://github.com/sveltia/sveltia-cms-auth) Cloudflare
   Worker, create a GitHub OAuth app pointing at it, then add the worker URL
   as `base_url:` under `backend:` in `config.yml`. Takes about ten minutes and
   is free.

## Things the old Wix site got wrong — already fixed here

- Every page shipped `<meta name="robots" content="noindex">`, telling Google
  to ignore the entire site. Removed.
- The social icons linked to Wix's own Twitter, LinkedIn and a dead Google+
  page. Removed rather than replaced — add real accounts if the journal has
  them.
- `Submit` and `Contact` in the navigation both pointed at the homepage. They
  are real pages now.
- A `sitemap-index.xml` and a `robots.txt` are generated on every build.
