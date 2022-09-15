Title: Third-party libraries are no party at all
Date: 2022-07-15
Summary: Details on how we evaluate whether to add new third-party libraries

_What better way to end the week than with a hot take?_

In my 8 years at Lyft, product managers or engineers have often wanted to add
third-party libraries to one of our apps. Sometimes it’s necessary to integrate
with a specific vendor (like PayPal), sometimes it’s to avoid having to build
something complicated, and sometimes it’s simply to not reinvent the wheel.

While these are generally reasonable considerations, the risks and associated
costs of using a third-party library are often overlooked or misunderstood. In
some cases the risk is worth it, but to be able to determine that you first need
to be able to define that risk accurately. To make that risk assessment more
transparent and consistent, we defined a process of things we look at to
determine how much risk we're incurring by integrating it and shipping it in one
or more production apps.

## Risks

Most larger organizations, including ours, have some form of code review as part
of their development practices. For those teams, adding a third-party library is
equivalent to adding a bunch of unreviewed code written by someone who doesn't
work on the team, subverting the standards upheld during code review and
shipping code of unknown quality. This introduces risk in how the app runs,
long-term development of the app, and, for larger teams, overall business risk.

### Runtime risks

Library code generally has the same level of access to system resources as
general app code, but they don't necessarily apply the best practices the
team put in place for managing these resources. This means they have access
to the disk, network, memory, CPU, etc. without any restrictions or
limitations, so they can (over)write files to disk, be memory or CPU hogs
with unoptimized code, cause dead locks or main thread delays, download (and
upload!) tons of data, etc. Worse, they can cause crashes or even [crash
loops][1]. [Twice][2].

Many of these situations aren't discovered until the app is already available to
customers, at which point fixing it requires creating a new build and going
through the review process which is often time intensive and costly. The risk
can be somewhat mitigated by invoking the library behind a feature flag, but
that isn't a silver bullet either (see below).

### Development risks

To quote a coworker: "every line of code is a liability", and this is even more
true for code you didn't write yourself. Libraries could be slow in adopting new
technologies or APIs holding the codebase back, or too fast causing a deployment
target that's too high. When Apple and Google introduce new OS versions each
year, they often require developers update their code based on changes in their
SDKs, and library developers have to follow suit. This requires coordinated
efforts, alignment in priorities, and the ability to get the work done in a
timely manner.

As the mobile platforms are ever-changing this becomes a continuous, ongoing
risk, compounded by the problem that teams and organizations aren't static
either. When a library that was integrated by a team that no longer exists needs
to be updated, it takes a long time to figure out who should do so. It has
proven extremely rare and extremely difficult to remove a library once it's
there, so we treat it as a long-term maintenance cost.

### Business risks

As I mentioned above, modern OSes make no distinction between app code and
library code, so in addition to system resources they also have access to user
information. As app developers we're responsible for using that information
properly, and any libraries are part of that responsibility.

If the user grants location access to the Lyft app, any third-party library
automatically gets access too. They could then upload that data to their own
servers, competitors' servers, or who knows where else. This is even more
problematic when a library needs a _new_ permissions we didn't already have.

Similarly, a system is as secure as its weakest link but if you include
unreviewed, unknown code you have no idea how secure it really is. Your
well-designed secure coding practices could all be undone by one misbehaving
library. The same goes for any policies Apple and Google put in place like "you
are not allowed to fingerprint the user".

## Mitigating the risk

When evaluating a library for production usage, we ask a few questions to
understand the need for the library in the first place.

**Can we build this functionality in-house?**

In some cases we were able to simply copy/paste the parts of a library we really
needed. In more complex scenarios, where a library talked to a custom backend we
reverse-engineered that API and built a mini-SDK ourselves (again, only the
parts we needed). This is the preferred option 90% of the time, but isn't always
feasible when integrating with very specific vendors or requirements.

**How many customers benefit from this library?**

In one scenario, we were considering adding a very risky library (according to
the criteria below) intended for a tiny subset of users while still exposing all
of our users to the library. We ran the risk of something going wrong for all
our customers in all our markets for a small group of customers we thought would
benefit from it.

**What transitive dependencies does this library have?**

We'll want to evaluate the criteria below for all dependencies of the library as
well.

**What are the exit criteria?**

If integration is successful, is there a path to moving it in-house? If it isn't
successful, is there a path to removal?

## Evaluation criteria

If at this point the team still wants to integrate the library, we ask them to
“score” the library according to a standard set of criteria. The list below is
not comprehensive but should give a good indication of the things we look at.

### Blocking criteria

These criteria will prevent us from including the library altogether, either
technically or by company policy, and need to be resolved before we can move
forward:

- **Too high deployment target/target SDKs**. We support major OSes going back
  at least 4 years so third-party libraries have to support at least that many
  too.
- **Improper/missing LICENSE**. We bundle license files with the apps to make
  sure we can legally use the code and attribute it to the license holders.
- **No conflicting transitive dependencies**. A library can't have a transitive
  dependency we already include but at a different version.
- **Does not display its own UI**. We put great care in making our products look
  as uniform as possible, custom UIs are a detriment to that.
- **Does not use private APIs**. We are not willing to risk app rejection over
  the use of private APIs.

### Major concerns

- **Closed source**. Access to the source means we can pick and choose which
  parts of a library we want to include and how to bundle that source with the
  rest of the app. A closed source, binary distribution is much more difficult
  for us to integrate.
- **Builds with warnings**. We have "warnings as errors" enabled, and a library
  with build warnings is a decent indication of the overall quality of the
  library.
- **Poor documentation**. We look for high quality inline docstrings, external
  "how to use" documentation, and meaningful change logs.
- **Binary size impact**. How big is this library? Some libraries provide a lot
  of functionality of which we only need a fraction. Especially without source
  access it's often an all-or-nothing situation.
- **External network traffic**. A library that communicates with upstream
  servers/endpoints we have no control over could take the entire app down when
  the server is down, bad data is sent back, etc. This also has the same privacy
  implications I mentioned above.
- **Technical support**. When things don't work as they should we need to be
  able to report/escalate issues and get them fixed in a reasonable amount of
  time. Open source projects are often run by volunteers and usually can't
  commit to timelines, but at least we could make changes ourselves. This is
  impossible without source access.
- **Inability to disable**. While most libraries specifically require us to
  initialize it, some are more "proactive" in their instantiation and will
  perform work themselves without us ever calling into it. This means when the
  library causes issues we have no option to turn it off through feature flags
  or other mechanisms.

We assign point values to all these (and a few others) criteria and ask
engineers to tally those up for the library they want to include. While low
scores aren't hard-rejected by default, we often ask for more justification to
move forward.

## Final notes

While this process may seem very strict and the potential risk hypothetical in
many cases, we have actual, real examples of every scenario I described in this
blog post. Having the evaluations written down and publicly available also helps
in conveying relative risk to people unfamiliar with how mobile platforms works
and demonstrating we're not arbitrarily evaluating the risks.

Also, I don't want to claim every third-party library is inherently bad. We
actually use quite a few at Lyft: RxSwift and RxJava, Bugsnag's SDK, Google
Maps, Tensorflow, and a few smaller ones for very specific use cases. But all of
these are either well-vetted, or we've decided the risk is worth the benefit
while actually having a clear idea of what those risks and benefits really are.

Lastly, as a developer pro-tip: always create your own abstractions on top of
the library's APIs and never call their APIs directly. This makes it much easier
to swap (or remove) underlying libraries in the future, again mitigating some
risk associated with long-term development.

[1]: https://www.theverge.com/2020/5/7/21250689/facebook-sdk-bug-ios-app-crash-apple-spotify-venmo-tiktok-tinder
[2]: https://github.com/facebook/facebook-ios-sdk/issues/1427
