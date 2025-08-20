Title: Managing code deprecations on iOS
Date: 2025-08-20
Description: Explanation of the problems with internal and external code deprecations

A great manager I once worked with had been at Google for a while and poked fun
at an aspect of its engineering culture: any given service was either deprecated
or not yet ready for adoption. I spend a lot of my time working on mobile
platform development and over the years have been exposed to both sides of this:
needing to get rid of code that's deprecated in new OS versions, and deprecating
technologies many internal teams depend on.

* **Vendor deprecations** usually involve the platform vendor releasing new APIs
  or technologies that replace older ones and they want their developer base to
  put in the work to use this new tech
* **Internal deprecations** come with a lot of non-technical work and a long
  migration path, often in the order of quarters or years, on top of the
  technical challenge and often ugly tradeoffs in making the old and systems
  compatible during the transition period

Both types of deprecations are a way of life for platform engineering, and yet
on Apple platforms we have very little tooling available to make these easier.
In fact, the only real tool we have is `@available()` to mark a type as having
been deprecated:

```swift
@available(*, deprecated, renamed: "myNewFunction()")
func myFunction() {} // deprecated and renamed to myNewFunction

@available(iOS, deprecated: 26.0)
func myFunction() {} // deprecated starting in iOS 26

@available(*, deprecated, message: "Please use myOtherNewFunction instead")
func myOtherFunction() {} // deprecated with a custom warning message
```

Apple uses this pattern extensively throughout their frameworks and every new OS
version introduces more deprecation annotations exactly like the examples above.
This makes raising the deployment target in a sufficiently large project a much
bigger initiative than it might seem at first, because suddenly you're facing a
large number of deprecation warnings.

Handling the deprecation of a single class can in extreme cases be a project on
its own. If you're looking to raise the deployment target to use the latest
SwiftUI APIs, it can be a bummer to first have to spend a bunch of time
resolving deprecation warnings, especially when `warnings-as-errors` is on and
the app doesn't even build.

Since `@available`'s only real logic is gating on OS and Swift versions, it
isn't helpful for internal deprecations. If I write a new database class that
replaces an old one that's used in 50+ places, I don't know what OS version to
specify because it's not related to OS-specific system APIs. It's more important
to think about how to manage the existing call sites, which in most cases means
I accepting the 50+ instances, ensuring it doesn't grow any further, and working
with the team to migrate them over time.

Annotating the old class with `@available(*, deprecated)` would immediately
cause build errors, so that's not an option. At Lyft we often resorted to the
ugly workaround of renaming the old class to `DeprecatedDatabase` or even
`DEPRECATEDDatabase`. This worked surprisingly well, but it also very clearly
highlights a gap in tooling.

[SE-0443: Precise Control Flags over Compiler Warnings] gives developers more
granular control over compiler warnings, even mentioning the deprecation use
case specifically. In short, there are now build settings that enable upgrading
and downgrading warnings of a specific type to and from errors. The proposal
gives this example to turn warnings-as-errors on except for deprecations:
`-warnings-as-errors -Wwarning Deprecated`. This leaves `warnings-as-errors` on
for everything except deprecations.

It's an OK first step, but not really sufficient:

1. There might be multiple deprecations happening at once, but you can only
   specify whether to enable or disable deprecation warnings as a whole, not per
   type
2. Even if per-type warning disables were available, that still means it's too
   easy to accidentally or unknowingly introduce new call sites of a deprecated
   type

The most ideal solution is bringing back a relic from the Objective-C past: C
compiler directives. In C-based languages, `#pragma` blocks could be used to
ignore specific instances of a warning:


```c
#pragma GCC diagnostic ignored "-Wdeprecated-declarations"

myDeprecatedFunction() // no warning

#pragma GCC diagnostic pop

myDeprecatedFunction() // warning: myDeprecatedFunction is deprecated
```

Although the syntax is clearly not very "2025", the idea is still good and
exactly what should happen to improve this bit of API tooling. The deprecation
warning on the call site that's "wrapped" in the `diagnostic` directive would be
ignored, and introducing a new caller of `myDeprecatedFunction` generates a
warning (or more ideally, a build error). You can choose to wrap that new call
in the same `#pragma` block, but then it's an explicit choice and not something
the developer was just unaware of.

Incidentally, having multiple levels of granularity is also exactly how e.g.
SwiftLint and linters on other platforms work: you can disable rules entirely,
per-file, per code-section, per-line, etc. It's too bad SE-443 didn't go that
far, but discussions in the [developer forums] have pointed out these same
problems so hopefully those will be considered in future improvements.


[SE-0443: Precise Control Flags over Compiler Warnings]: https://github.com/swiftlang/swift-evolution/blob/main/proposals/0443-warning-control-flags.md
[developer forums]: https://forums.swift.org/t/se-0443-precise-control-flags-over-compiler-warnings/74116
