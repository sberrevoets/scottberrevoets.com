Title: @objc class prefixes fixed in Xcode 7 beta 4
Date: 2015-07-23
Description: A follow-up on using @objc to rename classes in Objective-C from Swift


Back in December I [wrote](/2014/12/15/at-objc-creates-a-wrong-class-name-in-objective-c/) about what I thought was a bug in the Swift compiler that would expose the wrong class name for a Swift class in Objective-C. I then later [found out](https://devforums.apple.com/message/1072175#1072175) everything worked as intended and I had just misunderstood what `@objc()` exactly did. Apparently it was never supposed to modify the class name at compile time, but only at runtime.

I'm sure changing the class name just at runtime has its uses, but in my opinion, this would be most helpful if it also affected the compile time name of Objective-C classes. It allows you to namespace your classes in Objective-C using your three-letter prefix, without needing that prefix in Swift because you could namespace by way of modules.

And fortunately, in Xcode 7 beta 4, they have actually modified the `@objc()` notation so that it *does* do this. For example, if I have a Swift module that I want others to be able to use in their Objective-C codebase, I could write a class like this:

```swift
@objc(SDCMyClass)
class MyClass: NSObject {
    // ...
}
```

And in `MyProject-Swift.h` the Objective-C class is defined as:

```objective-c
SWIFT_CLASS_NAMED("MyClass")
@interface SDCMyClass : NSObject
- (nonnull instancetype)init OBJC_DESIGNATED_INITIALIZER;
@end
```

In Swift I can simply use the class as `MyClass`, but in Objective-C its name is `SDCMyClass`, which ensures it doesn't collide with other classes named `MyClass`. Needless to say, I'm very happy they changed this behavior, it makes much more sense now.
