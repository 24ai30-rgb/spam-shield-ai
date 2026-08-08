import hashlib
import os
import uuid
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from app.core.config import settings


# -------------------------------------------------------
# PDF REPORT SERVICE
# -------------------------------------------------------

class PDFReportService:

    def __init__(self):

        os.makedirs(
            settings.REPORT_DIR,
            exist_ok=True,
        )

        self.styles = getSampleStyleSheet()

        self.title_style = ParagraphStyle(
            "TitleStyle",
            parent=self.styles["Title"],
            alignment=TA_CENTER,
            fontSize=28,
            textColor=HexColor("#0F172A"),
            spaceAfter=20,
        )

        self.heading_style = ParagraphStyle(
            "Heading",
            parent=self.styles["Heading2"],
            fontSize=16,
            textColor=HexColor("#2563EB"),
            spaceBefore=10,
            spaceAfter=10,
        )

        self.body_style = ParagraphStyle(
            "Body",
            parent=self.styles["BodyText"],
            fontSize=10,
            leading=18,
        )

    # -------------------------------------------------------

    def generate(
        self,
        scan_id: str,
        verdict_data: dict,
    ):

        filename = (
            f"{scan_id}_"
            f"{uuid.uuid4().hex[:8]}.pdf"
        )

        filepath = os.path.join(
            settings.REPORT_DIR,
            filename,
        )

        doc = SimpleDocTemplate(
            filepath,
            pagesize=A4,
            rightMargin=1.5 * cm,
            leftMargin=1.5 * cm,
            topMargin=1.5 * cm,
            bottomMargin=1.5 * cm,
        )

        story = []

        # ====================================================
        # COVER PAGE
        # ====================================================

        story.append(
            Paragraph(
                "🛡 Spam Shield AI",
                self.title_style,
            )
        )

        story.append(
            Paragraph(
                "CYBER THREAT INVESTIGATION REPORT",
                ParagraphStyle(
                    "Cover",
                    parent=self.styles["Heading1"],
                    alignment=TA_CENTER,
                    fontSize=20,
                    textColor=HexColor("#DC2626"),
                ),
            )
        )

        story.append(Spacer(1, 0.7 * cm))

        verdict = verdict_data["verdict_label"].upper()

        score = verdict_data["risk_score"]

        confidence = round(
            verdict_data["confidence_score"] * 100,
            1,
        )

        category = (
            verdict_data.get("scam_category") or "Unknown"
        )

        cover_data = [
            ["Case ID", scan_id],
            [
                "Generated",
                datetime.now().strftime("%d %B %Y %H:%M:%S"),
            ],
            ["Risk Score", f"{score}/100"],
            ["Verdict", verdict],
            ["AI Confidence", f"{confidence} %"],
            ["Scam Category", category],
        ]

        table = Table(
            cover_data,
            colWidths=[5 * cm, 10 * cm],
        )

        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), HexColor("#0F172A")),
                    ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                    ("BACKGROUND", (0, 0), (0, -1), HexColor("#E2E8F0")),
                ]
            )
        )

        story.append(table)

        story.append(Spacer(1, 0.7 * cm))

        story.append(
            Paragraph(
                """
This report was generated automatically by
Spam Shield AI Multi-Agent Cyber Defense Platform.

The analysis combines:

- WHOIS Intelligence

- SSL Certificate Analysis

- Google Safe Browsing

- Threat Intelligence

- Gemini AI Reasoning

- Multi-Agent Risk Aggregation
                """,
                self.body_style,
            )
        )

        story.append(PageBreak())

        # ====================================================
        # INVESTIGATION SUMMARY
        # ====================================================

        story.append(
            Paragraph(
                "INVESTIGATION SUMMARY",
                self.heading_style,
            )
        )

        story.append(
            Paragraph(
                verdict_data["explanation_summary"],
                self.body_style,
            )
        )

        story.append(Spacer(1, 0.4 * cm))

        # ====================================================
        # TARGET INFORMATION
        # ====================================================

        story.append(
            Paragraph(
                "TARGET INFORMATION",
                self.heading_style,
            )
        )

        target = verdict_data.get("target_information", {})

        target_table = Table(
            [
                ["Input Type", target.get("input_type", "Unknown")],
                ["Target", target.get("target", "N/A")],
                ["Domain", target.get("domain", "N/A")],
                ["Protocol", target.get("scheme", "N/A")],
                ["Registrar", target.get("registrar", "Unknown")],
                ["Country", target.get("country", "Unknown")],
                ["Domain Age", target.get("age", "Unknown")],
                ["SSL Status", target.get("ssl", "Unknown")],
                ["Google Safe Browsing", target.get("safe_browsing", "Unknown")],
                ["Threat Intelligence", target.get("threat_intel", "Unknown")],
            ],
            colWidths=[5 * cm, 10 * cm],
        )

        target_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (0, -1), HexColor("#E2E8F0")),
                    ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )

        story.append(target_table)

        story.append(Spacer(1, 0.5 * cm))

        # ====================================================
        # AGENT ANALYSIS
        # ====================================================

        story.append(
            Paragraph(
                "MULTI-AGENT ANALYSIS",
                self.heading_style,
            )
        )

        agent_rows = [
            [
                "Agent",
                "Score",
                "Confidence",
                "Contribution",
            ]
        ]

        for agent in verdict_data["contributing_agents"]:

            agent_rows.append(
                [
                    agent["agent"],
                    str(agent["raw_score"]),
                    str(round(agent["confidence"] * 100)) + "%",
                    str(agent["contribution"]),
                ]
            )

        agent_table = Table(
            agent_rows,
            colWidths=[7 * cm, 2 * cm, 3 * cm, 3 * cm],
        )

        agent_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), HexColor("#2563EB")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                    ("BACKGROUND", (0, 1), (-1, -1), HexColor("#F8FAFC")),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )

        story.append(agent_table)

        story.append(Spacer(1, 0.5 * cm))

        # ====================================================
        # KEY EVIDENCE
        # ====================================================

        story.append(
            Paragraph(
                "KEY DIGITAL EVIDENCE",
                self.heading_style,
            )
        )

        evidence_rows = [
            [
                "Signal",
                "Description",
                "Severity",
            ]
        ]

        for item in verdict_data["key_evidence"]:

            evidence_rows.append(
                [
                    item.get("signal", ""),
                    item.get("description", ""),
                    item.get("severity", ""),
                ]
            )

        evidence_table = Table(
            evidence_rows,
            colWidths=[5 * cm, 8 * cm, 3 * cm],
        )

        evidence_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), HexColor("#DC2626")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ("BACKGROUND", (0, 1), (-1, -1), HexColor("#FEF2F2")),
                ]
            )
        )

        story.append(evidence_table)

        story.append(PageBreak())

        # ====================================================
        # AI REASONING
        # ====================================================

        story.append(
            Paragraph(
                "AI REASONING CHAIN",
                self.heading_style,
            )
        )

        for i, step in enumerate(
            verdict_data["reasoning_chain"],
            start=1,
        ):
            story.append(
                Paragraph(
                    f"<b>{i}.</b> {step}",
                    self.body_style,
                )
            )

        story.append(Spacer(1, 0.5 * cm))

        # ====================================================
        # RECOMMENDED ACTIONS
        # ====================================================

        story.append(
            Paragraph(
                "RECOMMENDED ACTIONS",
                self.heading_style,
            )
        )

        for action in verdict_data["recommended_actions"]:
            story.append(
                Paragraph(
                    f"• {action}",
                    self.body_style,
                )
            )

        story.append(PageBreak())

        # ====================================================
        # FORENSIC METADATA
        # ====================================================

        story.append(
            Paragraph(
                "FORENSIC REPORT DETAILS",
                self.heading_style,
            )
        )

        report_hash = hashlib.sha256(
            (
                scan_id
                + str(verdict_data["risk_score"])
                + verdict_data["verdict_label"]
            ).encode()
        ).hexdigest()

        metadata = [
            ["Case ID", scan_id],
            ["Report Version", "Spam Shield AI v2.0"],
            ["Generated", datetime.now().strftime("%d-%m-%Y %H:%M:%S")],
            ["SHA256 Report Hash", report_hash],
            ["Risk Score", str(verdict_data["risk_score"])],
            ["Verdict", verdict_data["verdict_label"].upper()],
        ]

        meta_table = Table(
            metadata,
            colWidths=[5 * cm, 10 * cm],
        )

        meta_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (0, -1), HexColor("#E2E8F0")),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )

        story.append(meta_table)

        story.append(Spacer(1, 0.7 * cm))

        # ====================================================
        # DIGITAL SIGNATURE
        # ====================================================

        story.append(
            Paragraph(
                "DIGITAL AUTHENTICATION",
                self.heading_style,
            )
        )

        story.append(
            Paragraph(
                """
<b>System:</b> Spam Shield AI<br/><br/>

<b>Analysis Engine:</b> Multi-Agent Detection System<br/><br/>

<b>Authentication:</b> Automatically generated by the Spam Shield AI
platform. This report has not been manually modified after generation.
""",
                self.body_style,
            )
        )

        story.append(Spacer(1, 0.7 * cm))

        # ====================================================
        # QR PLACEHOLDER
        # ====================================================

        story.append(
            Paragraph(
                "REPORT VERIFICATION",
                self.heading_style,
            )
        )

        story.append(
            Paragraph(
                """
QR verification can be enabled in future versions to allow
investigators to verify report authenticity.

Verification ID:
<b>{}</b>
""".format(scan_id),
                self.body_style,
            )
        )

        story.append(Spacer(1, 1 * cm))

        # ====================================================
        # DISCLAIMER
        # ====================================================

        story.append(
            Paragraph(
                "LEGAL DISCLAIMER",
                self.heading_style,
            )
        )

        story.append(
            Paragraph(
                """
This report was generated automatically using Spam Shield AI's
multi-agent cyber threat detection framework.

It is intended as a decision-support and digital forensic aid.
The results should be reviewed together with additional evidence
before legal or financial decisions are made.

Spam Shield AI does not guarantee that every malicious activity
will be detected, nor that every suspicious activity is malicious.
""",
                self.body_style,
            )
        )

        story.append(Spacer(1, 1 * cm))

        # ====================================================
        # FOOTER
        # ====================================================

        story.append(
            Paragraph(
                "<b>Spam Shield AI</b><br/>"
                "Cyber Threat Intelligence Platform<br/>"
                "Hackathon Edition 2026",
                ParagraphStyle(
                    "Footer",
                    parent=self.styles["Normal"],
                    alignment=TA_CENTER,
                    textColor=HexColor("#64748B"),
                    fontSize=9,
                ),
            )
        )

        # ====================================================
        # BUILD PDF
        # ====================================================

        doc.build(story)

        return filepath


pdf_report_service = PDFReportService()