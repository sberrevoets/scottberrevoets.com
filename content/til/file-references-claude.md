Title: Claude can load files "lazily" or "greedily"
Date: 2026-03-20

Typically, markdown files can referenced other files by _linking_ to them: `[My
File](myfile.md)`. Claude understands this syntax, making it a nicely
portable way to reference files. When prompting in Claude Code, referencing
other files works through the @-syntax: `@path/to/file`. This loads the file
into Claude's context similar to the markdown linking.

When Claude sees the @-syntax in a markdown file, it reads it as well. But
Claude doesn't treat the markdown and @ syntaxes as equals: _linking_ to a file
_may_ cause it to read that file when it feels like it's the right time for it.
The @-syntax will immediately and unconditionally inline that file into the
prompt.

In short, the markdown linking syntax is akin to "lazy loading", whereas the
@-syntax is "greedy loading".
