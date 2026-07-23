# -*- coding: utf-8 -*-

from pathlib import Path
import subprocess
import tempfile
import time

from core.ruby_converter import text_file_to_paragraphs
from core.html_builder import build_html


def find_edge_path() -> Path | None:
    candidates = [
        Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
        Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
    ]

    for path in candidates:
        if path.exists():
            return path

    return None


def normalize_windows_path(path_text: str) -> Path:
    path_text = path_text.strip().strip('"').replace("￥", "\\").replace("¥", "\\")
    return Path(path_text).resolve()


def wait_for_pdf(output_pdf: Path, timeout_seconds: int = 60) -> bool:
    deadline = time.time() + timeout_seconds

    while time.time() < deadline:
        try:
            if output_pdf.exists() and output_pdf.stat().st_size > 0:
                return True
        except OSError:
            pass

        time.sleep(0.5)

    return False


def generate_pdf(txt_path: str, output_pdf: str, cfg: dict) -> None:
    txt_path = normalize_windows_path(txt_path)
    output_pdf = normalize_windows_path(output_pdf)

    if not txt_path.exists():
        raise FileNotFoundError(f"输入文件不存在：{txt_path}")

    edge_path = find_edge_path()
    if not edge_path:
        raise FileNotFoundError("未找到 Microsoft Edge")

    content = text_file_to_paragraphs(txt_path)
    html_content = build_html(content, cfg, preview=False)

    output_pdf.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="ruby_pdf_", dir=output_pdf.parent, ignore_cleanup_errors=True) as temp_dir:
        temp_path = Path(temp_dir)
        temp_html = temp_path / "print.html"
        edge_profile = temp_path / "edge-profile"

        temp_html.write_text(html_content, encoding="utf-8")

        cmd = [
            str(edge_path),
            "--headless=new",
            "--disable-gpu",
            "--disable-extensions",
            "--no-first-run",
            "--no-default-browser-check",
            "--no-pdf-header-footer",
            "--print-to-pdf-no-header",
            f"--user-data-dir={str(edge_profile)}",
            f"--print-to-pdf={str(output_pdf)}",
            temp_html.as_uri(),
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

        if result.returncode != 0:
            raise RuntimeError(
                "Edge 生成 PDF 失败。\n\n"
                f"stdout:\n{result.stdout}\n\n"
                f"stderr:\n{result.stderr}"
            )

        if wait_for_pdf(output_pdf):
            return

    if output_pdf.exists():
        return

    raise RuntimeError(f"PDF 未生成：{output_pdf}")
