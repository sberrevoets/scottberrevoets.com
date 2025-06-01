Title: Art of the State
Date: 2025-06-02
Description: Best practices in defining better state and data models

`@State` plays a prominent role in any SwiftUI app, and for good reason: app
state is what ultimately drives the UI and how the user interacts with your app.
This has always been true, but SwiftUI embraces this reality with specific APIs
and a unidirectional data flow. UIKit-based apps or features were _also_ driven
by state, but this state would often live in the UI layer and was much more
hidden as a result.

!!! note

    This is actually true for frontend/web apps as well, as React works in a
    very similar way as SwiftUI and also uses a unidirectional data flow. In
    fact, I suspect SwiftUI drew some inspiration from React in terms of API
    design, but we probably won't ever get that confirmed :)

SwiftUI improves the data flow in applications, but there is much less
discussion on best practices for defining what that data looks like. This is too
bad, because thoughtful data and state modeling has cascading effects in API
design and testability of code. Suboptimal definitions of state in the the model
layer means that view models, view controllers, views, etc. all also suffer from
that suboptimal design.

No matter the app, state plays a critical role (even if that state largely comes
from the server) and I wanted to write down best practices and common pitfalls
I've seen when writing state models.

## Prefer value types

State is often passed down or otherwise accessed by different parts of the app.
In some cases you might want to mutate it or operate on a separate copy of that
state, without immediately affecting every other part of the app that relies on
that same state. Using value types provides the necessary guard rails to make
sure those changes don't unintentionally also impact other parts of the app,
while still making it possible, to also globally mutate state.

Making the main state type a struct or an enum is a good start but not always
sufficient: _all_ state in a tree is ideally using value types. This avoids
misusing a state type to be more than just the basic values that represent the
current condition of the app.

It also inherently means that almost all state should be a collection of
"primitives" like `String`, `Int`, `Float`/`Double`, and `Bool` that are used
either directly or wrapped in other types (e.g. `CGRect`,
`NumberFormatter.Style`, a custom type, etc.).

Basically any other type is out. No classes, closures, actors, or other more
complex types as they typically aren't good candidates to represent state.
Unfortunately, [tuples][1] are also not an option for now, but using a named
struct is usually worth that hassle.

I've found that a good way to validate this is by making all state types conform
to `Equatable` (or possibly `Sendable`). Types whose implementation of those
`Equatable` don't require a custom implementation of `==` are good to go, and if
the compiler complains about non-conformance there's some critical thinking to
do.

## Avoid singletons

If you needed more reasons to dislike singletons, here is another one: it makes
data modeling more difficult. Take this `UserManager` example:

```swift
struct User {
    let id: UUID
    let name: String
}

final class UserManager {
    static let shared = UserManager()

    var user: User?
}
```

Ignoring all other singleton-related issues, the problem here is that since
`UserManager` can be accessed even if the user isn't logged in, it gets hard to
model the `user` property:

* Make it optional and you're dealing with optionality everywhere, which is also
  not ideal (more on that below)
* Make it "empty" (e.g. `var user = User(id: UUID(), name: "")`, and it doesn't
  properly reflect the state the app could actually be in since a `user` isn't
  required for the app to function

It's better to architect this in a different way such that you can guarantee the
`user` and its properties are valid (i.e. non-nil and not just some default
value) when asking for it.

## Separate DTOs from domain models

**Data Transfer Objects** are the objects you get back directly from, typically,
an API. DTOs are directly bound to the data the API sends, which could have all
kinds of problems: missing or unused fields, wrong data types, optionality in
some cases but not in others, unexpected or inconsistent formats, different
versions, etc.

It's tempting to use these DTOs directly, especially when using mechanisms like
Codable to create them easily and to cover some of those flaws. However, it
might also be tempting to _not_ optimize the domain model for your app because
Codable isn't always the easiest to work it. This could handicap your data
models as they now have to follow the API design and all its flaws everywhere in
your app.

Admittedly, it is a bit annoying to write the data model "twice", but the work
often pays off and the decoupling is worth it. Perhaps AI or other tools can
help with this as well.

## Avoid state impossibilities

Imagine a `User` object that captures the user's email and its verification
status:

```swift
struct User {
    let email: String?
    let emailVerified: Bool
}
```

The `verified` status is required regardless of whether there is an email
address. But the combination `email = nil` and `emailVerified = true` means
nothing, so the state is modeling an impossible scenario. It's better to model
this as a tuple or a struct:

```swift
struct User {
    struct Email {
        let value: String
        let verified: Bool
    }

    let email: Email?
    // or
    let email: (value: String, verified: Bool)?
    
    // with optional conveniences:
    var emailAddress: String? { email?.address }
    var emailVerified: Bool { email?.verified == true }
}
```

Now either both fields are set, or neither are and the app doesn't have to
handle that "impossible" state.

## Minimize redundant state

Try to use the minimum amount of state possible to represent a scenario. For
example, you might start out with a simple flag to choose whether an account has
been selected, but the app's requirements later change to also capture _which_
account:

```swift
struct AccountSelection {
    let hasSelectedAccount: Bool
    let selectedAccount: Account?
}
```

Not only does this lead to another impossible state (`hasSelectedAccount =
true` and `selectedAccount = nil`), but `hasSelectedAccount` can also be
inferred from `selectedAccount`: if it's `nil`, no account has been selected.

Don't be lazy and let these redundancies build up in your app because the core
business logic and UI layers (and tests!) will have to deal with this
unnecessary complexity.

## Reduce optionals when possible

> The power of optionals is not using them
>
> \- Someone, at some point

In languages that have an `Optional` type, use them as little as possible. An
optional immediately forks a type into two possible values (`some` or `none`),
which incurs an additional code branch to test.

Note that "as little as possible" doesn't mean "never", so here are a few common
pitfalls I've encountered when an optional is the best tool available:

### Handle optionality as early as possible

If you're calling an API that returns an optional value that you expect to
always be there anyway, try to eliminate it as early as possible instead of
letting that optional permeate your entire tech stack. Define your model with
the value as a non-optional and assert on its existence in your model (or even
networking) layer.

In line with the DTO use above, that could look like this:

```swift
struct User {
    let name: String

    init(dto: UserDTO) throws {
        // UserDTO might not have a user's name for some reason
        guard let name = dto.name else {
            throw ParsingError.missingField("name")
        }

        self.name = dto.name
    }
}
```

This eliminates the need to test for what happens at every other layer (UI,
business logic, etc.) if that value were to be nil.

### Optional vs. empty arrays

A pattern I see a lot, unfortunately also in Apple's code, is an array defined
like this:

```swift
let myStrings: [String]?
```

The optional here makes the code more difficult to deal with, since now you have
to account for the `nil` case everywhere, in addition to the array being empty.

Hot take: in the vast majority of cases, code doesn't handle a `nil` array
differently from an empty array (search your codebase for `?? []` and you'll see
what I mean), so you might as well model it like that too.

In the situations where that difference _is_ meaningful, making the property
optional is fine:

```swift
struct User {
    let friends: [User]?
}
```

In this case, `nil` could mean we don't know who the user's friends are, and
an empty array could mean the user has no friends ☹️

### Consider enums instead of optionals

The `Result` type was introduced in Swift's standard library to eliminate the
awkward situation where both the value and the error are optional types yet one
of them will always be set. (Another example of state impossibility: what does
it mean if both the value _and_ the error are set? Or neither?)

I've often seen this awkwardness in state as well, and similar to `Result`, the
solution is often to model that state as an enum with associated values. As a
simplified example, instead of a bunch of optionals in an onboarding flow where
data is collected step by step, that state could be modeled as:

```swift
struct OnboardingState {
    case askForName
    case askForBirthday(name: String)
    case askForEmail(name: String, birthday: Date)
    case askForPhone(name: String, birthday: Date, email: String)
}
```

## Closing

Not all of the techniques above will be useful all the time, but I've often
found myself adjusting the data model when something was annoying to deal with
in layers that consumed it, and over time realized the importance of getting the
details there right to make the rest of the application easier to deal with too.

[1]: https://forums.swift.org/t/status-of-se-0283-tuples-conform-to-equatable-comparable-and-hashable/46942/3
