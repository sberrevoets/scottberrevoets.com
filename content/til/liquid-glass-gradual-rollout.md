Title: Liquid Glass can be gradually rolled out
Date: 2026-07-10

By default, Liquid Glass is enabled for apps that are built with Xcode 26. For
any Xcode 26 version, Apple has provided the `UIDesignRequiresCompatibility`
Info.plist key to opt out of Liquid Glass. However, Info.plist values are
impossible to either partially enable or gradually roll out.

But today someone in a private Slack workspace mentioned there is a
private/Apple-defined User Defaults value that controls whether the app enables
Liquid Glass even with `UIDesignRequiresCompatibility` in the Info.plist:
`com.apple.SwiftUI.IgnoreSolariumOptOut`. Set this value to `true` and
`UIDesignRequiresCompatibility` is ignored, enabling Liquid Glass; `false`
re-disables Liquid Glass:

```swift
// Enable Liquid Glass
UserDefaults.standard.set(true, forKey: "com.apple.SwiftUI.IgnoreSolariumOptOut")

// Disable Liquid Glass
UserDefaults.standard.set(false, forKey: "com.apple.SwiftUI.IgnoreSolariumOptOut")
```

This is more dynamically settable than the Info.plist, making it easier to get
internal builds tested with and without Liquid Glass or have a more gradual
rollout. Note that the app needs to be restarted for the changes to take effect
for both enabling and disabling.
