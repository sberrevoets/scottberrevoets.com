Title: git can tell you ignored files, and why
Date: 2026-02-10

Today I created a new file at `./Resources/Environment.xcconfig`, but git didn't
pick up on the file and didn't show it in `git status`. I suspected the file was
gitignored, but nothing in my `.gitignore` was obviously excluding this file.
`git status --ignored` adds a section in to the normal status output that lists
all the ignored files. My file was in it, but I still didn't know why.

`git check-ignore` as a bare command confirms the ignored status of the passed
in file, but adding the `-v` flag indicates the _source_ of the ignore. I ran
`git check-ignore -v Resources/Environment.xcconfig` and the exact line number
in gitignore showed what caused the file to be ignored.

In my case, a different Environment.xcconfig existed before and had been
removed from the repo, but not from gitignore so it caused the new file to be
ignored as well.
