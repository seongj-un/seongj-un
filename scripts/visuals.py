"""Animated banner and featured-project cards for the profile README."""

import datetime as dt
from xml.sax.saxutils import escape

FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI','Apple SD Gothic Neo','Malgun Gothic','Noto Sans KR','Noto Sans',Helvetica,Arial,sans-serif"

BANNER = {
    "light": {"name1": "#5b2fd6", "title": "#1f2328",
              "text": "#3d3a4f", "muted": "#7a7590", "border": "#e2dcf5"},
    "dark": {"name1": "#b79cff", "title": "#e6edf3",
             "text": "#e6edf3", "muted": "#9198a1", "border": "#2b2346"},
}

ROLES = ["Kotlin · Spring Boot", "FastAPI · PostgreSQL", "Kubernetes · Argo CD", "AI agents · MCP"]

PROJECTS = [
    {
        "name": "farero",
        "url": "https://github.com/farero-dev/farero-dev.github.io",
        "ko": ["AI 코딩 에이전트의 권한 요청을 노치에서", "승인하는 macOS 앱. MCP 게이트웨이·감사 로그"],
        "en": "macOS notch app that gates what coding agents do",
        "tags": ["Go", "Swift", "MCP", "SQLite"],
    },
    {
        "name": "hermes-headroom",
        "url": "https://github.com/seongj-un/hermes-headroom",
        "ko": ["작은 서버에서도 에이전트가 죽지 않도록", "무거운 작업을 줄 세우고 메모리를 제한"],
        "en": "Hermes plugin, listed in the official catalog",
        "tags": ["Python", "systemd", "Plugin"],
    },
    {
        "name": "ev-charge-time",
        "url": "https://github.com/seongj-un/ev-charge-time",
        "ko": ["전기차를 가장 싸게 충전할 시간을 추천.", "빛가람 AI·ICT 경진대회 출품작"],
        "en": "Cheapest EV charging time, from 2026 tariffs",
        "tags": ["FastAPI", "PostgreSQL", "TypeScript"],
    },
    {
        "name": "PairPay",
        "url": "https://github.com/seongj-un/duri",
        "ko": ["커플 둘이 쓰는 공동생활비·데이트비용", "정산 웹앱 백엔드"],
        "en": "Shared-expense settlement for couples",
        "tags": ["Kotlin", "Spring Boot 4", "PostgreSQL"],
    },
    {
        "name": "dev-ops-study",
        "url": "https://github.com/seongj-un/dev-ops-study",
        "ko": ["URL 단축 API로 CI/CD·쿠버네티스·", "GitOps·관측성을 직접 실습"],
        "en": "Hands-on CI/CD, Kubernetes and GitOps",
        "tags": ["Kotlin", "Kubernetes", "Argo CD", "Helm"],
    },
    {
        "name": "n8n-obsidian-rag",
        "url": "https://github.com/seongj-un/n8n-obsidian-rag",
        "ko": ["옵시디언 노트를 근거로 디스코드에서 답하는", "RAG 봇. 골든 60문항으로 품질 측정"],
        "en": "Discord RAG bot grounded in an Obsidian vault",
        "tags": ["n8n", "RAG", "Discord"],
    },
]


def _level(count, cuts):
    return 0 if count == 0 else 1 + sum(count > c for c in cuts)


def banner_svg(days, t, b, weeks=15):
    w, h = 708, 230
    days = days[-(weeks * 7):]
    nonzero = sorted(c for _, c in days if c)
    cuts = [nonzero[int(len(nonzero) * q)] for q in (0.25, 0.5, 0.75)] if nonzero else [1, 2, 3]
    offset = (dt.date.fromisoformat(days[0][0]).weekday() + 1) % 7 if days else 0
    cell, gap = 11, 3
    gx, gy = w - 36 - weeks * (cell + gap) + gap, 62
    grid = ""
    for i, (date, count) in enumerate(days):
        col, row = divmod(i + offset, 7)
        if col >= weeks:
            break
        grid += (f'<rect class="c" style="animation-delay:{0.4 + col * 0.05:.2f}s" x="{gx + col * (cell + gap)}" '
                 f'y="{gy + row * (cell + gap)}" width="{cell}" height="{cell}" rx="2.5" fill="{t["grid"][_level(count, cuts)]}">'
                 f'<title>{date}: {count}</title></rect>')

    n, step = len(ROLES), 2.6
    roles = ""
    for i, role in enumerate(ROLES):
        roles += (f'<text class="r" style="animation-delay:{i * step}s" x="40" y="176" font-size="15" '
                  f'font-weight="600" fill="{b["name1"]}">{escape(role)}</text>')
    total = n * step
    show = 100 / n

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Seongjun Park, Backend Developer">
<defs>
</defs>
<style>
  text {{ font-family: {FONT}; }}
  .c {{ opacity: 0; animation: pop .5s ease-out forwards; }}
  @keyframes pop {{ from {{ opacity: 0; transform: translateY(4px); }} to {{ opacity: 1; transform: none; }} }}
  .r {{ opacity: 0; animation: role {total}s infinite; }}
  @keyframes role {{ 0% {{ opacity: 0; transform: translateY(6px); }} {show * 0.12:.1f}% {{ opacity: 1; transform: none; }}
    {show * 0.85:.1f}% {{ opacity: 1; transform: none; }} {show:.1f}% {{ opacity: 0; transform: translateY(-6px); }} 100% {{ opacity: 0; }} }}
  .cur {{ animation: blink 1s steps(1) infinite; }}
  @keyframes blink {{ 50% {{ opacity: 0; }} }}
  .in {{ opacity: 0; animation: up .7s ease-out forwards; }}
  @keyframes up {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: none; }} }}
</style>
<text class="in" x="40" y="58" font-size="12" font-weight="700" letter-spacing="3" fill="{b["muted"]}">HELLO, I'M</text>
<text class="in" style="animation-delay:.1s" x="38" y="108" font-size="46" font-weight="800" letter-spacing="-1" fill="{b["title"]}">Seongjun Park</text>
<text class="in" style="animation-delay:.2s" x="40" y="140" font-size="17" fill="{b["text"]}">박성준 <tspan fill="{b["muted"]}">·</tspan> Backend Developer</text>
{roles}
<rect class="cur" x="40" y="186" width="44" height="2" rx="1" fill="{b["name1"]}"/>
<text x="40" y="210" font-size="11" fill="{b["muted"]}">Daedeok Software Meister High School</text>
{grid}
<text x="{w - 36}" y="{gy + 7 * (cell + gap) + 14}" font-size="11" fill="{b["muted"]}" text-anchor="end">contributions, last {weeks} weeks</text>
</svg>'''


def project_svg(p, t, b, w=350, h=168):
    tags, x = "", 24
    for tag in p["tags"]:
        tw = 14 + len(tag) * 6.6
        tags += (f'<rect x="{x}" y="{h - 40}" width="{tw:.0f}" height="20" rx="10" fill="{t["track"]}"/>'
                 f'<text x="{x + tw / 2:.1f}" y="{h - 26}" font-size="11" fill="{t["text"]}" text-anchor="middle">{escape(tag)}</text>')
        x += tw + 6
    ko = "".join(f'<text x="24" y="{66 + i * 20}" font-size="13" fill="{t["value"]}">{escape(line)}</text>' for i, line in enumerate(p["ko"]))
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(p["name"])}">'
        f'<style>text{{font-family:{FONT}}}</style>'
        f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="10" fill="{t["bg"]}" stroke="{t["border"]}"/>'
        f'<rect x="24" y="0.5" width="60" height="3" rx="1.5" fill="{b["name1"]}"/>'
        f'<text x="24" y="38" font-size="16" font-weight="700" fill="{t["title"]}">{escape(p["name"])}</text>'
        f'<text x="{w - 24}" y="38" font-size="15" fill="{t["text"]}" text-anchor="end">&#8599;</text>'
        f'{ko}'
        f'<text x="24" y="{66 + len(p["ko"]) * 20 + 2}" font-size="11" fill="{t["text"]}">{escape(p["en"])}</text>'
        f'{tags}</svg>'
    )
