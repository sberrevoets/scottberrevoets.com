Title: UIApplicationMain can choose an app delegate at runtime
Date: 2026-09-17

`@UIApplicationMain` was deprecated a while back and replaced with `@main`.
However, Swift still has a function called `UIApplicationMain` which creates the
`UIApplication` instance and instantiates the app delegate.

Most apps should continue to use `@main`, but calling `UIApplicationMain`
manually lets you specify the class for the app delegate. This is useful for
us when running tests: our actual app delegate does a bunch of work and
instead of guarding it all with some check to see if we're testing, we just
specify an entirely different app delegate with no setup code:

```swift
let isRunningUnitTests = NSClassFromString("XCTestCase") != nil
let delegateClass: AnyClass = isRunningUnitTests ? TestAppDelegate.self : AppDelegate.self

UIApplicationMain(
    CommandLine.argc,
    CommandLine.unsafeArgv,
    nil,
    NSStringFromClass(delegateClass)
)
```

This is top-level code in `main.swift` and is executed before the app is
launched. That means general app infrastructure isn't available, but basic
environment or runtime inspection is fine. The third argument, `nil` in the
example above, can be used to pass in a subclass of `UIApplication`. This
can be useful to include a hidden developer menu (for example, through a
global gesture in this subclass) for `DEBUG` builds only:

```swift
#if DEBUG
let principalClass: AnyClass = DeveloperApplication.self
#else
let principalClass: AnyClass = UIApplication.self
#endif

UIApplicationMain(
    CommandLine.argc,
    CommandLine.unsafeArgv,
    NSStringFromClass(principalClass),
    NSStringFromClass(AppDelegate.self)
)
```

Note that calling `UIApplicationMain` manually replaces the existing `@main`
(or its predecessor `@UIApplicationMain`).
