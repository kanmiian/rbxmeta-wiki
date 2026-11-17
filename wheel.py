import sys
import os
import http.server
import socketserver
import json
import subprocess
from builder import WikiBuilder

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    
    if len(sys.argv) < 2:
        print("""
=====================================================
🚀 Roblox Wiki Arbitrage Wheel CLI (站群自动化轮子)
=====================================================
Usage:
  python wheel.py build             -> Compile full static site to /dist
  python wheel.py deploy [project]  -> Build and deploy /dist to Cloudflare Pages
  python wheel.py serve [port]      -> Preview site locally (default: 8080)
  python wheel.py stats             -> Check site SEO metrics & page counts
  python wheel.py new "Game" "URL"  -> Scaffold a new game config
=====================================================
        """)
        return

    cmd = sys.argv[1].lower()

    if cmd == "build":
        builder = WikiBuilder(root_dir)
        builder.build_all()

    elif cmd == "deploy":
        builder = WikiBuilder(root_dir)
        builder.build_all()
        project_name = sys.argv[2] if len(sys.argv) > 2 else builder.config["site"].get("cfPagesProject", builder.config["site"]["gameId"].replace("-", ""))
        dist_dir = os.path.join(root_dir, 'dist')
        npx_bin = "npx.cmd" if os.name == "nt" else "npx"
        cmd_list = [npx_bin, "wrangler", "pages", "deploy", dist_dir, f"--project-name={project_name}"]
        print(f"🚀 Deploying {dist_dir} to Cloudflare Pages project '{project_name}'...")
        res = subprocess.run(cmd_list, check=False)
        if res.returncode != 0:
            print("\n⚠️ Deploy exited with non-zero code. If not logged in yet, run: npx.cmd wrangler login")
            sys.exit(res.returncode)

    elif cmd == "serve":
        port = int(sys.argv[2]) if len(sys.argv) > 2 else 8080
        dist_dir = os.path.join(root_dir, 'dist')
        if not os.path.exists(dist_dir):
            print("dist/ not found, building first...")
            builder = WikiBuilder(root_dir)
            builder.build_all()
        
        os.chdir(dist_dir)
        Handler = http.server.SimpleHTTPRequestHandler
        print(f"✨ Local Preview Server running at: http://localhost:{port}")
        print("Press Ctrl+C to stop.")
        with socketserver.TCPServer(("", port), Handler) as httpd:
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\nServer stopped.")

    elif cmd == "stats":
        dist_dir = os.path.join(root_dir, 'dist')
        if not os.path.exists(dist_dir):
            print("Run 'python wheel.py build' first.")
            return
        html_files = []
        for root, _, files in os.walk(dist_dir):
            for f in files:
                if f.endswith('.html'):
                    html_files.append(os.path.join(root, f))
        print("-----------------------------------------")
        print(f"📊 Site SEO & pSEO Metrics:")
        print(f"  • Total HTML Pages Generated: {len(html_files)}")
        print(f"  • Target Domain: {WikiBuilder(root_dir).config['site']['domain']}")
        print(f"  • Robots.txt: {'Present' if os.path.exists(os.path.join(dist_dir, 'robots.txt')) else 'Missing'}")
        print(f"  • Sitemap.xml: {'Present' if os.path.exists(os.path.join(dist_dir, 'sitemap.xml')) else 'Missing'}")
        print("-----------------------------------------")

    elif cmd == "new":
        if len(sys.argv) < 4:
            print("Error: Missing parameters. Example: python wheel.py new 'Anime Reborn' 'https://animerebornwiki.com'")
            return
        game_name = sys.argv[2]
        game_url = sys.argv[3]
        slug = game_name.lower().replace(" ", "-").replace("'", "")
        new_config = {
            "site": {
                "gameId": slug,
                "name": game_name,
                "domain": game_url,
                "title": f"{game_name} Wiki & Codes | Roblox Tier List & Database",
                "description": f"The comprehensive {game_name} Roblox wiki. Active codes, tier lists, and item database updated daily.",
                "themeColor": "#3b82f6",
                "accentColor": "#2563eb",
                "social": {
                    "roblox": f"https://www.roblox.com/games/{slug}",
                    "discord": f"https://discord.gg/{slug}",
                    "trello": f"https://trello.com/b/{slug}"
                },
                "ads": {
                    "enabled": False,
                    "adClient": "ca-pub-XXXXXXXXXXXXXXXX",
                    "slots": {
                        "header": "1234567890",
                        "inContent": "0987654321",
                        "sidebar": "1122334455"
                    }
                }
            },
            "faqs": [
                {
                    "question": f"What are the active codes for {game_name}?",
                    "answer": "Check our Codes page for daily verified active codes."
                },
                {
                    "question": f"How do I redeem codes in {game_name}?",
                    "answer": f"Open {game_name} in Roblox, tap the Codes/Settings icon, enter the code, and confirm."
                }
            ]
        }
        with open(os.path.join(root_dir, 'config.json'), 'w', encoding='utf-8') as f:
            json.dump(new_config, f, indent=2)
        print(f"✅ Initialized new game configuration for: '{game_name}' ({game_url})")

    else:
        print(f"Unknown command: {cmd}")

if __name__ == "__main__":
    main()
