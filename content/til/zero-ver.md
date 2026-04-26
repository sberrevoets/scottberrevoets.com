Title: ZeroVer is a (realistic) SemVer parody
Date: 2026-05-09

Software whose author has big ideas they want to implement before committing to
a [Semantic Versioning] (or SemVer) versioning methodology often starts with
many 0.x releases before ever reaching a 1.0 version. The 0.12.2 release of
neovim led me to [ZeroVer], which details and explains this method.

Given the popularity of tools that actually use ZeroVer without explicitly
saying so, I wasn't surprised to see it existed formally as well. But I'm glad I
read its about page, because it turns out it's satire: an April Fool's joke
from 2018. It's poking fun at massively used production software that hasn't
seen a 1.0 version but would've had many major version updates if it had
followed SemVer.

And yet it's actually a valid option for some software. Most people assume
SemVer is the status quo, but open source software that mostly relies on
volunteers for ongoing development can make it much easier for them to do that
if they're "allowed" to make breaking changes, not devise migration strategies,
and avoid angrying people over breaking their software. Many packages follow it
anyway, so why not formalize it?

[Semantic Versioning]: https://semver.org/
[ZeroVer]: https://0ver.org/
