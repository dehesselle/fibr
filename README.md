# fibr [faɪbə] - File Browser

![main screen](https://raw.githubusercontent.com/dehesselle/fibr/refs/heads/main/docs/screenshot.svg)

A simple file browser with a [Midnight Commander](https://midnight-commander.org)-style interface featuring:

- traditional dual-pane layout
- find-as-you-type per default
- ~~basic file operations vai UI: copy, move, mkdir~~ _Not implemented yet!_
- view/edit file delegated to external tools

And that's about it!

It's a very short and select feature set, so this might not be the tool your're looking for. If you're looking for a comprehensive TUI file manager, take a look at the original or other popular choices like [lf](https://github.com/gokcehan/lf), [superfile](https://github.com/yorukot/superfile) or [yazi](https://github.com/sxyazi/yazi).

fibr was created to scratch an itch of mine and is not looking to become a contender in the space of TUI file managers.

The project status is currently "alpha", i.e. it is neither feature-complete nor extensively tested.

Written in Python using the excellent [Textual](https://textual.textualize.io) framework.

## Installation

`fibr` is on [PyPi](https://pypi.org/project/fibr/), you can use the package manager of your choice to set yourself up. Here is an example using `uv`:

```bash
uv tool install fibr
```

## Usage

If you're familiar with Midnight Commander, the basics are identical:

- cursor up/down (⬆, ⬇) to move a line
- page up/down (⇞, ⇟) to move a page
- home/end (⇱, ⇲) to jump top/bottom
- enter (⏎) to enter a directory
- tab (⇥) to switch panels
- F3 to open the highlighted file in an external viewer (`$PAGER`)
- F4 to open the highlighted file in an external editor (`$EDITOR`)
- ~~F5 to copy file/directory~~  _Not implemented yet!_ 
- ~~F6 to move file/directory~~  _Not implemented yet!_ 
- ~~F7 to create directory~~  _Not implemented yet!_ 
- ~~F8 to delete file/directory~~  _Not implemented yet!_ 
- any alphanumeric key triggers "find-as-you-type"
  - escape (⎋) to cancel
  - tab/shift tab (⇥, ⇧⇥) to jump to next/previous match
  - enter (⏎) to confirm (will enter directory if search matches)
- ctrl+o (⌃o) to open a subshell
- ctrl+r (^r) to reload directory from disk
- ctrl+t (⌃t) to toggle file selection

> [!NOTE]  
> By default, the content of a directory is cached on first read and not automatically refreshed, even when you switch directories. You have to manually issue a reload to see newly created/deleted/updated files.  
> This behavior is under review.

## License

[GPL-2.0-or-later](https://github.com/dehesselle/fibr/blob/main/LICENSE)
