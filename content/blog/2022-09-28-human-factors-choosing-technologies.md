Title: Human factors in choosing technologies
Date: 2022-09-28
Summary: Discussion on what human factors to consider when choosing to adopt a new technology

I recently saw a thread where someone wanted to introduce a more capable
architecture pattern than what most apps start out with in a small team, but
received some pushback from teammates and was looking for help in countering
their arguments.

The thread for the most part focused on the technical benefits of the proposed
pattern, such as testability, separation of concerns, modularity, etc. These are
all valid trade-offs to consider: we’ve done the same at Lyft when figuring out
what architectures would suit us best. This is also not unique to architectures,
any big technology that influences the overall direction of the codebase:
SwiftUI vs. UIKit, RxSwift vs. Combine vs. async/await, etc.

But over time I’ve realized that even with a technically “perfect” solution (a
real oxymoron!), there is an entirely different yet equally important factor to
consider: who are the people using it—now and in the future? The success of a
particular technology is highly dependent on the answer to that question, and it
plays a huge role at different stages of the development of that technology.

In the thread I mentioned above there was very little focus on the human aspect
of the proposal, so I wanted to list a number of things that I personally ask
myself and our teams before considering moving forward:

**How much is the onboarding/ramp-up cost?** While I generally think short-term
pain is worth long-term gain, onboarding is often a continuous cost. New people
join, you might have interns, non-mobile engineers wanting to make quick
contributions, etc. If those people first need a lot of time to ramp up, it’s
worth wondering if the benefits are worth it, or how to reduce that burden. For
example, while we currently aren't using any SwiftUI at Lyft, we have a layer of
[sugar syntax on top of UIKit][2] that enables us to use SwiftUI-like syntax anyway.
This makes it easier for both new people that join and already know SwiftUI and
for everybody to move over to SwiftUI if/when we're ready for that.

**How easy is it to undo?** Or: what is the cost of mistakes? If things don’t
pan out the way we want them to, how easily could we switch to something else?
The more difficult switching back is, the higher the commitment level and the
more we need to be sure it’s worth it. This applies both to the internals of the
framework and how the code that uses the framework is structured.

**Is it easy to do the right thing?** This one is straightforward: if it’s easy
to do the right thing it’s more likely people will do the right thing and
achieve the architecture’s potential more. Conversely, if it’s easy to do the
wrong thing, the benefits aren’t realized as much. Especially considering my
previous point, if it’s hard to undo bad usage it’s maybe worth going back to
the drawing board.

**How much support is available?** Popular technologies have a lot of online
material available for support in the form of Stack Overflow questions and
answers, blog posts, videos, open source code + discussions on GitHub, etc. A
home-built solution means this knowledge only lives in-house which increases the
bus factor. The same is true for very opinionated third-party libraries like
RxSwift or The Composable Architecture. I’m a fan of both, but without fully
understanding how they’re implemented you’re at the mercy of the developers and
contributors of these libraries for years to come.

**How much institutional knowledge does it require?** Good architectures hide
domain complexity for its consumers, and incur the complexity internally. To
some extent that’s fine, but if the internals become so complicated that few
people know how it works there is again a high bus factor. It can absolutely be
worth putting some complexity/boilerplate burden onto feature owners to avoid
making complex abstractions that are hard to change in the future once it’s used
everywhere and the original developers have left.

**How much effort does it take to see 100% adoption?** Depending on the size of
the existing code base, it could take a long time to get 100% adoption. That can
be OK if this is the codebase’s first serious architecture, but if it’s version
5 and some parts of the codebase still use version 1 through 3, it’s probably
worth removing those first and reducing [lava layers][1]. Even if the change
from version 10 to 11 is small and easy, the fragmentation of the codebase
inhibits developer productivity. The quicker the migration the better, and if
the codebase can safely be migrated through automation that’s the best case
outcome.

But the most important one of all: **do people actually like the architecture?**
No one likes working in a codebase where everything is a hassle, the underlying
concepts never seem to make sense, abstractions are leaky, and you seem to
always have to do work for it instead of it working for you. Those codebases
diminish the team’s motivation levels and will affect many of the other points
from above.

On the flip side, if people like the proposed patterns, they will put in a lot
more work in to use them correctly, try harder to do the right thing, are
willing to help others, etc. If not, forcing patterns people don’t like could
lead to developer unhappiness and attrition. We have more than a few examples of
this at Lyft, where a slightly inferior technical solution is overall much more
beneficial because the pattern is a bit simpler to use than the alternative.

Going back to why I started writing this in the first place: in my opinion the
question “what counterarguments can I use” is not a great first question to ask
when it comes to convincing people your solution is the best one out there.
Understanding _why_ people are resistant is key. Sure, some people just don’t
like change, but papering over any of the concerns above with a technically
superior solution is a recipe for a bunch of barely-adopted technologies in a
codebase that’s often worse off than if nothing had been done in the first
place.

[1]: http://mikehadlow.blogspot.com/2014/12/the-lava-layer-anti-pattern.html
[2]: http://www.scottberrevoets.com/2021/10/14/ios-architecture-at-lyft/#declarative-ui
