Title: Why big companies are bad platform citizens
Date: 2026-10-05
Description: Why large companies are slow or refusing to adopt platform features

In the fall, when Apple releases new iPhones and major iOS versions, small/indie
developers take a lot of pride in being ready for this new tech on day 1. They
spend all summer learning new APIs and development tools, and integrate them in
their apps so their users can enjoy them as soon as the platforms they run on
become available.

This excitement about building for updated platforms couldn't be more different
at big tech companies: LinkedIn got dark mode support two years after Apple
introduced it, YouTube required a premium subscription for PiP (an OS level
feature), and many apps are still due for a Liquid Glass update. It seems
counterintuitive: the engineering teams behind these apps are very skilled,
large, and have demonstrated they can ship fast. So why are they so slow with
these platform-level features and integrations?

It's a fundamental difference in priorities: small app developers care about
their craft and are proud of the work they're doing. They enjoy using the latest
OS features, integrations, and technologies and making them (more) available to
their users, even if the road to get there is rocky. They hope to get featured,
get special recognition from Apple, and be part of keynotes or other marketing
materials. The blogs, pundits, and tech influencers will highlight their work
regularly enabling another good marketing opportunity.

But they're usually also the first to admit those moments don't tend to lead to
big spikes in downloads or sales. Even if there is a big spike, interest tends
to wane and after the news cycle for the new tech ends, so does the increased
interest in the indie apps.

### Excitement wanes fast

In some cases big app companies immediately jump on this new tech as well,
especially if they can be a launch partner on new tech that Apple or Google
market heavily. We saw this at Lyft too: when Apple first introduced 3rd party
Siri integrations and a more capable watchOS SDK we spent a good amount of time
in the lead up to WWDC partnering with them. They highlighted that work during
the keynote and we felt great about being good iOS citizens. We then spent a
good amount of the summer improving the experiences, polishing the UI, and
ensuring it was bug-free, so that we could launch all this on day 1.

But months later, usage was more or less 0 for both the Siri integration and
Apple Watch app. During a hackathon we also developed an Amazon Alexa app that
basically no one except for a few very excited Alexa users ever touched. These
integrations are fun to build, but don't tend to do much for user acquisition or
engagement. Rarely do these platform-level integrations make the experience of
an app _so_ much better that users choose you over a competitor. If they can't
tell Siri or Alexa to get you a ride, they'll just open the app instead.

Eventually, we dropped the Apple Watch App, Siri and Apple Maps integration, and
the Alexa app became unmaintained. Siri Shortcuts and app clips were not likely
to drive many users so were never implemented. Widgets were built in a hackathon
and were simple enough to support but also didn't see a ton of usage.

This is true for most companies whose app connects to their larger service:
banks, airlines, ride-sharing, social media, etc. Users are there to get
something done using that particular service and if Apple Pay isn't available or
they can't quick-launch the app through a Live Activity or a widget, they'll
find another way.

### There's always a cost

Meanwhile the cost of building platform integrations is easy to underestimate.
Codebases tend to run into multiple millions of lines of code with highly
complex architectures, many layers of tech debt, and a varying amount of red
tape to promote accountability and good use of engineering resources. Teams have
seen attrition, understaffing, and reorgs which all hurt the understandability
of the codebase and developer productivity. Early adopters also deal with all
the bugs, so being first means working through those pains as well.

Large companies also tend to go through quarterly or bi-annual planning cycles,
so what they work on is defined well before the platform vendor rolls out its
updates. Before deciding to prioritize a new platform integration, teams will
want to measure how that project contributes to company goals and make sure it's
not hurting any of the business metrics it cares about.

### Being a good citizen can be bad for business

That's assuming the metrics will improve (or at least stay neutral) by being a
good platform citizen, but in some cases user engagement, ad impressions, or
in-app upsells are actually expected to be negatively impacted:

* Letting users take action in your app/service without having to open it (e.g.
  through Siri, Shortcuts, or other system integrations) often means you lose
  the opportunity to upsell or show ads. We didn't love how Apple Maps showed
  the price of Uber and Lyft rides side by side without us even knowing how we
  compared on that specific ride. We wanted users to open the app so we could
  win them over if needed.
* Marketing push notifications are despised by people in tech (me included!),
  but the reality is they work _really_ well as an engagement or reactivation
  method for most people. Personally I revoke push notification permission if
  apps do this, but that's simply not true for the majority of people that use
  these services.
* Adtech is a multi-billion dollar industry, so despite App Tracking
  Transparency and Apple's efforts to not let app developers spy on their users,
  companies try to use any workaround they can think of to improve their
  attribution, conversion, and ad relevancy. "Do as much on device as possible
  and request as little user data as possible" is just not something companies
  are interested in: they _want_ the data. WhatsApp could easily work without
  access to your contacts, yet to start a new chat it requires that access
  anyway.

In some cases, the company's incentives align with the platform, which is a win
for everybody but generally still a decision driven by the company's own goals.
The recent wave of companies choosing native over React Native is for
engineering reasons; the fact that those apps will now offer a native user
experience is just a nice side benefit.

All of this is in stark contrast to the smaller developers that first and
foremost care about the craft and user experience. The quality and "at home"
feeling of their app matters more as they often rely on the platform's biggest
enthusiasts to use and review their apps. At larger organizations, this type of
craft is often driven by individual engineers as passion projects and is usually
secondary to business value.
