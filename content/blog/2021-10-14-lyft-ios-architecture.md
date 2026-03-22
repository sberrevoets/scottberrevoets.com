Title: iOS Architecture at Lyft
Date: 2021-10-14
Summary: Discussion on the different architectural components of Lyft's iOS apps


June 30, 2014 was my first day at Lyft as the first iOS hire on the ~3 person
team. The app was written in Objective-C, and the architecture was a 5000-line
nested switch statement.

Since then, the team has grown to about 70 people and the codebase to 1.5M lines
of code. This required some major changes to how we architect our code, and
since it had been a while since we've given an update like this, now seems as
good a time as any.

## Requirements

The effort to overhaul and modernize the architecture began around mid-2017.
We started to reach the limits of the patterns we established in the 2015
rewrite of the app, and it was clear the codebase and the team would continue to
grow and probably more rapidly than it had in the past.

The primary problems that the lack of a more mature architecture presented and
that we wanted to solve were:

- **Isolation**: Features were heavily intertwined, which made it difficult to
  safely make changes
- **Testability**: We were still mostly following MVC with view controllers being
  the main source of business logic which made it difficult to test that logic
- **State management**: The navigation in most of our app relied on local +
  server state, which grew with the number of features. How and when state
  changed then became too difficult to manage.

There was not going to be one solution that would solve all of this inherently,
but over the course of a few years we developed a number of processes and
technical solutions to reduce these problems.

## Modules

First, to provide better feature separation, we introduced modules. Every
feature had its own module, with its own test suite, that could be developed in
isolation from other modules. This forced us to think more about public APIs and
hiding implementation details behind them. Compile times improved, and it
required much less collaboration with other teams to make changes.

We also introduced an ownership model that ensured each module has at least one
team that's responsible for that module's tech debt, documentation, etc.

### Module types

After fully modularizing the app and having 700 modules worth of code, we took
this a step further and introduced a number of _module types_ that each module
would follow.

- `UI` modules only contain UI elements (views, view controllers)
- `Flow` modules contain [routing infrastructure](#flows)
- `Service` modules contain code to interact with endpoints related to the
  feature's functionality
- `Logic` modules contain pure business logic, data transformations, etc.

Breaking modules down this way enabled us to implement dependency validators: we
can validate that certain modules can't depend on others. For example, a logic
module can't depend on a `UI` module, and a `Service` module can't import UIKit.

This module structure also prevents complicated circular dependencies,
e.g. a `Coupons` module depending on `Payments` and vice versa. Instead, the
`Payments` module can now import `CouponsUI` without needing to import the full
`Coupons` feature. It's led to micromodules in some areas, but we've generally
been able to provide good tooling to make this easier to deal with.

All in all we now have almost 2000 modules total for all Lyft apps.

## Dependency Injection

Module types solved many of our dependency tree problems at the module level,
but we also needed something more scalable than singletons at the code level.

For that we've built a lightweight dependency injection framework which we
detailed in a [SLUG talk][1]. It resembles a service locator pattern, with a
basic dictionary mapping protocols to instantiations:

```swift
let getNetworkCommunicator: NetworkCommunicating =
    bind(NetworkCommunicating.self, to: { NetworkCommunicator() })
```

The implementation of `bind()` doesn't immediately return `NetworkCommunicator`,
but requires the object be mocked if we're in a testing environment:

```swift
let productionInstantiators: [ObjectIdentifier: () -> Any] = [:]
let mockedInstantiators: [ObjectIdentifier: () -> Any] = [:]

func bind<T>(protocol: T.Type, instantiator: () -> T) -> T {
    let identifier = ObjectIdentifier(T.self)

    if NSClassFromString("XCTestCase") == nil {
        return productionInstantiators[identifier] ?? instantiator()
    } else {
        return mockedInstantiators[identifier]!
    }
}
```

In tests, the mock is required or the test will crash:

```swift
final class NetworkingTests: XCTestCase {
    private var communicator = MockNetworkCommunicator()

    func testNetworkCommunications() {
        mock(NetworkCommunicating.self) { self.communicator }

        // ...
    }
}
```

This brings two benefits:

1. It forces developers to mock objects in tests, avoiding production side
   effects like making network requests
2. It provided a gradual adoption path rather than updating the entire app at
   once through some more advanced system

Although this framework has some of the same problems as other [Service
Locator][2] implementations, it works well enough for us and the limitations are
generally acceptable.

## Flows

Flows, inspired by Square's [Workflow][3], are the backbone of all Lyft apps.
Flows define the navigation rules around a number of related screens the user
can navigate to. The term `flow` was already common in everyday communications
("after finishing the in-ride flow we present the user with the payments flow")
so this terminology mapped nicely to familiar terminology.

Flows rely on state-driven routers that can either show a screen, or route to
other routers that driven by different state. This makes them easy to compose,
which promoted the goal of feature isolation.

At the core of flows lies the `Routable` protocol:

```swift
protocol Routable {
    let viewController: UIViewController
}
```

It just has to be able to produce a view controller. The (simplified) router
part of a flow is implemented like this:

```swift
final class Router<State> {
    private let routes: [(condition: (State) -> Bool, routable: Routable?)]

    func addRoute(routable: Routable?, _ condition: @escaping (State) -> Bool) {
        self.routes.append((condition, routable))
    }

    func route(for state: State) -> Routable? {
        self.routes.first { $0.condition(state) }
    }
}
```

In other words: it takes a bunch of rules where if the condition is true
(accepting the flow's state as input) it provides a `Routable`. Each flow defines
its own possible routes and matches those to a `Routable`:

```swift
struct OnboardingState {
    let phoneNumber: String?
    let verificationCode: String?
    let email: String?
}

final class OnboardingFlow {
    private let router = Router<OnboardingState>
    private let state = OnboardingState()

    init() {
        self.router.addRoute({ $0.phoneNumber == nil }, EnterPhoneNumberViewController())
        self.router.addRoute({ $0.verificationCode == nil }, VerifyPhoneViewController())
        self.router.addRoute({ $0.email == nil }, EnterEmailViewController())
        
        // If all login details are provided, return  `nil` to indicate this flow has
        // no (other) Routable to provide and should be exited
        self.router.addRoute({ _ in }, nil)
    }

    func currentRoutable() -> Routable {
        return self.router.route(for: state)
    }
}
```

We're then composing flows by adding `Routable` conformance to each flow and
have it provide a view controller, adding its current `Routable`s view
controller as a child:

```swift
extension Flow: Routable {
    var rootViewController: UIViewController {
        let parent = UIViewController()
        parent.addChild(self.currentRoutable().viewController)
        return parent
    }
}
```

Now a flow can also route to another flow by adding an entry to its router:

```swift
self.router.addRoute({ $0.needsOnboarding }, OnboardingFlow())
```

This pattern could let you build entire trees of flows:

![Simplified flow diagram](/images/flows.png)

When we first conceptualized flows we imagined having a tree of about 20 flows
total; today we have more than 80. Flows have become the "unit of development"
of our apps: developers no longer need to care about the full application or a
single module, but can build an ad-hoc app with just the flow they're working
on.

## Plugins

Although flows simplify state management and navigation, the logic of the
individual screens within a flow could still be very intertwined. To mitigate
that problem, we've introduced plugins. Plugins allow for attaching
functionality to a flow without the flow even knowing that the plugin exists.

For example, to add more screens to the OnboardingFlow from above, we can expose
a method on it that would call into its router:

```swift
extension OnboardingFlow {
    public func addRoutingPlugin(
        routable: Routable?,
        _ condition: @escaping (OnboardingState) -> Bool)
    {
        self.router.addRoute((condition, routable))
    }
}
```

Since this method is public, any plugin that imports it can add a new screen. The
flow doesn't know anything about this plugin, so the entire dependency tree is
inverted with plugins. Instead of a flow depending on all the functionalities of
all of its plugins, it provides a simple interface that lets plugins extend this
functionality in isolation by having them depend on the flow.

![Simplified plugin setup](/images/plugins.png)

Since all Lyft apps operate on a tree of flows, the overall dependency graph
changes from a tree shape to a "bubble" shape:

![Bubble dependency graph](/images/graph.png)

This setup provides feature isolation at the compiler level which makes it much
harder to accidentally intertwine features. Each plugin also has its own feature
flag, making it very easy to disable a feature if necessary.

In addition to routing plugins, we also provide interfaces to add additional
views to any view controller, deep link plugins to deep link to any arbitrary
part of the app, list plugins to build lists with custom content, and a few
others very unique to Lyft's use cases.

## Unidirectional Data Flow

More recently we introduced a redux-like unidirectional data flow (UDF) for
screens and views within flows. Flows were optimized for state management within
a collection of screens, the UDF brings the same benefits we saw there to
individual screens.

A typical redux implementation has state flowing into the UI and actions that
modify state coming out of the UI. Influenced by [The Composable
Architecture][4], our implementation of redux actions also includes executing
side effects to interact with the environment (network, disk, notifications,
etc.).

## Declarative UI

In 2018, we began building out our [Design System][5]. At the time, it was a
layer on top of UIKit, often with a slightly modernized API, that would provide
UI elements with common defaults like fonts, colors, icons, dimensions, etc.

When Apple introduced SwiftUI in mid-2019, it required a deployment target of
iOS 13. At the time, we still supported iOS 10 and even today we still support
iOS 12 so we still can't use it.

However, we did write an internal library called `DeclarativeUI`, which provides
the same declarative APIs that SwiftUI brings but leveraging the Design System
we had already built. Even better, we've built `binding` conveniences into both
DeclarativeUI and our UDF `Store` types to make them work together seamlessly: 

```swift
import DeclarativeUI
import Unidirectional

final class QuestionView: DeclarativeUI.View {
    private let viewStore: Store<QuestionState>

    init(store: Store<QuestionState>) {
        self.viewStore = store
    }

    var body: DeclarativeUI.View {
        return VStackView(spacing: .three) {
            HeaderView(store: self.store)
            Label(text: viewStore.bind(\.header))
                .textStyle(.titleF1)
                .textAlignment(.center)
                .lineLimit(nil)
                .accessibility(postScreenChanged: viewStore.bind(\.header))
            VStackView(viewStore.bind(\.choices), spacing: .two) { choice in
                TwoChoiceButton(choice: choice).onEvent(
                    .touchUpInside,
                    action: viewStore.send(.choiseSelected(index: choice.index)))
            }
            .hidden(viewStore.bind(\.choices.isEmpty))

            if viewStore.currentState.model.usesButtonToIncrementQuestion {
                NextQuestionButton(store: self.store)
                    .hidden(viewStore.bind(\.choices.isEmpty))
            }
        }
    }
}
```

## Putting it all together

All these technologies combined make for a completely different developer
experience now than five years ago. Doing the right thing is easy, doing the
wrong thing is difficult. Features are isolated from each other, and even
feature components are separated from each other in different modules.

Testing was never easier: unit tests for modules with pure business logic,
snapshot tests for UI modules, and for integration tests it takes little effort
to sping up a standalone app with just the flow you're interested in.

State is easy to track with debug conveniences built into the architectures,
building UI is more enjoyable than it was with plain UIKit, and adding a feature
from 1 app into another is often just a matter of attaching the plugin to a
second flow without detangling it from all other features on that screen.

It's amazing to look back at where the codebase started some 6 years ago, and
where it is now. Who knows where it will be in another 6 years!

_Note: If you're interested in hearing more, I also talked about many of these
technologies on the [Lyft Mobile Podcast][6]!_

[1]: https://www.youtube.com/watch?v=dA9rGQRwHGs
[2]: https://en.wikipedia.org/wiki/Service_locator_pattern
[3]: https://square.github.io/workflow/
[4]: https://github.com/pointfreeco/swift-composable-architecture
[5]: https://design.lyft.com/building-a-design-system-library-3a1f0d09088f
[6]: https://podcasts.apple.com/us/podcast/mobile-architecture-pt-1-with-scott-berrevoets/id1453587931?i=1000512549072
