Title: Localization troubles with Swift PM
Date: 2025-09-19
Description: An overview of how localizing works when an app is modularized with Swift PM

A few weeks ago we got bit by a piece of Apple magic in its localization
workflow when combined with Swift PM. The problem we ran into was that as soon
as we moved all our `Localizable.strings` files to an SPM package, none of the
localizations would be picked up anymore and the app would display in
English&mdash;but **only for first-time installations**. We followed the
documentation guidelines for how to localize an app in an Swift PM environment
and have no custom tooling in place, so it was a bit of a headscratcher.

The modern way of adding support for another language/region in Xcode is through
the project's _Info_ tab. Simply click the + and add a language and the app now
supports localizing in that language.

Adding localizations for any resource is done by clicking the _Localize..._
button in the Attributes inspector. After confirming the language, Xcode creates
a new `.lproj` folder for the selected language and moves the resource into that
folder. The end result is the project will have a `.lproj` folder for each
localization as well as the `Base.lproj`.

This _just works_. The `.lproj` folders get copied over to the `.app` and at
runtime the SDK knows how to read and use these folders. Xcode also gives visual
confirmation in the _Info_ tab by indicating for how many files it has picked up
a localized version per language/region.

![Xcode sees three localized files](/images/xcode-localizations-3.png)

Getting started with adding some SPM packages in our app, we moved the `.lproj`
folders into our `Localization` package at
`Localization/Sources/Localization/Resources/`, which follows the process
outlined in the [documentation]. Locally this seemed to work and we shipped the
change, only for QA to report localizations were broken throughout the app.

As it turns out, any `.lproj` folders in **SPM packages** aren't considered when
determining what localizations are available. At first this was a bit confusing,
but it makes sense for two reasons:

1. Through various layers of abstraction, the system looks up the available
   localizations using methods on `Bundle`. `Bundle.localizations` simply finds
   all `.lproj` folders in that bundle. SPM package bundles aren't included in
   `Bundle.main`, which is the bundle that's used to determine app-wide
   localizations.
2. An SPM package can be localized in different languages than the app that
   integrates the package, especially if the package is from an external vendor.
   It could be weird behavior to have the app's selected localization be
   determined by some SPM package.

!!! note
    There is an Info.plist key that would allow SPM packages to use a different
    localization than the main app: `CFBundleAllowMixedLocalizations`.
    I haven't tried for myself, but setting this to `YES` allows different
    localizations for the app and for every package.

When moving all `.lproj` folders into the SPM package, the app didn't have any
localized files left and Xcode indicated as much. 

![Xcode sees no localized files](/images/xcode-localizations-0.png)

As a result, the app would always default to English. This explained why things
were broken but there were still a few questions left.

**How come the correct localization was used for returning users?**

This issue only happened to users that freshly installed the app. Upon first
launch, we store the user's locale in `UserDefaults` (later giving users the
ability to override this manually). Instead of reading strings from
`Bundle.main` we read them from a new `Bundle` instance specifically scoped to
that locale:


```swift
let defaultLocale = Bundle.main.preferredLocalizations[0]
let userLanguage = UserDefaults.shared.language // e.g. "nl" for Dutch
let path = Bundle.main.pathForResource(language ?? defaultLocale , ofType: "lproj")
let customBundle = Bundle(path: path)

let localized = customBundle.localizedString(forKey: key, value: nil, table: nil)
```

This setup has some interesting results:

* ❌ `Bundle.main.preferredLocalizations` only contains the development default
  locale `en` as the main bundle doesn't have any localizations
* ❌ `customBundle.preferredLocalizations` only contains the localization it was
  scoped to
* ✅ `customBundle.localizedString(forKey:value:table:)` works as the SPM
  package's resources still get copied into the main app as a separate bundle
* ✅ `Bundle.module.preferredLocalizations` correctly returns all the supported
  localizations since they're defined in the SPM package
* ✅ `Bundle.module.localizedString(forKey:value:table:)` works for the same
  reason
* ❌ `Bundle.main.localizedString(forKey:value:table:)` does not work as the
  main bundle doesn't have any localizations

For first-time users we would read `en` as their preferred language through
`Bundle.main.preferredLocalizations`, but for returning users we'd read what
language they were using before from `UserDefaults`.

Conclusion: we should be using `Bundle.module.preferredLocalizations` instead.

**Why was it so difficult to figure this out?**

The build cache in Xcode messed with our ability to reproduce the issue. In
understanding what commit introduced the problem, we would often switch branches
but that didn't invalidate the build cache.

So building any commit before the offending change would copy the `.lproj`
folders into the main app's build cache, and those folders would stay there
after checking out and building the offending commit.

At first we thought the issue was only intermittently reproducible, but once we
realized the build cache was "polluted" we started to clean it every time. This
made it much easier to reproduce but much slower to test due to constantly doing
full builds.

**What am I supposed to do in a fully modularized app where there are no files
to localize in the main app?**

In theory, using `Bundle.module` everywhere would work as highlighted above.
However, that's pretty cumbersome and there's a nicer way:
`CFBundleLocalizations`. This is another [Info.plist key] that lets you
_explicitly_ define what localizations the app handles, instead of looking for
`.lproj` folders and implicitly supporting the localizations for the folders
Xcode finds. With that key set, Xcode still does look for these folders but now
it also considers SPM bundles, fixing the issue.

Finally, there's another way to be explicit about the localizations a project
supports: by adding a localization through Xcode's _Info_ tab. This sets the
`knownRegions` value in the Xcode project file, which is not only considered for
determining what localizations to consider at build time, but is also used to
export and import `xliff` files.

That would have fixed our issue as well, but I personally prefer to not touch
the project file as much as possible and be explicit about what localizations
are supported through `CFBundleLocalizations`.

[documentation]: https://developer.apple.com/documentation/xcode/localizing-package-resources
[Info.plist key]: https://developer.apple.com/documentation/bundleresources/information-property-list/cfbundlelocalizations
