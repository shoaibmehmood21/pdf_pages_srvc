@app.post("/convert")
async def convert_pdf(file: UploadFile = File(...)):
    input_bytes = await file.read()
    reader = PdfReader(BytesIO(input_bytes))
    writer = PdfWriter()

    cols = 2
    rows = 3
    per_page = cols * rows

    for i in range(0, len(reader.pages), per_page):
        output_page = writer.add_blank_page(width=595, height=842)  # A4

        for idx, src_page in enumerate(reader.pages[i:i+per_page]):
            scale_x = (595 / cols) / src_page.mediabox.width
            scale_y = (842 / rows) / src_page.mediabox.height
            scale = min(scale_x, scale_y)

            src_page.scale_by(scale)

            col = idx % cols
            row = idx // cols

            x = col * (595 / cols)
            y = 842 - ((row + 1) * (842 / rows))

            output_page.merge_translated_page(
                src_page,
                tx=x,
                ty=y
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
