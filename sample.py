from reportlab.pdfgen import canvas


pdf = canvas.Canvas("sample_contract.pdf")


text = pdf.beginText(50, 750)


content = """

SERVICE AGREEMENT


1. Termination

The company may terminate this agreement at any time without notice.


2. Liability

The vendor shall be responsible for all damages, losses and claims without any limitation of liability.


3. Confidentiality

Both parties agree to protect confidential information.


"""


for line in content.split("\n"):
    text.textLine(line)


pdf.drawText(text)

pdf.save()


print("sample_contract.pdf created")