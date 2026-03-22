Title: Silencing NSLog
Date: 2016-08-01
Summary: Details a way to clean up a noisy Xcode console


When your app has a lot of third-party dependencies, what often happens is that
those libraries log a bunch of things to the Xcode console to help their own
debugging. Unfortunately, a lot of these logs are useful only to the developers
of the library, but not the developers of apps that integrate the library. For
example, they log things like `<SomeLibrary> (version 1.2.3) initialized`, or
`<SomeLibrary> started <primary functionality>`, sometimes with a long list of
parameters or input sources that are irrelevant to you.

Finding your own log statements in a jungle of other logs can then be
very difficult and adds to the frustration of not being able to work the debugger
as you would like to.

If a library is open source you can suggest a change by removing the log or
otherwise make it less obtrusive. However, if your change gets accepted at all,
that doesn't solve the immediate problem of being able to debug your own code
using the console.

Meet `_NSSetLogCStringFunction()`. This C function has been around in Foundation
for a long time, and while there is some
[documentation](https://support.apple.com/kb/TA45403?locale=en_US) on it, it's
still a private method. However, that doesn't mean you can't use it in debug
mode when your logs are the most valuable!

In short, this function lets you set a function pointer that can log C strings,
which `NSLog` then uses instead of the normal implementation. You can do this
in two ways.

The first one is by adding this to your Objective-C bridging header:

```objective-c
#if DEBUG
extern void _NSSetLogCStringFunction(void(*)(const char*, unsigned, BOOL));
#endif
```

and then use it like this:

```swift
func disableNSLog() {
#if DEBUG
    _NSSetLogCStringFunction { message, _, _ in
        // no actual logging, message just gets lost
    }
#endif
```

If you want to stick to pure Swift, you can do so by adding this to your code
somewhere:

```swift
@_silgen_name("_NSSetLogCStringFunction")
func setNSLogFunction(_: @convention(c) (UnsafePointer<Int8>, UInt32, ObjCBool) -> Void)
```

and then use it like this:

```swift
func disableNSLog() {
#if DEBUG
    setNSLogFunction { message, _, _ in
        // no actual logging, message just gets lost
    }
#endif
}
```

Obviously, you can do anything you want inside the closure, including writing to
a file, annotating the message with a date/time, passing it to your custom
logging library, etc.

One downside of this is that Apple's frameworks use `NSLog` extensively as well,
so in the above case of completely disabling logging, helpful messages get lost
as well. You won't be able to use `NSLog` yourself either anymore, so I suggest
you use `print()` or a custom logging framework that's not `NSLog` based.

If you're not afraid of doing (more) horrible things in your codebase, you can
avoid losing Apple frameworks' messages by parsing the stack trace and looking
at the framework that called this function and see if it's something you want to
let through:

```swift
func disableNSLog() {
#if DEBUG
    _NSSetLogCStringFunction { message, _, _ in
        // message is of type UnsafePointer<Int8> so first see if we can get a
        // normal String from that. Safety first!

        guard let message = String.fromCString(message) else {
            return
        }

        let callStack = NSThread.callStackSymbols()
        let sourceString = callStack[6]
        let separatorSet = NSCharacterSet(charactersInString: " -[]+?.,")
        let stackFrame = sourceString.componentsSeparatedByCharactersInSet(separatorSet)
        let frameworkName = stackFrame[3]

        if frameworkName == "UIKit" || frameworkName == "Foundation" {
            MyCustomLogger.log(message)
        }
    }
#endif
}
```

This discards all logs, except if they're coming from `UIKit` or `Foundation`.
The stack trace parsing is by no means safe (its format could change, for
example), but since it's wrapped in `#if DEBUG` directives it won't mess with
anything in the App Store build.

Note that static libraries are part of your main app's target, which means you
have to filter out logs from your own target to hide those.

You could even go a bit farther and check the message for keywords you like or
don't like and make a decision on whether you want to log or not. Keep in mind,
though, that any work you do here needs to be fast as you don't always know just
how much is being logged.
