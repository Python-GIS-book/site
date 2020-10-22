# How to use this book

Here we describe the typographical and formatting conventions used in this book.

## General text formatting

Normal text is divided into sections and subsections using headings.
The top-level heading (H1) is reserved for page titles (major section titles).
Heading levels 2 and 3 are used for internal sections and sub-sections.
Heading level 4 should be used for "Check your understanding" sub-sections.

Text formatting conventions (commands/code in `monospace`, etc.)

### Glossary term

Important terms should be included in italics using the glossary.
Glossary terms can be added with the format

```
*{term}`Glossary term`*
```

where "Glossary term" is the item listed in the glossary at `back-matter/glossary.md`.
It is also possible to have different text listed when linking to a glossary item, such as 

```
*{term}`My glossary item <item>`*
```

where the link to the glossary entry "item" has the displayed text "My glossary item".

References

URLs should use footnotes such as[^url1].
Footnotes are formatted as `[^footnote]` when placed in the text.
They are enclosed in square brackets and start with the `^` character.
At the end of the document, the footnote definitions can be given in the form

```
[^footnote]: Footnote text and or URL with the form <https://jupyter.org>. Note the angled brackets `<` and `>` enclose the URL to autolink them.
```

## Special text formatting blocks

- Code blocks
- Admonitions (let's not use more than 2-3, if possible)

```{note}
This is a hint. It expands on the main text or indicates additional information not included in the main text. Additional reference material or differences from past topics, for example.
```

```{tip}
This is a tip. Tips should be used for helpful reminders or suggested use cases.
```

```{warning}
This is a warning. This is text that warns of potential for problems if it is ignored. This could be used to indicate unexpected behavior, such as needing to create copies of dataframes to avoid modifying source dataframes.
```

## Footnotes

[^url1]: https://python.org
