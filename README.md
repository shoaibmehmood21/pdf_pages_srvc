# PDF N-Up Service (6 pages per page)

## Features
- Converts any PDF into 2x3 layout (6 pages per output page)
- Handles 10+ pages (10 pages -> 2 output pages)
- Returns downloadable PDF
- Ready for Railway deployment

## API
POST /convert
Form-data:
- file: PDF

Returns:
- application/pdf