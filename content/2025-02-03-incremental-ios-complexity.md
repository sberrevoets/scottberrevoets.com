Title: Incremental complexity in iOS development
Date: 2025-02-03
Summary: A suggestion for redefining what it means to be a senior iOS developer

I wrote my first app, a map to navigate my college campus, in the winter of
2011, on iOS 4.x and with Xcode 4.x. There were 25 frameworks, iOS 7 hadn't been
invented yet, there was only 1 phone size, and we wrote apps with Objective-C.

But things have gotten much more complex over the years: within iOS you can
specialize in build engineering, architecture, performance & observability,
UIKit or SwiftUI, game development, security and privacy, Core Data or
SwiftData, iCloud, cross-platform apps with Catalyst, machine learning... The
list goes on and on, and that's on top of the already powerful frameworks from
the early days.

There are frameworks that enable entire categories of apps that weren't possible
in the early days, or if they were with much less OS integration than today.
HealthKit, WalletKit, StoreKit, RealityKit, ARKit all enable apps that were
pretty much unimaginable 15 years ago. And that's just iOS without even thinking
about watchOS, visionOS, or Apple's other platforms.

Swift went through a similar evolution. It started with a more functional
programming language compared to Objective-C, but quickly added new features:
protocol-oriented programming, property wrappers, function builders,
concurrency, macros, and a billion new keywords.

In my first few years, I was eager to learn everything there was to learn about
iOS. This was in the days when there was still an NDA anything related to iOS
APIs and the developer forums required a paid membership, so only anything
published by Apple was readily available. One of the first things I checked with
new platform versions was the API changes in UIKit and Foundation, and the iOS
and Xcode release notes were next. WWDC keynote days were overwhelming because a
year's worth of changes just shipped and I felt like I needed to learn all of it
in a few hours' time.

There are so many more sources to learn some part of the platform now that's
impossible to keep up with it all. You can easily be an iOS developer without
knowing 90% of its technologies. A "generalist" iOS developer will know many of
the UIKit/SwiftUI and Foundation APIs, as well as commonly used Swift features.
But if you're building an iOS app for an audio company that requires deep
knowledge of AVFoundation, you won't care or be able to keep up with
advancements in Core Location simply because they're irrelevant.

This feels like a pretty big difference from the first few years of the App
Store, when experienced developers went "broad" because "deep" didn't really
exist yet. There were no UI experts, iOS game developers, Swift enthusiasts, or
multiplatform lobbyists, so it was fun to learn more about all the frameworks
even if you weren't going to use them.

For beginning developers that increase in complexity isn't super obvious, as
everyone is "expected" to know basic UI and Swift knowledge and it takes some
time to learn that. But more senior developers looking for a new job where
experience with specific frameworks (sometimes not even Apple's own, like React
Native, RxSwift, or The Composable Architecture) is desired may feel like they
are not experienced enough. In reality they have plenty of great experience,
just in other parts of iOS.

Most companies that hire for a niche iOS specialty realize this and are
generally OK with someone who's willing to learn the technologies that specific
job requires. But how do those companies interview for that? For hands-on coding
exercises, there are a few options:

* **Ask more basic questions** that all people should know at least to some
  extent. This works OK but doesn't really distinguish senior from junior
  engineers.
* **Ask deeper questions** but run the risk the candidate happens to not have
  deep knowledge on the topic they're being asked about.
* **Let candidates choose the topic** they have deep knowledge of and talk about
  that, but run the risk of the interviewer knowing nothing about topic.

Having been deeply involved in designing an interview process, I'm growing more
convinced that evaluating candidates based on 60 minutes of hands-on coding
isn't going to get you the best developers and will primarily weed out the below
average ones. What I find more interesting for these positions is if candidates
have enough transferable knowledge in one framework to quickly ramp up with
another. You can learn a ton about someone's experience through questions like:

* How does Apple approach privacy and how is that reflected in its APIs? What is
  generally involved in requiring user permission to use sensitive user data and
  what is the best way to handle that data?
* What hardware and environmental constraints do iPhones have? How does the
  system deal with those limitations and in what ways are developers affected by
  that? What precautions can you take and how can you know if your app performs
  well?
* How would you do the research for a lightning talk about an iOS technology you
  currently know nothing about (e.g. data persistence)? What sources of
  information are there, how reliable are they, and which do you prefer?
* Think of an API, language feature, or pattern you've used recently that can be
  improved. What did you not like about it, how would you improve it, and why do
  you think Apple might have designed it this way?
* Apple introduces a new technology at WWDC and your boss hears about it and
  wants you to implement it in the company's app. What problems do you foresee?
* What App Store Review guideline would you get rid of and why? Which one would
  you introduce?

These questions feel decidedly more involved than typical questions like "how
does memory management work" and "what's the difference between a class and a
struct", and they give a lot more insight into someone's (lack of) experience
with the platform.

Being a senior iOS developer went from breadth of knowledge to depth of
knowledge, and I expect more defined specialties, perhaps iOS Security Engineer
or iOS Camera Engineer, to crystallize in the future. It's no longer about
watching every WWDC video and learning the latest UIKit tricks, knowing exactly
what APIs became available in what iOS version, and finding ways to use the
latest Swift features in your own code.

Instead, more experienced developers understand how Apple designs their
platforms and technologies, have surface-level knowledge of what is available to
them, and are able to take their existing knowledge and apply it to something
new to ramp up quickly and effectively. The rest they know they can learn on the
fly. Hopefully companies realize this too in their interviewing and onboarding
processes, because you might be onboarding an iOS developer who doesn't know a
single thing about the tech stack your app is running on.

!!! update "Update (February 2026)"

    This post is only a year old but many shifts have already happened. AI
    impacts the profession in a profound way and I no longer think more
    specialized jobs will exist. Instead, companies will have their engineers
    leverage AI to ramp up on new technologies quickly instead of trying to find
    their unicorn engineer that happens to be an expert on Bluetooth audio.

    Senior engineers with a baseline knowledge will need to upskill to learn how
    to use AI tools but will be fine in the end. Junior engineers will have a
    harder time as companies seem to be unwilling to train them, a bad trend in
    my opinion because the junior engineers are the senior engineers of the
    future.
