from docx import Document


def create_redline_doc(
    rewrites,
    output_path="redlined_contract.docx"
):

    document = Document()


    document.add_heading(
        "AI Contract Review - Redline",
        level=1
    )


    for item in rewrites:


        document.add_heading(
            f"Clause {item['clause_number']}",
            level=2
        )


        document.add_paragraph(
            "Original Clause:"
        )


        document.add_paragraph(
            item["original_clause"]
        )


        document.add_paragraph(
            "Suggested Revision:"
        )


        document.add_paragraph(
            item["rewritten_clause"]
        )


    document.save(
        output_path
    )


    return output_path