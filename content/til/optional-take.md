Title: Swift's Optional has a take() function
Slug: optional-has-a-take-function
Date: 2026-04-05

After the introduction of `Optional.toggle()` back in 2018, I thought I had
learned everything there is to `Optional`, but today I learned about another
method: `Optional.take()`. As the [documentation] points out, it returns the
value of a mutable optional (if not `nil`) and then resets the variable to
`nil`:

```swift
var myInt: Int? = 42
var myOtherInt = myInt.take() // 42
print(myInt) // nil
```

Because this also works if `myInt` was nil, `take()` returns an optional as
well. Nothing groundbreaking, but could save you an occasional line of code.

[documentation]: https://developer.apple.com/documentation/swift/optional/take()
