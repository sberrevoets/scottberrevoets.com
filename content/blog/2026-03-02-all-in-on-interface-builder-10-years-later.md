Title: All in on Interface Builder: 10 years later
Date: 2026-03-02
Description: Lessons from a contrarian technology bet that eventually expired


Back in 2017, I wrote about how we used [Interface Builder] as our primary way
of building UI at Lyft. Interestingly, Speak chose to use Interface Builder to
build UI too before SwiftUI came along, though without the same tooling we had
at Lyft. With Interface Builder mostly forgotten, including by Apple itself, I
think it's worth sharing some lessons learned after all this time.

I didn't explicitly share this in the original post, but we didn't take the
decision to use Interface Builder lightly. The main benefits we saw:

* The Swift toolchain was very young and not fully developed yet. The compiler
  was slow and autocomplete was much less advanced, so the more code we could
  shove in Interface Builder the less code that had to be compiled. This had a
  significant impact on build times and build failures for us.
* We were hoping for what Swift Previews eventually got much closer to: a quick
  way to understand what a view looks like at runtime without spinning up a
  simulator
* It saved developers a lot of typing manual, tedious Auto Layout code.
  Interface Builder provide immediate feedback about whether your constraints
  resolved cleanly

We were also aware of the pain points of Interface Builder and built good
tooling around managing those. We got to meet with Apple engineers to voice IB's
weaknesses that we couldn't tool our way out of, and were generally happy to not
be writing super verbose Auto Layout code. Merge conflicts still never were a
problem because we distributed the UI over many individual storyboards and xibs.

We felt we'd found a way to make Interface Builder scale pretty well, and it did
for a long time. But cracks started to form in the strategy:

* We had primarily invested in storyboards, but a stronger focus on code
  testability was directly in conflict with that investment
* New team members never fully got the hang of some of these more nuanced and
  advanced ways of using Interface Builder
* `@IBDesignable` never really lived up to its expectations, being buggy, slow,
  and unreliable
* Routing complexity changed our strategy over time to not use segues anymore,
  losing some of the benefits of using IB
* UIs became a lot more complicated and constraint management became difficult
  in Interface Builder (this likely would've also been hard in programmatic UI)
* Building Lyft's internal design system was more difficult while supporting
  Interface Builder

All these problems came with scale none of us had really seen before. At the
same time, the original problem of writing programmatic Auto Layout also still
was a concern, so a potential migration was costly with unclear benefits.

Until SwiftUI came along. With SwiftUI, we finally felt like the cons started to
outweigh the pros. We embarked on what ended up being a five year migration
journey away from Interface Builder, finally completing the effort mid-2024.
This multi-step migration was the largest we had undertaken on iOS (on Android
the Dagger 1 to Dagger 2 migration was of similar scale), and immediately
justified the investment into [DeclarativeUI] as a prelude to SwiftUI adoption.

Joining Speak also exposed me to the newcomer perspective of having so much UI
defined in Interface Builder. It's hard to understand the scope, complexity, and
context of a screen when all its configuration is tucked away in the right
sidebar, with many implicit behaviors from checkboxes, dropdowns, and long lists
of constraints and their properties.

We're also dealing with the same testability problem (even though dependency
injection with storyboards is a little easier nowadays), and the storyboards in
the Speak codebase are more like wireframes than actual designs, so navigating
them isn't any easier than code. Refactoring is harder because the UI definition is
split into two (some in code, some in Interface Builder), and the weakly typed
IB/code connections between `@IBOutlet`s and `@IBAction`s make it hard and risky
to understand which code is still used and which isn't.

A more modern problem is that because Interface Builder was not the popular
choice in an ecosystem where open source was already much less valued than in
other development domains, there is very little Interface Builder XML that AI
agents are trained on. This means their effectiveness is also much less compared
to plain Swift, which is doubly annoying when AI agents would otherwise reduce
the migration cost tremendously.

Let it be clear that I wouldn't recommend Interface Builder as a tool for
building UI anymore, but despite my change of heart, I can't say I regret the
choice of introducing it at the time we did. There were no signs a replacement
UI framework would come along, teams were reasonably productive with it, and we
benefited from its use for a good 4-5 years. Some of the tools and
implementations were arguably too clever for their own good, and that's a
valuable lesson learned.

But I think the bigger lesson is that there's a cost to architectural decisions
like these, and in an industry that's always changing, the pros and cons need
constant weighing. It's easy to adopt a sunk cost mentality and keep investing
more time and resources because the migration cost is high, but like other tech
debt it just increases the cost of migration at a later stage.

Relating this to my own post about [human factors in choosing technologies], the
adoption, ramp-up, and support factors were all pretty favorable. However, in
retrospect, IB scored low on the ability to undo (as many architectures would),
and after declarative UIs came along there was a downward trend in whether
engineers _liked_ using IB. Once that trend started, Interface Builder's days
were numbered, even if the path to obsolescence was long and painful. 

[Interface Builder]: https://scottberrevoets.com/2017/03/06/using-interface-builder-at-lyft/
[testabilty]: https://www.scottberrevoets.com/2024/11/18/shifting-the-testing-culture-motivation/
[DeclarativeUI]: https://www.scottberrevoets.com/2021/10/14/ios-architecture-at-lyft/#declarative-ui
[human factors in choosing technologies]: https://www.scottberrevoets.com/2022/09/28/human-factors-in-choosing-technologies/
