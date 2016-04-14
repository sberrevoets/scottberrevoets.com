Title: UIMenuController and the responder chain
Date: 2014-09-15
Description: Explaining unexpected behavior when using the responder chain and UIMenuController


The responder chain is a very important paradigm in the world of iOS development, and not terribly hard to understand. Dozens of articles have been written about it, and with some examples, the concept of finding a responder to a certain event by traversing a chain of potential responders is fairly straight-forward.

But today it completely threw me off. The goal was very simple and has been done many times before: showing a label whose text can be copied to the clipboard. Having never worked with `UIMenuController`, I fired up Google and of course found an excellent [NSHipster](http://nshipster.com/uimenucontroller/) article near the top.

I did as the article said. I created my `UILabel` subclass (only accepting `copy:` as an action it can perform), added my gesture recognizer, and configured and showed the `UIMenuController`. It worked, but instead of only showing the Copy menu item, it also showed the Select All item.

Well, that's weird. I implemented `canPerformAction:withSender:` like this:

```objective-c
- (BOOL)canPerformAction:(SEL)action withSender:(id)sender {
	return action == @selector(copy:);
}
```

I made sure that this method really only returned `YES` for the Copy item, proceeded to explicitly return `NO` for `selectAll:` and, when that failed as well, even changed the implementation of this method to just return `NO` for **any** item. But Select All doesn't take `NO` for an answer, and it stubbornly showed up anyway! I was baffled and could not get rid of this Select All item.

I did some research, and learned that `UIMenuController` uses the responder chain to figure out what items to show. Furthermore, the documentation for `canPerformAction:withSender:` read:

> This default implementation of this method returns YES if the responder class implements the requested action and calls the next responder if it does not.

That would explain the problem, if it weren't for the fact that Select All was the only other item that showed. Cut, Paste, Select, etc. did not. What was so special about Select All that no matter what I did, it always decided to make an unwanted appearance?

Finally I saw it. One of the last methods of the view controller that created this label had a method named, you guessed it, `selectAll:`. I didn't immediately connect the dots, but at least renaming that method to `selectAllContacts:` (which was a better name for that method anyway) got rid of Select All.

But how? I returned `NO` from my label's `canPerformAction:withSender:` for all actions except `copy:`. This means that for all other actions (see the informal `UIResponderStandardEditActions`), the next responder in the chain would be called. And (if necessary) the next, and the next.

At some point, my view controller, which participates in the responder chain, became the first responder and returned `YES` for the `selectAll:` action, simply because the method was implemented and part of `UIResponderStandardEditActions`.

So if implementing a method in that protocol is all that's needed to show the corresponding menu item, that would mean that implementing `canPerformAction:withSender:` in my `UILabel` subclass was unnecessary. I removed the method altogether and sure enough, the Copy menu item was still there. Problem solved.
