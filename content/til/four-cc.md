Title: Objective-C enums can be string-backed... sort of
Date: 2026-04-24

While looking at `AVAudioSessionErrorCode` in Xcode, I noticed something
interesting in its definition:

```objc
typedef CF_ENUM(AVAudioInteger, AVAudioSessionErrorCode) {
    AVAudioSessionErrorCodeNone = 0,
    AVAudioSessionErrorCodeMediaServicesFailed = 'msrv',   // 0x6D737276, 1836282486
    AVAudioSessionErrorCodeIsBusy = '!act',                // 0x21616374, 560030580
    AVAudioSessionErrorCodeIncompatibleCategory = '!cat',  // 0x21636174, 560161140
    AVAudioSessionErrorCodeCannotInterruptOthers = '!int', // 0x21696E74, 560557684
    AVAudioSessionErrorCodeMissingEntitlement = 'ent?',    // 0x656E743F, 1701737535
    AVAudioSessionErrorCodeSiriIsRecording = 'siri',       // 0x73697269, 1936290409
    AVAudioSessionErrorCodeCannotStartPlaying = '!pla',    // 0x21706C61, 561015905
    AVAudioSessionErrorCodeCannotStartRecording = '!rec',  // 0x21726563, 561145187
    AVAudioSessionErrorCodeBadParam = -50,
    AVAudioSessionErrorCodeInsufficientPriority = '!pri',  // 0x21707269, 561017449
    AVAudioSessionErrorCodeResourceNotAvailable = '!res',  // 0x21726573, 561145203
    AVAudioSessionErrorCodeUnspecified = 'what',           // 0x77686174, 2003329396
    AVAudioSessionErrorCodeExpiredSession = '!ses',        // 0x21736573, 561210739
    AVAudioSessionErrorCodeSessionNotActive = 'inac',      // 0x696e6163, 1768841571
};
```

The technique Apple used in defining the values of this enum is called [FourCC],
short for "four-character code". They are multi-character constants in C, but
they are not **strings**; they're **integers** created from the ASCII bytes of
each character. The comment after each value is the combined hex value of the
integer followed by that same value in base 10.

For `AVAudioSessionErrorCodeMediaServicesFailed`:
```
m = 0x6D
s = 0x73
r = 0x72
v = 0x76

0x6D737276 = 1836282486
```

The limitation is 4 ASCII characters, but with some creativity you can get
pretty far: `siri` is obvious, `msrv` is short for "media services", and `!rec`
means "not recording". I particularly like `what` for an unspecified error.

These strings are especially useful while printing/logging, since you can get
the four-character code printed using `printf("%.4s", (char*)&error);`. It's no
longer relevant to us in a Swift world where all of this is much easier, but
still a neat piece of history I learned more about.


[FourCC]: https://en.wikipedia.org/wiki/FourCC
