Title: Xcode & Objective-C Oddities
Date: 2014-08-10
Description: Some fun things about working with Xcode and Objective-C


Any developer that has worked with Xcode to write a little more than just "Hello, World" knows that Xcode and Objective-C have their quirks. Chances are you have heard of [@TextFromXcode](http://twitter.com/TextFromXcode), the Twitter handle that portrays Xcode as a high school bully in fake text conversations like this:

![Xcode Bully](http://cl.ly/image/0I2P191S0Q2k/20140227.PNG)

But it's not always Xcode that makes Apple platform developers sometimes frown and sigh. Sometimes it's the developers themselves, sometimes it's the documentation, and sometimes a hidden gem from within Apple frameworks makes an appearance. I've compiled a short list of things I've encountered. Because it's Sunday and I didn't have anything better to do.

## `UIGobblerGestureRecognizer`
Say what? A "[`gobbler`](https://github.com/nst/iOS-Runtime-Headers/blob/master/Frameworks/UIKit.framework/UIGobblerGestureRecognizer.h)" recognizer? Does it recognize when the user imitates a turkey? Well, maybe, but according to [BJ Homer](http://twitter.com/ortwingentz/status/225508227234791424), it is used to avoid recognition of a gesture while animations are in progress. Ah of course! Now the name "gobbler" makes perfect sense! 😶

## `UITapAndAHalfRecognizer`
Speaking of gesture recognizers, there's another remarkable one that lives in the private section of UIKit: `UITapAndAHalfRecognizer`. This is a private subclass of `UIGestureRecognizer` that records "a tap and a half".

So what does that mean? Does it detect whether the user goes in for a second tap, but never actually touches the screen? Or does the user touch the screen ever so slightly that the second tap can hardly be considered a complete tap? Nope! This recognizer fires when a second tap stays on the screen. Not sure for what functionality Apple needs this, but it's been around since at least iOS 4, so it probably has a purpose.

## Naming is hard
> There are only two hard things in Computer Science: cache invalidation and naming things.  
- Phil Karlton

Naming **is** hard, but Objective-C developers always say that verbosity is one of Objective-C's strengths because its naming conventions are self-documenting. Normally I'd agree, but in this case, I think Apple may want to consider a different name.

[`HMCharacteristicValueLockMechanismLastKnownActionUnsecuredUsingPhysicalMovementExterior`](https://developer.apple.com/library/prerelease/ios/releasenotes/General/iOS80APIDiffs/frameworks/HomeKit.html) is a brand new constant in iOS 8 and has got to be one of the longest constants that's available in iOS. Try saying it without taking a breath in the middle. 

I found it in the iOS 8 API diffs, but it did make me wonder. What is the longest Objective-C method available in Cocoa Touch? Well, a quick Google search led to a blog post by [Stuart Sharpe](http://initwithstyle.net/2013/10/in-search-of-the-longest-method), who used the Objective-C runtime to generate a list of methods in the iOS 7 SDK.

Turns out, the longest method in the iOS 7 SDK is

``` objective-c
+[CUIShapeEffectStack shapeEffectSingleBlurFrom:
                               withInteriorFill:
                                         offset:
                                       blurSize:
                                   innerGlowRed:
                                 innerGlowGreen:
                                  innerGlowBlue:
                               innerGlowOpacity:
                                 innerShadowRed:
                               innerShadowGreen:
                                innerShadowBlue:
                             innerShadowOpacity:
                                   outerGlowRed:
                                 outerGlowGreen:
                                  outerGlowBlue:
                               outerGlowOpacity:
                                 outerShadowRed:
                               outerShadowGreen:
                                outerShadowBlue:
                             outerShadowOpacity:
                            hasInsideShadowBlur:
                           hasOutsideShadowBlur:]
```

Unless iOS 8 introduces a longer method name, this one takes the cake with 22 arguments and 352 characters. If you have Xcode configured to line-break at 80 characters (yes, some people still do that), this method signature alone, without any arguments, takes up 5 lines.

Another beauty of a method lives in Core Animation and its method signature is 

``` objective-c
- [CAMediaTimingFunction functionWithControlPoints::::]
```

`::::`? Is that even valid syntax? Yes, and you call the method like this:

``` objective-c
[CAMediaTimingFunction functionWithControlPoints:0.25 :.50 :0 :1.0];
```

Was an array really too much to ask...?

## `[NSDate nilDate]`
This one has made the rounds throughout the developer community before, but I'm adding it here in case you haven't seen it yet. Try running the following code:

``` objective-c
NSCalendar *calendar = [NSCalendar currentCalendar];
[calendar components:NSCalendarUnitYear fromDate:nil toDate:[NSDate date] options:0];
```

In the console log, you'll find the following output:

> *** -[__NSCFCalendar components:fromDate:toDate:options:]: fromDate cannot be nil  
I mean really, what do you think that operation is supposed to mean with a nil fromDate?  
An exception has been avoided for now.  
A few of these errors are going to be reported with this complaint, then further violations will simply silently do whatever random thing results from the nil.

Either a grumpy Apple developer woke up at the wrong side of the bed or has a great sense of humor. In any case, I wouldn't mind if more sarcastic warnings started popping up in Xcode's console.

## Defying the Uncertainty Principle in iOS
> [I]n 1927, Werner Heisenberg stated that the more precisely the position of some particle is determined, the less precisely its momentum can be known, and vice versa.  
> [Wikipedia](http://en.wikipedia.org/wiki/Uncertainty_principle)

If that's true, and it's fairly safe to assume that it is, I'd avoid using `-[CLLocation speed]` for apps like radar detectors. I wonder if we're ever going to get a `-[CLSpeed location]` method, which has a more accurate speed and a less accurate location.

## Xcode at it again
Lastly, the following is a screenshot I personally took at work that completely baffled me.

{% img center /images/XcodeScreenshot.png 700 %}

This would not go away, even after cleaning the build folder and rebuilding. In the end I resolved the problem by running

``` bash
$ git stash
$ git reset --hard HEAD
```

Then, after a clean build and `git stash pop` the errors finally went away...

That's just a few things I've found while working with Xcode and Objective-C over the years. If you have more, please share!
