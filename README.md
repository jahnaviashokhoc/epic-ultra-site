# EPICUltra Website

Enterprise AI Engineered for Accountability — epicultra.ai

---

## How to Update the Site

### 1. Edit content only
Open `content.md` and change any text, headlines, stats, or copy.

### 2. Push to GitHub
```bash
git add content.md
git commit -m "Update: [what you changed]"
git push
```

### 3. Done
GitHub Action automatically runs `build.py`, regenerates all HTML files, commits them, and Netlify deploys — live in ~60 seconds.

---

## One-Time Setup

### Connect GitHub → Netlify

1. Go to [netlify.com](https://netlify.com) → **Add new site** → **Import an existing project**
2. Choose **GitHub** → select `jahnaviashokhoc/epic-ultra-site`
3. Set build settings:
   - **Build command:** `python3 build.py`
   - **Publish directory:** `.` (just a dot)
4. Click **Deploy site**
5. Connect your custom domain `epicultra.ai` in Site Settings → Domain management

### Enable GitHub Actions permissions
In your repo: **Settings** → **Actions** → **General** → set **Workflow permissions** to **Read and write permissions**

---

## File Structure

```
epic-ultra-site/
├── content.md          ← EDIT THIS to update site content
├── build.py            ← Build script (do not edit unless adding pages)
├── netlify.toml        ← Netlify config
├── index.html          ← Auto-generated (do not edit directly)
├── architecture.html   ← Auto-generated
├── agents.html         ← Auto-generated
├── governance.html     ← Auto-generated
├── usecases.html       ← Auto-generated
├── about.html          ← Auto-generated
├── resources.html      ← Auto-generated
└── .github/
    └── workflows/
        └── build.yml   ← GitHub Action (auto-runs on push)
```

---

## Local Development

```bash
# Build the site locally
python3 build.py

# Preview (Python built-in server)
python3 -m http.server 8080
# Open: http://localhost:8080
```

---

## Adding New Content

Tell Claude: `@content.md — [describe what to add]`
Claude will update `content.md`. Then push and the site auto-deploys.
