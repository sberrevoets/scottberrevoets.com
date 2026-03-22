Title: Migration strategies in large codebases
Date: 2022-11-15
Summary: Strategies we employ in completing migrations in our mobile codebases

Code migrations are a fact of life for large codebases. New technologies pop up,
platforms see improvements, and programming languages get new features you might
want to adopt. Not performing these migrations and keeping up with the times is
simply not an option in most cases. While some migrations are easy 1 for 1
replacements that can/should be scripted, that’s not true for the more
“semantic” migrations—the new code accomplishes the same but in an entirely
different manner.

We’ve done a number of these semantic migrations in Lyft’s mobile codebases and
while we’ve learned something from every one of them (and applied the learnings
the next time), they only get harder as time goes on.

What makes migrations so difficult? This generally comes down to how development
works in large codebases: there is no 1 mobile team, but rather a lot of
vertical teams (e.g. payments, new user experience, etc.) that all build their
own features, using shared foundational code and architectural patterns. The
coordination of dozens of teams on the progress of a migration is what makes
this difficult:

* Codebases tend to grow ad infinitum, so there is simply more code to migrate
  each time and there are more “weird” cases that make automating a migration
  difficult.
* Getting (and keeping) buy-in and commitment. Teams all have their own plans
  and priorities, and migrating code from pattern A to pattern B is often not
  high on the priority list. If it is, that could change before the migration is
  completed.
* Senior engineers on those teams tend to have good judgment on the importance
  of reducing tech debt and can weigh it against other priorities coming from
  product managers and designers. Junior engineers that get pulled in 4
  different directions are less likely to push back against their direct
  teammates, so tech debt tickets are moved to an ever-expanding Jira backlog.
* Teams are not static. You might inherit code written years ago that still
  works and is in use, but you didn’t even know it existed until last week. And
  now it needs to be migrated? Or it’s that one feature that is somehow mission
  critical but no one knows how to even get in the state to show it, let alone
  test new code in it.

So how do we get these migrations done anyway? There is no silver bullet, but we
have started using a number of strategies to make these migrations less
painful—and almost all of them have to do with improving the communication and
expectations everyone involved has.

## Migration tracker
The biggest leap forward for us was the rollout of an in-house web dashboard
that shows progress on all ongoing migrations in our iOS and Android codebases.
It shows all the important information anyone could want to know: the start
date, (projected) completion date, links to documentation and support channels,
relative priority (more on that below), etc.

But the real win is automatic progress tracking. Every migration is defined as
the presence of a certain pattern in the codebase we want to get rid of. A cron
job records all instances of that pattern on the main branch once a day, so we
know exactly how much code has been migrated and how much is left.

Furthermore, our codebase is heavily modularized, and through CODEOWNERS every
module is required to define what team owns it. This data is shared with the
Migration Tracker, so it can give a detailed breakdown by module *and by team*
of how much unmigrated code is left. This is extremely helpful in understanding
which teams might need extra time, help, or nudging in getting everything done.

## Timeline
The “deadline” of a migration needs to be carefully chosen. Not giving people
enough time makes them not do the work at all, giving them too much time means
people will procrastinate and needlessly extend the migration time. If it looks
like teams are not going to make the deadline (as projected by the Migration
Tracker), we ask them when they _can_ get it done. We usually accept whatever
answer the team gives, but hold them accountable to that since they themselves
picked that timeframe.

## Priorities
Teams that are far behind in code modernization might have to migrate their code
in multiple ways. We give each migration a priority (P0/P1/P2/P3) to give teams
a sense of where to focus their tech debt energy first.

A P0 migration is a “must-do-or-else” (externally mandated changes, tight
deadlines, extremely high impact on overall trajectory of the codebase or
product, etc.), a P1 is high impact but not as urgent, P2 is a nice to have, and
P3 is almost more of an FYI.

This helps everyone understand where they should focus their energy, instead of
seeing a potentially long list of items that are all seemingly equally important
migrations.

## Incremental value
Where possible (which is most cases), we try to bring incremental value as a
migration is being performed. For example, if we set out to replace all uses of
class A with class B because class B performs better, the places where class B
is used should see that performance increase before the rest of the code has
been migrated. This has a few benefits:

* It rewards teams that have done their part of the overall migration
* It’s easier to convince people doing their part has value since they
  themselves immediately see that value
* It de-risks long-running migrations—if it gets to 95% completion we realize
  95% of the benefits and not 0%

## Only invest in the new
The initial value (like performance improvements in the example above) teams get
from migrating their own code might not be enough to convince them to do it. But
as more and more improvements are made to “class B” (e.g. API ergonomics,
integrated analytics, compatibility with other systems) that “class A” doesn’t
have, the value proposition for the migration changes with time. We no longer
update A, which means there's some amount of bit rot and it becomes more
cumbersome to use.

In extreme cases we could even remove features of class A that would necessitate
a migration, but we haven’t done that so far and would like to avoid it to avoid
losing goodwill with teams.

## Develop great partnerships
Getting adoption of a new pattern or tool is difficult even if it doesn’t
involve a new migration, because there is no precedent. Early adopters will hit
all the rough edges and have often incomplete documentation and no sample code.
The developer experience isn’t great (yet), so we make ourselves very available
to their needs. We take their feedback seriously and address it promptly, sit
down with them to help solve their issues, and generally spend a lot of time
with them working out the kinks. We do this 1) to build more confidence that
what we built is production-ready and 2) to recognize/reward people that want to
try new things by reducing as much of the growing pains as possible.

Of course, good developer experience is important for all teams and not just
early adopters, but piloting teams can help us get the ball rolling with other
teams as well. Positive reviews from users of Great New Thing is different than
hearing it from the developers of Great New Thing.

## Avoid new uses
To avoid creating a moving target, as soon as we start a new migration we lock
down the uses of that pattern to only the current ones and no longer accept new
uses of this pattern. Depending on the situation we have a few different ways of
accomplishing this:

* We add a linter rule or sometimes entirely new type of (custom) linter and
  introduce exceptions to all existing use cases
* We rename a class or method by prepending the current name with `DEPRECATED`.
  This isn’t particularly elegant, but it alerts the author and PR reviewers
  that new legacy code is being introduced, which usually has them dig deeper
  and figure out what to do instead.
* If an entire module is being deprecated, we don’t easily let new modules
  depend on it. Exceptions are always possible, but engineers have to talk to us
  first so we can guide them in the right direction.

These measures are just to generate awareness that a pattern is outdated, it
doesn’t always communicate why it’s being deprecated and what’s replacing it.
But if people come to us asking for an exception we can explain it or link to
docs, an opportunity we wouldn’t have had if we didn’t do any of the things
above.

## Support, support, support
And that brings me to the most critical and time-consuming piece: support. This
means helping people with questions, plugging gaps new patterns have compared to
the old ones, checking in with people on progress, celebrating the completion of
major (or all!) migrations with everyone that helped contribute, assisting teams
that are having difficulty prioritizing the work, and anything else that gets
the work done.

Migrations are a very specific type of codebase maintenance due to the large
footprint they often have in a lot of the codebase. It’s an all-hands on deck
situation and requires proper coordination and communication, sometimes for
years on end. It’s hard to get them right and we’re still fine-tuning our
strategies but applying the learnings I described here have made us become
better at them. I can only hope one day refactoring tools become smart enough to
automate the work for us.
