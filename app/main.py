from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from pypdf import PdfReader, PdfWriter, Transformation
from io import BytesIO

app = FastAPI()

A4_WIDTH = 595
A4_HEIGHT = 842

@app.post("/convert")
async def convert_pdf(file: UploadFile = File(...)):
    input_bytes = await file.read()

    reader = PdfReader(BytesIO(input_bytes))
    writer = PdfWriter()

    cols = 2
    rows = 3
    per_page = cols * rows

    for i in range(0, len(reader.pages), per_page):
        output_page = writer.add_blank_page(
            width=A4_WIDTH,
            height=A4_HEIGHT
        )

        subset = reader.pages[i:i + per_page]

        for idx, src_page in enumerate(subset):
            col = idx % cols
            row = idx // cols

            cell_width = A4_WIDTH / cols
            cell_height = A4_HEIGHT / rows

            scale_x = cell_width / src_page.mediabox.width
            scale_y = cell_height / src_page.mediabox.height
            scale = min(scale_x, scale_y)

            x = col * cell_width
            y = A4_HEIGHT - ((row + 1) * cell_height)

            transform = (
                Transformation()
                .scale(scale)
                .translate(x, y)
            )

            output_page.merge_transformed_page(
                src_page,
                transform
            )

    output = BytesIO()
    writer.write(output)
    output.seek(0)

    return StreamingResponse(
        output,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=converted.pdf"
        }
    )
