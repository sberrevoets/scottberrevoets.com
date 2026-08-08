Title: The foundations of a mobile platform
Date: 2026-08-11
Description: Why mobile platform foundations matter for engineering velocity, reliability, observability, and distribution
CardDescription: How strong mobile platform foundations help product teams build and ship

In larger teams or companies, most people agree that the mobile platform is the
shared infrastructure an app and its features are built upon. In earlier stages,
that might simply mean "shared code and helper functions", but when the app and
team start scaling, the platform deserves a lot more investment and
consideration. The scope of the platform broadens very quickly, and its
foundations have a big influence on the engineering velocity of all product
teams and the overall reliability of the app in the hands of users.

For a good, scalable platform, a more complete definition is **the underlying
systems that enable product teams to build, run, observe, and distribute their
products**. The verbs above do a lot of heavy lifting in terms of what systems
they consist of:

* **Build**: architecture, CI/CD, build and lint tools, IDE, developer
experience, agent tooling, guidance, and context
* **Run**: networking, persistence, authentication, testing frameworks, and any
app/domain-specific systems such as audio playback/voice recording or the user
location and mapping frameworks
* **Observe**: analytics, logging, crash/error reporting, general observability
* **Distribute**: release/QA process, experimentation, bug reporting

The size of the platform scales with the size of the codebase, team, and
operational complexity. Many apps start simple with very basic functionality to
test out an idea, but if the idea catches on and the app scales, the feature set
grows, more people start contributing, and distribution and monitoring become
more complicated.

Most apps will have some of the systems I mentioned above, however simple, and
as the app's complexity or functionality set grows, so does the platform. Even
if there's no explicit task to build out some part of the platform, developers
tend to extract reusable code so it can be shared across features or even across
apps which is the start of the platform. 

## Mobile is even more complicated

These systems are not uniquely important on mobile, but they are
_especially_ important there. Native apps are downloaded once and run on the
end user's device, outside of the engineering team's controlled environment.
This means network conditions, hardware capabilities, other running apps,
and OS versions and settings all vary from user to user. New app versions
don't propagate to all users right away, but more gradually over time.
Observability into the user's hardware environment is critical, yet more
difficult to implement.

Getting the mobile platform right means accounting for all these variable
factors as best as possible. It means the design system is implemented in both
dark and light mode. It means the error reporting framework attaches relevant
context about the user and device to error reports. It means retrying network
requests for a reasonable amount of time and then failing gracefully if the
network is bad. It means code is easy to test because bugs in production will
stay around for a while.

## The impact of a good platform

Platform development becomes increasingly important as the app scales. Apps
that scale that much usually are popular and have a bigger company built
around the app, or there was already a company that's now building an app.

The platform is the foundation of the whole app, which means the quality of the
app is, to a large degree, defined by the quality of the platform:

* The quality of the design system decides the quality of the UI in terms of
  consistency, usability, and accessibility
* A fast networking layer with good retry and cancelation policies lets the user
  get their tasks done fast and without network frustration
* Architectural patterns decide how testable and reliable the app is
* Observability into runtime behavior and edge cases make it easier to catch
  and fix bugs

The quality of these systems has a [compounding effect], both good and bad. A
bad platform gets in the way, requires constant maintenance and firefighting,
and brings a lot of uncertainty. Engineers spend a lot of time answering
questions like:

* What networking client do I use? 
* Is there a way to easily mock the user service?
* How do I know my feature works as expected after rollout?
* Where in the codebase does my feature fit?
* Can I build this UI using existing components?

A good platform has clear answers to these questions:

* Use the standard networking client unless you need one of the documented
  unsupported cases
* Mocking services works the same way everywhere
* Observability is standardized and built-in; feature-specific observability
  uses the same logging, analytics, and alerting stack
* Module boundaries, naming, and project organization make it easy to
  navigate the codebase and find relevant code
* Feature UI starts from the design system and uses its components directly

Developers have high trust in this platform because it accelerates development
and operational velocity while improving feature quality.

In modern-day engineering, agentic workflows heavily depend on the strength
of the platform, as LLMs do better in codebases with consistent patterns, clear
constraints, and tests to validate changes. Agents will repeat the patterns they
see, so the stronger they are the stronger they will continue to be. If there
are multiple ways to do the same thing, the agent has to pick which one to
choose, or it introduces a third, hybrid pattern.

Existing documentation can double as agent guidance and requires less explicit
context. It can be the difference between a simple "implement a GET request to
the users endpoint" prompt and a much more specific one that requires the
engineer to type more and know and remember all the intricacies of the
networking client.

## Why is building a platform difficult?

### Industry standards are limited

Apple and Google as platform vendors provide the tools necessary to build and
ship an app, but their primary audience is smaller, often indie, app developers.
They provide very little tooling specific to larger teams: CI, observability and
code coverage dashboards, linters, blessed architectures, migration efforts,
etc. are either too limited or don't exist at all.

Some third-party tooling exists, but is often the under-rewarded effort of open
source developers that can't give this work the time and attention it deserves.
Other tools become paid if a company finds a way to monetize them. The platform
is a moving target with major updates every year and many smaller ones
throughout, so keeping up takes time.

Some of these systems also can't be built generically, like a design system and
its fonts, colors, spacing, etc., or need to be chosen across the stack like
experimentation or analytics frameworks.

### It requires good judgment

Building the platform well requires good judgment and experience, and ideally
experience in exercising good judgment. Generally this means more senior
engineers that have seen both good and bad, with technical depth in a lot of
different areas. Platform work means understanding when to duplicate or build an
abstraction, what kind of testing is the most effective, and what migrations are
worth doing and when, which doesn't come naturally to most engineers. I still
often have to remind myself that platform engineering in many ways is a very
different skill from product engineering.

### Changing course is expensive

When dozens of features rely on a system, you can't just remove that system or
replace it with something else. It requires a [code migration], which could take
months or years of consistent effort. Many teams are not willing to do that and
would rather live with the old system.

### It's a long-term bet

It's a long play: building out each system takes time, and teams don't
immediately see the benefits of the work. The real compounding effect happens
once many of these systems are adopted widely. Building a solid logging system
does nothing until most features use the system.

### It's a "people-y" job

Doing this work requires understanding team dynamics and other [human factors].
Knowing what battles to pick, how to educate people, working with others to find
the best solution for them, reiterating ideas and visions, etc. is critical for
this work. Other developers are the customers, and keeping the customer happy is
important.

## Who should own the platform?

Platform ownership is a long-term, continuous effort. This usually means a
dedicated team as the app scales. Org structure and size doesn't really
matter: at Speak I'm the only iOS platform engineer, at Lyft I led an org of
3 teams.

The development and maintenance of a platform usually undergoes multiple
iterations as the tech, industry, and OS evolve over the years. That upkeep is
much easier to execute on when one team develops a vision, builds the expertise,
and owns the development than if individual pieces are owned by different teams.

A platform whose quality depends on the deadlines, narrow viewpoints, and
political pressure of a product-oriented team is less likely to remain of high
quality as it evolves. That team might not be able to prioritize any ongoing
maintenance, doesn't look at its development holistically, or dissolves entirely
leaving the code more or less unowned.

The outcome tends to be better if a more neutral developer, with good
connections to all the teams is responsible. That developer is then in a better
position to come up with scalable solutions that work across the board instead
of solving a single use case.


[compounding effect]: https://scottberrevoets.com/2025/07/02/flywheel-of-tech-debt/
[code migration]: https://scottberrevoets.com/2022/11/15/migration-strategies-in-large-codebases/
[human factors]: https://scottberrevoets.com/2022/09/28/human-factors-in-choosing-technologies/
