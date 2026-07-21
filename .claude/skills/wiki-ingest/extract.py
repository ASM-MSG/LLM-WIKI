#!/usr/bin/env python3
"""xlsx/docx/pptx 텍스트 추출 (stdlib만 사용). 사용법: python extract.py <파일>"""
import re
import sys
import zipfile


def xml_text(data: bytes) -> str:
    # ponytail: 정식 XML 파싱 대신 태그 제거 — 서식 복원이 필요해지면 python-docx 등으로 교체
    text = re.sub(rb"<[^>]+>", b"\n", data).decode("utf-8", "ignore")
    lines = [l.strip() for l in text.splitlines()]
    return "\n".join(l for l in lines if l)


def main(path: str) -> None:
    z = zipfile.ZipFile(path)
    names = z.namelist()
    if path.endswith(".docx"):
        print(xml_text(z.read("word/document.xml")))
    elif path.endswith(".pptx"):
        for n in sorted(n for n in names if re.match(r"ppt/slides/slide\d+\.xml$", n)):
            print(f"--- {n} ---")
            print(xml_text(z.read(n)))
    elif path.endswith(".xlsx"):
        shared = []
        if "xl/sharedStrings.xml" in names:
            shared = re.findall(r"<t[^>]*>([^<]*)</t>", z.read("xl/sharedStrings.xml").decode("utf-8", "ignore"))
        print("\n".join(shared))
        for n in sorted(n for n in names if n.startswith("xl/worksheets/sheet")):
            print(f"--- {n} ---")
            print(xml_text(z.read(n)))
    else:
        sys.exit(f"지원하지 않는 포맷: {path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("사용법: python extract.py <파일>")
    main(sys.argv[1])
