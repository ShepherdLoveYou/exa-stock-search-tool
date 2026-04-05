"""
Report Exporter — dual Markdown + PDF output to separate folders
"""

import os
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, Optional

from .naming import ReportNaming

# Default output directories (relative to project root)
_PROJECT_ROOT = Path(__file__).parent.parent.parent
DEFAULT_MD_DIR = _PROJECT_ROOT / "research Output" / "markdown"
DEFAULT_PDF_DIR = _PROJECT_ROOT / "research Output" / "pdf"


class ReportExporter:
    """Export research reports in Markdown and PDF formats"""

    def __init__(
        self,
        md_dir: Optional[Path] = None,
        pdf_dir: Optional[Path] = None,
    ):
        self.md_dir = Path(md_dir) if md_dir else DEFAULT_MD_DIR
        self.pdf_dir = Path(pdf_dir) if pdf_dir else DEFAULT_PDF_DIR

    def _ensure_dirs(self):
        self.md_dir.mkdir(parents=True, exist_ok=True)
        self.pdf_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def export_markdown(
        self,
        content: str,
        ticker: str,
        framework: str,
        report_id: str,
        naming_pattern: Optional[str] = None,
    ) -> Path:
        """
        Save report as Markdown file.

        Returns:
            Path to the saved .md file
        """
        self._ensure_dirs()
        base = ReportNaming.generate(ticker, framework, report_id, naming_pattern)
        filename = ReportNaming.with_extension(base, "md")
        path = self.md_dir / filename
        path.write_text(content, encoding="utf-8")
        return path

    def export_pdf(
        self,
        content: str,
        ticker: str,
        framework: str,
        report_id: str,
        naming_pattern: Optional[str] = None,
    ) -> Path:
        """
        Convert Markdown content to PDF via Chromium (playwright).

        Falls back to fitz (pymupdf) if playwright/chromium is unavailable.

        Returns:
            Path to the saved .pdf file
        """
        self._ensure_dirs()
        base = ReportNaming.generate(ticker, framework, report_id, naming_pattern)
        pdf_name = ReportNaming.with_extension(base, "pdf")
        pdf_path = self.pdf_dir / pdf_name

        # Strategy 1: markdown → HTML → Chromium PDF (best quality)
        if self._try_chromium(content, pdf_path):
            return pdf_path

        # Strategy 2: fitz Story fallback
        if self._try_fitz(content, pdf_path):
            return pdf_path

        # Strategy 3: plain text dump
        self._fallback_text_pdf(content, pdf_path)
        return pdf_path

    def export_both(
        self,
        content: str,
        ticker: str,
        framework: str,
        report_id: str,
        naming_pattern: Optional[str] = None,
    ) -> Dict[str, Path]:
        """
        Export as both Markdown and PDF.

        Returns:
            Dict with keys 'markdown' and 'pdf', values are file Paths
        """
        md_path = self.export_markdown(content, ticker, framework, report_id, naming_pattern)
        pdf_path = self.export_pdf(content, ticker, framework, report_id, naming_pattern)
        return {"markdown": md_path, "pdf": pdf_path}

    # ------------------------------------------------------------------
    # PDF conversion strategies
    # ------------------------------------------------------------------

    @staticmethod
    def _try_chromium(md_content: str, pdf_path: Path) -> bool:
        """Convert Markdown → HTML → PDF using Playwright/Chromium."""
        try:
            import markdown as md_lib
            from playwright.sync_api import sync_playwright

            html_body = md_lib.markdown(
                md_content, extensions=["tables", "fenced_code", "toc"]
            )

            _, font_file, bold_file = ReportExporter._find_cjk_fonts()
            # Build font-family with preference for Microsoft YaHei
            if font_file and "msyh" in font_file.lower():
                body_font = "'Microsoft YaHei', 'PingFang SC', 'Noto Sans CJK SC', sans-serif"
            elif font_file and "simhei" in font_file.lower():
                body_font = "'SimHei', 'Microsoft YaHei', sans-serif"
            else:
                body_font = "'Microsoft YaHei', 'SimHei', 'PingFang SC', sans-serif"

            css = f"""
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: {body_font};
                font-size: 10.5pt;
                line-height: 1.8;
                color: #1a1a1a;
                padding: 0;
            }}
            h1 {{
                font-size: 22pt;
                font-weight: 700;
                color: #111;
                margin: 32px 0 16px 0;
                padding-bottom: 8px;
                border-bottom: 2.5px solid #333;
            }}
            h1:first-child {{ margin-top: 0; }}
            h2 {{
                font-size: 16pt;
                font-weight: 700;
                color: #222;
                margin: 28px 0 12px 0;
                padding-bottom: 5px;
                border-bottom: 1px solid #ddd;
            }}
            h3 {{
                font-size: 13pt;
                font-weight: 700;
                color: #333;
                margin: 20px 0 8px 0;
            }}
            h4 {{
                font-size: 11.5pt;
                font-weight: 700;
                color: #444;
                margin: 16px 0 6px 0;
            }}
            p {{
                margin: 6px 0 10px 0;
            }}
            strong {{ font-weight: 700; }}
            em {{ font-style: italic; }}
            ul, ol {{
                margin: 6px 0 10px 24px;
                padding-left: 8px;
            }}
            li {{
                margin: 3px 0;
                line-height: 1.75;
            }}
            li > ul, li > ol {{
                margin-top: 2px;
                margin-bottom: 2px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 12px 0 16px 0;
                font-size: 9.5pt;
                page-break-inside: avoid;
            }}
            th {{
                font-weight: 700;
                text-align: left;
                padding: 9px 12px;
                border: 1px solid #dee2e6;
                background-color: #f8f9fa;
                color: #333;
            }}
            td {{
                padding: 7px 12px;
                border: 1px solid #dee2e6;
                vertical-align: top;
            }}
            tr:nth-child(even) td {{
                background-color: #fafbfc;
            }}
            code {{
                background-color: #f4f4f5;
                padding: 1px 5px;
                border-radius: 3px;
                font-size: 9pt;
                font-family: 'Consolas', 'Courier New', monospace;
            }}
            pre {{
                background-color: #f8f9fa;
                padding: 14px 16px;
                border: 1px solid #e9ecef;
                border-radius: 4px;
                margin: 10px 0;
                font-size: 8.5pt;
                overflow-x: auto;
                white-space: pre-wrap;
                word-wrap: break-word;
            }}
            pre code {{
                background: none;
                padding: 0;
                border-radius: 0;
            }}
            blockquote {{
                margin: 12px 0;
                padding: 10px 16px;
                border-left: 4px solid #4a90d9;
                background-color: #f0f6ff;
                color: #333;
            }}
            blockquote p {{ margin: 4px 0; }}
            hr {{
                border: none;
                border-top: 1px solid #ddd;
                margin: 20px 0;
            }}
            a {{ color: #2563eb; text-decoration: none; }}
            """

            full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<style>{css}</style>
</head>
<body>{html_body}</body>
</html>"""

            with sync_playwright() as pw:
                browser = pw.chromium.launch(headless=True)
                page = browser.new_page()
                page.set_content(full_html, wait_until="networkidle")
                page.pdf(
                    path=str(pdf_path),
                    format="A4",
                    margin={
                        "top": "25mm",
                        "bottom": "20mm",
                        "left": "20mm",
                        "right": "20mm",
                    },
                    display_header_footer=True,
                    header_template="<span></span>",
                    footer_template=(
                        '<div style="width:100%;text-align:center;font-size:9px;color:#999;">'
                        '<span class="pageNumber"></span> / <span class="totalPages"></span>'
                        '</div>'
                    ),
                    print_background=True,
                )
                browser.close()

            return pdf_path.exists() and pdf_path.stat().st_size > 0
        except Exception:
            return False

    @staticmethod
    def _try_xhtml2pdf(md_content: str, pdf_path: Path) -> bool:
        """Convert Markdown → HTML → PDF using xhtml2pdf with CJK font."""
        try:
            import markdown as md_lib
            from xhtml2pdf import pisa
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.ttfonts import TTFont
            from reportlab.lib.fonts import addMapping

            html_body = md_lib.markdown(
                md_content, extensions=["tables", "fenced_code", "toc"]
            )

            # Register CJK fonts via reportlab (supports TTC subfontIndex)
            font_dir, font_file, bold_file = ReportExporter._find_cjk_fonts()
            font_registered = False
            if font_dir and font_file:
                regular_path = os.path.join(font_dir, font_file)
                is_ttc = font_file.lower().endswith(".ttc")
                try:
                    if is_ttc:
                        pdfmetrics.registerFont(TTFont("CJK", regular_path, subfontIndex=0))
                    else:
                        pdfmetrics.registerFont(TTFont("CJK", regular_path))
                    if bold_file:
                        bold_path = os.path.join(font_dir, bold_file)
                        if bold_file.lower().endswith(".ttc"):
                            pdfmetrics.registerFont(TTFont("CJK-Bold", bold_path, subfontIndex=0))
                        else:
                            pdfmetrics.registerFont(TTFont("CJK-Bold", bold_path))
                        addMapping("CJK", 0, 0, "CJK")       # normal
                        addMapping("CJK", 1, 0, "CJK-Bold")   # bold
                        addMapping("CJK", 0, 1, "CJK")       # italic → normal
                        addMapping("CJK", 1, 1, "CJK-Bold")   # bold-italic → bold
                    font_registered = True
                except Exception:
                    font_registered = False

            body_font = '"CJK"' if font_registered else 'sans-serif'

            css = f"""
            @page {{
                size: A4;
                margin: 2.5cm 2cm 2cm 2cm;
                @frame footer {{
                    -pdf-frame-content: footerContent;
                    bottom: 0.5cm;
                    margin-left: 2cm;
                    margin-right: 2cm;
                    height: 1cm;
                }}
            }}
            body {{
                font-family: {body_font};
                font-size: 10.5pt;
                line-height: 1.75;
                color: #1a1a1a;
            }}
            h1 {{
                font-family: {body_font};
                font-size: 20pt;
                font-weight: bold;
                color: #111;
                margin-top: 24px;
                margin-bottom: 14px;
                padding-bottom: 6px;
                border-bottom: 2px solid #333;
            }}
            h2 {{
                font-family: {body_font};
                font-size: 16pt;
                font-weight: bold;
                color: #222;
                margin-top: 20px;
                margin-bottom: 10px;
                padding-bottom: 4px;
                border-bottom: 1px solid #ddd;
            }}
            h3 {{
                font-family: {body_font};
                font-size: 13pt;
                font-weight: bold;
                color: #333;
                margin-top: 16px;
                margin-bottom: 8px;
            }}
            h4 {{
                font-family: {body_font};
                font-size: 11.5pt;
                font-weight: bold;
                color: #444;
                margin-top: 12px;
                margin-bottom: 6px;
            }}
            p {{
                margin-top: 4px;
                margin-bottom: 8px;
            }}
            ul, ol {{
                margin-top: 4px;
                margin-bottom: 8px;
                margin-left: 18px;
            }}
            li {{
                margin-top: 2px;
                margin-bottom: 2px;
                line-height: 1.7;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
                margin-bottom: 14px;
                font-size: 9.5pt;
            }}
            th {{
                font-weight: bold;
                text-align: left;
                padding: 8px 10px;
                border: 1px solid #dee2e6;
                background-color: #f8f9fa;
                color: #333;
            }}
            td {{
                padding: 6px 10px;
                border: 1px solid #dee2e6;
                vertical-align: top;
            }}
            tr {{
                -pdf-keep-in-frame-mode: shrink;
            }}
            code {{
                background-color: #f4f4f5;
                padding: 1px 4px;
                font-size: 9pt;
            }}
            pre {{
                background-color: #f8f9fa;
                padding: 12px 14px;
                border: 1px solid #e9ecef;
                margin-top: 8px;
                margin-bottom: 8px;
                font-size: 8.5pt;
                white-space: pre-wrap;
                word-wrap: break-word;
            }}
            blockquote {{
                margin: 10px 0;
                padding: 8px 14px;
                border-left: 4px solid #4a90d9;
                background-color: #f0f6ff;
                color: #333;
            }}
            hr {{
                border: none;
                border-top: 1px solid #ddd;
                margin: 16px 0;
            }}
            strong {{
                font-weight: bold;
            }}
            """

            full_html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><style>{css}</style></head>
<body>
{html_body}
<div id="footerContent" style="text-align:center; font-size:8pt; color:#999;">
    <pdf:pagenumber /> / <pdf:pagecount />
</div>
</body>
</html>"""

            with open(str(pdf_path), "wb") as out_file:
                status = pisa.CreatePDF(full_html, dest=out_file, encoding="utf-8")

            return not status.err and pdf_path.exists()
        except Exception:
            return False

    @staticmethod
    def _find_cjk_fonts() -> tuple:
        """Find CJK fonts on the system. Returns (font_dir, regular_file, bold_file).
        bold_file may be None if only regular is found."""
        import platform
        system = platform.system()
        if system == "Windows":
            fonts_dir = os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts")
            # Prefer Microsoft YaHei (modern, clean) over SimHei
            candidates = [
                ("msyh.ttc", "msyhbd.ttc"),      # Microsoft YaHei + Bold
                ("msjh.ttc", "msjhbd.ttc"),       # Microsoft JhengHei + Bold
                ("simhei.ttf", None),              # SimHei (fallback, no bold variant)
                ("simsun.ttc", None),              # SimSun (fallback)
            ]
        elif system == "Darwin":
            fonts_dir = "/System/Library/Fonts"
            candidates = [
                ("PingFang.ttc", None),
                ("STHeiti Light.ttc", None),
            ]
        else:
            fonts_dir = "/usr/share/fonts"
            candidates = [
                ("truetype/noto/NotoSansCJK-Regular.ttc", "truetype/noto/NotoSansCJK-Bold.ttc"),
                ("opentype/noto/NotoSansCJK-Regular.ttc", "opentype/noto/NotoSansCJK-Bold.ttc"),
                ("truetype/droid/DroidSansFallbackFull.ttf", None),
            ]
        for regular, bold in candidates:
            full = os.path.join(fonts_dir, regular)
            if os.path.exists(full):
                bold_file = os.path.basename(bold) if bold and os.path.exists(os.path.join(fonts_dir, bold)) else None
                return os.path.dirname(full), os.path.basename(full), bold_file
        return None, None, None

    @staticmethod
    def _find_cjk_font() -> tuple:
        """Backward-compatible wrapper. Returns (font_dir, font_filename)."""
        font_dir, regular, _ = ReportExporter._find_cjk_fonts()
        return font_dir, regular

    @staticmethod
    def _try_mdpdf(md_path: Path, pdf_path: Path) -> bool:
        try:
            result = subprocess.run(
                ["mdpdf", "-o", str(pdf_path), str(md_path)],
                capture_output=True, text=True, timeout=60,
            )
            return result.returncode == 0 and pdf_path.exists()
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False

    @staticmethod
    def _try_fitz(md_content: str, pdf_path: Path) -> bool:
        try:
            import markdown as md_lib
            import fitz  # pymupdf

            html = md_lib.markdown(md_content, extensions=["tables", "fenced_code"])

            font_dir, font_file, bold_file = ReportExporter._find_cjk_fonts()

            # Build @font-face declarations
            font_faces = ""
            if font_dir and font_file:
                font_faces += f"@font-face {{font-family: 'CJK'; src: url('{font_file}'); font-weight: normal;}}"
                if bold_file:
                    font_faces += f"@font-face {{font-family: 'CJK'; src: url('{bold_file}'); font-weight: bold;}}"
                body_font = "'CJK', -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
            else:
                body_font = "-apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"

            # Professional CSS matching the reference PDF style
            # NOTE: MuPDF CSS parser is limited — no nth-child, no comma-separated
            # selectors (e.g. "ul, ol"), no shorthand that it can't parse.
            user_css = font_faces + "\n".join([
                f"body {{ font-family: {body_font}; font-size: 10.5pt; line-height: 1.75; color: #1a1a1a; }}",
                "h1 { font-size: 22pt; font-weight: bold; color: #111; margin-top: 28px; margin-bottom: 16px; padding-bottom: 8px; border-bottom-width: 2px; border-bottom-style: solid; border-bottom-color: #333; }",
                "h2 { font-size: 17pt; font-weight: bold; color: #222; margin-top: 24px; margin-bottom: 12px; padding-bottom: 6px; border-bottom-width: 1px; border-bottom-style: solid; border-bottom-color: #ddd; }",
                "h3 { font-size: 13pt; font-weight: bold; color: #333; margin-top: 18px; margin-bottom: 8px; }",
                "h4 { font-size: 11.5pt; font-weight: bold; color: #444; margin-top: 14px; margin-bottom: 6px; }",
                "p { margin-top: 6px; margin-bottom: 10px; }",
                "strong { font-weight: bold; }",
                "ul { margin-top: 6px; margin-bottom: 10px; margin-left: 20px; padding-left: 8px; }",
                "ol { margin-top: 6px; margin-bottom: 10px; margin-left: 20px; padding-left: 8px; }",
                "li { margin-top: 3px; margin-bottom: 3px; line-height: 1.7; }",
                "table { border-collapse: collapse; width: 100%; margin-top: 12px; margin-bottom: 16px; font-size: 10pt; }",
                "th { font-weight: bold; text-align: left; padding: 10px; border: 1px solid #dee2e6; background-color: #f8f9fa; color: #333; }",
                "td { padding: 8px; border: 1px solid #dee2e6; }",
                "code { background-color: #f4f4f5; padding: 2px; font-size: 9.5pt; }",
                "pre { background-color: #f8f9fa; padding: 14px; border: 1px solid #e9ecef; margin-top: 10px; margin-bottom: 10px; }",
                "blockquote { margin-top: 12px; margin-bottom: 12px; padding: 10px; padding-left: 16px; border-left-width: 4px; border-left-style: solid; border-left-color: #4a90d9; background-color: #f0f6ff; }",
                "hr { border-top-width: 1px; border-top-style: solid; border-top-color: #ddd; margin-top: 20px; margin-bottom: 20px; }",
            ])

            full_html = (
                "<!DOCTYPE html><html><head><meta charset='utf-8'>"
                "</head><body>" + html + "</body></html>"
            )

            archive = fitz.Archive(font_dir) if font_dir else None
            if archive:
                story = fitz.Story(full_html, user_css=user_css, archive=archive)
            else:
                story = fitz.Story(full_html, user_css=user_css)
            writer = fitz.DocumentWriter(str(pdf_path))
            mediabox = fitz.paper_rect("a4")
            # Wider margins for a professional look: ~25mm left/right, ~30mm top/bottom
            where = mediabox + (72, 85, -72, -72)

            more = True
            while more:
                dev = writer.begin_page(mediabox)
                more, _ = story.place(where)
                story.draw(dev)
                writer.end_page()
            writer.close()
            return pdf_path.exists()
        except Exception:
            return False

    @staticmethod
    def _fallback_text_pdf(content: str, pdf_path: Path):
        """Last resort: write a very basic PDF with plain text lines"""
        try:
            import fitz  # pymupdf
            _, font_file = ReportExporter._find_cjk_font()
            font_dir, _ = ReportExporter._find_cjk_font()
            fontfile_path = os.path.join(font_dir, font_file) if font_dir and font_file else None

            doc = fitz.open()
            lines = content.split("\n")
            page = doc.new_page(width=595, height=842)
            y = 50
            for line in lines:
                if y > 790:
                    page = doc.new_page(width=595, height=842)
                    y = 50
                kwargs = {"fontsize": 10}
                if fontfile_path:
                    kwargs["fontfile"] = fontfile_path
                    kwargs["fontname"] = "CJK"
                page.insert_text((50, y), line, **kwargs)
                y += 14
            doc.save(str(pdf_path))
            doc.close()
        except Exception:
            # Absolute fallback: save as plain text with .pdf extension
            pdf_path.write_text(content, encoding="utf-8")
