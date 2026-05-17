// ieee.typ — IEEE conference-style two-column template for Typst

#let ieee-paper(
  title:    "",
  authors:  (),   // array of (name, affiliation, email)
  abstract: [],
  keywords: (),
  body,
) = {

  // ---- Document metadata ------------------------------------------------
  set document(title: title)

  // ---- Page layout ------------------------------------------------------
  set page(
    paper:  "us-letter",
    margin: (x: 0.71in, top: 0.75in, bottom: 1.0in),
  )

  // ---- Typography -------------------------------------------------------
  set text(
    font:   ("Times New Roman", "Times", "Nimbus Roman"),
    size:   10pt,
    lang:   "en",
  )
  set par(
    justify:  true,
    leading:  0.55em,
    spacing:  0.8em,
  )

  // ---- Headings ---------------------------------------------------------
  show heading.where(level: 1): it => {
    v(0.8em, weak: true)
    set text(size: 10pt, weight: "bold")
    upper(it.body)
    v(0.4em, weak: true)
  }
  show heading.where(level: 2): it => {
    v(0.6em, weak: true)
    set text(size: 10pt, style: "italic", weight: "bold")
    it.body
    v(0.3em, weak: true)
  }

  // ---- Figure & table numbering -----------------------------------------
  set figure(numbering: "1")
  show figure.where(kind: table): set figure(supplement: "TABLE",
                                              numbering: "I")
  show figure.where(kind: image): set figure(supplement: "Fig.",
                                              numbering: "1")

  set figure.caption(separator: ". ")
  show figure.where(kind: table): set figure.caption(position: top)

  // ---- Links ------------------------------------------------------------
  show link: it => underline(it)

  // ---- Title block (single column) -------------------------------------
  align(center)[
    #v(0.5em)
    #text(size: 14pt, weight: "bold")[#title]
    #v(0.6em)
    #grid(
      columns: range(authors.len()).map(_ => 1fr),
      gutter: 1em,
      ..authors.map(a => align(center)[
        #text(size: 10pt)[#a.name] \
        #text(size: 9pt, style: "italic")[#a.affiliation] \
        #text(size: 9pt)[#a.email]
      ])
    )
    #v(0.8em)
  ]

  // ---- Abstract block (single column) ----------------------------------
  block(width: 100%, inset: (x: 0pt))[
    #set text(size: 9pt)
    #set par(justify: true)
    *Abstract*—#abstract
    #v(0.4em)
    *Index Terms*—#keywords.join(", ")
  ]

  v(0.8em)
  line(length: 100%, stroke: 0.5pt)
  v(0.6em)

  // ---- Two-column body -------------------------------------------------
  columns(2, gutter: 0.25in)[
    #body
  ]
}

// Helper: span a figure across both columns
#let wide-figure(content) = {
  place(
    top,
    float: true,
    scope: "parent",
    content,
  )
}
