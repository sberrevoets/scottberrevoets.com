Title: macOS can remember SSH passphrases
Date: 2026-03-02

Having to type out my password every time in SSH into a machine got a little
tedious for me. Turns out macOS can save these passphrases to the Keychain to
save some typing each time you try to connect to a host over SSH.

To enable this, make sure you're **using the macOS-native** `ssh` version. I had
a homebrew version installed, which doesn't support this. Verify with `which
ssh`, which should output `/usr/bin/ssh`.

Then run the following:

```bash
# Add private key to Keychain
ssh-add --apple-use-keychain ~/.ssh/id_ed25519

# SSH config to read from Keychain
echo "Host *
    UseKeychain yes
    AddKeysToAgent yes
    IdentityFile ~/.ssh/id_ed25519" >> ~/.ssh/config
```

This is enough to make it work one-time, but to preserve this option across
reboots add the following line to your `~/.zshrc`:

```
ssh-add --apple-load-keychain -q
```

Now SSH works without having to enter a passphrase or password again. In theory
this also works with RSA keys, but not all modern servers support that for
security purposes. Try an `ed25519` key instead if the steps above don't work
with an RSA key pair.
