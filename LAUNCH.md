# Launch guide

Work through these in order. Steps 1 and 4 have waiting periods measured in
days, so start them early — everything else can happen while you wait.

Total cost when you're done: the domain renewal, about $10–12 a year. Nothing
else on this list costs money.

---

## Step 0 · Get it running on your laptop
**~20 minutes. Do this first so you can see changes as you make them.**

1. Install **Node.js** (LTS version) from https://nodejs.org — you need v20 or
   newer. Verify with `node -v` in a terminal.
2. Unzip `sapient-journal-site.zip` somewhere sensible. Not Downloads — this
   folder becomes the website.
3. Open a terminal, `cd` into that folder, and run:
   ```bash
   npm install
   npm run dev
   ```
4. Open http://localhost:4321.

**You'll know it worked when:** the homepage loads with grey placeholder
images. Leave `npm run dev` running while you work — the browser refreshes
itself every time you save a file. `Ctrl+C` stops it.

---

## Step 1 · Find out who actually owns the domain
**~10 minutes now, then a waiting period later. Start today.**

1. Go to https://lookup.icann.org and search `sapientjournal.com`.
2. Read the **Registrar** field.

- **If it says Wix** (or "Wix.com Ltd"): the domain is inside the account
  you're about to cancel. You'll move it in Step 6. Do not cancel anything
  until that's done.
- **If it says Columbia, GoDaddy, Namecheap or similar:** good — the domain is
  independent of Wix. You can skip Step 6 entirely and just change DNS in
  Step 5.

Also check the **Registry Expiry Date**. If it's within the next 60 days,
renew it now, wherever it currently lives. An expired domain is the one
failure mode here that is genuinely hard to undo.

> ⚠️ A domain cannot be transferred within 60 days of being registered or of
> its last transfer. If Wix registered it recently, you'll have to wait out
> the clock before Step 6.

---

## Step 2 · Move the content over
**Half a day, spread out. See `MIGRATION.md` for the exact URLs.**

Do this while the Wix site is still live — those files disappear with it.

1. Download the six PDFs listed in `MIGRATION.md` into `public/volumes/`.
2. Open each one and check the volume number on the cover, then correct the
   `year` and `label` fields in `src/data/journal.json`. My numbering there is
   a guess based on the order Wix listed them.
3. Save the Volume 13 cover into `public/images/covers/vol-13.png`. For older
   covers, screenshot page 1 of each PDF.
4. Copy each Hominin Hub post's text from the Wix site into the matching file
   in `src/content/blog/`. Titles, authors and dates are already filled in —
   you only need the body, pasted below the `---` line.
5. Fill in `src/data/board.json` with the current board, and put their photos
   in `public/images/board/`.

**You'll know it worked when:** no grey placeholders remain on
localhost:4321.

---

## Step 3 · Put it on GitHub
**~30 minutes.**

1. Create a **GitHub organization**, not a personal repo:
   https://github.com/account/organizations/new → Free plan. Name it something
   like `sapient-journal`.

   *This matters more than it sounds. A repo on your personal account
   graduates with you. An organization can outlive every board member, and you
   add and remove students as collaborators.*

2. Inside the organization, create a repository called `website`. Public is
   fine and free.
3. Push the folder up. Easiest route if you don't use git daily is
   [GitHub Desktop](https://desktop.github.com): *Add Local Repository* → pick
   your folder → *Publish repository*.

   From the terminal instead:
   ```bash
   git init
   git add .
   git commit -m "Rebuild off Wix"
   git branch -M main
   git remote add origin https://github.com/sapient-journal/website.git
   git push -u origin main
   ```

**You'll know it worked when:** your files are visible on github.com. There
should be no `node_modules` folder there — `.gitignore` handles that.

---

## Step 4 · Deploy to Cloudflare Pages
**~15 minutes. The site goes live at a temporary address.**

1. Sign up at https://dash.cloudflare.com (free).
2. **Compute (Workers & Pages)** → *Create* → *Pages* → *Connect to Git*.
3. Authorise GitHub, pick the `website` repo.
4. Settings:
   - Framework preset: **Astro**
   - Build command: `npm run build`
   - Build output directory: `dist`
5. *Save and Deploy*, then wait about a minute.

**You'll know it worked when:** `sapient-journal.pages.dev` (or similar) loads
the real site. From now on, every push to GitHub redeploys automatically.

Click through every page here before going further.

---

## Step 5 · Point the domain at it
**~30 minutes of work, up to 24 hours of waiting.**

This switches the live website over. Do it when Step 4 looks right.

1. In Cloudflare: **Add a domain** → `sapientjournal.com` → Free plan.
2. Cloudflare scans the existing DNS records. **Check the list carefully
   before continuing** — especially any `MX` records, which carry email. If
   the journal's Gmail routes through this domain and you drop those records,
   email stops arriving.
3. Cloudflare shows you two nameservers. Go to wherever the domain is
   registered (from Step 1) and replace the existing nameservers with those.
4. Wait for Cloudflare to mark the domain **Active** — usually under an hour.
5. Back in your Pages project → *Custom domains* → add **both**
   `sapientjournal.com` and `www.sapientjournal.com`. Cloudflare creates the
   records for you.
6. Delete any leftover DNS records still pointing at Wix.

**You'll know it worked when:** https://www.sapientjournal.com shows the new
site. Test an old link too, like
`www.sapientjournal.com/post/scavenging-a-home-how-ice-age-humans-built-houses-from-mammoth-bones`
— it should redirect to the new blog.

---

## Step 6 · Move the domain registration off Wix
**5 minutes of work, up to 7 days of waiting. Skip if Step 1 said Wix doesn't own it.**

Only do this after Step 5 is confirmed working.

1. In Wix: *Domains* → your domain → *Advanced* → **Transfer away from Wix**.
   Unlock the domain, turn off privacy protection if prompted, and request the
   **authorization code** (also called an EPP code). Wix emails it to the
   address on file.
2. In Cloudflare: **Domain Registration** → *Transfer Domains* → select
   `sapientjournal.com` → paste the code → pay one year at cost (~$10).
3. Approve the confirmation email when it arrives. Approving speeds it up;
   ignoring it means waiting the full 5–7 days.

**You'll know it worked when:** the domain appears under Cloudflare's
*Domain Registration* and ICANN lookup shows Cloudflare as registrar.

Set a calendar reminder for the renewal date and put it somewhere the next
board will see it.

---

## Step 7 · Turn on the CMS

Two options. Start with A, move to B before you hand over.

### A · Just for you, right now — 5 minutes

1. Edit `public/admin/config.yml` and set:
   ```yaml
   repo: sapient-journal/website
   ```
2. Push the change.
3. Visit `www.sapientjournal.com/admin/` and sign in with a GitHub personal
   access token when prompted.

That's enough for one technical person. It's not enough for students who
shouldn't have to know what a personal access token is.

### B · Proper sign-in for future editors — ~20 minutes

This is the part that makes the site survivable after you leave. Do it before
handover, not during.

1. Deploy the authenticator: go to
   https://github.com/sveltia/sveltia-cms-auth and click **Deploy to
   Cloudflare Workers**. Copy the resulting worker URL — it looks like
   `https://sveltia-cms-auth.something.workers.dev`.
2. Register an OAuth app at https://github.com/settings/applications/new:
   - Application name: `Sapient CMS`
   - Homepage URL: `https://www.sapientjournal.com`
   - **Authorization callback URL:** `<YOUR_WORKER_URL>/callback`
   
   Then click *Generate a new client secret* and keep both values on screen.
3. In Cloudflare → your `sveltia-cms-auth` worker → *Settings* → *Variables*,
   add:
   - `GITHUB_CLIENT_ID` — the client ID
   - `GITHUB_CLIENT_SECRET` — the secret (click **Encrypt**)
   - `ALLOWED_DOMAINS` — `sapientjournal.com, *.sapientjournal.com`
   
   Save and deploy.
4. In `public/admin/config.yml`, uncomment the `base_url` line and set it to
   your worker URL. Push.

**You'll know it worked when:** `/admin/` shows a "Sign in with GitHub" button
and logging in lists the Hominin Hub posts.

---

## Step 8 · Run both, then cancel

1. Leave both sites up for a week.
2. Check: every page loads, the PDFs download, `/admin/` works, old `/post/`
   links redirect, and email to `sapientjournal@gmail.com` still arrives.
3. Submit the site to https://search.google.com/search-console — the old
   version was tagged `noindex`, so Google may need re-introducing to it.
4. **Only now** cancel the Wix subscription.
5. Archive everything you downloaded in Step 2 into a shared Drive folder the
   board owns collectively.

---

## Handing over next year

Add the incoming editors as collaborators on the GitHub organization, show
them `/admin/`, and point them at the "For editors" table in `README.md`.
That's the whole handover — no passwords to pass along, no subscription to
transfer, nothing that expires if the board forgets about it over the summer.

## If something breaks

- **Build fails on Cloudflare:** open the deploy log; it names the file. The
  live site stays on the last successful build, so a bad push can't take the
  site down.
- **A change looks wrong:** every save is a git commit. Revert it on GitHub.
- **Everything looks broken locally:** delete `node_modules` and run
  `npm install` again.
