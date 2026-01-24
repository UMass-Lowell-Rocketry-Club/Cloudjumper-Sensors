# Submodule Maintenance

This document is intended to be used by anyone who needs to maintain the **Cloudjumper-Sensors** submodule within the **Cloudjumper-Ground-Station** or **Cloudjumper-Payload** repositories. It contains all the necessary information about how the submodule is configured.

## About Submodules

A Git submodule is, by default, **a subdirectory synced to a specific commit from another repository**. The submodule will keep the same contents **even if its source repository has been changed**, since the submodule is synced to a specific commit, not necessarily the latest commit. The commit the submodule uses is decided by the main repository (ex. Cloudjumper-Ground-Station) and is treated like a tracked file. This means that if the submodule is updated to a more recent commit (`git submodule update`), the main repository treats this like a change which must be added and committed.

In this way, the main repository ensures that **its commits always use a consistent version of its submodules**. No matter what changes have been made to a submodule's source repository, **two people who check out a specific commit in the main repository will always see the same content in the submodules**.

## Submodule Creation

To add a submodule to a repository, you use the `git submodule add` command. In this case, the https address of the submodule's repository is used because this address is public. If the ssh address was used, users would have to authenticate to pull the submodule even if they cloned the main repository using its public https address.

```bash
git submodule add https://github.com/UMass-Lowell-Rocketry-Club/Cloudjumper-Sensors
```

Adding a submodule is considered a change to the main repository. Add this change and commit it to ensure everyone else using this repository has the submodule.

```bash
git add Cloudjumper-Sensors
git commit -m "added Cloudjumper-Sensors submodule"
git push
```

After cloning a repository with a submodule, you must run `git submodule init` to initialize the local configuration file and then `git submodule update` to fetch all the data from the submodule's repository and check out the appropriate commit. Alternatively, you can run add the `--recurse-submodules` flag to the `git clone` command to automatically run both the above commands.

```bash
# when someone else clones the main repository
git clone --recurse-submodules https://github.com/UMass-Lowell-Rocketry-Club/Cloudjumper-Ground-Station
```

## Updating Submodules

You can update all submodules using `git submodule update --remote`, which updates the submodule to the `HEAD` commit of its repository. **Note that this does not update the main repository—this is considered a change that must be committed like all other changes.**

You can set the submodule to track a specific branch with `git config -f .gitmodules submodule.[submodule name].branch [branch name]`. This just adds `branch = [branch name]` to the module in `.gitmodules`.

Now, when you're working on the Ground Station normally, you'll probably want to edit the sensor code and push your changes. Because a Git submodule is just a specific commit by default, you can't do this normally. To fix this, you must go into the submodule with `cd [submodule name]` and switch to a specific branch with `git switch [branch name]`. The submodule is now checking out a specific branch, and you can commit and push any changes you make.

Pulling changes to a submodule is a problem though, since by default this will reset the submodule to the HEAD commit of the branch it's tracking. Supplying the `--merge` or `--rebase` flag to the `git submodule update --remote` call will force incoming commits to be merged or rebased, keeping the submodule on the branch it's checking out. This can be automatically applied for every submodule update with `git config -f .gitmodules submodule.Cloudjumper-Sensors.branch main`.

Also, by default pushing changes to the main repository will **not** push changes to submodules. You can always push your changes directly from the submodule directories, but if you want this to happen automatically you can update the configuration with `git config -f .gitmodules push.recurseSubmodules on-demand`, which automatically pushes any changes from all submodules before pushing changes to the main repository.

Finally, you can run `git config -f .gitmodules submodule.recurse true` to make any commands that can recurse submodules do it automatically. This is most useful for `git pull`, which will now update all submodules automatically.

git config -f .gitmodules submodule.Cloudjumper-Sensors.pushurl git@github.com:UMass-Lowell-Rocketry-Club/Cloudjumper-Sensors


This is a test commit to edit an existing file