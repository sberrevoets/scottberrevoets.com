# ScottBerrevoets.com

This repository contains the source for
[ScottBerrevoets.com](http://scottberrevoets.com). It uses
[Pelican](http://getpelican.com) to generate all content, including file and
directory structures. I'm using a custom Pelican theme. You may use this theme
for your own Pelican installation, but I can't help you out with customizations.

## Installation

```bash
# Install Pelican and markdown
$ pip3 install pelican
$ pip3 install markdown

$ pelican content
```

The full blog will be generated in `./output`.

## Writing

Because I always forget.

- Edit content, then run `$ pelican content` from the root
- To preview: `$ pelican --listen` (with `-r` for continuous regeneration)
- To deploy: `make ftp_upload`, using .netrc for FTP credentials

## Contributing

Found a mistake, typo, or formatting error? Contributions are welcome! 

## License

- Code is published under the [MIT license](https://github.com/sberrevoets/scottberrevoets.com/blob/master/LICENSE)
- Content is published under [CC BY-NC 3.0](https://creativecommons.org/licenses/by-nc/3.0/)
