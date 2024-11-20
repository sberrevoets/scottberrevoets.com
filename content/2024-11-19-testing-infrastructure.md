Title: Shifting the testing culture: Infrastructure
Date: 2024-11-21
Summary: Infrastructure changes we made to optimize the ergonomics and developer experience of writing tests.

!!! note
    This is the second post in a series on shifting our testing culture.

    1. [Motivation]
    2. Infrastructure
    3. [Code coverage]

[Motivation]: {filename}2024-11-18-testing-motivation.md
[Code coverage]: {filename}2024-11-20-testing-code-coverage.md

This second article goes a bit deeper into the testing infrastructure we built
over the years to optimize the ergonomics and developer experience as much as
possible.

[before]: {filename}2021-10-14-lyft-ios-architecture.md#modules

Our initial test suites only had basic tests for some foundational code in
shared modules. Initially these were written in [Quick and Nimble], but we moved
to the default `XCTest` to reduce the learning curve. When we started
writing UI tests, we immediately used `XCUITest` and still use that today.

[Quick and Nimble]: https://github.com/Quick/Quick

(`swift-testing` looks very nice and we're exploring how we can start using this
in our own codebase.)

## Modules

When we modularized the codebase (which I wrote a little bit about [before]), we
did so specifically with testing in mind. All modules got their own test bundle
to test that module's code.

Later on, we also specialized each module to the type of code it contained. A
module with primarily UI code in it is a `UI` module, and a module with
core business logic is a `logic` module. This approach has three (testing)
benefits:

1. It separates business logic from UI logic at a higher level
2. You can now establish the level of testing that's expected per module type
   (e.g. higher for `logic` modules than for `UI` modules)
3. The module type defines what type of tests should be written for that module
   (e.g. snapshot tests for `UI` modules, unit tests for `logic` modules)

Since each module is owned and maintained by a specific team, that team is now
fully in control over the tests they want to write for their own features. For
example, a UI-heavy feature is more likely to have snapshot tests than unit
tests. Complicated flows might have both or use UI tests for integration-like
tests.

## Avoiding flakiness

Test flakiness, tests that sometimes pass and sometimes fail, became more common
as we grew the number tests. This is a problem for multiple reasons:

* people lose confidence in the system if tests fail when they shouldn't
* it slows engineers down
* it's disruptive when tests that have been around for months suddenly start
  failing

The source of flakiness was generally an infrastructure problem, a test problem,
or a code problem. Infrastructure problems were usually not actionable by
product engineers and was something related to CI, Xcode, the test runner, the
simulator, or the intersection between any of these.

If the code was flaky that may have actually been a bug (yay tests!). Often this
meant some globally mutable state was involved, and was different than what the
tests expected for some reason.

If the test itself was flaky, it wasn't always obvious why and how that could be
avoided. The code is hard to debug because the issue doesn't always reproduce
(sometimes only on CI) and if there didn't seem to be any bugs people would
understandably give up on that test if tracking the issue down took too long.

On the infrastructure side we've made many improvements over the years to reduce
flakiness to a minimum:

* retry a failing test to reduce the impact of infrastructure failures
* disable a test that failed multiple times in a row and report it to the
  maintainer of the module that has the failing test
* increase the timeouts for test suites to run to avoid timing out slow-running,
  but passing, tests
* keep track of common errors out of our control (e.g. bugs in Xcode) and
  explicitly ignore them, try again, or work around them
* ensure tests always ran in the same environment: iOS version, device simulator,
  locale, etc.

Infrastructure flakiness still happens on rare occasion, but the sytems are much
more robust and forgiving of intermittent issues than when we first started.

## Making simple things simple

> _Simple things should be simple, complex things should be possible._
>
> \- Alan Kay

Further architecture improvements led us to standardize on a Unidirectional
Data Flow using RxSwift. These patterns are very testable, but required quite a
bit of boilerplate and significant knowledge of best testing practices within
those systems.

With a more RxSwift-centric architecture, more asynchronousness code patterns
emerged as well. Initially we used `XCTestExpectation`s to deal with that since
that's what Apple recommended, but regularly having to increase the timeout on
these expectations felt bad and we figured there had to be better ways.

We first adopted RxBlocking, but later realized RxTest was where the real money
was for us. Having two extra libraries just for testing felt heavy-handed at the
time, but have become invaluable for us.

Because the new standard for features was that they were all written using
in-house architectural components without too much deviation, we could also
standardize the test-writing part through a thin glaze of syntax sugar. Testing
a single action's outcome in a reducer now looks like this:

```swift
func testAcknowledgingError() {
    self.reducer.assert(
        state: .init(error: .mock()), // easy error state setup with mock data
        action: .acknowledgeError, // acknowledge the error
        result: { $0.activeError = nil } // error has been acknowledged
    )
}
```

With many conveniences like these in place, many tests are easy to read and take
just a few lines of code. I'm optimistic that once we adopt `swift-testing`'s
parameterized testing we can probably reduce this even more.

## Mocking

Our [dependency injection system] enables mocking with protocols which carries a
bit more boilerplate than I'd prefer but isn't too bad overall. We've also built
"automock" tooling: a pre-compile tool that generates mock classes for all
protocols it found in a module. That looks something like this:

[dependency injection system]: {filename}2021-10-14-lyft-ios-architecture.md#dependency-injection

```swift
// handwritten by a developer:

protocol MyAPI {
    func getDataFromServer() -> [String: Any] // json
    func postDataToServer(param: Bool)
}

// autogenerated by automock:

open class MyAPIMock: MyAPI {
    public var getDataFromServerReturn: [String: Any] = [:]
    
    public getDataFromServerCalls: [Int] = []
    public get postDataToServerParams: [Bool] = []

    func getDataFromServer() -> [String: Any] {
        getDataFromServerCalls += 1
        return getDataFromServerReturn
    }

    func postDataToServer(param: Bool) {
        postDataToServerParams.append(param)
    }
}
```

`MyAPIMock` can be used in tests to verify that the right methods are called at
the right time, and with the right parameters.

Automock supports more complicated use cases like closures, and more complex
parameter and return types as well. This saves developer time writing mock
classes and promotes consistency in naming and mocking usage.

It even works for model data, but it's less used and I'm more interested in a
macro approach that looks something like this:

```swift
@Mock
struct User {
    let name: String
    let age: Int?
    let active: Bool
}

// @Mock expands to:

extension User {
    static func mock(name: String = "", age: Int? = nil, active: Bool = true) {
        User(name: name, age: age, active: active)
    }
}
```

Generating mock data is now as simple as `User.mock()` (or even `.mock()` if the
type can be inferred) while still having the ability to set parameters manually
if needed.

## Other improvements

We've made a plethora of other improvements as well: sharding to parallelize
tests, only running test bundles for changed modules, a `TestKit` module to
remove common `setUp()` boilerplate, and a bunch of small things I'm probably
forgetting right now.

But the most meaningful and impactful improvements have been related to how we
handle code coverage. So much so that I thought it deserved a whole separate
post.
