from pypdf import PdfReader
from docx import Document


def load_document(file_path):

    if file_path.endswith(".pdf"):

        return load_pdf(file_path)


    elif file_path.endswith(".docx"):

        return load_docx(file_path)


    elif file_path.endswith(".txt"):

        return load_txt(file_path)


    else:

        raise ValueError(
            "Unsupported file format"
        )



def load_pdf(file_path):

    reader = PdfReader(file_path)


    text = ""


    for page in reader.pages:

        extracted = page.extract_text()

        if extracted:

            text += extracted + "\n"


    return text



def load_docx(file_path):

    document = Document(file_path)


    text = "\n".join(
        [
            paragraph.text
            for paragraph in document.paragraphs
        ]
    )


    return text



def load_txt(file_path):

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()