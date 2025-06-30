Title: Flywheel of tech debt
Date: 2025-07-02
Description: Explanation of why tech debt in infrastructure is much more risky than further downstream

Tech debt is often compared to financial debt, in that you're borrowing
development time now to pay it off with more development time later. When
"later" comes around, the development time needed to fix the issues introduced
earlier is too high so the new thing is also not built "correctly", and the
pattern repeats itself: tech debt begets tech debt.

A few years ago I came across an article about the [Taxonomy of Tech Debt],
which talks about the contagion of tech debt: the easier a piece of tech debt
spreads, the higher its impact because fixing that fragile code means
preemptively fixing it in future cases as well.

A more extreme version of this is a **flywheel of tech debt**&trade;: tech debt
that doesn't just expand linearly because of a high contagion factor, but that
multiplies at an excessive rate. This tends to happen in one specific part of
the codebase: the infrastructure. Any libraries, frameworks, architectures,
foundational patterns, etc. with tech debt have this flywheel and once it's
rotating it's very difficult to stop.

> With a sufficient number of users of an API, it does not matter what you
> promise in the contract: all observable behaviours of your system will be
> depended on by somebody.
>
> [Hyrum's Law]

Hyrum's Law is the primary reason why it's so hard to remove any tech debt from
infrastructure code: even if the tech debt is internal to the architecture to
account for one edge case, the behavior is there and _will_ be depended on by
somebody. If the tech debt is more severe and affects the API, the flywheel goes
brrr and now _requires_ all consumers of that API to incur the tech debt as
well, unless they specifically understand (how) to avoid it. 

What's worse is that after some time passes and people are using these APIs,
it's much more difficult to remove because it also requires removing it at all
the call sites that API. For a large team/codebase, this requires a lot of
coordination between teams and can take years of time and effort. One team that
doesn't pull its weight impacts everyone else.

This is ironic because in many situations that foundational layer with good
abstractions and nice developer ergonomics is specifically created to _avoid_
tech debt. The more this happens, the more brittle the foundations get until we
get to the [other xkcd]. As such, I tend to advocate for moving the fragile code
downstream, to the feature code as much as possible. This reduces chances of it
impacting other features, even if that means the fragile code is worse or more
risky.

The cost of fragile infrastructure code is so high because that code is
generally long-lived, where the feature may be scrapped before it even launches.
The team that introduces this code is now also directly responsible for it
without impacting everybody else in the process. And, if the tech debt finally
becomes too painful to deal with, fixing it is much simpler and easier to roll
out than a fundamental change in the foundational layer of an app.

In the past I reluctantly accepted a hack here and there in some foundational
libraries, but I intend to push back harder going forward. Spending years
working out a single parameter from a public method in some part of our
architecture is a valuable lesson learned...

[Taxonomy of Tech Debt]: https://technology.riotgames.com/news/taxonomy-tech-debt
[Hyrum's Law]: https://xkcd.com/1172/
[other xkcd]: https://xkcd.com/2347/
