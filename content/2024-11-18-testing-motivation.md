Title: Shifting the testing culture: Motivation
Date: 2024-11-20
Summary: Motivation for investing in automated testing and the benefits and drawbacks we've experienced at Lyft

Five years ago I began promoting automated testing heavily within Lyft even
though I didn't have any real experience in writing big test suites myself. Many
hands make light work, so I found a few people who shared this thinking and we
started on what turned out a multi-year testing journey. What did we do?

1. We optimized the architecture in a much more profound way than just "you can
   write tests more easily"
2. We built a ton of tooling to improve the developer experience and to hold
   ourselves more accountable
3. We started measuring and reporting progress on our efforts regularly
4. We included testing in company-wide processes like incident review and
   biannual planning

The end result of all the major efforts, minor quality-of-life improvements, and
fixing tiny paper cuts has led to test-writing now being a huge part of our
engineering culture. That's not to say we're there—there is definitely still
more work to be done. But the progress is pretty remarkable and I wanted to
share more about it.

I'll do this in a series of blog posts, this being the first one:

1. **Motivation**: why we thought this was an important area to invest in
2. **[Infrastructure]**: how we upgraded our infrastructure to optimize for
   testability
3. **[Code coverage]**: how we measure, report, and act on our code coverage

[Infrastructure]: {filename}2024-11-19-testing-infrastructure.md
[Code coverage]: {filename}2024-11-20-testing-code-coverage.md

## Motivation

After experiencing the hypergrowth of both our team and codebase in 2017-2019,
it became clear that the only way to maintain code and product quality was
through automated testing. Prior to that, a lot of testing would happen through
knowledgeable developers, QA processes, and dogfooding, but that wasn't going to
hold up indefinitely for a few reasons:

* QA time is costly because a human hour is much more expensive than a computer
  hour. Writing a unit test means you can now validate any code change with that
  test in a fraction of a second, but a QA engineer needs to spend that time
  again and again.
* QA processes themselves are expensive: test plan management and maintenance
  costs time and money and the process itself needs to be developed, documented,
  and updated
* People leave, and with them institutional knowledge leaves as well. It takes a
  long time for new people to build that knowledge, if they ever get there.

In short, computers can handle 80-90% of this work faster and more accurately
than developers can. As with all infrastructure, it takes some time to set it up
in an effective way, but since that's a one-time effort it should pay itself off
over time.

## Testing methodologies

Unit testing, acceptance testing, integration testing, system testing,
regression testing, UI testing... fanatics will tell you they're all important.
I don't necessarily disagree, but how hard you go also depends on how you need
to balance quality and velocity. Aviation software leans much more toward
quality, a rideshare app comparably more toward velocity.

So we initially focused on two types of testing: unit testing and UI testing.
After snapshot testing became popular on both iOS and Android we added that to
our arsenal as well.

Unit and snapshot tests are written by mobile developers for their own code, UI
tests cover larger flows and are written by SETs. (In my opinion UI tests, if
you choose to invest in them, should also be written by the developers that
wrote the original code, but that is not the setup we have today.)

## Benefits

It feels a bit weird to be writing these articles pretending it's some novel
idea that writing tests benefits an engineering organization like that isn't
already common knowledge. However, testing culture in the iOS community, and I
suspect all "frontend" disciplines (web, mobile, TVs, etc.), is weak compared to
that in other communities. For one because UI is hard to test, but also because
Apple itself doesn't promote it much as a best practice.

To not just speak in hypotheticals, the benefits we've experienced firsthand
are:

* **Behavior validation**: The most obvious benefit is that tests validate how
  code behaves. Bug fixes will see fewer regressions, refactors are safer, and
  the app is generally of higher quality because every bug happens only once (in
  theory) and many are prevented from happening at all.
* **Behavior documentation**: Code becomes more self-documenting as a lot of the
  behavior is prescribed in tests. You can skim test names/descriptions to
  understand how a class is supposed to behave, with little risk of the
  documentation becoming outdated because the tests will fail if they don't
  match the actual behavior.
* **Code readability**: in order to write reasonable tests, code has to be
  structured reasonably well too. Test setup is hard with spaghetti code, so
  there's an incentive to write cleaner code. (Unfortunately, the opposite is
  true too: poorly written code can often lead to poorly written or no tests.)
* **Engineering satisfaction**: a well-tested codebase is more satisfying to
  work in because developers have higher confidence in the correctness of their
  code. It "feels" easier to make changes because you can rely on the tests to
  catch any mistakes.

## Drawbacks

I don't really like writing these articles without also mentioning the
drawbacks. The main ones we've experienced are:

* **Time cost**: it simply takes time to write tests, and there's strong
  correlation between a codebase that _desperately needs tests_ and the time it
  takes to write those tests
* **False sense of security**: it's easy to become overly confident in the test
  suite and assume a passing test suite means there are no bugs, when in reality
  the test suite might be incomplete or of low quality
* **Learning curve**: there's a learning curve involved, especially in a large
  codebase, and not everyone is interested in learning this
* **More code to maintain**: code requires maintenance and test code is no
  different

Over time we've tried to minimize these drawbacks as best as we could, but most
of them will likely always be a factor. In the next articles I'll go in a
bit more depth on the mitigation strategies we've used and how effective they've
been.
