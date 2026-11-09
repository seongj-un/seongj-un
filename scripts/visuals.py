"""Header and featured-project cards for the profile README (GitHub-native look)."""

from xml.sax.saxutils import escape

FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI','Apple SD Gothic Neo','Malgun Gothic','Noto Sans KR','Noto Sans',Helvetica,Arial,sans-serif"

# GitHub's own link blue, so the cards read like part of the page
LINK = {"light": "#0969da", "dark": "#4493f8"}

PROJECTS = [
    {
        "name": "farero",
        "url": "https://github.com/farero-dev/farero-dev.github.io",
        "ko": ["AI 코딩 에이전트의 권한 요청을 노치에서", "승인하는 macOS 앱. MCP 게이트웨이·감사 로그"],
        "tags": ["Go", "Swift", "MCP", "SQLite"],
    },
    {
        "name": "hermes-headroom",
        "url": "https://github.com/seongj-un/hermes-headroom",
        "ko": ["작은 서버에서도 에이전트가 죽지 않도록", "무거운 작업을 줄 세우고 메모리를 제한"],
        "tags": ["Python", "systemd", "Plugin"],
    },
    {
        "name": "ev-charge-time",
        "url": "https://github.com/seongj-un/ev-charge-time",
        "ko": ["전기차를 가장 싸게 충전할 시간을 추천.", "빛가람 AI·ICT 경진대회 출품작"],
        "tags": ["FastAPI", "PostgreSQL", "TypeScript"],
    },
    {
        "name": "PairPay",
        "url": "https://github.com/seongj-un/duri",
        "ko": ["커플 둘이 쓰는 공동생활비·데이트비용", "정산 웹앱 백엔드"],
        "tags": ["Kotlin", "Spring Boot 4", "PostgreSQL"],
    },
    {
        "name": "dev-ops-study",
        "url": "https://github.com/seongj-un/dev-ops-study",
        "ko": ["URL 단축 API로 CI/CD·쿠버네티스·", "GitOps·관측성을 직접 실습"],
        "tags": ["Kotlin", "Kubernetes", "Argo CD", "Helm"],
    },
    {
        "name": "n8n-obsidian-rag",
        "url": "https://github.com/seongj-un/n8n-obsidian-rag",
        "ko": ["옵시디언 노트를 근거로 디스코드에서 답하는", "RAG 봇. 골든 60문항으로 품질 측정"],
        "tags": ["n8n", "RAG", "Discord"],
    },
]


def header_svg(t, theme, w=708, h=120):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" '
        f'aria-label="Seongjun Park, Backend Developer"><style>text{{font-family:{FONT}}}</style>'
        f'<text x="0" y="52" font-size="38" font-weight="700" letter-spacing="-1" fill="{t["title"]}">Seongjun Park</text>'
        f'<text x="2" y="86" font-size="16" fill="{t["text"]}">박성준  ·  Backend Developer  ·  Daedeok Software Meister High School</text>'
        f'<rect x="2" y="104" width="40" height="3" rx="1.5" fill="{LINK[theme]}"/></svg>'
    )


def project_svg(p, t, theme, w=350, h=130):
    lines = "".join(f'<text x="20" y="{60 + i * 19}" font-size="13" fill="{t["value"]}">{escape(line)}</text>'
                    for i, line in enumerate(p["ko"]))
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" '
        f'aria-label="{escape(p["name"])}"><style>text{{font-family:{FONT}}}</style>'
        f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="6" fill="{t["bg"]}" stroke="{t["border"]}"/>'
        f'<text x="20" y="34" font-size="15" font-weight="600" fill="{LINK[theme]}">{escape(p["name"])}</text>'
        f'{lines}'
        f'<text x="20" y="{h - 18}" font-size="12" fill="{t["text"]}">{escape("  ·  ".join(p["tags"]))}</text></svg>'
    )
