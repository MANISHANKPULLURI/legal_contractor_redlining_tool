from docx import Document
from docx.shared import RGBColor
from datetime import datetime



def add_deleted_text(document, text):

    para = document.add_paragraph()

    run = para.add_run(text)

    run.font.strike = True

    run.font.color.rgb = RGBColor(
        180,
        0,
        0
    )




def add_added_text(document, text):

    para = document.add_paragraph()

    run = para.add_run(text)

    run.bold = True

    run.font.color.rgb = RGBColor(
        0,
        120,
        0
    )




def create_redline_doc(
    rewrites,
    output_path="redlined_contract.docx"
):

    document = Document()


    document.add_heading(
        "LegalContractor AI - Contract Review Report",
        level=1
    )


    document.add_paragraph(
        "AI generated contract risk analysis, recommendations and redlined improvements."
    )


    document.add_paragraph(
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    )



    for item in rewrites:


        clause_number = item.get(
            "clause_number",
            "Unknown"
        )


        original_clause = item.get(
            "original_clause",
            ""
        )


        rewritten_clause = item.get(
            "rewritten_clause",
            ""
        )


        risk_level = item.get(
            "risk_level",
            "LOW"
        )


        explanation = item.get(
            "explanation",
            ""
        )


        recommendation = item.get(
            "recommendation",
            ""
        )


        issues = item.get(
            "issues",
            []
        )




        document.add_page_break()



        document.add_heading(
            f"Clause {clause_number} - AI Legal Review",
            level=2
        )



        # =========================
        # Risk Summary
        # =========================


        document.add_heading(
            "Risk Analysis",
            level=3
        )


        document.add_paragraph(
            f"Risk Level: {risk_level}"
        )



        if issues:

            document.add_paragraph(
                "Issues Found:"
            )


            for issue in issues:


                if isinstance(issue, dict):

                    text = issue.get(
                        "issue",
                        ""
                    )

                else:

                    text = str(issue)



                document.add_paragraph(
                    f"- {text}"
                )



        if explanation:


            document.add_paragraph(
                "Explanation:"
            )


            document.add_paragraph(
                explanation
            )



        if recommendation:


            document.add_paragraph(
                "Recommendation:"
            )


            document.add_paragraph(
                recommendation
            )



        # =========================
        # Original
        # =========================


        document.add_heading(
            "Original Clause",
            level=3
        )


        document.add_paragraph(
            original_clause
        )



        # =========================
        # Redline
        # =========================


        document.add_heading(
            "Redline Changes",
            level=3
        )


        document.add_paragraph(
            "Deleted:"
        )


        add_deleted_text(
            document,
            original_clause
        )


        document.add_paragraph(
            "Added:"
        )


        add_added_text(
            document,
            rewritten_clause
        )




        # =========================
        # Final Clause
        # =========================


        document.add_heading(
            "Final Recommended Clause",
            level=3
        )


        document.add_paragraph(
            rewritten_clause
        )



    document.save(
        output_path
    )


    return output_path