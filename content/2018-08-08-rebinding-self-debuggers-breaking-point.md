Title: Re-binding self: the debugger's break(ing) point
Date: 2018-08-08
Summary: Explanation of how nice syntax for re-binding self breaks the debugger


For the Objective-C veterans in the audience, the strong-self-weak-self dance is
a practice mastered early on and one that is used very frequently. There are a
lot of different incantations, but the most basic one goes something like this:

```objective-c
__weak typeof(self) weakSelf = self;
dispatch_group_async(dispatch_get_main_queue(), ^{
    [weakSelf doSomething];
});
```

Then, if you needed a strong reference to `self` again inside the block, you'd
change it to this:

```objective-c
__weak typeof(self) weakSelf = self;
dispatch_group_async(dispatch_get_main_queue(), ^{
    typeof(weakSelf) strongSelf = weakSelf;
    [strongSelf.someOtherObject doSomethingWith:strongSelf];
});
```

Fortunately, this was much easier on day 1 of Swift when using the `[weak self]`
directive:

```swift
DispatchQueue.main.async { [weak self] in
    if let strongSelf = self {
        strongSelf.someOtherObject.doSomething(with: strongSelf)
    }
}
```

`self` is now `weak` inside the closure, making it an optional. Unwrapping it
into `strongSelf` makes it a non-optional while still avoiding a retain cycle.
It doesn't feel very Swifty, but it's not terrible.

More recently, it's become known that Swift supports re-binding `self` if you
wrap it in backticks. That makes for an arguably much nicer syntax:

```swift
DispatchQueue.main.async { [weak self] in
    guard let `self` = self else { return }
    self.someOtherObject.doSomething(with: self)
}
```

This was long considered, and [confirmed](https://lists.swift.org/pipermail/swift-evolution/Week-of-Mon-20160118/007425.html) to be, a hack that worked due to a bug in the compiler, but
since it worked and there weren't plans to remove it, people (including us at
Lyft) started treating it as a feature.

**However, there is one big caveat**: the debugger is entirely hosed for
anything you do in that closure. Ever seen an error like this in your Xcode
console?

```
error: warning: <EXPR>:12:9: warning: initialization of variable '$__lldb_error_result' was never used; consider replacing with assignment to '_' or removing it
    var $__lldb_error_result = __lldb_tmp_error
        ~~~~^~~~~~~~~~~~~~~~~~~~
```

That's because `self` was re-bound. This is easy to reproduce: create a new
Xcode project and add the following snippet to `viewDidLoad()`:

```swift
DispatchQueue.main.async { [weak self] in
    guard let `self` = self else { return }

    let description = self.description
    print(description) // set a breakpoint here
}
```

When the breakpoint hits, execute `(lldb) po description` and you'll see the
error from above. Note that you're not even _using_ `self` - merely re-binding
it makes the debugger entirely useless inside that scope.

People with way more knowledge of LLDB than I do can explain this in more detail
(and [have](https://bugs.swift.org/browse/SR-6156)), but the gist is that the
debugger doesn't like `self`'s type changing. At the beginning of the closure
scope, the debugging context assumes that `self`'s type is `Optional`, but it is
then re-bound to a non-optional, which the debugger doesn't know how to handle.
It's actually pretty surprising the compiler supports changing a variable's type
at all.

Because of this problem, at Lyft we have decided to eliminate this pattern
entirely in our codebases, and instead re-bind `self` to a variable named
`this`.

If you do continue to use this pattern, note that in a
[discussion](https://forums.swift.org/t/the-future-of-weak-self-rebinding/10846)
on the Swift forums many people agreed that re-binding `self` should be
supported by the language without the need for backticks. The [pull
request](https://github.com/apple/swift/pull/15306) was merged shortly after and
with the release of Swift 4.2 in the fall, you'll be able to use `guard let self
= self else { return }` (at the cost of losing debugging capabilities!)
