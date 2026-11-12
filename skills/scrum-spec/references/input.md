# Preparing input

Read this file in step 0 and step 1 before summarizing the input.

## Use only what is in the input

- Every item in In Scope, Out of Scope and Backbone must trace back to the input · Write the source in Reference, e.g. "PDF pages 2–3", "frames C.1–C.4" or "user's note"
- Long input (many pages, or a whole board): first extract the exact text of the parts you use, then summarize from that text only · Cut anything with no supporting text, or make it an `[ask]`
- Input conflicts with the code or glossary: point it out with the path, then ask which side to follow

## PDF

Try reading it with Read first. If the file is too large, extract the text with:

```bash
pdftotext -layout "<file.pdf>" "<temp folder>/input.txt"
```

- If `pdftotext` is missing, ask the user to install poppler themselves (instructions are in the skill's `README.md`) or to copy and paste the text · Do not install it yourself
- A board is often one huge page. Crop only the part you need. Do not render the whole page:

```bash
# find word coordinates with: pdftotext -bbox "<file.pdf>" "<temp folder>/bbox.html"
pdftoppm -q -r 36 -x <x> -y <y> -W <width> -H <height> -png "<file.pdf>" "<temp folder>/crop"
```

- If the board has several tickets, summarize only the one the user named. If they did not name one, ask first.

## Languages whose characters drop out of PDFs

Text extracted from a PDF in a language that uses combining marks (for example Thai, Lao, Khmer, Devanagari) often loses vowel or tone marks. For example, Thai "ห้องประชุม" may come out as "หองประชม".

- Fill a mark back in only when the word has a single possible reading, and check the words in key parts (scope, team notes, ticket names) by rendering that part as an image and looking at it
- Show every word you filled in yourself in chat as the line `Words I filled in: <word>, <word>` for the user to check · Ask about any proper name you are unsure of

## Images and links

- Images (PNG, JPG): open them with Read directly
- Design tool links (e.g. Figma, Miro): cannot be opened. Ask the user to export to PDF or an image
- Do not copy customer personal data, passwords or tokens from the input into the docs
