Title: How GitHub handles Git LFS
Date: 2026-07-01
Description: Notes from looking at Git LFS for snapshot test artifacts and learning how GitHub stores, bills, downloads, and removes LFS objects.

Snapshot tests have become an increasingly popular tool for mobile
teams to verify UI changes, but one question all teams run into is: where
do we store hundreds if not thousands of PNG files? Git Large File Storage
(LFS) is one of the more common ways to do this for various reasons[^1].

At Speak we recently went down this same path and in doing so learned a few
things about how Git LFS works and how GitHub handles it. Initially we just
learned the basic premise: instead of checking in a file, check in a small
human-readable pointer file that identifies the large file:

```
version https://git-lfs.github.com/spec/v1
oid sha256:907b5c652cce59e009e3c7fb2dc92d3bf598251315bed741aee037f2046bd32e
size 251222
```

The `oid` is an object ID for the file that's fetched from the configured LFS
server. Use `git lfs track ./Snapshots/*.png` to specify snapshots should be
stored in LFS and then commit `.gitattributes` to preserve that setting.

But soon we started getting warnings from GitHub that we were exceeding our
Git LFS budget. In investigating, we learned five more things that formed
our mental model around how to think about Git LFS when using GitHub:

1. **GitHub charges for [storage and bandwidth]**: similar to S3, both storage
   and bandwidth cost money. Our snapshots don't take up too much storage but CI
   clones the iOS and Android repos for every build, which is when all PNGs are
   downloaded, incurring bandwidth usage.
2. **You can skip downloading certain LFS objects to avoid bandwidth usage**: to
   avoid this, Git LFS offers a clone option to avoid downloading large files
   when they aren't needed through `git clone --config
   lfs.fetchexclude="./Snapshots/*.png"`. This saves bandwidth, clone time, and
   local storage. `git lfs pull --include="./Snapshots/*.png"` lets you
   redownload them.
3. **Removing a tracked file only removes it from git, not from storage**:
   removing the pointer files that get checked in and committing that change
   does nothing to the actual object in storage. Removing the file from git
   leaves a dangling object that still takes up storage space.
4. **Fully removing references requires [rewriting history]**: removing a
   file from git isn't sufficient because older commits may still refer to an
   LFS file and fail future clones. Fully purging it requires rewriting the git
   history using `git filter-repo`, which is obviously not ideal but arguably
   still better than irreversibly not being able to check out certain commits
   in the repo ever again.
5. **Rewriting history doesn't delete the file from storage**: even after all
   references to a file are deleted, the LFS object itself still needs to be
   deleted as well for storage to be freed up. The only way to do this other
   than to contact support, is to delete the repo (and all its associated data)
   and recreate it.

All of these details make it clear that Git LFS isn't a regular git repository
that handles large files better; there's a sophisticated cloud storage layer
behind it that needs the same considerations that more mainstream cloud storage
does. Git is the version control layer, but doesn't touch the raw objects
directly.

[^1]: Checking in large binary files that change regularly causes repo
      bloat, and cloud storage solutions like S3 or GCS make for a more
      complicated setup.

[storage and bandwidth]: https://docs.github.com/en/billing/concepts/product-billing/git-lfs#how-use-of-git-lfs-is-measured
[rewriting history]: https://docs.github.com/en/repositories/working-with-files/managing-large-files/removing-files-from-git-large-file-storage#removing-a-single-file
