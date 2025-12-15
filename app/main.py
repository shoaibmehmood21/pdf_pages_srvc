from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO

app = FastAPI(title="PDF N-Up Service")

@app.post("/convert")
async def convert_pdf(file: UploadFile = File(...)):
    input_bytes = await file.read()
    reader = PdfReader(BytesIO(input_bytes))
    writer = PdfWriter()

    pages = reader.pages
    width, height = A4
    cols = 2
    rows = 3
    per_page = cols * rows

    for i in range(0, len(pages), per_page):
        packet = BytesIO()
        c = canvas.Canvas(packet, pagesize=A4)
        subset = pages[i:i+per_page]

        for idx, page in enumerate(subset):
            r = idx // cols
            col = idx % cols
            x = col * (width / cols)
            y = height - ((r + 1) * (height / rows))

            page.scaleBy((width/cols) / page.mediabox.width)
            page.mergeTranslatedPage(page, x, y)

        c.save()
        packet.seek(0)
        new_reader = PdfReader(packet)
        writer.add_page(new_reader.pages[0])

    output = BytesIO()
    writer.write(output)
    output.seek(0)

    return StreamingResponse(
        output,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=converted.pdf"}
    )