Title: Using Interface Builder at Lyft
Date: 2017-03-06
Summary: An overview of how we use Interface Builder to build the Lyft app


Last week people realized that Xcode 8.3 by default uses storyboards in new
projects without a checkbox to turn this off. This of course sparked the
Interface Builder vs. programmatic UI discussion again, so I wanted to give some
insight in our experience using Interface Builder in building the Lyft app. This
is not intended as hard "you should also use Interface Builder" advice, but
rather to show that IB _can_ work at a larger scale.

First, some stats about the Lyft app:

- 40 storyboards
- 100 XIB files
- 150 view controllers
- 20 people on the iOS team with occasional outside contributors

With the
[rewrite](https://www.skilled.io/u/keithsmiley/tales-of-a-rewrite-at-lyft) of
our app we moved to using IB for about 95% of our UI.

The #1 complaint about using Interface Builder for a project with more than 1
developer is that it's impossible to resolve merge conflicts. **We never have
this problem.** Everybody on the team can attest that they have never run into
major conflicts they couldn't reasonably resolve.

With that concern out of the way, what about some of the other common criticisms
Interface Builder regularly gets?

## Improving the workflow

Out of the box, IB has a number of shortcomings that could make working with it
more painful than it needs to be. For example, referencing IB objects from code
still can only be done with string identifiers. There is also no easy way to
embed custom views (designed in IB) in other custom views.

Over time we have improved the workflow for our developers to mitigate some of
these shortcomings, either by writing some tools or by writing a little bit of
code that can be used project-wide.

### storyboarder script
To solve the issue of stringly-typed view controller identifiers, we wrote a
script that, just before compiling the app, generates a struct with static
properties that exposes all view controllers from the app in a strongly-typed
manner. This means that now we can instantiate a view controller in code like
this:

```swift
let viewController = Onboarding.SignUp.instantiate()
```

Not only is `viewController` now guaranteed to be there at runtime (if something
is wrong in the setup of IB the code won't even compile), but it's also
recognized as a `SignUpViewController` and not a generic `UIViewController`.

### Strongly-typed segues
All our view controllers have a base view controller named `ViewController`.
This base controller implements `prepare(for:sender:)` like this:

```swift
open override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
    guard let identifier = segue.identifier else {
        return
    }

    let segueName = identifier.firstLetterUpperString()
    let selector = Selector("prepareFor\(segueName):sender:")
    if self.responds(to: selector) {
        self.perform(selector, with: segue.destination, with: sender)
    }
}
```

This means that a view controller that has a segue to
`TermsOfServiceViewController` can now do this:

```swift
@objc
private func prepareForTermsOfService(_ viewController: TermsOfServiceViewController, sender: Any?) {
    viewController.onTermsAccepted = { [weak self] self?.proceed() }
}
```

We no longer have to implement `prepareForSegue` and then `switch` on the
segue's identifier or destination controller, but we can implement a separate
method for every segue from this view controller instead which makes the code
much more readable.

### `NibView`

We wrote a `NibView` class to make it more convenient to embed custom views in
other views from IB. We marked this class with `@IBDesignable` so that it knows
to render itself in IB. All we have to do is drag out a regular `UIView` from
the object library and change its class. If there is a XIB with the same name as
the class, `NibView` will automatically instantiate it and render it in the
canvas at design time and on screen at runtime.

Every standalone view we design in IB (which effectively means every view in our
app) inherits from `NibView` so we can have an "unlimited" number of nested
views show up and see the final result.

### Basic `@IBDesignable`s
Since a lot of our views have corner radii and borders, we have created this
`UIView` extension:

```swift
public extension UIView {
    @IBInspectable public var cornerRadius: CGFloat {
        get { return self.layer.cornerRadius }
        set { self.layer.cornerRadius = newValue }
    }

    @IBInspectable public var borderWidth: CGFloat {
        get { return self.layer.borderWidth }
        set { self.layer.borderWidth = newValue }
    }

    @IBInspectable public var borderColor: UIColor {
        get { return UIColor(cgColor: self.layer.borderColor!) }
        set { self.layer.borderColor = newValue.cgColor }
    }
}
```

This lets us easily set these properties on _any_ view (including the ones from
UIKit) from Interface Builder.

### Linter
We wrote a linter to make sure views are not misplaced, have
accessibility labels, trait variations are disabled (since we only officially
support portrait mode on iPhone), etc.

### ibunfuck
A [bug](https://forums.developer.apple.com/thread/8116) impacting developers
that use Interface Builder on both Retina and non-Retina screens (which at Lyft
is every developer) has caused us enough grief to write
[`ibunfuck`](https://github.com/Reflejo/ib-unfuck-git) - a tool to remove
unwanted changes from IB files.

### Color palette
We created a custom color palette with the commonly used colors in our app so
it's easy to select these colors when building a new UI. The color names in the
palette follow the same names designers use when they give us new designs, so
it's easy to refer to and use without having to copy RGB or hex values.

## Our approach

In addition to these tools and project-level improvements, we have a number of
"rules" around our use of IB to keep things sane:

- Do as little as possible in code, do as much as possible in IB. That means
  fonts, colors, images, and other properties should not be set in code if they
  don't change at runtime.
- Use `@IBInspectable` on custom views whenever possible.
- Create as much Auto Layout constraints in IB as possible. Sometimes this means
  being clever with how we create constraints so that at runtime we need very
  little code to manipulate a layout.
- If we do need to create constraints in code, we don't use the
  `NSLayoutConstraint` (or `NSLayoutAnchor`) methods directly. Instead we use
  [SnapKit](https://github.com/SnapKit/SnapKit)'s convenience methods.
- We still manually push and present view controllers where possible. Even
  though we have created some niceties around using segues, it's still easy to
  accidentally remove one and not find out about it until runtime.
- We tend to create a new storyboard when we recognize a common theme in related
  view controllers. Just as with code, we don't want bloated storyboards with
  all kinds of unrelated things in there. Most of our storyboards have fewer
  than 10 scenes.
- [Our outlets are defined
  carefully.](https://scottberrevoets.com/2016/03/21/outlets-strong-or-weak/)


Of course, even with these improvements everything is not peaches and cream.
There are definitely still problems. New versions of Xcode often change the XML
representation which leads to a noisy diff. Some properties can simply not be
set in IB meaning we're forced to break our "do everything in IB" rule.
Interface Builder has bugs we can't always work around.

However, with our improved infrastructure and the points from above, we are
happy with how IB works for us. We don't have to write tons of Auto Layout code
(which would be incredibly painful due to the nature of our UIs), get a visual
representation of how a view looks without having to run the app after every
minor change, and maybe one day we can get our designers make changes to our UI
without developers' help.
