Title: Objective-C prefixes: a thing of the past?
Date: 2014-07-25
Description: Some insights about whether Objective-C prefixes are still necessary


This past week, there was, again, a lot to do about Objective-C and prefixing. To most iOS developers, the story sounds familiar: one camp is strongly in favor, another camps is strongly against, and a third camp couldn't really care less.

Unless I'm unaware of any other platforms where the discussion was also a hot topic, this time I was at least a little responsible for instigating a debate that will never see a clear winner, with the following tweet:

<blockquote class="twitter-tweet" lang="en" align="center"><p><a href="https://twitter.com/bobmccune">@bobmccune</a> <a href="https://twitter.com/invalidname">@invalidname</a> Also no option to enter class prefix anymore, even for Objective-C projects</p>&mdash; Scott Berrevoets (@ScottBerrevoets) <a href="https://twitter.com/ScottBerrevoets/statuses/492012762940588033">July 23, 2014</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>


Let's first clear up that Swift doesn't **need** to have class prefixes, because it has built-in support for namespacing through modules. From what I read, earlier Xcode 6/Swift betas did not have module support, but at least we know it's coming before 1.0 hits.

However, this doesn't solve any of the problems Objective-C has, and so it was surprising to see this field was removed when creating a new Objective-C project. You can still set this prefix per project **after** you create it, but since most Xcode templates create source files for you, those files will be created without a prefix.

I noticed the lack of this option, as well as the lack of a file template for Objective-C categories, back in beta 2 and immediately filed two bugs. The missing file template is as of this writing still open, but the class prefix got closed a few days later. Normally, radars aren't known for their wealth of information related to the issue the radar was filed for, but Apple Engineering made an exception this time.

> After much deliberation, engineering has removed this feature.

> This was removed intentionally. We are no longer encouraging the use of prefixes for app code, and for frameworks, you can create a prefix in the Project Inspector after creating the project.

Okay, so no more prefixes for app code. Didn't see that coming. Does Apple now encourage developers to start making extensive use of frameworks?

> No. If you want to use a prefix, you can set one in the project inspector. Especially for frameworks, this is easy since the template creates no source files that should be prefixed. If you really want to prefix the classes in your main app binary, you might need to rename the few that are created initially, but the recommendation is generally that frameworks should use prefixes (in Obj-C, not in Swift) to avoid namespace issues, and apps generally don't need to.

The key part here is in the last few words: "don't need to".

Third-party libraries, especially frameworks that don't ship with the source code, need a prefix, because the chances of naming collisions with other code or, even worse, other libraries is significant. Users of the libraries can't (and even if they can, are likely not willing to) change the name of your classes because they collide with some other library's code.

"App code" on the other hand, is very unique to one particular app. It contains the UI and some of the business logic that puts your app together. Most view controllers, for example, are app code. App code is not likely to be reused, because it's very specific in what it does and is therefore unlikely to collide with other classes (assuming you name your classes well). If you think "well, this functionality may be reused in some other project", it's a great candidate for a framework!

I was always a big fan of the class prefixes, and while it was sometimes hard to come up with what prefix to use, I've come to actually **like** how they look, too. Classes that don't have a prefix feel like they're missing something. However, the guideline of "prefix frameworks, not app code" does make sense, so I will start using that from now on as well.
