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
        self.guides = self.load_json('data/guides.json')

    def load_json(self, rel_path):
        path = os.path.join(self.root_dir, rel_path)
        if not os.path.exists(path):
            return {} if rel_path.endswith('config.json') else []
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
        .rarity-Secret { background: rgba(244, 63, 94, 0.2); color: #fb7185; border: 1px solid rgba(244, 63, 94, 0.45); }
        .rarity-Crusader { background: rgba(56, 189, 248, 0.2); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.45); }
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
        .ad-slot { width: 100%; min-height: 90px; margin: 1.25rem 0 1.75rem; padding: 0.65rem; border: 1px solid var(--border); border-radius: 0.65rem; background: rgba(15, 23, 42, 0.45); text-align: center; overflow: hidden; }
        .ad-label { display: block; margin-bottom: 0.35rem; color: var(--text-muted); font-size: 0.68rem; line-height: 1.2; letter-spacing: 0.08em; text-transform: uppercase; }
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

    def render_native_banner(self, page_key):
        """Render one native banner slot on selected high-intent pages."""
        ads = self.config.get("ads", {})
        if not ads.get("enabled", False) or not ads.get("nativeBanner", False):
            return ""
        if page_key not in ads.get("nativeBannerPages", []):
            return ""
        return """
        <aside class="ad-slot" aria-label="Advertisement">
            <span class="ad-label">Advertisement</span>
            <div id="container-6685037f30de53de5bf208c3aedfb0d4"></div>
            <script async="async" data-cfasync="false" src="https://bauval.org/21/6685037f30de53de5bf208c3aedfb0d4"></script>
        </aside>
        """

    def render_global_ad_scripts(self):
        """Load optional site-wide ad formats only when enabled in config.json."""
        ads = self.config.get("ads", {})
        if not ads.get("enabled", False):
            return ""
        scripts = []
        if ads.get("popunder", False):
            scripts.append('<script data-cfasync="false" src="https://abscloud.org/1/73061a6afb03c8d0cfb09a2c91442a31"></script>')
        if ads.get("socialBar", False):
            scripts.append('<script data-cfasync="false" src="https://bauval.org/14/c9a84dddc3cd2c4192c9eb8c0f9f4193"></script>')
        return "\n".join(scripts)

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
            const orig = btn.innerText;
            const done = (ok) => {{
                btn.innerText = ok ? "COPIED!" : "COPY FAILED";
                btn.style.background = ok ? "#34d399" : "#ef4444";
                setTimeout(() => {{ btn.innerText = orig; btn.style.background = ""; }}, 1800);
            }};
            if (navigator.clipboard && navigator.clipboard.writeText) {{
                navigator.clipboard.writeText(code).then(() => done(true)).catch(() => {{
                    try {{
                        const ta = document.createElement('textarea');
                        ta.value = code;
                        document.body.appendChild(ta);
                        ta.select();
                        const ok = document.execCommand('copy');
                        document.body.removeChild(ta);
                        done(ok);
                    }} catch (e) {{ done(false); }}
                }});
            }} else {{
                done(false);
            }}
        }}
        </script>
        {self.render_global_ad_scripts()}
        """

    def render_schema_breadcrumbs(self, items):
        domain = self.config['site']['domain'].rstrip('/')
        elements = [{"@type": "ListItem", "position": idx, "name": name, "item": f"{domain}{path}"} for idx, (name, path) in enumerate(items, 1)]
        return f'<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": elements})}</script>'

    def render_schema_article(self, headline, description, path, date_modified=None, schema_type="WebPage"):
        """Render page metadata without inventing a publication date."""
        domain = self.config['site']['domain'].rstrip('/')
        data = {
            "@context": "https://schema.org", "@type": schema_type,
            "name" if schema_type == "WebPage" else "headline": headline,
            "description": description,
            "image": [f"{domain}/assets/images/favicon-192x192.png"],
            "mainEntityOfPage": {"@type": "WebPage", "@id": f"{domain}{path}"},
            "author": {"@type": "Organization", "name": "RBXMeta", "url": domain},
            "publisher": {"@type": "Organization", "name": "RBXMeta", "logo": {"@type": "ImageObject", "url": f"{domain}/assets/images/favicon-192x192.png"}}
        }
        if date_modified:
            data["dateModified"] = date_modified
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
            <p style="color:var(--text-muted);margin-bottom:1rem;">Choose one banner at a time. Gems are applied only to the selected pity counter; this tool does not assume Mythic and Secret counters share progress.</p>
            <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:1rem;">
                <div class="calc-input-group"><label class="calc-label" for="acx-banner">Banner:</label><select id="acx-banner" class="calc-select"><option value="mythic">Mythic (200 pity)</option><option value="secret">Secret / Crusader (2,000 pity)</option></select></div>
                <div class="calc-input-group"><label class="calc-label" for="acx-pity-current">Current pulls toward selected pity:</label><input type="number" id="acx-pity-current" class="calc-input" value="40" min="0" step="1"></div>
                <div class="calc-input-group"><label class="calc-label" for="acx-gems">Current Gems:</label><input type="number" id="acx-gems" class="calc-input" value="5000" min="0" step="1"></div>
                <div class="calc-input-group"><label class="calc-label" for="acx-cost">Gems per summon:</label><select id="acx-cost" class="calc-select"><option value="50">50 Gems (single summon)</option><option value="500">500 Gems (10x summon)</option></select></div>
            </div>
            <button class="calc-btn" style="margin-top:1rem;" onclick="calcAcxPity()">Calculate selected banner</button>
            <div id="acx-pity-res" class="calc-result" style="display:none;" aria-live="polite"></div>
        </div>
        <script>
        function calcAcxPity() {
            const banner = document.getElementById('acx-banner').value;
            const currentRaw = document.getElementById('acx-pity-current').value;
            const gemsRaw = document.getElementById('acx-gems').value;
            const current = Number(currentRaw);
            const gems = Number(gemsRaw);
            const perPull = Number(document.getElementById('acx-cost').value);
            const el = document.getElementById('acx-pity-res');
            if (currentRaw === '' || gemsRaw === '' || !Number.isInteger(current) || !Number.isInteger(gems) || current < 0 || gems < 0) {
                el.style.display = 'block';
                el.textContent = 'Enter non-negative whole numbers for current pulls and Gems.';
                return;
            }
            const threshold = banner === 'mythic' ? 200 : 2000;
            const rate = banner === 'mythic' ? 0.005 : 0.0005;
            if (current > threshold) {
                el.style.display = 'block';
                el.textContent = 'Current pulls cannot exceed the selected pity threshold (' + threshold.toLocaleString() + ').';
                return;
            }
            const pullsFromGems = Math.floor(gems / perPull);
            const remaining = Math.max(0, threshold - current);
            const pullsToPityAfterGems = Math.max(0, remaining - pullsFromGems);
            const rawChance = pullsFromGems === 0 ? 0 : (1 - Math.pow(1 - rate, pullsFromGems)) * 100;
            el.style.display = 'block';
            el.innerHTML = '<div><strong>Selected banner:</strong> ' + (banner === 'mythic' ? 'Mythic' : 'Secret / Crusader') + '</div>' +
                '<div><strong>Summons from Gems:</strong> ' + pullsFromGems.toLocaleString() + ' (' + (pullsFromGems * perPull).toLocaleString() + ' Gems used)</div>' +
                '<div><strong>Pulls remaining before this budget:</strong> ' + remaining.toLocaleString() + '</div>' +
                '<div><strong>Pulls still needed after this budget to reach listed pity:</strong> ' + pullsToPityAfterGems.toLocaleString() + (pullsToPityAfterGems === 0 ? (remaining === 0 ? ' — current counter is already at the listed threshold.' : ' — listed pity is reached within this Gem budget.') : '') + '</div>' +
                '<div><strong>Raw-rate chance over these summons:</strong> ' + rawChance.toFixed(2) + '%</div>' +
                '<p style="color:var(--text-muted);margin-top:.6rem;font-size:.85rem;">Raw-rate chance assumes independent rolls at a constant listed rate and excludes any pity-rate changes. Pity thresholds and rates must be checked against the current in-game banner.</p>';
        }
        </script>
        """

    def render_head_meta(self, title, description, path="/", robots="index, follow, max-image-preview:large"):
        domain = self.config['site']['domain'].rstrip('/')
        canonical = f"{domain}{path}"
        og_img = f"{domain}/assets/images/favicon-192x192.png"
        return f"""
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title}</title>
            <meta name="description" content="{description}">
            <meta name="robots" content="{robots}">
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
        confirmed_codes = [c for c in self.codes if c["status"] == "Active" and "Unverified" not in c.get("verification", "")]
        unverified_codes = [c for c in self.codes if c["status"] == "Active" and "Unverified" in c.get("verification", "")]
        codes_html = "".join([f'<div class="code-row"><div><span class="code-val">{c["code"]}</span><span class="code-reward">({c["reward"]})</span></div><button class="btn-copy" onclick="copyCode(this, \'{c["code"]}\')">COPY CODE</button></div>' for c in confirmed_codes[:3]])
        hill_units = [e for e in self.entities if "hill" in e["type"].lower()]
        tier_html = ""
        for tk in ["S+", "S", "A"]:
            t_items = [x for x in hill_units if x["tier"] == tk]
            if not t_items:
                continue
            pills = "".join([f'<a href="/units/{x["slug"]}" class="tier-item-pill"><div style="display:flex;justify-content:space-between;"><strong>{x["name"]}</strong><span class="rarity-badge rarity-{x["rarity"]}">{x["rarity"]}</span></div><p style="color:var(--text-muted);font-size:0.86rem;margin-top:0.25rem;">{x["description"][:110]}...</p></a>' for x in t_items])
            tier_html += f'<div class="tier-row"><div class="tier-label tier-{tk.replace("+", "-plus")}">{tk}</div><div class="tier-items">{pills}</div></div>'

        db_html = "".join([f'<a href="/units/{e["slug"]}" class="entity-card"><div><div style="display:flex;justify-content:space-between;margin-bottom:0.6rem;"><div><h3 style="font-size:1.1rem;font-weight:800;color:#fff;">{e["name"]}</h3><span style="font-size:0.78rem;color:var(--text-muted);">{e["type"]} • Tier {e["tier"]}</span></div><span class="rarity-badge rarity-{e["rarity"]}">{e["rarity"]}</span></div><p style="color:var(--text-muted);font-size:0.88rem;">{e["description"]}</p></div><div style="margin-top:0.85rem;color:var(--accent);font-weight:700;font-size:0.86rem;">Unit Stats →</div></a>' for e in self.entities[:6]])
        guides_html = "".join([f'<a href="/guides/{g["slug"]}" class="tier-item-pill"><span class="badge-verified" style="margin-bottom:0.4rem;">{g["category"]}</span><h3 style="font-size:1.05rem;font-weight:800;color:#fff;margin-bottom:0.25rem;">{g["title"]}</h3><p style="color:var(--text-muted);font-size:0.86rem;">{g["excerpt"]}</p></a>' for g in self.guides])
        domain = self.config['site']['domain'].rstrip('/')
        ws_schema = {"@context": "https://schema.org", "@type": "WebSite", "name": "RBXMeta — Anime Crusaders X Tools & Wiki", "url": f"{domain}/", "potentialAction": {"@type": "SearchAction", "target": f"{domain}/units/?q={{search_term_string}}", "query-input": "required name=search_term_string"}}

        html = f"""<!DOCTYPE html><html lang="en"><head>{self.render_head_meta(self.config['site']['title'], self.config['site']['description'], "/")}{self.get_base_css()}<script type="application/ld+json">{json.dumps(ws_schema)}</script>{self.render_schema_article("Anime Crusaders X Tools, Tier List & Wiki", self.config['site']['description'], "/")}{self.render_schema_faq(self.config['faqs'])}</head><body>{self.render_nav("home")}
        <header class="hero"><div class="container"><div class="badge-verified">⚡ ANNIVERSARY RE-RELEASE • VERIFIED {datetime.now().strftime('%Y-%m-%d')}</div><h1>Anime Crusaders X Tier List, Tools &amp; Wiki</h1><p>Welcome to the ultimate Anime Crusaders X resource hub! Discover the latest tier list, explore detailed unit stats, compare characters, and build powerful teams with our free tools.</p><div style="display:flex;justify-content:center;gap:0.85rem;flex-wrap:wrap;"><a href="/tier-list" class="btn-copy" style="padding:0.75rem 1.4rem;">Tier List</a><a href="/team-builder" class="tab-btn">Team Builder</a><a href="/unit-comparison" class="tab-btn">Unit Comparison</a><a href="/units/" class="tab-btn">Units ({len(self.entities)})</a><a href="/codes" class="tab-btn">Codes ({len(confirmed_codes)}+{len(unverified_codes)})</a></div><div class="hero-stats"><div class="hero-stat-box"><div class="hero-stat-num">{len(confirmed_codes)} Confirmed</div><div class="hero-stat-label">+{len(unverified_codes)} Unverified Code</div></div><div class="hero-stat-box"><div class="hero-stat-num">{len(self.entities)}</div><div class="hero-stat-label">Featured Units</div></div><div class="hero-stat-box"><div class="hero-stat-num">4</div><div class="hero-stat-label">Interactive Tools</div></div></div></div></header>
        <main class="container main-layout">
            <section class="card"><div class="card-header"><h2 class="card-title">🧰 Anime Crusaders X Core Interactive Tools</h2></div><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:1rem;"><a href="/tier-list" class="tier-item-pill"><strong>🏆 Tier List</strong><p style="color:var(--text-muted);font-size:0.86rem;">Searchable S+ to A rankings by Hill, Ground, Hybrid &amp; Support.</p></a><a href="/team-builder" class="tier-item-pill"><strong>🛡️ Team Builder</strong><p style="color:var(--text-muted);font-size:0.86rem;">Assemble a 6-unit lineup and check role &amp; support coverage.</p></a><a href="/unit-comparison" class="tier-item-pill"><strong>⚖️ Unit Comparison</strong><p style="color:var(--text-muted);font-size:0.86rem;">Compare two units side-by-side by role, tier &amp; synergies.</p></a><a href="/best-units" class="tier-item-pill"><strong>⭐ Best Units Guide</strong><p style="color:var(--text-muted);font-size:0.86rem;">Upgrade priority, Best DPS, and Best Support picks.</p></a></div></section>
            {self.render_native_banner("home")}
            <section class="card"><div class="card-header"><h2 class="card-title">🎲 Anime Crusaders X Gem &amp; Pity Calculator</h2><a href="/calculator" style="color:var(--accent);font-weight:700;">Full Calculator →</a></div>{self.render_pity_calculator()}</section>
            <section class="card"><div class="card-header"><h2 class="card-title">🎁 Anime Crusaders X Active Codes (32x Group + Lobby Circle)</h2><a href="/codes" style="color:var(--accent);font-weight:700;">All Codes →</a></div>{codes_html}</section>
            <section class="card"><div class="card-header"><h2 class="card-title">🏆 Anime Crusaders X Tier List (Hill &amp; Hybrid)</h2><a href="/tier-list" style="color:var(--accent);font-weight:700;">Filter Full Tier List →</a></div>{tier_html}</section>
            <section class="card"><div class="card-header"><h2 class="card-title">🔥 Anime Crusaders X Evolution, Fusion &amp; Trait Guides</h2><a href="/guides/" style="color:var(--accent);font-weight:700;">All Guides ({len(self.guides)}) →</a></div><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:1rem;">{guides_html}</div></section>
            <section class="card"><div class="card-header"><h2 class="card-title">📚 Anime Crusaders X Units Database</h2><a href="/units/" style="color:var(--accent);font-weight:700;">Browse All ({len(self.entities)}) →</a></div><div class="entity-grid">{db_html}</div></section>
            <section class="card">
                <div class="card-header"><h2 class="card-title">📖 How the Anime Crusaders X Tier List &amp; Meta Work</h2></div>
                <p style="color:#cbd5e1;margin-bottom:1rem;">In <strong>Anime Crusaders X</strong> (also searched as <em>Anime Crusader X</em>), building a winning squad requires balancing four distinct placement and role categories rather than simply stacking high-rarity pulls. Our tier list evaluates every unit across Story, Progressive, Boss, and Infinite waves using multi-source consensus data, evolution scaling, and team synergy.</p>
                <h3 style="color:#38bdf8;font-size:1.1rem;margin:1rem 0 0.4rem;">1. Hill &amp; Hybrid DPS Units</h3>
                <p style="color:var(--text-muted);margin-bottom:0.85rem;">Hill and Hybrid units provide elevated sightlines and flexible tile coverage across tight corners and multi-lane maps. Current S+ tier staples such as <strong>Goju vs Sukuno (Heian)</strong>, <strong>Gilgamesh (The Golden King)</strong>, and <strong>Barusu (From Zero)</strong> anchor late-game Infinite runs because they maintain consistent uptime even on crowded maps, while <strong>Ishtall</strong>, <strong>Einz (Sorcerer King)</strong>, and <strong>Eskanoor (The One)</strong> deliver high burst damage once evolved.</p>
                <h3 style="color:#38bdf8;font-size:1.1rem;margin:1rem 0 0.4rem;">2. Ground Lane Carries</h3>
                <p style="color:var(--text-muted);margin-bottom:0.85rem;">Ground DPS units lock down primary enemy paths and absorb early-wave pressure. <strong>Mely (Assault)</strong> and <strong>Higuru (Judgement)</strong> lead the Ground meta thanks to strong damage scaling and wave-clear reliability, backed by <strong>Spear (Vigorous Warrior)</strong>, <strong>Powaa (Blood Queen)</strong>, and <strong>Excalibur (King of Blades)</strong>. Mid-game players progressing through Story chapters can also rely on <strong>Sun Woo (System)</strong>, <strong>Ant King</strong>, and <strong>Ryoma</strong>.</p>
                <h3 style="color:#38bdf8;font-size:1.1rem;margin:1rem 0 0.4rem;">3. Support, Economy &amp; Crowd Control</h3>
                <p style="color:var(--text-muted);margin-bottom:0.85rem;">No Infinite mode team survives past wave 50 without dedicated Support units. <strong>Kurimi (Time Queen)</strong> provides crucial time-manipulation and crowd control, <strong>AI (Idol)</strong> amplifies team-wide DPS, and <strong>Zero (True Emperor)</strong> offers tactical utility. Use our <a href="/team-builder" style="color:var(--accent);">Team Builder</a> to verify that your 6-slot lineup covers Hill/Hybrid, Ground, and Support roles before spending Trait Remnants.</p>
                <h3 style="color:#38bdf8;font-size:1.1rem;margin:1rem 0 0.4rem;">4. Pity Math, Trait Rerolls &amp; Upgrade Priority</h3>
                <p style="color:var(--text-muted);">Before rolling banners, always check the <strong>Gem &amp; Pity Calculator</strong> above: Mythic units guarantee at <strong>200 pulls</strong> (0.5% base rate, 10,000 Gems at 50 Gems per pull) and Secret / Crusader units guarantee at <strong>2,000 pulls</strong> (0.05% base rate). Once you secure an S+ or S tier carry, redeem active <a href="/codes" style="color:var(--accent);">Anime Crusaders X Codes</a> for Trait Remnants and aim for Damage, Range, or Cooldown Reduction traits on DPS units and Range or Cost Reduction on Supports.</p>
            </section>
            <section class="card"><div class="card-header"><h2 class="card-title">❓ Anime Crusaders X Frequently Asked Questions</h2></div>{''.join([f'<div style="margin-bottom:1.25rem;"><h3 style="color:#38bdf8;font-size:1.05rem;">{f["question"]}</h3><p style="color:var(--text-muted);">{f["answer"]}</p></div>' for f in self.config['faqs']])}</section>
        </main>{self.render_footer()}</body></html>"""
        with open(os.path.join(self.dist_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(html)

    def build_codes(self):
        active = [c for c in self.codes if c.get("status", "").lower() == "active"]
        confirmed = [c for c in active if "unverified" not in c.get("verification", "").lower()]
        unverified = [c for c in active if "unverified" in c.get("verification", "").lower()]

        def render_code(c, is_unverified=False):
            v_status = c.get("verification", "Verification pending")
            v_color = "#fbbf24" if is_unverified else "#34d399"
            warning = '<p style="color:#fbbf24;font-size:.85rem;margin-top:.4rem;">Reports conflict; redemption is not confirmed. Try at your own discretion.</p>' if is_unverified else ""
            return f"""<div class="code-row" style="flex-direction:column;align-items:stretch;gap:.6rem;">
                <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:.5rem;">
                    <div><span class="code-val">{c['code']}</span><span class="code-reward">({c['reward']})</span>
                    <span style="display:inline-block;margin-left:.5rem;font-size:.74rem;font-weight:800;padding:.15rem .5rem;border-radius:.35rem;border:1px solid {v_color};color:{v_color};">{v_status}</span></div>
                    <button class="btn-copy" onclick="copyCode(this, '{c['code']}')">COPY CODE</button>
                </div>
                <div style="font-size:.82rem;color:var(--text-muted);display:flex;gap:1rem;flex-wrap:wrap;">
                    <span><strong>Level Req:</strong> {c.get('levelReq', 'Not specified')}</span>
                    <span><strong>First Seen:</strong> {c.get('firstSeen', c.get('addedDate', ''))}</span>
                    <span><strong>Last Checked:</strong> {c.get('lastVerified', 'Not recorded')}</span>
                    <span><strong>Source:</strong> {c.get('method', c.get('source', 'Community'))}</span>
                </div>{warning}
            </div>"""

        rows = "".join(render_code(c) for c in confirmed)
        unverified_rows = "".join(render_code(c, True) for c in unverified)
        html = f"""<!DOCTYPE html><html lang="en"><head>{self.render_head_meta(f"{self.config['site']['name']} Codes | Confirmed & Reported Codes", f"Anime Crusaders X codes separated by cross-source confirmed and unverified reports, with requirements and sources.", "/codes")}{self.render_hreflang("codes")}{self.get_base_css()}{self.render_schema_breadcrumbs([("Home", "/"), ("Codes", "/codes")])}</head><body>{self.render_nav("codes")}
        <main class="container main-layout"><div class="breadcrumbs"><a href="/">Home</a> <span>/</span> <span>Codes</span></div><div class="card">{self.render_lang_switcher("codes", "en")}<div class="badge-verified" style="margin-bottom:.75rem;">CODE STATUS • UPDATED {datetime.now().strftime('%Y-%m-%d')}</div><h1 style="font-size:2.2rem;font-weight:900;margin-bottom:.75rem;">{self.config['site']['name']} Codes</h1><p style="color:var(--text-muted);margin-bottom:1.5rem;">Confirmed codes are listed separately from codes with mixed or unverified reports. Cross-source confirmation does not mean we personally redeemed the code in-game.</p><h2 style="font-size:1.3rem;margin:1rem 0;">Cross-source Confirmed ({len(confirmed)})</h2>{rows or '<p>No confirmed active codes are currently listed.</p>'}{'<h2 style="font-size:1.3rem;margin:2rem 0 1rem;color:#fbbf24;">Reported — Unverified (' + str(len(unverified)) + ')</h2>' + unverified_rows if unverified else ''}{self.render_native_banner("codes")}<div style="margin-top:2rem;padding-top:1.5rem;border-top:1px solid var(--border);"><h2 style="font-size:1.3rem;margin-bottom:.75rem;">How to Redeem Codes in {self.config['site']['name']}</h2><ol style="margin-left:1.5rem;color:#cbd5e1;line-height:1.9;"><li>Join the official <strong>32x</strong> Roblox group and favorite the game.</li><li>Launch <strong>{self.config['site']['name']}</strong> and enter the green <strong>Codes</strong> circle in the lobby.</li><li>Paste a code and click <strong>Redeem</strong>. Check any level requirements shown above.</li></ol></div></div></main>{self.render_footer()}</body></html>"""
        with open(os.path.join(self.dist_dir, 'codes.html'), 'w', encoding='utf-8') as f:
            f.write(html)

    def build_tierlist(self):
        groups = [
            ("Hill_Hybrid", "Hill &amp; Hybrid", "Top Hill & Hybrid units for Progressive and Infinite modes in Anime Crusaders X.", [e for e in self.entities if "hill" in e["type"].lower()]),
            ("Ground", "Ground", "Best Ground lane-control DPS units in Anime Crusaders X.", [e for e in self.entities if e["type"].lower() == "ground"]),
            ("Support", "Support", "Essential Support units for buffs, economy, and crowd control.", [e for e in self.entities if "support" in e["type"].lower()]),
            ("Hero", "Hero Slot", "Dedicated Hero-slot units (do not occupy standard 6-unit deployment slots).", [e for e in self.entities if "hero" in e["type"].lower()]),
        ]
        panels = ""
        for idx, (cid, label, desc, items) in enumerate(groups):
            disp = "block" if idx == 0 else "none"
            trows, tbl = "", ""
            for tk in ["S+", "S", "A"]:
                t_items = [x for x in items if x["tier"] == tk]
                if not t_items:
                    continue
                pills = "".join([f'<a href="/units/{x["slug"]}" class="tier-item-pill"><div style="display:flex;justify-content:space-between;"><strong>{x["name"]}</strong><span class="rarity-badge rarity-{x["rarity"]}">{x["rarity"]}</span></div><p style="color:var(--text-muted);font-size:0.88rem;margin-top:0.25rem;">{x["description"][:115]}...</p></a>' for x in t_items])
                trows += f'<div class="tier-row"><div class="tier-label tier-{tk.replace("+", "-plus")}">{tk}</div><div class="tier-items">{pills}</div></div>'
                for x in t_items:
                    tbl += f'<tr><td><strong>{tk}</strong></td><td><a href="/units/{x["slug"]}" style="color:var(--accent);font-weight:700;">{x["name"]}</a></td><td>{x["rarity"]}</td><td>{x.get("role", "DPS")}</td><td>{x.get("gameMode", "Progressive & Infinite")}</td><td>{x.get("traits", "Damage / Range")}</td><td>{x["description"][:95]}...</td></tr>'
            panels += f'<section class="tier-category-panel" id="panel-{cid}" style="display:{disp};"><h2 style="font-size:1.4rem;margin-bottom:0.4rem;">{label} Tier List</h2><p style="color:var(--text-muted);margin-bottom:1.25rem;">{desc}</p>{trows}<table class="stats-table"><thead><tr><th>Tier</th><th>Unit</th><th>Rarity</th><th>Role</th><th>Best Mode</th><th>Traits</th><th>Meta Notes</th></tr></thead><tbody>{tbl}</tbody></table></section>'

        html = f"""<!DOCTYPE html><html lang="en"><head>{self.render_head_meta(f"{self.config['site']['name']} Tier List | Best Units Ranked", f"Searchable {self.config['site']['name']} (Anime Crusader X) unit tier list across Hill, Ground, Hybrid, Support & Hero Slot for Infinite and Story modes.", "/tier-list")}{self.get_base_css()}{self.render_schema_breadcrumbs([("Home", "/"), ("Tier List", "/tier-list")])}{self.render_schema_article(f"{self.config['site']['name']} Tier List", "Complete unit rankings across Hill, Ground, Hybrid, Support, and Hero Slot.", "/tier-list")}</head><body>{self.render_nav("tierlist")}
        <main class="container main-layout"><div class="breadcrumbs"><a href="/">Home</a> <span>/</span> <span>Tier List</span></div><div class="card"><div class="badge-verified" style="margin-bottom:0.75rem;">✓ LAST UPDATED: {datetime.now().strftime('%Y-%m-%d')} • UNIFIED ROSTER DATA</div><h1 style="font-size:2.2rem;font-weight:900;margin-bottom:0.5rem;">{self.config['site']['name']} Tier List</h1><p style="color:var(--text-muted);margin-bottom:1.25rem;">Filterable rankings across Hill/Hybrid, Ground, Support, and Dedicated Hero Slot (also known as Anime Crusader X Tier List). Powered by the same unified unit database.</p><input type="text" id="tl-search" class="search-input" placeholder="🔍 Search Goju, Gilgamesh, Eskanoor, Kurimi, Mely..." oninput="filterTierList()"><div class="tab-bar"><button class="tab-btn active" onclick="switchCategory('Hill_Hybrid')">Hill &amp; Hybrid</button><button class="tab-btn" onclick="switchCategory('Ground')">Ground</button><button class="tab-btn" onclick="switchCategory('Support')">Support</button><button class="tab-btn" onclick="switchCategory('Hero')">Hero Slot</button></div>{panels}{self.render_native_banner("tier-list")}<div style="margin-top:2rem;padding-top:1.5rem;border-top:1px solid var(--border);"><h2 style="font-size:1.3rem;margin-bottom:0.85rem;">🎲 Gem &amp; Pity Calculator</h2>{self.render_pity_calculator()}</div></div></main>{self.render_footer()}<script>function switchCategory(c){{document.querySelectorAll('.tab-btn').forEach(b=>b.classList.toggle('active',b.getAttribute('onclick').includes(c)));document.querySelectorAll('.tier-category-panel').forEach(p=>p.style.display=(p.id==='panel-'+c)?'block':'none');}}function filterTierList(){{const q=(document.getElementById('tl-search').value||'').toLowerCase();document.querySelectorAll('.tier-item-pill').forEach(el=>{{el.style.display=(!q||el.innerText.toLowerCase().includes(q))?'block':'none';}});document.querySelectorAll('.tier-category-panel table tbody tr').forEach(tr=>{{tr.style.display=(!q||tr.innerText.toLowerCase().includes(q))?'':'none';}});}}</script></body></html>"""
        with open(os.path.join(self.dist_dir, 'tier-list.html'), 'w', encoding='utf-8') as f:
            f.write(html)

    def build_calculator(self):
        schema = {"@context": "https://schema.org", "@type": "SoftwareApplication", "name": f"{self.config['site']['name']} Summon & Trait Odds Calculator", "operatingSystem": "Web", "applicationCategory": "GameApplication", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}
        html = f"""<!DOCTYPE html><html lang="en"><head>{self.render_head_meta(f"{self.config['site']['name']} Gem, Pity & Trait Calculator", "Calculate Mythic (200) & Secret (2,000) pity requirements and Trait Remnant reroll probabilities in Anime Crusaders X.", "/calculator")}{self.get_base_css()}{self.render_schema_breadcrumbs([("Home", "/"), ("Calculator", "/calculator")])}<script type="application/ld+json">{json.dumps(schema)}</script></head><body>{self.render_nav("calc")}
        <main class="container main-layout"><div class="breadcrumbs"><a href="/">Home</a> <span>/</span> <span>Calculator</span></div><div class="card"><h1 style="font-size:2.2rem;font-weight:900;margin-bottom:0.5rem;">{self.config['site']['name']} Gem, Pity &amp; Evolution Calculator</h1><p style="color:var(--text-muted);margin-bottom:1.5rem;">Calculate Mythic (200) &amp; Secret/Crusader (2,000) pity requirements, Trait Remnant reroll odds using real 12-Trait probabilities, and Evolution material deficits.</p>{self.render_pity_calculator()}{self.render_native_banner("calculator")}<h2 style="font-size:1.35rem;margin:2rem 0 1rem;color:#38bdf8;">Trait Remnant Reroll Odds Calculator</h2><div class="calc-box"><div class="calc-input-group"><label class="calc-label">Select Target Trait (Auto-fills Drop Rate):</label><select id="trait-preset" class="calc-select" onchange="document.getElementById('rate').value=this.value"><option value="0.1">Crusader (0.1% — +300% DMG, -10% CD, +10% Range)</option><option value="0.15">Biohazard (0.15% — +85% Toxic DMG/54s)</option><option value="0.2">Radiant (0.2% — +27.5% DMG, -15% CD, +15% Range)</option><option value="0.36">Aurora (0.36% — +10% DMG, +20% True DMG, +25% Range)</option><option value="0.8">Eclipse (0.8% — +22.5% DMG, +25% Boss DMG)</option><option value="1.5">Overdrive (1.5% — -20% Cooldown)</option><option value="2.5">Hawkeye (2.5% — +30% Range)</option><option value="5.0">Gilded (5.0% — -10% Cost, +20% Yen)</option><option value="9.99">Tactician (9.99% — +50% XP)</option><option value="24.8">Focus / Agile (24.8% — Range / Cooldown)</option><option value="29.8">Fierce (29.8% — +10% to +15% DMG)</option></select></div><div class="calc-input-group"><label class="calc-label">Total Pulls / Trait Remnants (e.g. 100):</label><input type="number" id="pulls" class="calc-input" value="100" min="1" max="5000"></div><div class="calc-input-group"><label class="calc-label">Target Drop Rate (%):</label><input type="number" id="rate" class="calc-input" value="0.1" step="0.01" min="0.01" max="100"></div><button class="calc-btn" onclick="calcOdds()">Calculate Cumulative Odds</button><div id="res" class="calc-result" style="display:none;"></div><p style="color:var(--text-muted);font-size:0.82rem;margin-top:0.85rem;">Formula: <code>P = 1 - (1 - p)^n</code> (assumes independent, constant-rate rolls without trait pity; Hero units like Eskanoor use a separate Hero trait pool).</p></div><h2 style="font-size:1.35rem;margin:2rem 0 1rem;color:#34d399;">Evolution Material &amp; Cube Planner</h2><div class="calc-box"><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:1rem;"><div class="calc-input-group"><label class="calc-label">Required Cubes / Stones (e.g. 50):</label><input type="number" id="evo-req" class="calc-input" value="50" min="1" max="5000"></div><div class="calc-input-group"><label class="calc-label">Owned in Inventory (e.g. 15):</label><input type="number" id="evo-own" class="calc-input" value="15" min="0" max="5000"></div><div class="calc-input-group"><label class="calc-label">Avg Drop per Clear (e.g. 2):</label><input type="number" id="evo-drop" class="calc-input" value="2" min="1" max="100"></div></div><button class="calc-btn" style="background:#10b981;" onclick="calcEvo()">Calculate Remaining Runs</button><div id="evo-res" class="calc-result" style="display:none;border-color:#10b981;"></div><p style="color:var(--text-muted);font-size:0.82rem;margin-top:0.85rem;">Note: Enter your observed stage drop average from Challenges or Legend Stages.</p></div></div></main>{self.render_footer()}<script>function calcOdds(){{const n=Math.max(0,parseInt(document.getElementById('pulls').value)||0);const rRaw=parseFloat(document.getElementById('rate').value);const pct=isNaN(rRaw)?0:Math.max(0,Math.min(100,rRaw));const p=pct/100;const prob=(n===0||p===0)?'0.00':(p>=1?'100.00':((1-Math.pow(1-p,n))*100).toFixed(2));const el=document.getElementById('res');el.style.display='block';el.innerHTML='<strong>Chance after '+n+' rolls at '+pct+'%:</strong> <span style=\"color:var(--accent);font-size:1.25rem;font-weight:900;\">'+prob+'%</span>';}}function calcEvo(){{const req=Math.max(0,parseInt(document.getElementById('evo-req').value)||0);const own=Math.max(0,parseInt(document.getElementById('evo-own').value)||0);const drop=Math.max(0,parseFloat(document.getElementById('evo-drop').value)||0);const need=Math.max(0,req-own);const el=document.getElementById('evo-res');el.style.display='block';if(need===0){{el.innerHTML='<strong style=\"color:#34d399;\">You already have enough materials to evolve!</strong>';return;}}if(drop<=0){{el.innerHTML='<strong>Missing Materials:</strong> '+need+' • <span style=\"color:#fbbf24;\">Enter an average drop > 0 to estimate stage runs.</span>';return;}}const runs=Math.ceil(need/drop);el.innerHTML='<strong>Missing Materials:</strong> '+need+' • <strong>Estimated Clears Needed:</strong> <span style=\"color:#34d399;font-weight:900;\">'+runs+' runs</span>';}}</script></body></html>"""
        with open(os.path.join(self.dist_dir, 'calculator.html'), 'w', encoding='utf-8') as f:
            f.write(html)

    def build_team_builder(self):
        schema = {"@context": "https://schema.org", "@type": "SoftwareApplication", "name": f"{self.config['site']['name']} Team Builder", "operatingSystem": "Web", "applicationCategory": "GameApplication", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}
        standard_units = [e for e in self.entities if "hero" not in e["type"].lower()]
        hero_units = [e for e in self.entities if "hero" in e["type"].lower()]
        units_json = json.dumps([{"slug": e["slug"], "name": e["name"], "type": e["type"], "tier": e["tier"], "role": e.get("role", "Unknown")} for e in standard_units])
        hero_slugs_json = json.dumps([e["slug"] for e in hero_units])
        options_html = "".join([f'<option value="{e["slug"]}">[{e["tier"]}] {e["name"]} ({e["type"]})</option>' for e in standard_units])
        hero_options = "".join([f'<option value="{e["slug"]}">[{e["tier"]}] {e["name"]} ({e["type"]})</option>' for e in hero_units])
        slots_html = "".join([f'<div class="calc-input-group"><label class="calc-label" for="slot-{i}">Deployment Slot {i}:</label><select id="slot-{i}" class="calc-select" onchange="updateTeam()"><option value="">— Select Unit —</option>{options_html}</select></div>' for i in range(1, 7)])
        hero_html = f'<div class="calc-input-group" style="margin-top:1rem;"><label class="calc-label" for="hero-slot">Dedicated Hero Slot (separate from six deployment slots):</label><select id="hero-slot" class="calc-select" onchange="updateTeam()"><option value="">— No Hero selected —</option>{hero_options}</select></div>' if hero_units else ""
        html = f"""<!DOCTYPE html><html lang="en"><head>{self.render_head_meta(f"{self.config['site']['name']} Team Builder | Team Coverage Checker", "Build a six-unit Anime Crusaders X lineup and check Hill, Ground and Support coverage, with a separate Hero slot.", "/team-builder")}{self.get_base_css()}{self.render_schema_breadcrumbs([("Home", "/"), ("Team Builder", "/team-builder")])}<script type="application/ld+json">{json.dumps(schema)}</script></head><body>{self.render_nav("teambuilder")}
        <main class="container main-layout"><div class="breadcrumbs"><a href="/">Home</a> <span>/</span> <span>Team Builder</span></div><div class="card"><h1 style="font-size:2.2rem;font-weight:900;margin-bottom:.5rem;">{self.config['site']['name']} Team Coverage Checker</h1><p style="color:var(--text-muted);margin-bottom:1.5rem;">Choose up to six standard deployment units. This tool checks placement coverage and duplicate selections; it does not estimate damage, team strength, crowd control, or mode readiness.</p><div class="calc-box"><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:1rem;">{slots_html}</div>{hero_html}<div id="team-summary" class="calc-result" style="margin-top:1.25rem;" aria-live="polite">Select units to check coverage.</div></div></div></main>{self.render_footer()}
        <script>
        const units = {units_json};
        const unitMap = Object.fromEntries(units.map(u => [u.slug, u]));
        const heroSlugs = new Set({hero_slugs_json});
        function updateTeam() {{
            const chosen = [];
            for (let i = 1; i <= 6; i++) {{
                const v = document.getElementById('slot-' + i).value;
                if (v && unitMap[v]) chosen.push(unitMap[v]);
            }}
            const duplicates = chosen.map(u => u.slug).filter((slug, i, arr) => arr.indexOf(slug) !== i);
            const counts = {{ hill: 0, ground: 0, support: 0 }};
            chosen.forEach(u => {{
                const t = u.type.toLowerCase();
                if (t.includes('hill') || t.includes('hybrid')) counts.hill++;
                if (t.includes('ground')) counts.ground++;
                if (t.includes('support')) counts.support++;
            }});
            const heroSelect = document.getElementById('hero-slot');
            const heroLabel = heroSelect && heroSelect.value ? heroSelect.options[heroSelect.selectedIndex].text : 'None selected';
            const el = document.getElementById('team-summary');
            if (!chosen.length && (!heroSelect || !heroSelect.value)) {{ el.textContent = 'Select units to check coverage.'; return; }}
            const missing = [];
            if (!counts.hill) missing.push('Hill / Hybrid');
            if (!counts.ground) missing.push('Ground');
            if (!counts.support) missing.push('Support');
            const duplicateMessage = duplicates.length ? '<p style="color:#fbbf24;margin-top:.5rem;"><strong>Duplicate selection:</strong> ' + [...new Set(duplicates)].map(slug => unitMap[slug].name).join(', ') + '. Each slot currently counts as a separate selection; remove duplicates if unintended.</p>' : '';
            el.innerHTML = '<div><strong>Selected standard units:</strong> ' + chosen.length + '/6</div>' +
                '<div style="margin-top:.5rem;"><strong>Coverage:</strong> Hill / Hybrid ' + counts.hill + ' • Ground ' + counts.ground + ' • Support ' + counts.support + '</div>' +
                '<div style="margin-top:.5rem;"><strong>Dedicated Hero Slot:</strong> ' + heroLabel + '</div>' +
                '<div style="margin-top:.5rem;color:' + (missing.length ? '#fbbf24' : '#34d399') + ';">' + (missing.length ? 'No selected unit in: ' + missing.join(', ') + '.' : 'All three tracked placement categories are represented.') + '</div>' + duplicateMessage +
                '<p style="color:var(--text-muted);font-size:.85rem;margin-top:.6rem;">Coverage is based only on the placement labels in the current unit dataset. It is not a performance or Infinite-mode recommendation.</p>';
        }}
        const addSlug = new URLSearchParams(location.search).get('add');
        if (addSlug && heroSlugs.has(addSlug) && document.getElementById('hero-slot')) {{
            document.getElementById('hero-slot').value = addSlug;
            document.getElementById('slot-1').value = 'goju-vs-sukuno';
        }} else if (addSlug && unitMap[addSlug]) {{
            document.getElementById('slot-1').value = addSlug;
        }} else {{
            document.getElementById('slot-1').value = 'goju-vs-sukuno';
        }}
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
        html = f"""<!DOCTYPE html><html lang="en"><head>{self.render_head_meta(f"{self.config['site']['name']} Unit Comparison | Compare Units", "Compare Anime Crusaders X units by placement, tier, traits, recorded stats, costs, and build notes.", "/unit-comparison")}{self.get_base_css()}{self.render_schema_breadcrumbs([("Home", "/"), ("Unit Comparison", "/unit-comparison")])}<script type="application/ld+json">{json.dumps(schema)}</script></head><body>{self.render_nav("compare")}
        <main class="container main-layout"><div class="breadcrumbs"><a href="/">Home</a> <span>/</span> <span>Unit Comparison</span></div><div class="card"><h1 style="font-size:2.2rem;font-weight:900;margin-bottom:.5rem;">Compare {self.config['site']['name']} Units</h1><p style="color:var(--text-muted);margin-bottom:1.5rem;">Select two units. Only values recorded in the unit database are shown; missing values are marked Not recorded.</p><div class="calc-box"><div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;"><div><label class="calc-label" for="unit-a">Unit A:</label><select id="unit-a" class="calc-select" onchange="compareUnits()">{options_html}</select></div><div><label class="calc-label" for="unit-b">Unit B:</label><select id="unit-b" class="calc-select" onchange="compareUnits()">{options_html}</select></div></div><div id="cmp-out" style="margin-top:1.5rem;"></div></div></div></main>{self.render_footer()}
        <script>
        const allUnits = {units_json};
        const uMap = Object.fromEntries(allUnits.map(u => [u.slug, u]));
        const esc = value => String(value ?? 'Not recorded').replace(/[&<>"']/g, ch => ({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[ch]));
        function statRows(a, b) {{
            const excluded = new Set(['tier ranking', 'placement', 'role', 'best game mode', 'recommended traits', 'rarity']);
            const keys = [...new Set([...Object.keys(a.stats || {{}}), ...Object.keys(b.stats || {{}})])].filter(k => !excluded.has(k.toLowerCase()));
            return keys.map(k => '<tr><td>' + esc(k) + '</td><td>' + esc((a.stats || {{}})[k]) + '</td><td>' + esc((b.stats || {{}})[k]) + '</td></tr>').join('');
        }}
        function compareUnits() {{
            const a = uMap[document.getElementById('unit-a').value];
            const b = uMap[document.getElementById('unit-b').value];
            if (!a || !b) return;
            const rows = [
                ['Placement', a.type, b.type], ['Role', a.role, b.role], ['Tier', a.tier, b.tier],
                ['Rarity', a.rarity, b.rarity], ['Best Game Mode', a.gameMode, b.gameMode],
                ['Recommended Traits', a.traits, b.traits],
                ['DPS', a.dps, b.dps], ['SPA', a.spa, b.spa], ['Range', a.range, b.range],
                ['Place Cost', a.placeCost, b.placeCost], ['Max Upgrade Cost', a.upgradeCost, b.upgradeCost]
            ].map(r => '<tr><td>' + esc(r[0]) + '</td><td>' + esc(r[1]) + '</td><td>' + esc(r[2]) + '</td></tr>').join('');
            document.getElementById('cmp-out').innerHTML = '<table class="stats-table"><thead><tr><th>Attribute</th><th>' + esc(a.name) + '</th><th>' + esc(b.name) + '</th></tr></thead><tbody>' + rows + statRows(a, b) +
                '<tr><td>Description</td><td>' + esc(a.description) + '</td><td>' + esc(b.description) + '</td></tr>' +
                '<tr><td>Best Build / Synergy</td><td>' + esc(a.bestBuild) + '</td><td>' + esc(b.bestBuild) + '</td></tr>' +
                '<tr><td>Full Page</td><td><a href="/units/' + encodeURIComponent(a.slug) + '" style="color:var(--accent);">View ' + esc(a.name) + ' →</a></td><td><a href="/units/' + encodeURIComponent(b.slug) + '" style="color:var(--accent);">View ' + esc(b.name) + ' →</a></td></tr>' +
                '</tbody></table>';
        }}
        const qa = new URLSearchParams(location.search).get('a');
        document.getElementById('unit-a').value = (qa && uMap[qa]) ? qa : 'goju-vs-sukuno';
        document.getElementById('unit-b').value = (document.getElementById('unit-a').value === 'gilgamesh') ? 'goju-vs-sukuno' : 'gilgamesh';
        compareUnits();
        </script></body></html>"""
        with open(os.path.join(self.dist_dir, 'unit-comparison.html'), 'w', encoding='utf-8') as f:
            f.write(html)

    def build_editorial_pages(self):
        pages = [
            ("best-units", f"{self.config['site']['name']} Featured Units | Tracked Roster", f"Featured Units in {self.config['site']['name']}", "Browse the complete RBXMeta tracked roster by current tier labels. This is not a separate mode-specific ranking.", sorted(self.entities, key=lambda e: ({"S+": 0, "S": 1, "A": 2}.get(e.get("tier"), 3), e.get("name", "")))),
            ("best-dps", f"{self.config['site']['name']} DPS Units | Tracked Damage Dealers", f"DPS Units in {self.config['site']['name']}", "Tracked units labelled Main DPS, grouped across standard placement types and dedicated Hero slots; not a measured DPS ranking.", [e for e in self.entities if "dps" in e.get("role", "").lower()]),
            ("best-support", f"{self.config['site']['name']} Support Units | Tracked Roster", f"Support Units in {self.config['site']['name']}", "All tracked units currently labelled Support; the list does not imply verified buff values or a mode-specific ranking.", [e for e in self.entities if "support" in e["type"].lower()]),
        ]
        for slug, title, h1, desc, subset in pages:
            cards = "".join([f'<a href="/units/{e["slug"]}" class="entity-card"><div><div style="display:flex;justify-content:space-between;margin-bottom:0.5rem;"><strong>{e["name"]}</strong><span class="rarity-badge rarity-{e["rarity"]}">{e["rarity"]}</span></div><p style="color:var(--text-muted);font-size:0.88rem;">{e["type"]} • Tier {e["tier"]} — {e["description"]}</p></div><div style="margin-top:0.75rem;color:var(--accent);font-weight:700;">View Build →</div></a>' for e in subset])
            html = f"""<!DOCTYPE html><html lang="en"><head>{self.render_head_meta(title, desc, f"/{slug}")}{self.get_base_css()}{self.render_schema_breadcrumbs([("Home", "/"), (h1, f"/{slug}")])}{self.render_schema_article(h1, desc, f"/{slug}")}</head><body>{self.render_nav("bestunits" if slug=="best-units" else "")}
            <main class="container main-layout"><div class="breadcrumbs"><a href="/">Home</a> <span>/</span> <span>{h1}</span></div><div class="card"><div class="badge-verified" style="margin-bottom:0.75rem;">✓ UPDATED {datetime.now().strftime('%Y-%m-%d')}</div><h1 style="font-size:2.2rem;font-weight:900;margin-bottom:0.5rem;">{h1}</h1><p style="color:var(--text-muted);margin-bottom:1.5rem;">{desc} Test lineups in our <a href="/team-builder" style="color:var(--accent);">Team Builder</a> or <a href="/unit-comparison" style="color:var(--accent);">Unit Comparison</a>.</p><div class="entity-grid">{cards}</div></div></main>{self.render_footer()}</body></html>"""
            with open(os.path.join(self.dist_dir, f"{slug}.html"), 'w', encoding='utf-8') as f:
                f.write(html)

        confirmed_code_names = [c["code"] for c in self.codes if c.get("status", "").lower() == "active" and "unverified" not in c.get("verification", "").lower()]
        confirmed_code_text = ", ".join(f"<code>{code}</code>" for code in confirmed_code_names) or "No cross-source confirmed codes currently listed"
        updates_html = f"""<!DOCTYPE html><html lang="en"><head>{self.render_head_meta(f"{self.config['site']['name']} Updates & Patch Notes", "Latest Anime Crusaders X Anniversary Re-Release patch notes, new Hero units, and meta shifts.", "/updates")}{self.get_base_css()}{self.render_schema_breadcrumbs([("Home", "/"), ("Updates", "/updates")])}{self.render_schema_article(f"{self.config['site']['name']} Updates", "Latest Anime Crusaders X patch notes and meta changes.", "/updates")}</head><body>{self.render_nav("updates")}
        <main class="container main-layout"><div class="breadcrumbs"><a href="/">Home</a> <span>/</span> <span>Updates</span></div><div class="card"><h1 style="font-size:2.2rem;font-weight:900;margin-bottom:1rem;">{self.config['site']['name']} Update Log</h1><div style="background:var(--bg-card-sub);border:1px solid var(--border);border-radius:0.65rem;padding:1.25rem;margin-bottom:1rem;"><span class="badge-verified">2026-11-16 • ANNIVERSARY RE-RELEASE</span><h2 style="margin:0.5rem 0;">Anime Crusaders X Re-Release &amp; New Codes</h2><p style="color:var(--text-muted);">Added Eskanoor (first Hero unit), Vegeto Fusion, and cross-source confirmed codes: {confirmed_code_text}. Codes with mixed reports are shown separately on the <a href="/codes" style="color:var(--accent);">Codes</a> page.</p>Check the updated <a href="/tier-list" style="color:var(--accent);">Tier List</a>.</div></div></main>{self.render_footer()}</body></html>"""
        with open(os.path.join(self.dist_dir, "updates.html"), 'w', encoding='utf-8') as f:
            f.write(updates_html)

    def build_database(self):
        db_dir = os.path.join(self.dist_dir, 'units')
        os.makedirs(db_dir, exist_ok=True)
        cards = "".join([f'<a href="/units/{e["slug"]}" class="entity-card" data-type="{e["type"].lower()}" data-name="{e["name"].lower()} {e["rarity"].lower()}"><div><div style="display:flex;justify-content:space-between;margin-bottom:0.6rem;"><div><h3 style="font-size:1.1rem;font-weight:800;color:#fff;">{e["name"]}</h3><span style="font-size:0.78rem;color:var(--text-muted);">{e["type"]} • Tier {e["tier"]}</span></div><span class="rarity-badge rarity-{e["rarity"]}">{e["rarity"]}</span></div><p style="color:var(--text-muted);font-size:0.88rem;">{e["description"]}</p></div><div style="margin-top:0.85rem;color:var(--accent);font-weight:700;font-size:0.86rem;">View Unit →</div></a>' for e in self.entities])
        idx_html = f"""<!DOCTYPE html><html lang="en"><head>{self.render_head_meta(f"{self.config['site']['name']} Units Database | All Units & Stats", "Browse all Hill, Ground, Hybrid & Support units in Anime Crusaders X.", "/units/")}{self.get_base_css()}{self.render_schema_breadcrumbs([("Home", "/"), ("Units", "/units/")])}</head><body>{self.render_nav("units")}
        <main class="container main-layout"><div class="breadcrumbs"><a href="/">Home</a> <span>/</span> <span>Units</span></div><div class="card"><h1 style="font-size:2.2rem;font-weight:900;margin-bottom:0.5rem;">Featured {self.config['site']['name']} Meta Units ({len(self.entities)})</h1><p style="color:var(--text-muted);margin-bottom:1.25rem;">Core featured roster verified across recent meta lists. Additional units (including Beyond Heaven, Bun, Dracula, Ichi, Igrith, Kyruto, Toju, Esdead, Speedcart, and Ayzen) are queued for staged expansion.</p>{self.render_native_banner("units")}<input type="text" id="q" class="search-input" placeholder="Search Goju, Gilgamesh, Kurimi, Mely, Eskanoor..." oninput="flt()"><div class="tab-bar"><button class="tab-btn active" onclick="setT('all')">All ({len(self.entities)})</button><button class="tab-btn" onclick="setT('hill')">Hill &amp; Hybrid</button><button class="tab-btn" onclick="setT('ground')">Ground</button><button class="tab-btn" onclick="setT('support')">Support</button><button class="tab-btn" onclick="setT('hero')">Hero Slot</button></div><div class="entity-grid">{cards}</div></div></main>{self.render_footer()}<script>let act='all';function setT(t){{act=t;document.querySelectorAll('.tab-btn').forEach(b=>b.classList.toggle('active',b.getAttribute('onclick').includes(t)));flt();}}function flt(){{const q=(document.getElementById('q').value||'').toLowerCase();document.querySelectorAll('.entity-card').forEach(c=>{{const ct=c.getAttribute('data-type'),cn=c.getAttribute('data-name');c.style.display=((act==='all'||ct.includes(act))&&(!q||cn.includes(q)||ct.includes(q)))?'flex':'none';}});}}const iq=new URLSearchParams(location.search).get('q');if(iq){{document.getElementById('q').value=iq;flt();}}</script></body></html>"""
        with open(os.path.join(db_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(idx_html)

        for e in self.entities:
            srows = "".join([f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in e["stats"].items()])
            rel = [x for x in self.entities if x["slug"] != e["slug"] and x["type"] == e["type"]][:4]
            rel_html = "".join([f'<a href="/units/{r["slug"]}" class="tier-item-pill"><strong>{r["name"]}</strong><p style="color:var(--text-muted);font-size:0.84rem;">{r["type"]} • Tier {r["tier"]}</p></a>' for r in rel])
            uhtml = f"""<!DOCTYPE html><html lang="en"><head>{self.render_head_meta(f"{e['name']} Stats & Tier | {self.config['site']['name']} Wiki", e['description'], f"/units/{e['slug']}")}{self.get_base_css()}{self.render_schema_breadcrumbs([("Home", "/"), ("Units", "/units/"), (e["name"], f"/units/{e['slug']}")])}{self.render_schema_article(f"{e['name']} - {self.config['site']['name']}", e['description'], f"/units/{e['slug']}")}</head><body>{self.render_nav("units")}
            <main class="container main-layout"><div class="breadcrumbs"><a href="/">Home</a> <span>/</span> <a href="/units/">Units</a> <span>/</span> <span>{e['name']}</span></div><div class="card"><div style="display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid var(--border);padding-bottom:1rem;margin-bottom:1.25rem;flex-wrap:wrap;gap:1rem;"><div><h1 style="font-size:2.1rem;font-weight:900;">{e['name']}</h1><p style="color:var(--text-muted);">{e['type']} • Tier {e['tier']}</p></div><span class="rarity-badge rarity-{e['rarity']}">{e['rarity']}</span></div><p style="color:#cbd5e1;font-size:1.05rem;margin-bottom:1.5rem;">{e['description']}</p><table class="stats-table">{srows}</table><p style="color:var(--text-muted);font-size:0.85rem;margin-top:0.85rem;"><strong>Data Source:</strong> {e.get('source', 'Community Tier Lists')} • <strong>Last Verified:</strong> {e.get('lastTested', '2026-11-17')}</p><div style="display:flex;gap:0.75rem;flex-wrap:wrap;margin:1.25rem 0;"><a href="/tier-list" class="tab-btn">View Tier List</a><a href="/team-builder?add={e['slug']}" class="tab-btn">Add to Team Builder</a><a href="/unit-comparison?a={e['slug']}" class="tab-btn">Compare Unit</a></div><h2 style="font-size:1.25rem;margin:1.5rem 0 0.5rem;color:#38bdf8;">How to Obtain &amp; Best Synergies</h2><p style="color:#cbd5e1;">{e['howToGet']} {e['bestBuild']}</p><div style="margin-top:2rem;border-top:1px solid var(--border);padding-top:1.25rem;"><h3 style="margin-bottom:0.85rem;">Related {e['type']} Units</h3><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:0.75rem;">{rel_html}</div></div></div></main>{self.render_footer()}</body></html>"""
            with open(os.path.join(db_dir, f"{e['slug']}.html"), 'w', encoding='utf-8') as f:
                f.write(uhtml)

    def build_guides(self):
        gdir = os.path.join(self.dist_dir, 'guides')
        os.makedirs(gdir, exist_ok=True)
        cards = "".join([f'<article class="card" style="margin-bottom:1.25rem;"><span class="badge-verified">{g["category"]}</span><h2 style="font-size:1.35rem;margin:0.5rem 0;color:#fff;"><a href="/guides/{g["slug"]}">{g["title"]}</a></h2><p style="color:var(--text-muted);margin-bottom:0.75rem;">{g["excerpt"]}</p><a href="/guides/{g["slug"]}" style="color:var(--accent);font-weight:700;">Read Full Guide →</a></article>' for g in self.guides])
        idx = f"""<!DOCTYPE html><html lang="en"><head>{self.render_head_meta(f"{self.config['site']['name']} Guides", "Evolution, fusion, trait reroll, and strategy guides for Anime Crusaders X.", "/guides/")}{self.get_base_css()}{self.render_schema_breadcrumbs([("Home", "/"), ("Guides", "/guides/")])}</head><body>{self.render_nav("guides")}<main class="container main-layout"><div class="breadcrumbs"><a href="/">Home</a> <span>/</span> <span>Guides</span></div><div class="card"><h1 style="font-size:2.1rem;font-weight:900;margin-bottom:1.25rem;">{self.config['site']['name']} Guides</h1>{cards}{self.render_native_banner("guides")}</div></main>{self.render_footer()}</body></html>"""
        with open(os.path.join(gdir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(idx)
        for g in self.guides:
            gh = f"""<!DOCTYPE html><html lang="en"><head>{self.render_head_meta(f"{g['title']} | {self.config['site']['name']}", g['excerpt'], f"/guides/{g['slug']}")}{self.get_base_css()}{self.render_schema_breadcrumbs([("Home", "/"), ("Guides", "/guides/"), (g['title'], f"/guides/{g['slug']}")])}{self.render_schema_article(g['title'], g['excerpt'], f"/guides/{g['slug']}", g['updatedDate'], schema_type="Article")}</head><body>{self.render_nav("guides")}<main class="container main-layout"><div class="breadcrumbs"><a href="/">Home</a> <span>/</span> <a href="/guides/">Guides</a> <span>/</span> <span>{g['title']}</span></div><article class="card"><span class="badge-verified">{g['category']}</span><h1 style="font-size:2.15rem;font-weight:900;margin:0.75rem 0;">{g['title']}</h1><p style="color:var(--text-muted);margin-bottom:1.5rem;">Updated: {g['updatedDate']}</p><div style="font-size:1.08rem;line-height:1.8;color:#e2e8f0;">{g['content'].replace('/database/', '/units/')}</div>{self.render_native_banner("guides")}</article></main>{self.render_footer()}</body></html>"""
            with open(os.path.join(gdir, f"{g['slug']}.html"), 'w', encoding='utf-8') as f:
                f.write(gh)

    def build_localized_pages(self):
        today = datetime.now().strftime('%Y-%m-%d')
        active = [c for c in self.codes if c.get("status", "").lower() == "active" and "unverified" not in c.get("verification", "").lower()]
        for lang, label_codes, label_tl in [("es", "Códigos de Anime Crusaders X (Noviembre 2026)", "Tier List de Anime Crusaders X"), ("pt", "Códigos de Anime Crusaders X (Novembro 2026)", "Tier List de Anime Crusaders X")]:
            ldir = os.path.join(self.dist_dir, lang)
            os.makedirs(ldir, exist_ok=True)
            rows = "".join([f'<div class="code-row"><div><span class="code-val">{c["code"]}</span><span class="code-reward">({c["reward"]})</span></div><button class="btn-copy" onclick="copyCode(this, \'{c["code"]}\')">COPY</button></div>' for c in active])
            ch = f'<!DOCTYPE html><html lang="{lang}"><head>{self.render_head_meta(label_codes, label_codes, f"/{lang}/codes", robots="noindex, follow")}{self.get_base_css()}</head><body>{self.render_nav("codes")}<main class="container main-layout"><div class="card">{self.render_lang_switcher("codes", lang)}<div class="badge-verified" style="margin-bottom:0.75rem;">✓ {today}</div><h1>{label_codes}</h1><div style="margin-top:1rem;">{rows}</div></div></main>{self.render_footer()}</body></html>'
            with open(os.path.join(ldir, 'codes.html'), 'w', encoding='utf-8') as f:
                f.write(ch)
            tbl = ""
            for e in self.entities:
                tbl += f'<tr><td><strong>{e["tier"]}</strong></td><td>{e["type"]}</td><td><a href="/units/{e["slug"]}" style="color:var(--accent);">{e["name"]}</a></td><td>{e["description"][:95]}...</td></tr>'
            th = f'<!DOCTYPE html><html lang="{lang}"><head>{self.render_head_meta(label_tl, label_tl, f"/{lang}/tier-list", robots="noindex, follow")}{self.get_base_css()}</head><body>{self.render_nav("tierlist")}<main class="container main-layout"><div class="card">{self.render_lang_switcher("tier-list", lang)}<div class="badge-verified" style="margin-bottom:0.75rem;">✓ {today}</div><h1>{label_tl}</h1><table class="stats-table"><thead><tr><th>Tier</th><th>Role</th><th>Unit</th><th>Notes</th></tr></thead><tbody>{tbl}</tbody></table></div></main>{self.render_footer()}</body></html>'
            with open(os.path.join(ldir, 'tier-list.html'), 'w', encoding='utf-8') as f:
                f.write(th)

    def build_trust_pages(self):
        today = datetime.now().strftime('%Y-%m-%d')
        about_html = f"""<!DOCTYPE html><html lang="en"><head>{self.render_head_meta("About RBXMeta | Anime Crusaders X Tools & Wiki", "About RBXMeta, an independent fan-made database and interactive utility hub for Anime Crusaders X on Roblox.", "/about")}{self.get_base_css()}{self.render_schema_breadcrumbs([("Home", "/"), ("About", "/about")])}{self.render_schema_article("About RBXMeta", "Independent fan-made utility hub for Anime Crusaders X.", "/about")}</head><body>{self.render_nav()}
        <main class="container main-layout"><div class="breadcrumbs"><a href="/">Home</a> <span>/</span> <span>About</span></div><div class="card"><h1 style="font-size:2.1rem;font-weight:900;margin-bottom:1rem;">About RBXMeta</h1><p style="color:#cbd5e1;margin-bottom:1rem;"><strong>RBXMeta</strong> is an independent, fan-made database and interactive tools hub built for Roblox players—starting with <strong>Anime Crusaders X</strong>.</p><p style="color:#cbd5e1;margin-bottom:1rem;">Instead of publishing bare text tables, we focus on interactive utilities: a <strong>Gem &amp; Pity Calculator</strong> (200 Mythic / 2,000 Secret), <strong>Trait Reroll Odds Calculator</strong>, <strong>Evolution Material Planner</strong>, <strong>6-Slot Team Builder</strong>, and <strong>Side-by-Side Unit Comparison</strong>.</p><p style="color:var(--text-muted);"><strong>Disclaimer:</strong> RBXMeta is not affiliated with, endorsed by, or sponsored by 32x or Roblox Corporation.</p></div></main>{self.render_footer()}</body></html>"""
        with open(os.path.join(self.dist_dir, "about.html"), 'w', encoding='utf-8') as f:
            f.write(about_html)

        policy_html = f"""<!DOCTYPE html><html lang="en"><head>{self.render_head_meta("Editorial Policy & Verification Standards | RBXMeta", "How RBXMeta evaluates Anime Crusaders X Tier List rankings, verifies Codes (Verified vs Unverified), and calculates summon probabilities.", "/editorial-policy")}{self.get_base_css()}{self.render_schema_breadcrumbs([("Home", "/"), ("Editorial Policy", "/editorial-policy")])}{self.render_schema_article("Editorial Policy & Verification Standards", "How RBXMeta sources and verifies Anime Crusaders X data.", "/editorial-policy")}</head><body>{self.render_nav()}
        <main class="container main-layout"><div class="breadcrumbs"><a href="/">Home</a> <span>/</span> <span>Editorial Policy</span></div><div class="card"><h1 style="font-size:2.1rem;font-weight:900;margin-bottom:1rem;">Editorial Policy &amp; Data Sources</h1><h2 style="font-size:1.25rem;color:#38bdf8;margin:1rem 0 0.5rem;">1. Tier List Methodology</h2><p style="color:#cbd5e1;margin-bottom:1rem;">Unit rankings evaluate <strong>Infinite &amp; Progressive mode utility, placement flexibility (Hill/Ground/Hybrid/Support), scaling, and team synergy</strong>—not rarity alone. Current rankings cross-check consensus data from MrGuider, Destructoid, IGN, and community feedback. We never fabricate playtest claims.</p><h2 style="font-size:1.25rem;color:#38bdf8;margin:1rem 0 0.5rem;">2. Code Verification Labels</h2><ul style="margin-left:1.5rem;color:#cbd5e1;line-height:1.9;"><li><strong>In-game Verified:</strong> Directly redeemed and confirmed inside the live Roblox client.</li><li><strong>Cross-source Confirmed:</strong> Confirmed across multiple independent trackers (e.g., IGN, Beebom, Eurogamer, RBLXSTAT) with exact level requirements noted; pending personal in-game check.</li><li><strong>Unverified (Mixed Reports):</strong> Reported by at least one source but flagged as unverified or inconsistent by another (for example, <code>THANKYOUFOR30KMAJORFIXES</code>).</li><li><strong>Expired:</strong> Confirmed inactive and archived so players do not waste time.</li></ul><h2 style="font-size:1.25rem;color:#38bdf8;margin:1rem 0 0.5rem;">3. Calculator Math</h2><p style="color:#cbd5e1;">Our Gem &amp; Pity Calculator uses standard cumulative probability (<code>1 - (1 - p)^n</code>, assuming independent constant-rate rolls) alongside fixed 200-pull Mythic and 2,000-pull Secret/Crusader pity thresholds.</p></div></main>{self.render_footer()}</body></html>"""
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
            ("/units/", today, "weekly", "0.9"),
            ("/team-builder", today, "weekly", "0.9"),
            ("/unit-comparison", today, "weekly", "0.9"),
            ("/best-units", today, "weekly", "0.85"),
            ("/best-dps", today, "weekly", "0.85"),
            ("/best-support", today, "weekly", "0.85"),
            ("/codes", today, "daily", "0.9"),
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
            f.write(f"User-agent: Googlebot\nAllow: /\n\nUser-agent: Bingbot\nAllow: /\n\nUser-agent: OAI-SearchBot\nAllow: /\n\nUser-agent: GPTBot\nAllow: /\n\nUser-agent: *\nAllow: /\n\nSitemap: {domain}/sitemap.xml\n")
        with open(os.path.join(self.dist_dir, '_redirects'), 'w', encoding='utf-8') as f:
            f.write("\n".join(reds) + "\n")
        indexnow_key = "d9fff1aa6c384251b984519c49ed6831"
        with open(os.path.join(self.dist_dir, f'{indexnow_key}.txt'), 'w', encoding='utf-8') as f:
            f.write(indexnow_key)
        with open(os.path.join(self.dist_dir, 'BingSiteAuth.xml'), 'w', encoding='utf-8') as f:
            f.write('<?xml version="1.0"?>\n<users>\n\t<user>5A5AB05B40BF829D89012A846FF57A00</user>\n</users>\n')

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
