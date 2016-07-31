Title: Outlets: strong! or weak?
Date: 2016-03-21
Summary: A quick overview of some best practices when creating IBOutlets


There are a lot of styles out there when it comes to using Interface Builder outlets in Swift. Even Apple's documentation and sample code isn't always consistent. The most common one, the one Apple uses in its sample code, follows this pattern:

`@IBOutlet private weak var someLabel: UILabel!`

Let's break this down by keyword:

- `@IBOutlet` makes Interface Builder recognize the outlet
- `private` ensures the outlet isn't accessed outside the current class
- `weak` is used because in most situations the owner of the outlet isn't the same as the owner of the view. For example, a view controller doesn't own `someLabel` - the view controller's `view` does.
- `var` because outlets are, by definition, set *after* initialization
- `someLabel: UILabel` is just an example, this applies to outlets of any kind
- `!`, or the implicitly unwrapped optional, is convenient because you don't have to litter your code with `?` and `if let`s (or just `!`) everywhere

While at first this seems like a solid approach, at Lyft we quickly realized we weren't fans of this one-size-fits-all way of defining outlets. Instead, the behavior and consequences of the different elements should define the outlet's exact syntax, just like any other variable.

For example, if there is a code path that removes an outlet from its superview, or the outlet is (intentionally) not hooked up in the storyboard, it needs to be an optional because the outlet is not guaranteed to be there when it's accessed.

`@IBOutlet private var someLabel: UILabel?`

If there is no code path that re-adds the outlet to the view hierarchy, it would also be good to make it `weak` to not hold on to it unnecessarily when it gets removed:
 
`@IBOutlet private weak var someLabel: UILabel?`

This ensures that if the label is removed from the superview, it's not being kept in memory by the strong reference in the view controller. In the most common case, where there is an outlet that will always be there, a strong, implicitly unwrapped optional is appropriate:

`@IBOutlet private var someLabel: UILabel!`

The outlet isn't `weak` in case the code ever changes so that there *is* a code path that removes the view from the view hierarchy but you forget to update the optionality of the property. The object will stay in memory and using it won't crash your app.

These examples all follow 3 simple rules:

1. `!` needs a guarantee that the view exists, so always use `strong` to provide that guarantee
2. If it's possible the view isn't part of the view hierarchy, use `?` and appropriate optional-handling (optional binding/chaining) for safety
3. If you don't need a view anymore after removing it from the view hierarchy, use `weak` so it gets removed from memory.

Applying these three rules means you properly use the optional semantics. After all, using `!` for a view that may not exist is no different than defining any other property as an implicitly unwrapped optional that may not exist.
