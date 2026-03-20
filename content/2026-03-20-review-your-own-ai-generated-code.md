Title: Review your own AI-generated code
Date: 2026-03-20
Description: Code review was designed for a world where humans wrote all the code. In a world where agents do, the value of peer review shifts from code to plans and specs.

Years ago, when we started to have 5+ contributors to our codebase at Lyft, we
had to establish a code review process with high enough value to justify the
friction it caused. However, "value" is very subjective, as not everyone cares
about the same qualities of a pull request:

* Catching runtime problems like bugs, security vulnerabilities, or performance
  issues
* Knowledge and context sharing, mentoring, or general collaboration
* Code quality and maintainability
* Upholding code consistency, conventions, style, naming, grammar, etc.

Over the last 10-15 years, the industry has seen its **engineering foundations**
greatly improved: programming languages, CI systems, build tools, internal
architectures and processes, and engineering principles have improved so much
that human review of many of these potential issues has lost a lot of their
value. Linters keep code consistent as much as possible, standardized
architectures should enable reliability and testability, modern programming
languages and paradigms enable low code complexity, and CI validates all these
conditions before deploying.

With these advancements over the years, I find myself leaving significantly
fewer comments on PRs than before. Any comments I do leave are usually about
local, low-severity code quality improvements, avoiding suppressing linter
violations, asking for specs/context, double-checking intention, etc. Whenever
possible, I try to instead invest in some of these foundations: an additional
linter rule, updating CI, providing better architectural patterns. That time
investment scales much better than me leaving comments on individual PRs.

And that brings us to 2026, where we get to re-evaluate the "value" of code
review because of AI agents. The impact of AI on code review is threefold:

1. **Output quality**: a year ago we called it vibe-coding, today it's much more
   difficult to tell apart agent code from human code if the human(s) behind the
   agent code put real effort into getting high-quality output from the agent
2. **Agentic review**: many teams have agents review other agents' code. Codex
   has `/review`, Claude Code has [Code Review], and Cursor, Copilot, and
   various observability and SRE tools all have code review agents as well.

       I've made code review part of my own workflow as well: write a plan, have
       an agent refactor a bunch of code, and have other agents review it for
       issues. [OpenAI] is, unsurprisingly, pushing the boundaries with an
       internal project where all code is reviewed by agents and mostly not by
       humans at all.

3. **Code volume**: engineers are "writing" a lot more code than before and, if
   we stick to our old practices, the burden of code review increases more too

We have gotten faster at producing high-quality code, but if it can't be
reviewed at higher speed as well, we've just found ourselves a _new_ bottleneck.

The status quo is that engineers review _each other_'s code to avoid **author
bias**, which could lead to overestimating the quality, performance, and clarity
of the code written by the author. But in a world where the entire development
workflow is changing and code is increasingly written by agents, we're no longer
actually reviewing _each other_'s code, we're reviewing _agents'_ code. The bias
no longer exists at the code level; it moves to the plan level.

Human accountability and oversight are still important, but **the primary
responsibility of code review can shift to the engineer that drove the agent in
the first place**. That engineer is coming in with all the context and can
review the code much faster than other engineers. For bigger changes, their
author bias could still apply to the _plan_, so it's good to have other
engineers review that, but the code itself is just execution.

With the right plan and LLM guidance in place, agents have gotten excellent at
implementing exactly according to spec. When an agent introduces a bug, it's
less likely to be an implementation issue and more likely an underspecification
of the plan, guidance, or documentation. The correctness of these documents is
still a shared team responsibility.

The outcome is more than just removing the new bottleneck in writing code.
Engineers are more autonomous in shipping because they don't have to wait for
others, possibly in different time zones, and can fully unblock themselves in
all the work they are doing. With strong PR checks, such as linters and code
quality gates, in place to prevent old-fashioned vibe-coding, the bar remains
high while increasing velocity.

There is one notable downside to this approach: the reduced context sharing and
mentoring. It's a real benefit of "traditional" code review, but not the most
effective time to break knowledge silos. As I mentioned earlier, _plans_ still
warrant review by others, and plans are usually derivatives of tech specs or
PRDs. A well-written document provides the necessary context, the whys, the
thought process, and the alternatives considered. It's also easier to ask
questions and act on feedback in this stage because it's much earlier in the
development lifecycle.

In a world where agentic engineering is the norm, teams review plans, specs, and
agent guidance together so they capture the intended design and behavior; the
code becomes an implementation detail of the plan that can be self-reviewed by
the driver of the agent.


[Code Review]: https://code.claude.com/docs/en/code-review
[OpenAI]: https://openai.com/index/harness-engineering/
