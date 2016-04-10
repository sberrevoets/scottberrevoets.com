Title: @objc creates a wrong class name in Objective-C
Date: 2014-12-15
Description: There are some unexpected compiler issues when using @objc to rename a class in Xcode 6.1


A few months ago, I decided I'd get started porting [SDCAlertView](http://github.com/sberrevoets/SDCAlertView) to Swift, but I was only a few minutes in until I ran into a problem I had no idea how to solve: I couldn't get my class names right in both Swift and Objective-C. Even though there are copious amounts of documentation covering the interoperability of Swift and Objective-C, somehow I couldn't get it to work and I brushed it off as me being stupid.

Tonight I tried again, and after some more research it turned out that the behavior I saw was actually a bug in the compiler! I'm surprised that the latest Xcode version is 6.1.1 and that apparently not enough people have run into this problem for Apple to make it a priority.

The bug can easily be reproduced by creating an Objective-C project in Xcode, and then adding the following Swift class:

```swift
import UIKit

@objc(SDCMyLabel)
class MyLabel: UILabel {
}
```

You would expect that, once you import `MyProject-Swift.h` in your Objective-C class, you could instantiate a class named `SDCMyLabel`. However, instead, you can only instantiate a class named `MyLabel`.

I found this very recent [Stack Overflow](http://stackoverflow.com/questions/26132823/name-of-swift-class-when-exposed-to-objective-c-code-does-not-respect-the-objc) question which pretty much asks the same thing. "milos" gives a great answer by explaining the observed behavior in Xcode 6.0.1, and the expected behavior according to the WWDC session [video](https://developer.apple.com/videos/wwdc/2014/).

After reading the answer and watching the relevant parts of the vide, I slightly changed my previously-drawn conclusion from "I'm stupid" to "Xcode's stupid" and filed [rdar://19261044](rdar://19261044). If you're running into the same problem, please duplicate and cross your fingers the engineers at the fruit company will fix it soon.
