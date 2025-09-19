Title: Composing a resume in markdown
Date: 2025-03-15
Summary: Building a resume in markdown for improved maintainability and portability

I recently updated my resume, and after a few iterations of tweaking the same
Pages file I started more than a decade ago, I decided that I really wanted
source control to make it easier to keep track of changes and to have different
versions of the same resume. Additionally, the very consistent structure and
simplicity of a resume makes it a perfect candidate to be written in markdown,
which is a text-based format and easy to have in source control.

Some quick searching confirmed my suspicion that many people were already doing
this and that there are various tools available to make this easier. The
primary tool is [pandoc](http://pandoc.org/), which is a universal document
converter. It can convert between many different formats, including markdown and
PDF.

!!! note
    The other tool that makes for a very structured resume is [JSON
    Resume](https://jsonresume.org). It's a JSON schema with standard fields for
    common resume sections like 'experience' and 'education' that can then
    easily be themed. I found this a little too limiting and not as readable in
    plain text as markdown.

In my case, I'm converting from markdown to HTML, injecting some CSS to make it
look the way I want it to, and then converting that to PDF. LaTeX was another
option but I wasn't familiar with either LaTeX or ConTeXt and didn't want to
bother learning it just for this exercise.

Converting to HTML was generally easy.

```bash
pandoc --standalone --include-in-header resume.css --output resume.html resume.md
```

This gives a pretty good starting point even with no CSS at all. `pandoc` uses a
custom markdown dialect with some extensions and other features, which makes it
easy to add ids and classes to `<h1>`-`<h6>` elements. This is useful as it
makes applying the right style to the right element easy. The resume itself is
simple and so is the resulting HTML. `pandoc` does inject its own CSS as well,
which is easy to override in the custom CSS file.

After tweaking the CSS to my liking, the next step was to convert the HTML to
PDF format. This was a bit more complicated as there were multiple ways to do
that:

* **Safari** (or another browser): There is an export as PDF option or the
  option to print and then save as PDF. This worked but required manual steps I
  wanted to automate.
* **wkhtmltopdf**: a command line tool that converts HTML to PDF using a WebKit
  engine
* **pandoc**: can convert to PDF directly with some options that, supposedly,
  affect the final PDF output. I tried using it with `wkhtmltopdf` as its
  engine, and it can also use LaTeX or ConTeXt as an intermediate format that
  bypasses HTML generation altogether.

I struggled a bit with which to choose, as the format for all of them wasn't
quite right except for the print to PDF option in Safari. I ultimately settled
on using `wkhtmltopdf` directly (without using `pandoc` for this step), after
experimenting with these options and seeing which output I liked best.
Converting the HTML to PDF was as simple as:

```bash
wkhtmltopdf -s letter resume.html resume.pdf
```

The `-s letter` option sets the paper size to US Letter since the default is A4.
Nowadays it doesn't really matter as resumes are only ever used in digital
format so the size of the PDF doesn't really matter anyway.

I then wrapped both commands in a simple shell script to make it easier to run:

```bash
pandoc \
    --standalone \
    --include-in-header resume.css \
    --output resume.html \
    resume.md

wkhtmltopdf -s letter resume.html resume.pdf

open resume.pdf && open resume.html
```

After some modifications to the markdown, running this script will quickly
generate the HTML and PDF files and open them both so I can validate the result.

This setup ends up working pretty well for me for 3 reasons:

1. With everything in a git repo I can make changes as I like, undo them easily,
   and use all of git's features on my resume. I push the markdown, HTML, and
   PDF versions to GitHub so I always have the latest version handy in a few
   different formats.
2. The format and the content are for the most part separate, making it easier
   to focus on one or the other.
3. Since everything is now text-based and not in proprietary binary formats,
   it's also easy to overengineer this in the future by including certain
   sections when applying to different jobs, including certain information only
   when certain flags are set, differentiating between a CV and a resume, etc.
