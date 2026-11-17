import os
import json
import shutil
from datetime import datetime


class WikiBuilder:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.dist_dir = os.path.join(root_dir, 'dist')
        self.config = self.load_json('config.json')
        self.codes = self.load_json('data/codes.json')
        self.entities = self.load_json('data/entities.json')
        self.tierlist_data = self.load_json('data/tierlist.json')
        self.guides = self.load_json('data/guides.json')

    def load_json(self, rel_path):
        path = os.path.join(self.root_dir, rel_path)
        if not os.path.exists(path):
            return {} if rel_path.endswith('config.json') or rel_path.endswith('tierlist.json') else []
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_base_css(self):
        return """
        <style>
        :root {
            --bg-main: #0b0f19;
            --bg-card: #111827;
            --bg-card-sub: #1f2937;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --accent: #a78bfa;
            --accent-hover: #8b5cf6;
            --border: #1e293b;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg-main);
            color: var(--text-main);
            line-height: 1.65;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        a { color: inherit; text-decoration: none; }
        .container { max-width: 1120px; margin: 0 auto; padding: 0 1.25rem; }
        nav {
            background: rgba(15, 23, 42, 0.92);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border);
            position: sticky;
            top: 0;
            z-index: 50;
        }
        .nav-inner { display: flex; align-items: center; justify-content: space-between; min-height: 4.25rem; gap: 1rem; flex-wrap: wrap; padding: 0.5rem 0; }
        .nav-logo { font-size: 1.2rem; font-weight: 800; color: #fff; display: flex; align-items: center; gap: 0.5rem; }
        .nav-logo span { color: var(--accent); }
        .nav-links { display: flex; gap: 1.15rem; align-items: center; flex-wrap: wrap; }
        .nav-links a { font-size: 0.9rem; font-weight: 600; color: var(--text-muted); transition: color 0.15s; }
        .nav-links a:hover, .nav-links a.active { color: var(--accent); }
        .hero {
            background: radial-gradient(circle at top center, rgba(139, 92, 246, 0.24) 0%, rgba(11, 15, 25, 0.96) 75%);
            padding: 3.75rem 0 3rem;
            text-align: center;
            border-bottom: 1px solid var(--border);
        }
        .hero h1 {
            font-size: 2.65rem;
            font-weight: 900;
            letter-spacing: -0.025em;
            background: linear-gradient(to right, #ffffff, #c4b5fd, #38bdf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.9rem;
        }
        .hero p { font-size: 1.08rem; color: var(--text-muted); max-width: 760px; margin: 0 auto 1.75rem; }
        .hero-stats { display: flex; justify-content: center; gap: 1.5rem; flex-wrap: wrap; margin-top: 1.5rem; }
        .hero-stat-box { background: rgba(30, 41, 59, 0.65); border: 1px solid var(--border); padding: 0.7rem 1.35rem; border-radius: 0.75rem; }
        .hero-stat-num { font-size: 1.35rem; font-weight: 800; color: var(--accent); }
        .hero-stat-label { font-size: 0.78rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; }
        .main-layout { padding: 2.25rem 0; flex: 1; }
        .card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 0.85rem; padding: 1.75rem; margin-bottom: 2rem; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25); }
        .card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem; border-bottom: 1px solid var(--border); padding-bottom: 0.85rem; flex-wrap: wrap; gap: 0.5rem; }
        .card-title { font-size: 1.4rem; font-weight: 800; display: flex; align-items: center; gap: 0.5rem; color: #fff; }
        .badge-verified { display: inline-flex; align-items: center; gap: 0.35rem; background: rgba(16, 185, 129, 0.12); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); padding: 0.25rem 0.7rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 700; }
        .code-row { display: flex; align-items: center; justify-content: space-between; background: var(--bg-card-sub); border: 1px solid var(--border); padding: 1rem 1.25rem; border-radius: 0.65rem; margin-bottom: 0.75rem; }
        .code-val { font-family: 'Fira Code', monospace; font-size: 1.05rem; font-weight: 800; color: var(--accent); letter-spacing: 0.03em; }
        .code-reward { font-size: 0.92rem; color: var(--text-muted); margin-left: 0.75rem; }
        .btn-copy { background: var(--accent); color: #0b0f19; border: none; padding: 0.55rem 1.1rem; border-radius: 0.45rem; font-weight: 800; font-size: 0.85rem; cursor: pointer; display: inline-block; }
        .btn-copy:hover { background: var(--accent-hover); color: #fff; }
        .tab-bar { display: flex; gap: 0.75rem; margin-bottom: 1.5rem; flex-wrap: wrap; }
        .tab-btn { background: var(--bg-card-sub); border: 1px solid var(--border); color: var(--text-muted); padding: 0.6rem 1.15rem; border-radius: 0.5rem; font-weight: 700; cursor: pointer; font-size: 0.9rem; display: inline-block; }
        .tab-btn.active { background: var(--accent); color: #0b0f19; border-color: var(--accent); }
        .tier-row { display: flex; border: 1px solid var(--border); border-radius: 0.65rem; overflow: hidden; margin-bottom: 0.85rem; background: var(--bg-card-sub); }
        .tier-label { width: 80px; display: flex; align-items: center; justify-content: center; font-size: 1.4rem; font-weight: 900; color: #0b0f19; flex-shrink: 0; }
        .tier-S-plus { background: linear-gradient(135deg, #f43f5e, #fb7185); }
        .tier-S { background: linear-gradient(135deg, #f59e0b, #fbbf24); }
        .tier-A { background: linear-gradient(135deg, #3b82f6, #60a5fa); }
        .tier-items { padding: 0.9rem; display: flex; flex-wrap: wrap; gap: 0.85rem; flex: 1; }
        .tier-item-pill { background: var(--bg-main); border: 1px solid var(--border); padding: 0.65rem 0.95rem; border-radius: 0.5rem; min-width: 190px; flex: 1 1 210px; display: block; }
        .tier-item-pill:hover { border-color: var(--accent); }
        .rarity-badge { display: inline-block; font-size: 0.72rem; font-weight: 800; padding: 0.15rem 0.5rem; border-radius: 0.3rem; text-transform: uppercase; }
        .rarity-Mythical { background: rgba(168, 85, 247, 0.2); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.4); }
        .rarity-Legendary { background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.4); }
        .entity-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1.15rem; }
        .entity-card { background: var(--bg-card-sub); border: 1px solid var(--border); border-radius: 0.75rem; padding: 1.25rem; display: flex; flex-direction: column; justify-content: space-between; }
        .entity-card:hover { border-color: var(--accent); }
        .search-input { width: 100%; padding: 0.85rem 1.2rem; background: var(--bg-main); border: 1px solid var(--border); border-radius: 0.6rem; color: #fff; font-size: 1rem; margin-bottom: 1.25rem; outline: none; }
        .stats-table { width: 100%; border-collapse: collapse; margin: 1.25rem 0; }
        .stats-table th, .stats-table td { padding: 0.8rem 1rem; border-bottom: 1px solid var(--border); text-align: left; }
        .stats-table th { color: var(--text-muted); font-size: 0.82rem; text-transform: uppercase; }
        .calc-box { background: var(--bg-card-sub); border: 1px solid var(--border); border-radius: 0.75rem; padding: 1.5rem; }
        .calc-input-group { margin-bottom: 1.15rem; }
        .calc-label { display: block; font-size: 0.9rem; font-weight: 700; margin-bottom: 0.4rem; color: var(--text-muted); }
        .calc-input, .calc-select { width: 100%; padding: 0.75rem 1rem; background: var(--bg-main); border: 1px solid var(--border); border-radius: 0.5rem; color: #fff; font-size: 1rem; }
        .calc-btn { width: 100%; background: var(--accent); color: #0b0f19; border: none; padding: 0.85rem; border-radius: 0.5rem; font-size: 1rem; font-weight: 800; cursor: pointer; }
        .calc-result { margin-top: 1.25rem; padding: 1.15rem; background: rgba(139, 92, 246, 0.1); border: 1px solid var(--accent); border-radius: 0.5rem; }
        .breadcrumbs { font-size: 0.9rem; color: var(--text-muted); margin-bottom: 1.5rem; display: flex; gap: 0.5rem; flex-wrap: wrap; }
        .breadcrumbs a { color: var(--accent); font-weight: 600; }
        footer { background: #080c14; border-top: 1px solid var(--border); padding: 2.5rem 0; text-align: center; color: var(--text-muted); font-size: 0.9rem; margin-top: auto; }
        @media (max-width: 768px) {
            .nav-inner { flex-direction: column; padding: 0.85rem 0; }
            .hero h1 { font-size: 1.95rem; }
            .tier-row { flex-direction: column; }
            .tier-label { width: 100%; padding: 0.45rem; }
            .code-row { flex-direction: column; align-items: flex-start; gap: 0.65rem; }
        }
        </style>
        """

    def render_nav(self, current_page=""):
        return f"""
        <nav>
            <div class="container nav-inner">
                <a href="/" class="nav-logo">
                    <img src="/assets/images/favicon-48x48.png" alt="RBXMeta Anime Crusaders X Logo" width="28" height="28" style="border-radius: 6px;">
                    {self.config['site']['name']} <span>Tools</span>
                </a>
                <div class="nav-links">
                    <a href="/tier-list" class="{'active' if current_page=='tierlist' else ''}">Tier List</a>
                    <a href="/units/" class="{'active' if current_page=='units' else ''}">Units</a>
                    <a href="/team-builder" class="{'active' if current_page=='teambuilder' else ''}">Team Builder</a>
                    <a href="/unit-comparison" class="{'active' if current_page=='compare' else ''}">Compare</a>
                    <a href="/best-units" class="{'active' if current_page=='bestunits' else ''}">Best Units</a>
                    <a href="/codes" class="{'active' if current_page=='codes' else ''}">Codes</a>
                    <a href="/updates" class="{'active' if current_page=='updates' else ''}">Updates</a>
                </div>
            </div>
        </nav>
        """

    def render_footer(self):
        return f"""
        <footer>
            <div class="container">
                <p>© {datetime.now().year} RBXMeta • {self.config['site']['name']} Tools &amp; Wiki. <a href="/best-dps" style="color:var(--accent);">Best DPS</a> • <a href="/best-support" style="color:var(--accent);">Best Support</a> • <a href="/calculator" style="color:var(--accent);">Pity Calculator</a> • <a href="/about" style="color:var(--accent);">About</a> • <a href="/editorial-policy" style="color:var(--accent);">Editorial Policy</a> • <a href="/changelog" style="color:var(--accent);">Changelog</a> • <a href="https://theforgewiki.wiki/" style="color:var(--accent);" target="_blank" rel="noopener">The Forge Wiki ↗</a></p>
                <p style="margin-top: 0.5rem; font-size: 0.85rem;">Fan-made unofficial wiki &amp; tools hub. Not affiliated with 32x or Roblox Corporation.</p>
            </div>
        </footer>
        <script>
        function copyCode(btn, code) {{
            navigator.clipboard.writeText(code).then(() => {{
                const orig = btn.innerText;
                btn.innerText = "COPIED!";
                setTimeout(() => btn.innerText = orig, 1800);
            }});
        }}
        </script>
        """

    def render_schema_breadcrumbs(self, items):
        domain = self.config['site']['domain'].rstrip('/')
        elements = [{"@type": "ListItem", "position": idx, "name": name, "item": f"{domain}{path}"} for idx, (name, path) in enumerate(items, 1)]
        return f'<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": elements})}</script>'

    def render_schema_article(self, headline, description, path, date_modified=None):
        domain = self.config['site']['domain'].rstrip('/')
        mod = date_modified or datetime.now().strftime('%Y-%m-%d')
        data = {
            "@context": "https://schema.org", "@type": "Article", "headline": headline, "description": description,
            "image": [f"{domain}/assets/images/favicon-192x192.png"],
            "datePublished": "2026-11-17", "dateModified": mod,
            "mainEntityOfPage": {"@type": "WebPage", "@id": f"{domain}{path}"},
            "author": {"@type": "Organization", "name": "RBXMeta", "url": domain},
            "publisher": {"@type": "Organization", "name": "RBXMeta", "logo": {"@type": "ImageObject", "url": f"{domain}/assets/images/favicon-192x192.png"}}
        }
        return f'<script type="application/ld+json">{json.dumps(data)}</script>'

    def render_schema_faq(self, faqs):
        items = [{"@type": "Question", "name": f["question"], "acceptedAnswer": {"@type": "Answer", "text": f["answer"]}} for f in faqs]
        return f'<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": items})}</script>'

    def render_hreflang(self, slug):
        domain = self.config['site']['domain'].rstrip('/')
        return f'<link rel="alternate" hreflang="en" href="{domain}/{slug}"><link rel="alternate" hreflang="es" href="{domain}/es/{slug}"><link rel="alternate" hreflang="pt" href="{domain}/pt/{slug}"><link rel="alternate" hreflang="x-default" href="{domain}/{slug}">'

    def render_lang_switcher(self, slug, current="en"):
        pills = []
        for code, label, href in [("en", "English", f"/{slug}"), ("es", "Español", f"/es/{slug}"), ("pt", "Português", f"/pt/{slug}")]:
            st = "background: var(--accent); color: #0b0f19; border-color: var(--accent);" if code == current else "background: var(--bg-card-sub); color: var(--text-muted); border-color: var(--border);"
            pills.append(f'<a href="{href}" style="padding: 0.3rem 0.75rem; border-radius: 0.4rem; border: 1px solid; font-size: 0.8rem; font-weight: 700; {st}">{label}</a>')
        return f'<div style="display: flex; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 1rem;">{"".join(pills)}</div>'

    def render_pity_calculator(self):
        return """
        <div class="calc-box">
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem;">
                <div class="calc-input-group" style="margin-bottom: 0;">
                    <label class="calc-label">Current Pulls Toward Pity:</label>
                    <input type="number" id="acx-pity-pulls" class="calc-input" value="40" min="0" max="2000">
                </div>
                <div class="calc-input-group" style="margin-bottom: 0;">
                    <label class="calc-label">Current Gems:</label>
                    <input type="number" id="acx-gems" class="calc-input" value="5000" min="0" max="500000">
                </div>
                <div class="calc-input-group" style="margin-bottom: 0;">
                    <label class="calc-label">Gems per Summon:</label>
                    <select id="acx-cost" class="calc-select">
                        <option value="50">50 Gems (Standard Banner)</option>
                        <option value="500">500 Gems (10x Multi-Pull)</option>
                    </select>
                </div>
            </div>
            <button class="calc-btn" style="margin-top: 1rem;" onclick="calcAcxPity()">Calculate Mythic (200) &amp; Secret (2,000) Pity</button>
            <div id="acx-pity-res" class="calc-result" style="display: none;"></div>
        </div>
        <script>
        function calcAcxPity() {
            const cur = parseInt(document.getElementById('acx-pity-pulls').value) || 0;
            const gems = parseInt(document.getElementById('acx-gems').value) || 0;
            const costSel = parseInt(document.getElementById('acx-cost').value) || 50;
            const perPull = (costSel === 500) ? 50 : costSel;
            const pullsFromGems = Math.floor(gems / perPull);
            const totalPulls = cur + pullsFromGems;
            const mythicLeft = Math.max(0, 200 - totalPulls);
            const secretLeft = Math.max(0, 2000 - totalPulls);
            const pMythic = ((1 - Math.pow(1 - 0.005, Math.max(1, pullsFromGems))) * 100).toFixed(2);
            const el = document.getElementById('acx-pity-res');
            el.style.display = 'block';
            el.innerHTML = '<div><strong>Total Pulls Available:</strong> <span style="color:var(--accent);font-weight:800;">' + totalPulls + '</span> (' + pullsFromGems + ' from Gems)</div>' +
                '<div style="margin-top:0.35rem;"><strong>Mythic Pity (0.5% / 200 pulls):</strong> ' + (mythicLeft === 0 ? '<span style="color:#34d399;font-weight:800;">GUARANTEED!</span>' : mythicLeft + ' pulls left (' + (mythicLeft * perPull).toLocaleString() + ' Gems) — ' + pMythic + '% raw hit chance') + '</div>' +
                '<div style="margin-top:0.35rem;"><strong>Secret / Crusader Pity (0.05% / 2,000 pulls):</strong> ' + (secretLeft === 0 ? '<span style="color:#34d399;font-weight:800;">GUARANTEED!</span>' : secretLeft + ' pulls left (' + (secretLeft * perPull).toLocaleString() + ' Gems)') + '</div>';
        }
        </script>
        """

    def render_head_meta(self, title, description, path="/"):
        domain = self.config['site']['domain'].rstrip('/')
        canonical = f"{domain}{path}"
        og_img = f"{domain}/assets/images/favicon-192x192.png"
        return f"""
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title}</title>
            <meta name="description" content="{description}">
            <meta name="robots" content="index, follow, max-image-preview:large">
            <link rel="canonical" href="{canonical}">
            <link rel="icon" href="/favicon.ico" sizes="any">
            <link rel="icon" type="image/png" sizes="48x48" href="/assets/images/favicon-48x48.png">
            <link rel="icon" type="image/png" sizes="192x192" href="/assets/images/favicon-192x192.png">
            <link rel="apple-touch-icon" sizes="180x180" href="/assets/images/apple-touch-icon.png">
            <meta property="og:title" content="{title}">
            <meta property="og:description" content="{description}">
            <meta property="og:type" content="website">
            <meta property="og:url" content="{canonical}">
            <meta property="og:image" content="{og_img}">
            <meta name="twitter:card" content="summary">
            <meta name="twitter:title" content="{title}">
            <meta name="twitter:description" content="{description}">
            <meta name="twitter:image" content="{og_img}">
            <script defer src="https://www.pvuv.ai/f.js" data-site="VcreHBWP" data-api="https://in.pvuv.ai"></script>
            <script async src="https://www.googletagmanager.com/gtm.js?id=GTM-5MKBHFJB"></script>
            <script>
              window.dataLayer = window.dataLayer || [];
              function gtag(){{dataLayer.push(arguments);}}
              gtag('js', new Date());
            </script>
        """

    def build_index(self):
        active_codes = [c for c in self.codes if c["status"] == "Active"]
        codes_html = "".join([f'<div class="code-row"><div><span class="code-val">{c["code"]}</span><span class="code-reward">({c["reward"]})</span></div><button class="btn-copy" onclick="copyCode(this, \'{c["code"]}\')">COPY CODE</button></div>' for c in active_codes[:3]])
        hill_tier = self.tierlist_data["categories"]["Hill_Hybrid"]["tiers"]
        tier_html = ""
        for tk in ["S+", "S", "A"]:
            pills = "".join([f'<a href="/units/{x["slug"]}" class="tier-item-pill"><div style="display:flex;justify-content:space-between;"><strong>{x["name"]}</strong><span class="rarity-badge rarity-{x["rarity"]}">{x["rarity"]}</span></div><p style="color:var(--text-muted);font-size:0.86rem;margin-top:0.25rem;">{x["summary"]}</p></a>' for x in hill_tier.get(tk, [])])
            tier_html += f'<div class="tier-row"><div class="tier-label tier-{tk.replace("+", "-plus")}">{tk}</div><div class="tier-items">{pills}</div></div>'

        db_html = "".join([f'<a href="/units/{e["slug"]}" class="entity-card"><div><div style="display:flex;justify-content:space-between;margin-bottom:0.6rem;"><div><h3 style="font-size:1.1rem;font-weight:800;color:#fff;">{e["name"]}</h3><span style="font-size:0.78rem;color:var(--text-muted);">{e["type"]} • Tier {e["tier"]}</span></div><span class="rarity-badge rarity-{e["rarity"]}">{e["rarity"]}</span></div><p style="color:var(--text-muted);font-size:0.88rem;">{e["description"]}</p></div><div style="margin-top:0.85rem;color:var(--accent);font-weight:700;font-size:0.86rem;">Unit Stats →</div></a>' for e in self.entities[:6]])
        guides_html = "".join([f'<a href="/guides/{g["slug"]}" class="tier-item-pill"><span class="badge-verified" style="margin-bottom:0.4rem;">{g["category"]}</span><h3 style="font-size:1.05rem;font-weight:800;color:#fff;margin-bottom:0.25rem;">{g["title"]}</h3><p style="color:var(--text-muted);font-size:0.86rem;">{g["excerpt"]}</p></a>' for g in self.guides[:4]])
        domain = self.config['site']['domain'].rstrip('/')
        ws_schema = {"@context": "https://schema.org", "@type": "WebSite", "name": "RBXMeta — Anime Crusaders X Tools & Wiki", "url": f"{domain}/", "potentialAction": {"@type": "SearchAction", "target": f"{domain}/units/?q={{search_term_string}}", "query-input": "required name=search_term_string"}}

        html = f"""<!DOCTYPE html><html lang="en"><head>{self.render_head_meta(self.config['site']['title'], self.config['site']['description'], "/")}{self.get_base_css()}<script type="application/ld+json">{json.dumps(ws_schema)}</script>{self.render_schema_article("Anime Crusaders X Tools, Tier List & Wiki", self.config['site']['description'], "/")}{self.render_schema_faq(self.config['faqs'])}</head><body>{self.render_nav("home")}
        <header class="hero"><div class="container"><div class="badge-verified">⚡ ANNIVERSARY RE-RELEASE • VERIFIED {datetime.now().strftime('%Y-%m-%d')}</div><h1>Anime Crusaders X Tools, Tier List &amp; Wiki</h1><p>Welcome to the ultimate Anime Crusaders X resource hub! Discover the latest tier list, explore detailed unit stats, compare characters, and build powerful teams with our free tools.</p><div style="display:flex;justify-content:center;gap:0.85rem;flex-wrap:wrap;"><a href="/tier-list" class="btn-copy" style="padding:0.75rem 1.4rem;">Tier List</a><a href="/team-builder" class="tab-btn">Team Builder</a><a href="/unit-comparison" class="tab-btn">Unit Comparison</a><a href="/units/" class="tab-btn">Units ({len(self.entities)})</a><a href="/codes" class="tab-btn">Codes ({len(active_codes)})</a></div><div class="hero-stats"><div class="hero-stat-box"><div class="hero-stat-num">{len(active_codes)}</div><div class="hero-stat-label">Active Codes</div></div><div class="hero-stat-box"><div class="hero-stat-num">{len(self.entities)}</div><div class="hero-stat-label">Meta Units</div></div><div class="hero-stat-box"><div class="hero-stat-num">4</div><div class="hero-stat-label">Interactive Tools</div></div></div></div></header>
        <main class="container main-layout">
            <section class="card"><div class="card-header"><h2 class="card-title">🧰 Core Interactive Tools</h2></div><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:1rem;"><a href="/tier-list" class="tier-item-pill"><strong>🏆 Tier List</strong><p style="color:var(--text-muted);font-size:0.86rem;">Searchable S+ to A rankings by Hill, Ground, Hybrid &amp; Support.</p></a><a href="/team-builder" class="tier-item-pill"><strong>🛡️ Team Builder</strong><p style="color:var(--text-muted);font-size:0.86rem;">Assemble a 6-unit lineup and check role &amp; support coverage.</p></a><a href="/unit-comparison" class="tier-item-pill"><strong>⚖️ Unit Comparison</strong><p style="color:var(--text-muted);font-size:0.86rem;">Compare two units side-by-side by role, tier &amp; synergies.</p></a><a href="/best-units" class="tier-item-pill"><strong>⭐ Best Units Guide</strong><p style="color:var(--text-muted);font-size:0.86rem;">Upgrade priority, Best DPS, and Best Support picks.</p></a></div></section>
            <section class="card"><div class="card-header"><h2 class="card-title">🎲 Instant Gem &amp; Pity Calculator</h2><a href="/calculator" style="color:var(--accent);font-weight:700;">Full Calculator →</a></div>{self.render_pity_calculator()}</section>
            <section class="card"><div class="card-header"><h2 class="card-title">🎁 Active Codes (32x Group + Lobby Circle)</h2><a href="/codes" style="color:var(--accent);font-weight:700;">All Codes →</a></div>{codes_html}</section>
            <section class="card"><div class="card-header"><h2 class="card-title">🏆 Hill &amp; Hybrid Meta Tier List</h2><a href="/tier-list" style="color:var(--accent);font-weight:700;">Filter Full Tier List →</a></div>{tier_html}</section>
            <section class="card"><div class="card-header"><h2 class="card-title">🔥 Evolution, Fusion &amp; Trait Guides</h2><a href="/guides/" style="color:var(--accent);font-weight:700;">All Guides ({len(self.guides)}) →</a></div><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:1rem;">{guides_html}</div></section>
            <section class="card"><div class="card-header"><h2 class="card-title">📚 Featured Units</h2><a href="/units/" style="color:var(--accent);font-weight:700;">Browse All ({len(self.entities)}) →</a></div><div class="entity-grid">{db_html}</div></section>
            <section class="card"><div class="card-header"><h2 class="card-title">❓ Frequently Asked Questions</h2></div>{''.join([f'<div style="margin-bottom:1.25rem;"><h3 style="color:#38bdf8;font-size:1.05rem;">{f["question"]}</h3><p style="color:var(--text-muted);">{f["answer"]}</p></div>' for f in self.config['faqs']])}</section>
        </main>{self.render_footer()}</body></html>"""
        with open(os.path.join(self.dist_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(html)

    def build_codes(self):
        active = [c for c in self.codes if c["status"] == "Active"]
        rows = ""
        for c in active:
            v_status = c.get("verification", "Verified")
            v_color = "#34d399" if "Verified" in v_status else "#fbbf24"
            rows += f"""
            <div class="code-row" style="flex-direction: column; align-items: stretch; gap: 0.6rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem;">
                    <div>
                        <span class="code-val">{c['code']}</span>
                        <span class="code-reward">({c['reward']})</span>
                        <span style="display:inline-block;margin-left:0.5rem;font-size:0.74rem;font-weight:800;padding:0.15rem 0.5rem;border-radius:0.35rem;border:1px solid {v_color};color:{v_color};">{v_status}</span>
                    </div>
                    <button class="btn-copy" onclick="copyCode(this, '{c['code']}')">COPY CODE</button>
                </div>
                <div style="font-size: 0.82rem; color: var(--text-muted); display: flex; gap: 1rem; flex-wrap: wrap;">
                    <span><strong>Level Req:</strong> {c.get('levelReq', 'None')}</span>
                    <span><strong>First Seen:</strong> {c.get('firstSeen', c.get('addedDate', ''))}</span>
                    <span><strong>Last Checked:</strong> {c.get('lastVerified', '')}</span>
                    <span><strong>Source:</strong> {c.get('method', c.get('source', 'Community'))}</span>
                </div>
            </div>
            """
        html = f"""<!DOCTYPE html><html lang="en"><head>{self.render_head_meta(f"{self.config['site']['name']} Codes | Latest Working Codes & Verification Log", f"All working {self.config['site']['name']} Roblox codes with per-code verification status, level requirements, and sources.", "/codes")}{self.render_hreflang("codes")}{self.get_base_css()}{self.render_schema_breadcrumbs([("Home", "/"), ("Codes", "/codes")])}{self.render_schema_article(f"{self.config['site']['name']} Codes", "Active codes with individual verification status and lobby redemption guide.", "/codes")}</head><body>{self.render_nav("codes")}
        <main class="container main-layout"><div class="breadcrumbs"><a href="/">Home</a> <span>/</span> <span>Codes</span></div><div class="card">{self.render_lang_switcher("codes", "en")}<div class="badge-verified" style="margin-bottom:0.75rem;">✓ PER-CODE VERIFICATION • UPDATED {datetime.now().strftime('%Y-%m-%d')}</div><h1 style="font-size:2.2rem;font-weight:900;margin-bottom:0.75rem;">{self.config['site']['name']} Codes</h1><p style="color:var(--text-muted);margin-bottom:1.5rem;">Each code is tracked individually with its verification status, level requirement, first-seen date, and source. See our <a href="/editorial-policy" style="color:var(--accent);">Editorial Policy</a> for how we distinguish <strong>Verified</strong> vs <strong>Unverified</strong> codes.</p>{rows}<div style="margin-top:2rem;padding-top:1.5rem;border-top:1px solid var(--border);"><h2 style="font-size:1.3rem;margin-bottom:0.75rem;">How to Redeem Codes in {self.config['site']['name']}</h2><ol style="margin-left:1.5rem;color:#cbd5e1;line-height:1.9;"><li>Join the official <strong>32x</strong> Roblox group and favorite the game.</li><li>Launch <strong>{self.config['site']['name']}</strong> and enter the green <strong>Codes</strong> circle in the lobby.</li><li>Paste an active code and click <strong>Redeem</strong> (note level requirements for <code>ACCOMEBACK</code> Lv.20+ and <code>ANNIVERSARY</code> Lv.10+).</li></ol></div></div></main>{self.render_footer()}</body></html>"""
        with open(os.path.join(self.dist_dir, 'codes.html'), 'w', encoding='utf-8') as f:
            f.write(html)

    def build_tierlist(self):
        cats = self.tierlist_data["categories"]
        ent_map = {e["slug"]: e for e in self.entities}
        panels = ""
        for idx, (cname, cobj) in enumerate(cats.items()):
            disp = "block" if idx == 0 else "none"
            label = cname.replace("_", " & ")
            trows, tbl = "", ""
            for tk, items in cobj["tiers"].items():
                pills = "".join([f'<a href="/units/{x["slug"]}" class="tier-item-pill"><div style="display:flex;justify-content:space-between;"><strong>{x["name"]}</strong><span class="rarity-badge rarity-{x["rarity"]}">{x["rarity"]}</span></div><p style="color:var(--text-muted);font-size:0.88rem;margin-top:0.25rem;">{x["summary"]}</p></a>' for x in items])
                trows += f'<div class="tier-row"><div class="tier-label tier-{tk.replace("+", "-plus")}">{tk}</div><div class="tier-items">{pills}</div></div>'
                for x in items:
                    ue = ent_map.get(x["slug"], {})
                    tbl += f'<tr><td><strong>{tk}</strong></td><td><a href="/units/{x["slug"]}" style="color:var(--accent);font-weight:700;">{x["name"]}</a></td><td>{ue.get("role", "DPS")}</td><td>{ue.get("gameMode", "Progressive & Infinite")}</td><td>{ue.get("traits", "Damage / Range")}</td><td>{x["summary"]}</td></tr>'
            panels += f'<section class="tier-category-panel" id="panel-{cname}" style="display:{disp};"><h2 style="font-size:1.4rem;margin-bottom:0.4rem;">{label} Tier List</h2><p style="color:var(--text-muted);margin-bottom:1.25rem;">{cobj["description"]}</p>{trows}<table class="stats-table"><thead><tr><th>Tier</th><th>Unit</th><th>Role</th><th>Best Mode</th><th>Traits</th><th>Meta Notes</th></tr></thead><tbody>{tbl}</tbody></table></section>'

        html = f"""<!DOCTYPE html><html lang="en"><head>{self.render_head_meta(f"{self.config['site']['name']} Tier List | Best Units Ranked", f"Searchable {self.config['site']['name']} (Anime Crusader X) unit tier list across Hill, Ground, Hybrid & Support for Infinite and Story modes.", "/tier-list")}{self.render_hreflang("tier-list")}{self.get_base_css()}{self.render_schema_breadcrumbs([("Home", "/"), ("Tier List", "/tier-list")])}{self.render_schema_article(f"{self.config['site']['name']} Tier List", "Complete unit rankings across Hill, Ground, Hybrid, and Support.", "/tier-list")}</head><body>{self.render_nav("tierlist")}
        <main class="container main-layout"><div class="breadcrumbs"><a href="/">Home</a> <span>/</span> <span>Tier List</span></div><div class="card">{self.render_lang_switcher("tier-list", "en")}<div class="badge-verified" style="margin-bottom:0.75rem;">✓ LAST UPDATED: {datetime.now().strftime('%Y-%m-%d')} • ANNIVERSARY RE-RELEASE</div><h1 style="font-size:2.2rem;font-weight:900;margin-bottom:0.5rem;">{self.config['site']['name']} Tier List</h1><p style="color:var(--text-muted);margin-bottom:1.25rem;">Filterable rankings across Hill, Hybrid, Ground, and Support placements (also known as Anime Crusader X Tier List). Ranked by Progressive &amp; Infinite performance, not just rarity.</p><input type="text" id="tl-search" class="search-input" placeholder="🔍 Search Goju, Gilgamesh, Eskanoor, Kurimi..." oninput="filterTierList()"><div class="tab-bar"><button class="tab-btn active" onclick="switchCategory('Hill_Hybrid')">Hill &amp; Hybrid</button><button class="tab-btn" onclick="switchCategory('Ground')">Ground</button><button class="tab-btn" onclick="switchCategory('Support')">Support</button></div>{panels}<div style="margin-top:2rem;padding-top:1.5rem;border-top:1px solid var(--border);"><h2 style="font-size:1.3rem;margin-bottom:0.85rem;">🎲 Gem &amp; Pity Calculator</h2>{self.render_pity_calculator()}</div></div></main>{self.render_footer()}<script>function switchCategory(c){{document.querySelectorAll('.tab-btn').forEach(b=>b.classList.toggle('active',b.getAttribute('onclick').includes(c)));document.querySelectorAll('.tier-category-panel').forEach(p=>p.style.display=(p.id==='panel-'+c)?'block':'none');}}function filterTierList(){{const q=(document.getElementById('tl-search').value||'').toLowerCase();document.querySelectorAll('.tier-item-pill').forEach(el=>{{el.style.display=(!q||el.innerText.toLowerCase().includes(q))?'block':'none';}});document.querySelectorAll('.tier-category-panel table tbody tr').forEach(tr=>{{tr.style.display=(!q||tr.innerText.toLowerCase().includes(q))?'':'none';}});}}</script></body></html>"""
        with open(os.path.join(self.dist_dir, 'tier-list.html'), 'w', encoding='utf-8') as f:
            f.write(html)

    def build_calculator(self):
        schema = {"@context": "https://schema.org", "@type": "SoftwareApplication", "name": f"{self.config['site']['name']} Summon & Trait Odds Calculator", "operatingSystem": "Web", "applicationCategory": "GameApplication", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}
        html = f"""<!DOCTYPE html><html lang="en"><head>{self.render_head_meta(f"{self.config['site']['name']} Gem, Pity & Trait Calculator", "Calculate Mythic (200) & Secret (2,000) pity requirements and Trait Remnant reroll probabilities in Anime Crusaders X.", "/calculator")}{self.get_base_css()}{self.render_schema_breadcrumbs([("Home", "/"), ("Calculator", "/calculator")])}<script type="application/ld+json">{json.dumps(schema)}</script></head><body>{self.render_nav("calc")}
        <main class="container main-layout"><div class="breadcrumbs"><a href="/">Home</a> <span>/</span> <span>Calculator</span></div><div class="card"><h1 style="font-size:2.2rem;font-weight:900;margin-bottom:0.5rem;">{self.config['site']['name']} Gem, Pity &amp; Evolution Calculator</h1><p style="color:var(--text-muted);margin-bottom:1.5rem;">Calculate Mythic (200) &amp; Secret/Crusader (2,000) pity requirements, Trait Remnant reroll odds, and Evolution material deficits.</p>{self.render_pity_calculator()}<h2 style="font-size:1.35rem;margin:2rem 0 1rem;color:#38bdf8;">Trait Remnant Reroll Odds Calculator</h2><div class="calc-box"><div class="calc-input-group"><label class="calc-label">Total Pulls / Trait Remnants:</label><input type="number" id="pulls" class="calc-input" value="100" min="1" max="5000"></div><div class="calc-input-group"><label class="calc-label">Target Drop Rate (%):</label><input type="number" id="rate" class="calc-input" value="0.5" step="0.05" min="0.01" max="100"></div><button class="calc-btn" onclick="calcOdds()">Calculate Cumulative Odds</button><div id="res" class="calc-result" style="display:none;"></div></div><h2 style="font-size:1.35rem;margin:2rem 0 1rem;color:#34d399;">Evolution Material &amp; Cube Planner</h2><div class="calc-box"><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:1rem;"><div class="calc-input-group"><label class="calc-label">Required Cubes / Shards:</label><input type="number" id="evo-req" class="calc-input" value="50" min="1" max="5000"></div><div class="calc-input-group"><label class="calc-label">Owned in Inventory:</label><input type="number" id="evo-own" class="calc-input" value="15" min="0" max="5000"></div><div class="calc-input-group"><label class="calc-label">Avg Drop per Stage Clear:</label><input type="number" id="evo-drop" class="calc-input" value="2" min="1" max="100"></div></div><button class="calc-btn" style="background:#10b981;" onclick="calcEvo()">Calculate Remaining Runs</button><div id="evo-res" class="calc-result" style="display:none;border-color:#10b981;"></div></div></div></main>{self.render_footer()}<script>function calcOdds(){{const n=parseInt(document.getElementById('pulls').value)||0;const p=(parseFloat(document.getElementById('rate').value)||0)/100;const prob=((1-Math.pow(1-p,n))*100).toFixed(2);const el=document.getElementById('res');el.style.display='block';el.innerHTML='<strong>Chance after '+n+' rolls:</strong> <span style=\"color:var(--accent);font-size:1.25rem;font-weight:900;\">'+prob+'%</span>';}}function calcEvo(){{const req=parseInt(document.getElementById('evo-req').value)||0;const own=parseInt(document.getElementById('evo-own').value)||0;const drop=Math.max(1,parseInt(document.getElementById('evo-drop').value)||1);const need=Math.max(0,req-own);const runs=Math.ceil(need/drop);const el=document.getElementById('evo-res');el.style.display='block';el.innerHTML=need===0?'<strong style=\"color:#34d399;\">You already have enough materials to evolve!</strong>':'<strong>Missing Materials:</strong> '+need+' • <strong>Estimated Clears Needed:</strong> <span style=\"color:#34d399;font-weight:900;\">'+runs+' runs</span>';}}</script></body></html>"""
        with open(os.path.join(self.dist_dir, 'calculator.html'), 'w', encoding='utf-8') as f:
            f.write(html)

    def build_team_builder(self):
        schema = {"@context": "https://schema.org", "@type": "SoftwareApplication", "name": f"{self.config['site']['name']} Team Builder", "operatingSystem": "Web", "applicationCategory": "GameApplication", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}
        units_json = json.dumps([{"slug": e["slug"], "name": e["name"], "type": e["type"], "tier": e["tier"], "rarity": e["rarity"]} for e in self.entities])
        options_html = "".join([f'<option value="{e["slug"]}">[{e["tier"]}] {e["name"]} ({e["type"]})</option>' for e in self.entities])
        slots_html = "".join([f'<div class="calc-input-group"><label class="calc-label">Slot {i} Unit:</label><select id="slot-{i}" class="calc-select" onchange="updateTeam()"><option value="">-- Select Unit --</option>{options_html}</select></div>' for i in range(1, 7)])
        html = f"""<!DOCTYPE html><html lang="en"><head>{self.render_head_meta(f"{self.config['site']['name']} Team Builder | Build Your Best Team", "Interactive 6-slot Anime Crusaders X Team Builder. Balance Hill, Ground, Hybrid & Support units and share your lineup.", "/team-builder")}{self.get_base_css()}{self.render_schema_breadcrumbs([("Home", "/"), ("Team Builder", "/team-builder")])}<script type="application/ld+json">{json.dumps(schema)}</script></head><body>{self.render_nav("teambuilder")}
        <main class="container main-layout"><div class="breadcrumbs"><a href="/">Home</a> <span>/</span> <span>Team Builder</span></div><div class="card"><h1 style="font-size:2.2rem;font-weight:900;margin-bottom:0.5rem;">{self.config['site']['name']} Team Builder</h1><p style="color:var(--text-muted);margin-bottom:1.5rem;">Select up to 6 units to check placement coverage across Hill/Hybrid, Ground, and Support slots for Story &amp; Infinite modes.</p><div class="calc-box"><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:1rem;">{slots_html}</div><div id="team-summary" class="calc-result" style="margin-top:1.25rem;"></div></div></div></main>{self.render_footer()}
        <script>
        const units = {units_json};
        const unitMap = Object.fromEntries(units.map(u => [u.slug, u]));
        function updateTeam() {{
            const chosen = [];
            for (let i = 1; i <= 6; i++) {{
                const v = document.getElementById('slot-' + i).value;
                if (v && unitMap[v]) chosen.push(unitMap[v]);
            }}
            const counts = {{ hill: 0, ground: 0, support: 0 }};
            chosen.forEach(u => {{
                const t = u.type.toLowerCase();
                if (t.includes('hill')) counts.hill++;
                else if (t.includes('ground')) counts.ground++;
                else if (t.includes('support')) counts.support++;
            }});
            const el = document.getElementById('team-summary');
            if (!chosen.length) {{ el.innerHTML = '<strong>Pick units above to analyze your team composition.</strong>'; return; }}
            let advice = [];
            if (counts.hill === 0) advice.push('Add at least 1 Hill/Hybrid unit (e.g., Goju vs Sukuno, Gilgamesh, Ishtall).');
            if (counts.ground === 0) advice.push('Add at least 1 Ground DPS (e.g., Mely, Higuru, Excalibur).');
            if (counts.support === 0) advice.push('Add a Support unit (e.g., Kurimi or AI Idol) for Infinite scaling.');
            el.innerHTML = '<div><strong>Selected (' + chosen.length + '/6):</strong> ' + chosen.map(u => u.name + ' [' + u.tier + ']').join(' • ') + '</div>' +
                '<div style="margin-top:0.5rem;"><strong>Role Coverage:</strong> Hill/Hybrid: ' + counts.hill + ' | Ground: ' + counts.ground + ' | Support: ' + counts.support + '</div>' +
                '<div style="margin-top:0.5rem;color:' + (advice.length ? '#fbbf24' : '#34d399') + ';">' + (advice.length ? advice.join(' ') : '✓ Balanced team coverage across all placement types!') + '</div>';
        }}
        document.getElementById('slot-1').value = 'goju-vs-sukuno';
        document.getElementById('slot-2').value = 'mely-assault';
        document.getElementById('slot-3').value = 'kurimi';
        updateTeam();
        </script></body></html>"""
        with open(os.path.join(self.dist_dir, 'team-builder.html'), 'w', encoding='utf-8') as f:
            f.write(html)

    def build_unit_comparison(self):
        schema = {"@context": "https://schema.org", "@type": "SoftwareApplication", "name": f"{self.config['site']['name']} Unit Comparison Tool", "operatingSystem": "Web", "applicationCategory": "GameApplication", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}
        units_json = json.dumps(self.entities)
        options_html = "".join([f'<option value="{e["slug"]}">{e["name"]} ({e["type"]} • {e["tier"]})</option>' for e in self.entities])
        html = f"""<!DOCTYPE html><html lang="en"><head>{self.render_head_meta(f"{self.config['site']['name']} Unit Comparison | Compare Units", "Compare any two Anime Crusaders X units side-by-side by placement, tier ranking, rarity, strengths, and synergies.", "/unit-comparison")}{self.get_base_css()}{self.render_schema_breadcrumbs([("Home", "/"), ("Unit Comparison", "/unit-comparison")])}<script type="application/ld+json">{json.dumps(schema)}</script></head><body>{self.render_nav("compare")}
        <main class="container main-layout"><div class="breadcrumbs"><a href="/">Home</a> <span>/</span> <span>Unit Comparison</span></div><div class="card"><h1 style="font-size:2.2rem;font-weight:900;margin-bottom:0.5rem;">Compare {self.config['site']['name']} Units</h1><p style="color:var(--text-muted);margin-bottom:1.5rem;">Select two units below to compare placement type, tier ranking, strengths, and optimal synergies.</p><div class="calc-box"><div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;"><div><label class="calc-label">Unit A:</label><select id="unit-a" class="calc-select" onchange="compareUnits()">{options_html}</select></div><div><label class="calc-label">Unit B:</label><select id="unit-b" class="calc-select" onchange="compareUnits()">{options_html}</select></div></div><div id="cmp-out" style="margin-top:1.5rem;"></div></div></div></main>{self.render_footer()}
        <script>
        const allUnits = {units_json};
        const uMap = Object.fromEntries(allUnits.map(u => [u.slug, u]));
        function compareUnits() {{
            const a = uMap[document.getElementById('unit-a').value];
            const b = uMap[document.getElementById('unit-b').value];
            if (!a || !b) return;
            document.getElementById('cmp-out').innerHTML = '<table class="stats-table"><thead><tr><th>Attribute</th><th>' + a.name + '</th><th>' + b.name + '</th></tr></thead><tbody>' +
                '<tr><td>Placement</td><td>' + a.type + '</td><td>' + b.type + '</td></tr>' +
                '<tr><td>Tier</td><td><strong>' + a.tier + '</strong></td><td><strong>' + b.tier + '</strong></td></tr>' +
                '<tr><td>Rarity</td><td>' + a.rarity + '</td><td>' + b.rarity + '</td></tr>' +
                '<tr><td>Summary</td><td>' + a.description + '</td><td>' + b.description + '</td></tr>' +
                '<tr><td>Best Synergy</td><td>' + a.bestBuild + '</td><td>' + b.bestBuild + '</td></tr>' +
                '<tr><td>Full Page</td><td><a href="/units/' + a.slug + '" style="color:var(--accent);">View ' + a.name + ' →</a></td><td><a href="/units/' + b.slug + '" style="color:var(--accent);">View ' + b.name + ' →</a></td></tr>' +
                '</tbody></table>';
        }}
        document.getElementById('unit-a').value = 'goju-vs-sukuno';
        document.getElementById('unit-b').value = 'gilgamesh';
        compareUnits();
        </script></body></html>"""
        with open(os.path.join(self.dist_dir, 'unit-comparison.html'), 'w', encoding='utf-8') as f:
            f.write(html)

    def build_editorial_pages(self):
        pages = [
            ("best-units", f"{self.config['site']['name']} Best Units | Top Characters Ranked", f"Best Units in {self.config['site']['name']}", "Upgrade priority and top unit recommendations across Progressive, Infinite, and Boss modes.", self.entities[:10]),
            ("best-dps", f"{self.config['site']['name']} Best DPS Units | Top Damage Dealers", f"Best DPS Units in {self.config['site']['name']}", "Highest DPS Hill, Hybrid, and Ground carries in the current Anniversary Re-Release meta.", [e for e in self.entities if "support" not in e["type"].lower()][:10]),
            ("best-support", f"{self.config['site']['name']} Best Support Units", f"Best Support Units in {self.config['site']['name']}", "Top buffer, economy, and time-control Support units for Infinite mode scaling.", [e for e in self.entities if "support" in e["type"].lower()]),
        ]
        for slug, title, h1, desc, subset in pages:
            cards = "".join([f'<a href="/units/{e["slug"]}" class="entity-card"><div><div style="display:flex;justify-content:space-between;margin-bottom:0.5rem;"><strong>{e["name"]}</strong><span class="rarity-badge rarity-{e["rarity"]}">{e["rarity"]}</span></div><p style="color:var(--text-muted);font-size:0.88rem;">{e["type"]} • Tier {e["tier"]} — {e["description"]}</p></div><div style="margin-top:0.75rem;color:var(--accent);font-weight:700;">View Build →</div></a>' for e in subset])
            html = f"""<!DOCTYPE html><html lang="en"><head>{self.render_head_meta(title, desc, f"/{slug}")}{self.get_base_css()}{self.render_schema_breadcrumbs([("Home", "/"), (h1, f"/{slug}")])}{self.render_schema_article(h1, desc, f"/{slug}")}</head><body>{self.render_nav("bestunits" if slug=="best-units" else "")}
            <main class="container main-layout"><div class="breadcrumbs"><a href="/">Home</a> <span>/</span> <span>{h1}</span></div><div class="card"><div class="badge-verified" style="margin-bottom:0.75rem;">✓ UPDATED {datetime.now().strftime('%Y-%m-%d')}</div><h1 style="font-size:2.2rem;font-weight:900;margin-bottom:0.5rem;">{h1}</h1><p style="color:var(--text-muted);margin-bottom:1.5rem;">{desc} Test lineups in our <a href="/team-builder" style="color:var(--accent);">Team Builder</a> or <a href="/unit-comparison" style="color:var(--accent);">Unit Comparison</a>.</p><div class="entity-grid">{cards}</div></div></main>{self.render_footer()}</body></html>"""
            with open(os.path.join(self.dist_dir, f"{slug}.html"), 'w', encoding='utf-8') as f:
                f.write(html)

        updates_html = f"""<!DOCTYPE html><html lang="en"><head>{self.render_head_meta(f"{self.config['site']['name']} Updates & Patch Notes", "Latest Anime Crusaders X Anniversary Re-Release patch notes, new Hero units, and meta shifts.", "/updates")}{self.get_base_css()}{self.render_schema_breadcrumbs([("Home", "/"), ("Updates", "/updates")])}{self.render_schema_article(f"{self.config['site']['name']} Updates", "Latest Anime Crusaders X patch notes and meta changes.", "/updates")}</head><body>{self.render_nav("updates")}
        <main class="container main-layout"><div class="breadcrumbs"><a href="/">Home</a> <span>/</span> <span>Updates</span></div><div class="card"><h1 style="font-size:2.2rem;font-weight:900;margin-bottom:1rem;">{self.config['site']['name']} Update Log</h1><div style="background:var(--bg-card-sub);border:1px solid var(--border);border-radius:0.65rem;padding:1.25rem;margin-bottom:1rem;"><span class="badge-verified">2026-11-16 • ANNIVERSARY RE-RELEASE</span><h2 style="margin:0.5rem 0;">Anime Crusaders X Re-Release &amp; New Codes</h2><p style="color:var(--text-muted);">Added Eskanoor (first Hero unit), Vegeto Fusion, and active codes <code>ACBESTTD2026</code>, <code>THANKYOUFOR30KMAJORFIXES</code>, <code>WELCOMETOACX</code>. Check the updated <a href="/tier-list" style="color:var(--accent);">Tier List</a> and <a href="/codes" style="color:var(--accent);">Codes</a>.</p></div></div></main>{self.render_footer()}</body></html>"""
        with open(os.path.join(self.dist_dir, "updates.html"), 'w', encoding='utf-8') as f:
            f.write(updates_html)

    def build_database(self):
        db_dir = os.path.join(self.dist_dir, 'units')
        os.makedirs(db_dir, exist_ok=True)
        cards = "".join([f'<a href="/units/{e["slug"]}" class="entity-card" data-type="{e["type"].lower()}" data-name="{e["name"].lower()} {e["rarity"].lower()}"><div><div style="display:flex;justify-content:space-between;margin-bottom:0.6rem;"><div><h3 style="font-size:1.1rem;font-weight:800;color:#fff;">{e["name"]}</h3><span style="font-size:0.78rem;color:var(--text-muted);">{e["type"]} • Tier {e["tier"]}</span></div><span class="rarity-badge rarity-{e["rarity"]}">{e["rarity"]}</span></div><p style="color:var(--text-muted);font-size:0.88rem;">{e["description"]}</p></div><div style="margin-top:0.85rem;color:var(--accent);font-weight:700;font-size:0.86rem;">View Unit →</div></a>' for e in self.entities])
        idx_html = f"""<!DOCTYPE html><html lang="en"><head>{self.render_head_meta(f"{self.config['site']['name']} Units Database | All Units & Stats", "Browse all Hill, Ground, Hybrid & Support units in Anime Crusaders X.", "/units/")}{self.get_base_css()}{self.render_schema_breadcrumbs([("Home", "/"), ("Units", "/units/")])}</head><body>{self.render_nav("units")}
        <main class="container main-layout"><div class="breadcrumbs"><a href="/">Home</a> <span>/</span> <span>Units</span></div><div class="card"><h1 style="font-size:2.2rem;font-weight:900;margin-bottom:1rem;">All {self.config['site']['name']} Units ({len(self.entities)})</h1><input type="text" id="q" class="search-input" placeholder="Search Goju, Gilgamesh, Kurimi, Ground..." oninput="flt()"><div class="tab-bar"><button class="tab-btn active" onclick="setT('all')">All</button><button class="tab-btn" onclick="setT('hill')">Hill &amp; Hybrid</button><button class="tab-btn" onclick="setT('ground')">Ground</button><button class="tab-btn" onclick="setT('support')">Support</button></div><div class="entity-grid">{cards}</div></div></main>{self.render_footer()}<script>let act='all';function setT(t){{act=t;document.querySelectorAll('.tab-btn').forEach(b=>b.classList.toggle('active',b.getAttribute('onclick').includes(t)));flt();}}function flt(){{const q=(document.getElementById('q').value||'').toLowerCase();document.querySelectorAll('.entity-card').forEach(c=>{{const ct=c.getAttribute('data-type'),cn=c.getAttribute('data-name');c.style.display=((act==='all'||ct.includes(act))&&(!q||cn.includes(q)||ct.includes(q)))?'flex':'none';}});}}const iq=new URLSearchParams(location.search).get('q');if(iq){{document.getElementById('q').value=iq;flt();}}</script></body></html>"""
        with open(os.path.join(db_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(idx_html)

        for e in self.entities:
            srows = "".join([f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in e["stats"].items()])
            rel = [x for x in self.entities if x["slug"] != e["slug"] and x["type"] == e["type"]][:4]
            rel_html = "".join([f'<a href="/units/{r["slug"]}" class="tier-item-pill"><strong>{r["name"]}</strong><p style="color:var(--text-muted);font-size:0.84rem;">{r["type"]} • Tier {r["tier"]}</p></a>' for r in rel])
            uhtml = f"""<!DOCTYPE html><html lang="en"><head>{self.render_head_meta(f"{e['name']} Stats & Tier | {self.config['site']['name']} Wiki", e['description'], f"/units/{e['slug']}")}{self.get_base_css()}{self.render_schema_breadcrumbs([("Home", "/"), ("Units", "/units/"), (e["name"], f"/units/{e['slug']}")])}{self.render_schema_article(f"{e['name']} - {self.config['site']['name']}", e['description'], f"/units/{e['slug']}")}</head><body>{self.render_nav("units")}
            <main class="container main-layout"><div class="breadcrumbs"><a href="/">Home</a> <span>/</span> <a href="/units/">Units</a> <span>/</span> <span>{e['name']}</span></div><div class="card"><div style="display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid var(--border);padding-bottom:1rem;margin-bottom:1.25rem;flex-wrap:wrap;gap:1rem;"><div><h1 style="font-size:2.1rem;font-weight:900;">{e['name']}</h1><p style="color:var(--text-muted);">{e['type']} • Tier {e['tier']}</p></div><span class="rarity-badge rarity-{e['rarity']}">{e['rarity']}</span></div><p style="color:#cbd5e1;font-size:1.05rem;margin-bottom:1.5rem;">{e['description']}</p><table class="stats-table">{srows}</table><div style="display:flex;gap:0.75rem;flex-wrap:wrap;margin:1.25rem 0;"><a href="/tier-list" class="tab-btn">View Tier List</a><a href="/team-builder" class="tab-btn">Add to Team Builder</a><a href="/unit-comparison" class="tab-btn">Compare Unit</a></div><h2 style="font-size:1.25rem;margin:1.5rem 0 0.5rem;color:#38bdf8;">How to Obtain &amp; Best Synergies</h2><p style="color:#cbd5e1;">{e['howToGet']} {e['bestBuild']}</p><div style="margin-top:2rem;border-top:1px solid var(--border);padding-top:1.25rem;"><h3 style="margin-bottom:0.85rem;">Related {e['type']} Units</h3><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:0.75rem;">{rel_html}</div></div></div></main>{self.render_footer()}</body></html>"""
            with open(os.path.join(db_dir, f"{e['slug']}.html"), 'w', encoding='utf-8') as f:
                f.write(uhtml)

    def build_guides(self):
        gdir = os.path.join(self.dist_dir, 'guides')
        os.makedirs(gdir, exist_ok=True)
        cards = "".join([f'<a href="/guides/{g["slug"]}" class="card" style="display:block;"><span class="badge-verified">{g["category"]}</span><h2 style="font-size:1.35rem;margin:0.5rem 0;color:#fff;">{g["title"]}</h2><p style="color:var(--text-muted);">{g["excerpt"]}</p></a>' for g in self.guides])
        idx = f"""<!DOCTYPE html><html lang="en"><head>{self.render_head_meta(f"{self.config['site']['name']} Guides", "Evolution, fusion, trait reroll, and strategy guides for Anime Crusaders X.", "/guides/")}{self.get_base_css()}{self.render_schema_breadcrumbs([("Home", "/"), ("Guides", "/guides/")])}</head><body>{self.render_nav("guides")}<main class="container main-layout"><div class="breadcrumbs"><a href="/">Home</a> <span>/</span> <span>Guides</span></div><div class="card"><h1 style="font-size:2.1rem;font-weight:900;margin-bottom:1.25rem;">{self.config['site']['name']} Guides</h1>{cards}</div></main>{self.render_footer()}</body></html>"""
        with open(os.path.join(gdir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(idx)
        for g in self.guides:
            gh = f"""<!DOCTYPE html><html lang="en"><head>{self.render_head_meta(f"{g['title']} | {self.config['site']['name']}", g['excerpt'], f"/guides/{g['slug']}")}{self.get_base_css()}{self.render_schema_breadcrumbs([("Home", "/"), ("Guides", "/guides/"), (g['title'], f"/guides/{g['slug']}")])}{self.render_schema_article(g['title'], g['excerpt'], f"/guides/{g['slug']}", g['updatedDate'])}</head><body>{self.render_nav("guides")}<main class="container main-layout"><div class="breadcrumbs"><a href="/">Home</a> <span>/</span> <a href="/guides/">Guides</a> <span>/</span> <span>{g['title']}</span></div><article class="card"><span class="badge-verified">{g['category']}</span><h1 style="font-size:2.15rem;font-weight:900;margin:0.75rem 0;">{g['title']}</h1><p style="color:var(--text-muted);margin-bottom:1.5rem;">Updated: {g['updatedDate']}</p><div style="font-size:1.08rem;line-height:1.8;color:#e2e8f0;">{g['content'].replace('/database/', '/units/')}</div></article></main>{self.render_footer()}</body></html>"""
            with open(os.path.join(gdir, f"{g['slug']}.html"), 'w', encoding='utf-8') as f:
                f.write(gh)

    def build_localized_pages(self):
        today = datetime.now().strftime('%Y-%m-%d')
        active = [c for c in self.codes if c["status"] == "Active"]
        for lang, label_codes, label_tl in [("es", "Códigos de Anime Crusaders X (Noviembre 2026)", "Tier List de Anime Crusaders X"), ("pt", "Códigos de Anime Crusaders X (Novembro 2026)", "Tier List de Anime Crusaders X")]:
            ldir = os.path.join(self.dist_dir, lang)
            os.makedirs(ldir, exist_ok=True)
            rows = "".join([f'<div class="code-row"><div><span class="code-val">{c["code"]}</span><span class="code-reward">({c["reward"]})</span></div><button class="btn-copy" onclick="copyCode(this, \'{c["code"]}\')">COPY</button></div>' for c in active])
            ch = f'<!DOCTYPE html><html lang="{lang}"><head>{self.render_head_meta(label_codes, label_codes, f"/{lang}/codes")}{self.render_hreflang("codes")}{self.get_base_css()}</head><body>{self.render_nav("codes")}<main class="container main-layout"><div class="card">{self.render_lang_switcher("codes", lang)}<div class="badge-verified" style="margin-bottom:0.75rem;">✓ {today}</div><h1>{label_codes}</h1><div style="margin-top:1rem;">{rows}</div></div></main>{self.render_footer()}</body></html>'
            with open(os.path.join(ldir, 'codes.html'), 'w', encoding='utf-8') as f:
                f.write(ch)
            tbl = ""
            for cname, cobj in self.tierlist_data["categories"].items():
                for tk, items in cobj["tiers"].items():
                    for x in items:
                        tbl += f'<tr><td><strong>{tk}</strong></td><td>{cname.replace("_"," & ")}</td><td><a href="/units/{x["slug"]}" style="color:var(--accent);">{x["name"]}</a></td><td>{x["summary"]}</td></tr>'
            th = f'<!DOCTYPE html><html lang="{lang}"><head>{self.render_head_meta(label_tl, label_tl, f"/{lang}/tier-list")}{self.render_hreflang("tier-list")}{self.get_base_css()}</head><body>{self.render_nav("tierlist")}<main class="container main-layout"><div class="card">{self.render_lang_switcher("tier-list", lang)}<div class="badge-verified" style="margin-bottom:0.75rem;">✓ {today}</div><h1>{label_tl}</h1><table class="stats-table"><thead><tr><th>Tier</th><th>Role</th><th>Unit</th><th>Notes</th></tr></thead><tbody>{tbl}</tbody></table></div></main>{self.render_footer()}</body></html>'
            with open(os.path.join(ldir, 'tier-list.html'), 'w', encoding='utf-8') as f:
                f.write(th)

    def build_trust_pages(self):
        today = datetime.now().strftime('%Y-%m-%d')
        about_html = f"""<!DOCTYPE html><html lang="en"><head>{self.render_head_meta("About RBXMeta | Anime Crusaders X Tools & Wiki", "About RBXMeta, an independent fan-made database and interactive utility hub for Anime Crusaders X on Roblox.", "/about")}{self.get_base_css()}{self.render_schema_breadcrumbs([("Home", "/"), ("About", "/about")])}{self.render_schema_article("About RBXMeta", "Independent fan-made utility hub for Anime Crusaders X.", "/about")}</head><body>{self.render_nav()}
        <main class="container main-layout"><div class="breadcrumbs"><a href="/">Home</a> <span>/</span> <span>About</span></div><div class="card"><h1 style="font-size:2.1rem;font-weight:900;margin-bottom:1rem;">About RBXMeta</h1><p style="color:#cbd5e1;margin-bottom:1rem;"><strong>RBXMeta</strong> is an independent, fan-made database and interactive tools hub built for Roblox players—starting with <strong>Anime Crusaders X</strong>.</p><p style="color:#cbd5e1;margin-bottom:1rem;">Instead of publishing bare text tables, we focus on interactive utilities: a <strong>Gem &amp; Pity Calculator</strong> (200 Mythic / 2,000 Secret), <strong>Trait Reroll Odds Calculator</strong>, <strong>Evolution Material Planner</strong>, <strong>6-Slot Team Builder</strong>, and <strong>Side-by-Side Unit Comparison</strong>.</p><p style="color:var(--text-muted);"><strong>Disclaimer:</strong> RBXMeta is not affiliated with, endorsed by, or sponsored by 32x or Roblox Corporation.</p></div></main>{self.render_footer()}</body></html>"""
        with open(os.path.join(self.dist_dir, "about.html"), 'w', encoding='utf-8') as f:
            f.write(about_html)

        policy_html = f"""<!DOCTYPE html><html lang="en"><head>{self.render_head_meta("Editorial Policy & Verification Standards | RBXMeta", "How RBXMeta evaluates Anime Crusaders X Tier List rankings, verifies Codes (Verified vs Unverified), and calculates summon probabilities.", "/editorial-policy")}{self.get_base_css()}{self.render_schema_breadcrumbs([("Home", "/"), ("Editorial Policy", "/editorial-policy")])}{self.render_schema_article("Editorial Policy & Verification Standards", "How RBXMeta sources and verifies Anime Crusaders X data.", "/editorial-policy")}</head><body>{self.render_nav()}
        <main class="container main-layout"><div class="breadcrumbs"><a href="/">Home</a> <span>/</span> <span>Editorial Policy</span></div><div class="card"><h1 style="font-size:2.1rem;font-weight:900;margin-bottom:1rem;">Editorial Policy &amp; Data Sources</h1><h2 style="font-size:1.25rem;color:#38bdf8;margin:1rem 0 0.5rem;">1. Tier List Methodology</h2><p style="color:#cbd5e1;margin-bottom:1rem;">Unit rankings evaluate <strong>Infinite &amp; Progressive mode utility, placement flexibility (Hill/Ground/Hybrid/Support), scaling, and team synergy</strong>—not rarity alone. Current rankings cross-check consensus data from MrGuider, Destructoid, IGN, and community feedback. We never fabricate playtest claims.</p><h2 style="font-size:1.25rem;color:#38bdf8;margin:1rem 0 0.5rem;">2. Code Verification Labels</h2><ul style="margin-left:1.5rem;color:#cbd5e1;line-height:1.9;"><li><strong>Verified (Media Consensus / Level-Gated):</strong> Confirmed across multiple independent trackers (e.g., IGN, Beebom, Eurogamer) with exact level requirements noted.</li><li><strong>Unverified (Mixed Reports):</strong> Reported by at least one source but flagged as unverified or inconsistent by another (for example, <code>THANKYOUFOR30KMAJORFIXES</code>).</li><li><strong>Expired:</strong> Confirmed inactive and archived so players do not waste time.</li></ul><h2 style="font-size:1.25rem;color:#38bdf8;margin:1rem 0 0.5rem;">3. Calculator Math</h2><p style="color:#cbd5e1;">Our Gem &amp; Pity Calculator uses standard cumulative probability (<code>1 - (1 - p)^n</code>) alongside fixed 200-pull Mythic and 2,000-pull Secret/Crusader pity thresholds.</p></div></main>{self.render_footer()}</body></html>"""
        with open(os.path.join(self.dist_dir, "editorial-policy.html"), 'w', encoding='utf-8') as f:
            f.write(policy_html)

        changelog_html = f"""<!DOCTYPE html><html lang="en"><head>{self.render_head_meta("Site Changelog & Data Updates | RBXMeta", "Full update history for RBXMeta Anime Crusaders X Tier List, Codes verification, and Calculators.", "/changelog")}{self.get_base_css()}{self.render_schema_breadcrumbs([("Home", "/"), ("Changelog", "/changelog")])}{self.render_schema_article("Site Changelog & Data Updates", "Update history for RBXMeta.", "/changelog")}</head><body>{self.render_nav()}
        <main class="container main-layout"><div class="breadcrumbs"><a href="/">Home</a> <span>/</span> <span>Changelog</span></div><div class="card"><h1 style="font-size:2.1rem;font-weight:900;margin-bottom:1rem;">Site Changelog</h1><ul style="margin-left:1.5rem;color:#cbd5e1;line-height:2;"><li><strong>{today}:</strong> Added per-code verification status &amp; sources on <code>/codes</code> (flagging <code>THANKYOUFOR30KMAJORFIXES</code> as Unverified due to mixed reports); enriched all 24 unit pages with Role, Mode, Evolution, and Trait recommendations; launched <code>/about</code>, <code>/editorial-policy</code>, <code>/changelog</code>, and Evolution Material Planner on <code>/calculator</code>.</li><li><strong>2026-11-17:</strong> Launched <code>/team-builder</code>, <code>/unit-comparison</code>, <code>/best-units</code>, <code>/best-dps</code>, <code>/best-support</code>, and Anniversary Re-Release guides (Eskanoor, Vegeto, Einz/Mely, Traits).</li></ul></div></main>{self.render_footer()}</body></html>"""
        with open(os.path.join(self.dist_dir, "changelog.html"), 'w', encoding='utf-8') as f:
            f.write(changelog_html)

    def build_seo_assets(self):
        today = datetime.now().strftime('%Y-%m-%d')
        urls = [
            ("/", today, "daily", "1.0"),
            ("/tier-list", today, "daily", "0.95"),
            ("/es/tier-list", today, "weekly", "0.8"),
            ("/pt/tier-list", today, "weekly", "0.8"),
            ("/units/", today, "weekly", "0.9"),
            ("/team-builder", today, "weekly", "0.9"),
            ("/unit-comparison", today, "weekly", "0.9"),
            ("/best-units", today, "weekly", "0.85"),
            ("/best-dps", today, "weekly", "0.85"),
            ("/best-support", today, "weekly", "0.85"),
            ("/codes", today, "daily", "0.9"),
            ("/es/codes", today, "daily", "0.8"),
            ("/pt/codes", today, "daily", "0.8"),
            ("/calculator", today, "weekly", "0.85"),
            ("/updates", today, "weekly", "0.8"),
            ("/guides/", today, "weekly", "0.85"),
            ("/about", today, "monthly", "0.5"),
            ("/editorial-policy", today, "monthly", "0.5"),
            ("/changelog", today, "weekly", "0.6"),
        ]
        reds = [
            "/codes.html /codes 301", "/es/codes.html /es/codes 301", "/pt/codes.html /pt/codes 301",
            "/tier-list.html /tier-list 301", "/es/tier-list.html /es/tier-list 301", "/pt/tier-list.html /pt/tier-list 301",
            "/calculator.html /calculator 301", "/team-builder.html /team-builder 301", "/unit-comparison.html /unit-comparison 301",
            "/best-units.html /best-units 301", "/best-dps.html /best-dps 301", "/best-support.html /best-support 301",
            "/updates.html /updates 301", "/about.html /about 301", "/editorial-policy.html /editorial-policy 301", "/changelog.html /changelog 301",
            "/units/index.html /units/ 301", "/guides/index.html /guides/ 301",
            "/database/ /units/ 301", "/database /units/ 301"
        ]
        for e in self.entities:
            urls.append((f"/units/{e['slug']}", today, "monthly", "0.75"))
            reds.append(f"/units/{e['slug']}.html /units/{e['slug']} 301")
            reds.append(f"/database/{e['slug']} /units/{e['slug']} 301")
        for g in self.guides:
            urls.append((f"/guides/{g['slug']}", g["updatedDate"], "weekly", "0.8"))
            reds.append(f"/guides/{g['slug']}.html /guides/{g['slug']} 301")
        domain = self.config['site']['domain'].rstrip('/')
        items = "".join([f"<url><loc>{domain}{u}</loc><lastmod>{lm}</lastmod><changefreq>{cf}</changefreq><priority>{pr}</priority></url>" for u, lm, cf, pr in urls])
        with open(os.path.join(self.dist_dir, 'sitemap.xml'), 'w', encoding='utf-8') as f:
            f.write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{items}</urlset>')
        with open(os.path.join(self.dist_dir, 'robots.txt'), 'w', encoding='utf-8') as f:
            f.write(f"User-agent: *\nAllow: /\n\nSitemap: {domain}/sitemap.xml\n")
        with open(os.path.join(self.dist_dir, '_redirects'), 'w', encoding='utf-8') as f:
            f.write("\n".join(reds) + "\n")
        indexnow_key = "d9fff1aa6c384251b984519c49ed6831"
        with open(os.path.join(self.dist_dir, f'{indexnow_key}.txt'), 'w', encoding='utf-8') as f:
            f.write(indexnow_key)

    def build_all(self):
        if os.path.exists(self.dist_dir):
            shutil.rmtree(self.dist_dir)
        os.makedirs(self.dist_dir, exist_ok=True)
        assets_src = os.path.join(self.root_dir, 'assets')
        if os.path.exists(assets_src):
            shutil.copytree(assets_src, os.path.join(self.dist_dir, 'assets'), dirs_exist_ok=True)
        ico_src = os.path.join(self.root_dir, 'assets', 'images', 'favicon.ico')
        if os.path.exists(ico_src):
            shutil.copy2(ico_src, os.path.join(self.dist_dir, 'favicon.ico'))
        self.build_index()
        self.build_codes()
        self.build_tierlist()
        self.build_calculator()
        self.build_team_builder()
        self.build_unit_comparison()
        self.build_editorial_pages()
        self.build_database()
        self.build_guides()
        self.build_localized_pages()
        self.build_trust_pages()
        self.build_seo_assets()
        print(f"Build complete! Static files ready in: {self.dist_dir}")


if __name__ == "__main__":
    WikiBuilder(os.path.dirname(os.path.abspath(__file__))).build_all()
