#!/usr/bin/env python3
import json
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "profile.config.json"
TEMPLATE_PATH = ROOT / "README.template.md"
OUTPUT_PATH = ROOT / "README.md"


def url_encode(text: str) -> str:
    return urllib.parse.quote(str(text), safe="")


def build_tech_stack_html(tech_stack):
    blocks = []
    for group in tech_stack:
        lines = [f"**{group['title']}**", ""]
        badges = []
        for item in group["items"]:
            img = f'<img src="{item["badge"]}" alt="{item["name"]}" />'
            if item.get("url"):
                img = f'<a href="{item["url"]}" target="_blank">{img}</a>'
            badges.append(img)
        lines.append("\n".join(badges))
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks)


def build_socials_html(socials):
    links = []
    for s in socials:
        links.append(
            f'<a href="{s["url"]}" target="_blank">\n'
            f'  <img src="{s["badge"]}" alt="{s["name"]}" />\n'
            f'</a>'
        )
    return "\n".join(links)


def main():
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    template = TEMPLATE_PATH.read_text(encoding="utf-8")

    typing_lines = ";".join(
        url_encode(line) for line in config["typing_lines"]
    )

    replacements = {
        "{{GITHUB_USERNAME}}": config.get("github_username", "YOUR_USERNAME"),
        "{{TITLE_ENCODED}}": url_encode(config["title"]),
        "{{SUBTITLE_ENCODED}}": url_encode(config["subtitle"]),
        "{{FONT_COLOR}}": config.get("font_color", "ffffff"),
        "{{TYPING_COLOR}}": config.get("typing_color", "BB86FC"),
        "{{TYPING_LINES_ENCODED}}": typing_lines,
        "{{TECH_STACK_HTML}}": build_tech_stack_html(config["tech_stack"]),
        "{{SOCIAL_LINKS_HTML}}": build_socials_html(config["socials"]),
    }

    for key, value in replacements.items():
        template = template.replace(key, value)

    OUTPUT_PATH.write_text(template, encoding="utf-8")
    print("README.md 已生成")


if __name__ == "__main__":
    main()