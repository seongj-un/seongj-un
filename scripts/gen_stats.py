"""Render GitHub stats cards (light + dark SVG) for the profile README.

Uses only the standard library. Needs GITHUB_TOKEN (the Actions token is enough:
every query here reads public data).
"""

import datetime as dt
import json
import os
import pathlib
import urllib.request
from xml.sax.saxutils import escape

LOGIN = os.environ.get("STATS_USER", "seongj-un")
EXCLUDED_ORGS = ["team-xquare"]  # left out of every number on the cards
EXCLUDE = "".join(f"+-org:{o}" for o in EXCLUDED_ORGS)
OUT = pathlib.Path(__file__).resolve().parent.parent / "assets"
TOKEN = os.environ["GITHUB_TOKEN"]

THEMES = {
    "light": {"bg": "#ffffff", "border": "#d0d7de", "title": "#1f2328", "text": "#59636e", "value": "#1f2328", "track": "#eff2f5"},
    "dark": {"bg": "#0d1117", "border": "#30363d", "title": "#e6edf3", "text": "#9198a1", "value": "#e6edf3", "track": "#21262d"},
}
FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif"
LANG_COLORS = {
    "Kotlin": "#A97BFF", "Python": "#3572A5", "TypeScript": "#3178c6", "JavaScript": "#f1e05a",
    "Java": "#b07219", "Dart": "#00B4AB", "Go": "#00ADD8", "Swift": "#F05138", "HCL": "#844FBA",
    "HTML": "#e34c26", "CSS": "#563d7c", "Shell": "#89e051", "Dockerfile": "#384d54",
}
CARD_H = 200  # both cards share a height so they line up side by side
SKIP_LANGS = {"HTML", "CSS", "Dockerfile", "Mako", "Shell", "Go Template"}  # markup/config, not code I write


def gql(query, **variables):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {TOKEN}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = json.load(resp)
    if body.get("errors"):
        raise RuntimeError(body["errors"])
    return body["data"]


def rest(path):
    req = urllib.request.Request(f"https://api.github.com/{path}", headers={"Authorization": f"bearer {TOKEN}"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def collect():
    year = dt.datetime.now(dt.timezone.utc).year
    data = gql(
        """query($login:String!,$from:DateTime!){user(login:$login){
          contributionsCollection(from:$from){totalCommitContributions contributionCalendar{totalContributions}
            commitContributionsByRepository(maxRepositories:100){repository{owner{login}} contributions{totalCount}}
            pullRequestContributionsByRepository(maxRepositories:100){repository{owner{login}} contributions{totalCount}}
            issueContributionsByRepository(maxRepositories:100){repository{owner{login}} contributions{totalCount}}
            pullRequestReviewContributionsByRepository(maxRepositories:100){repository{owner{login}} contributions{totalCount}}}
          pullRequests{totalCount}
          repositories(ownerAffiliations:OWNER,isFork:false,privacy:PUBLIC,first:100){totalCount nodes{
            stargazerCount languages(first:20,orderBy:{field:SIZE,direction:DESC}){edges{size node{name}}}}}
        }}""",
        login=LOGIN,
        **{"from": f"{year}-01-01T00:00:00Z"},
    )["user"]
    prs = rest(f"search/issues?q=author:{LOGIN}+is:pr{EXCLUDE}&per_page=1")["total_count"]
    merged = rest(f"search/issues?q=author:{LOGIN}+is:pr+is:merged{EXCLUDE}&per_page=1")["total_count"]
    external = rest(f"search/issues?q=author:{LOGIN}+is:pr+is:merged+-user:{LOGIN}{EXCLUDE}&per_page=100")
    external_repos = {item["repository_url"] for item in external["items"]}

    langs = {}
    for repo in data["repositories"]["nodes"]:
        for edge in repo["languages"]["edges"]:
            name = edge["node"]["name"]
            if name not in SKIP_LANGS:
                langs[name] = langs.get(name, 0) + edge["size"]
    cc = data["contributionsCollection"]
    def excluded(key):
        return sum(r["contributions"]["totalCount"] for r in cc[key] if r["repository"]["owner"]["login"] in EXCLUDED_ORGS)
    commits_out = excluded("commitContributionsByRepository")
    total_out = commits_out + sum(excluded(k) for k in ("pullRequestContributionsByRepository", "issueContributionsByRepository", "pullRequestReviewContributionsByRepository"))
    return {
        "year": year,
        "rows": [
            (f"Contributions ({year})", cc["contributionCalendar"]["totalContributions"] - total_out),
            (f"Commits ({year})", cc["totalCommitContributions"] - commits_out),
            ("Pull requests", prs),
            ("Merged PRs", merged),
            ("Repos contributed to", len(external_repos)),
        ],
        "langs": sorted(langs.items(), key=lambda kv: -kv[1]),
    }


def card(width, height, title, body, t):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" '
        f'role="img" aria-label="{escape(title)}"><style>text{{font-family:{FONT}}}</style>'
        f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="6" fill="{t["bg"]}" stroke="{t["border"]}"/>'
        f'<text x="24" y="36" font-size="15" font-weight="600" fill="{t["title"]}">{escape(title)}</text>{body}</svg>'
    )


def stats_svg(s, t):
    body = ""
    for i, (label, value) in enumerate(s["rows"]):
        y = 70 + i * 26
        body += (
            f'<text x="24" y="{y}" font-size="13" fill="{t["text"]}">{escape(label)}</text>'
            f'<text x="326" y="{y}" font-size="13" font-weight="600" fill="{t["value"]}" text-anchor="end">{value:,}</text>'
        )
    return card(350, CARD_H, "Activity", body, t)


def langs_svg(s, t, top=6):
    langs = s["langs"][:top]
    other = sum(size for _, size in s["langs"][top:])
    if other:
        langs.append(("Other", other))
    total = sum(size for _, size in langs) or 1
    bar_w, x = 302, 24.0
    body = f'<rect x="24" y="54" width="{bar_w}" height="8" rx="4" fill="{t["track"]}"/>'
    body += '<clipPath id="bar"><rect x="24" y="54" width="302" height="8" rx="4"/></clipPath><g clip-path="url(#bar)">'
    for name, size in langs:
        w = bar_w * size / total
        body += f'<rect x="{x:.2f}" y="54" width="{w:.2f}" height="8" fill="{LANG_COLORS.get(name, "#8b949e")}"/>'
        x += w
    body += "</g>"
    for i, (name, size) in enumerate(langs):
        col, row = i % 2, i // 2
        cx, cy = 24 + col * 160, 88 + row * 24
        body += (
            f'<circle cx="{cx + 5}" cy="{cy - 4}" r="5" fill="{LANG_COLORS.get(name, "#8b949e")}"/>'
            f'<text x="{cx + 16}" y="{cy}" font-size="13" fill="{t["text"]}">{escape(name)} '
            f'<tspan fill="{t["value"]}" font-weight="600">{size / total * 100:.1f}%</tspan></text>'
        )
    return card(350, CARD_H, "Most Used Languages", body, t)


def main():
    s = collect()
    OUT.mkdir(exist_ok=True)
    for theme, t in THEMES.items():
        (OUT / f"stats-{theme}.svg").write_text(stats_svg(s, t), encoding="utf-8")
        (OUT / f"langs-{theme}.svg").write_text(langs_svg(s, t), encoding="utf-8")
    print(json.dumps({"rows": s["rows"], "langs": s["langs"][:8]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
