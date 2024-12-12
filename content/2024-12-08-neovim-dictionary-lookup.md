Title: Looking up words in a dictionary with Neovim
Date: 2024-12-08
Summary: Configuring Neovim to enable a quick dictionary lookup for words under the cursor

When writing code in neovim, I frequently use `K` to look up documentation,
function signatures, variable definitions, etc. In markdown files that doesn't
make too much sense, but I wanted to use it to look up words in the dictionary
instead. This didn't appear to be possible out of the box but the power of
(neo)vim is its extensibility so I decided to build it myself.

The steps to build this roughly were:

1. Write a dictionary lookup tool
2. Parse this tool's output and show it in neovim
3. Configure neovim's `K` functionality

## `dict`

`dict` seemed like an appropriate, easy name to look up a word in the
dictionary. As I'm a macOS user I first wanted to use the built-in dictionary
through
[`pyobjc-framework-CoreServices`](https://gist.github.com/lambdamusic/bdd56b25a5f547599f7f)
but `DCSCopyTextDefinition` doesn't return dictionary entries in a
well-structured or consistent way, so I ultimately decided to write a quick
lookup using [dictionaryapi.dev](https://dictionaryapi.dev). I also added some
other formatting and ANSI coloring to improve the CLI output:

```python
#!/usr/bin/env python3

import requests
import argparse

_TERMINAL_RESET = "\033[0m"
_TERMINAL_BOLD = "\033[1m"
_TERMINAL_DIM = "\033[2m"
_TERMINAL_RED = "\033[91m"
_TERMINAL_GREEN = "\033[92m"
_TERMINAL_BLUE = "\033[94m"


def _fetch_word_definition(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)

    # Handle API errors
    if response.status_code != 200:
        return None

    return response.json()


def _format_definition_output(word_data):
    if not word_data:
        return f"{_TERMINAL_RED}error: word not found{_TERMINAL_RESET}"

    word = word_data[0]["word"]
    meanings = word_data[0].get("meanings", [])

    output = f"{_TERMINAL_GREEN}{_TERMINAL_BOLD}{word}{_TERMINAL_RESET}\n"

    for part_of_speech in meanings:
        pos = part_of_speech["partOfSpeech"]
        output += f"\n{_TERMINAL_BLUE}{pos}{_TERMINAL_RESET}"

        synonyms = ", ".join(part_of_speech["synonyms"])
        output += (
            f"  {_TERMINAL_DIM}({synonyms}){_TERMINAL_RESET}"
            if synonyms
            else ""
        )
        output += "\n"

        for i, definition in enumerate(part_of_speech["definitions"], 1):
            definition_text = definition.get("definition", "N/A")
            example = definition.get("example", "")
            output += f"  {i}. {definition_text}"
            if example:
                output += f" (e.g., {example})"
            output += "\n"

    return output


def _get_word_definition(word):
    word_data = _fetch_word_definition(word)
    return _format_definition_output(word_data)


def main():
    parser = argparse.ArgumentParser(
        description="Fetch word definitions from API dictionary.dev."
    )
    parser.add_argument("word", help="Word to look up")
    args = parser.parse_args()

    word = args.word
    print(_get_word_definition(word))


if __name__ == "__main__":
    main()
```

This file needs to be in the `PATH` which I did by putting it in
`~/.bin/dict.py` and setting `export PATH="$HOME/.bin:$PATH"`.

`dict ambiguous` now gives a nicely formatted definition:

![Dictionary lookup of the word ambiguous in the
terminal](/images/dictionary-lookup-cli.png)


## Neovim integration

I wanted to invoke `dict` using `K` passing in the word under the cursor as the
trigger and show the output in a popup window. Other than the plain vim
configuration this required some text manipulation so I put all that in
`~/.vim/plugin/dictionary.lua`:

```lua
-- Create a new buffer with the given message and apply ANSI highlighting
local function create_buf(message)
  local buf = vim.api.nvim_create_buf(false, true)

  local lines = vim.split(message, "\n", { plain = true })
  for i, line in ipairs(lines) do
    local stripped = line:gsub("\27%[[0-9;]+m", "")
    vim.api.nvim_buf_set_lines(buf, i - 1, i, false, { stripped })
    apply_ansi_highlighting(buf, i - 1, line)
  end

  return buf
end

-- Show a popup window with the given buffer
local function show_popup(buf)
  vim.g.popup_window = vim.api.nvim_open_win(buf, false, {
    relative = "cursor",
    width = 100,
    height = 15,
    row = 1,
    col = 0,
    anchor = "NW",
    style = "minimal",
    border = "single",
  })
end

-- Close the popup window
function ClosePopup()
  local window = vim.g.popup_window
  if vim.g.popup_window and vim.api.nvim_win_is_valid(window) then
    vim.api.nvim_win_close(window, true)
    vim.g.popup_window = nil
  end
end

-- Look up the definition of the word under the cursor
function DictionaryLookup()
  local word = vim.fn.expand("<cword>")
  local file = assert(io.popen("dict " .. word, "r"))
  local definition = assert(file:read("*a"))
  file:close()
  show_popup(create_buf(definition))
end
```

This creates 2 functions, `DictionaryLookup()` and `ClosePopup()` that show and
dismiss the popup, stripping the ANSI codes from the output as they were
rendered raw in the popup.

However, note the call to `apply_ansi_highlighting` (line 9),
which replaces the ANSI codes with neovim specific highlight groups. This turned
out to be quite involved but I wanted the formatted output and used this as an
opportunity to learn lua a bit more. 

```lua
vim.api.nvim_set_hl(0, "Normal", { fg = "fg", bold = false, underline = false, italic = false })
vim.api.nvim_set_hl(0, "Bold", { bold = true, underline = true })
vim.api.nvim_set_hl(0, "Dim", { fg = "gray", italic = true })
vim.api.nvim_set_hl(0, "Red", { fg = "red" })
vim.api.nvim_set_hl(0, "Green", { fg = "green" })
vim.api.nvim_set_hl(0, "Blue", { fg = "blue" })

local ansi_patterns = {
  { pattern = "\27%[0m", highlight = "Normal" },
  { pattern = "\27%[1m", highlight = "Bold" },
  { pattern = "\27%[2m", highlight = "Dim" },
  { pattern = "\27%[91m", highlight = "Red" },
  { pattern = "\27%[92m", highlight = "Green" },
  { pattern = "\27%[94m", highlight = "Blue" },
}

-- Find the highlight group for a given ANSI escape code
local function find_ansi_pattern(text)
  for _, entry in pairs(ansi_patterns) do
    if text:find(entry.pattern) then
      return entry.highlight
    end
  end
  return nil
end

-- Apply ANSI highlighting to a line of text in the given buffer
local function apply_ansi_highlighting(buf, line_num, text)
  text = text:gsub("\27%[0m$", "")
  local pattern = "\27%[[0-9]+m"

  local start_pos, end_pos, match = text:find("(" .. pattern .. ")")
  local cursor = 1
  local pos_in_stripped = 0

  local next = text
  while start_pos do
    if next:find("^" .. pattern) then
      start_pos, end_pos, match = next:find("(" .. pattern .. ")")
      cursor = end_pos + 1
      vim.api.nvim_buf_add_highlight(
        buf,
        -1,
        find_ansi_pattern(match) or "Normal",
        line_num,
        pos_in_stripped,
        -1
      )
    else
      start_pos = next:find(pattern)
      if start_pos then
        pos_in_stripped = pos_in_stripped + start_pos - 1
        cursor = start_pos
      end
    end

    next = next:sub(cursor, -1)
  end
end
```

## Configuring `K`

Opening any file and calling `:lua DictionaryLookup()` already works (and `:lua
ClosePopup()` to dismiss it) but that's a lot of typing and it better fits `K`
in markdown files since that's otherwise unused anyway.

I mapped the first to a vim command `:Dict` and wanted to hide the window with
any cursor movement, similar to how this works for other documentation lookups. 
`keywordprg` is the command that gets invoked through `K` (and can also be set
through `set keywordprg`).

I put this in `~/.vim/ftplugin/markdown.lua` so that it automatically is applied
to markdown files:

```lua
vim.api.nvim_create_user_command("Dict", DictionaryLookup, { nargs = 1 })
vim.opt["keywordprg"] = ":Dict"

vim.api.nvim_create_autocmd("CursorMoved", {
  pattern = "*",
  callback = ClosePopup,
})
```

With the end result being:

![Dictionary lookup of the word ambiguous in
neovim](/images/dictionary-lookup-neovim.png)

Dictionary lookup also still works in non-markdown files by directly invoking
`:Dict`, which is a bit more typing but also much less common. That's all that
was needed, now `⌘K` performs a dictionary lookup and shows it nicely formatted
in-line and is automatically hidden when needed. This may be nice as a generic
plugin as well so I might do that at some point in the future as well.
