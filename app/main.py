from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse, StreamingResponse
from pypdf import PdfReader, PdfWriter
from io import BytesIO
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

app = FastAPI(title="PDF Pages Service")

@app.get("/", response_class=HTMLResponse)
def index():
    index_file = os.path.join(STATIC_DIR, "index.html")
    if not os.path.exists(index_file):
        return "<h3>UI not found</h3>"
    with open(index_file, "r", encoding="utf-8") as f:
        return f.read()

@app.post("/convert")
async def convert_pdf(file: UploadFile = File(...)):
    input_bytes = await file.read()
    reader = PdfReader(BytesIO(input_bytes))
    writer = PdfWriter()

    A4_W, A4_H = 595, 842
    cols, rows = 2, 3
    per_page = cols * rows

    for i in range(0, len(reader.pages), per_page):
        out_page = writer.add_blank_page(width=A4_W, height=A4_H)

        for idx, src_page in enumerate(reader.pages[i:i+per_page]):
            scale_x = (A4_W / cols) / src_page.mediabox.width
            scale_y = (A4_H / rows) / src_page.mediabox.height
            scale = min(scale_x, scale_y)

            src_page.scale_by(scale)

            col = idx % cols
            row = idx // cols

            x = col * (A4_W / cols)
            y = A4_H - ((row + 1) * (A4_H / rows))

            out_page.merge_translated_page(src_page, x, y)

    output = BytesIO()
    writer.write(output)
    output.seek(0)

    return StreamingResponse(
        output,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=converted.pdf"}
    )