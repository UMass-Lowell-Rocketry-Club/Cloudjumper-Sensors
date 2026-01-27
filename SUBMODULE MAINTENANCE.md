# Submodule Maintenance

This document is intended to be used by anyone who needs to maintain the **Cloudjumper-Sensors** submodule within the **Cloudjumper-Ground-Station** or **Cloudjumper-Payload** repositories. It contains all the necessary information about how the submodule is configured.

## About Submodules

A Git submodule is, by default, **a repository in a subdirectory synced to a specific commit from another repository**. The submodule will keep the same contents **even if its source repository has been changed**, since the submodule is synced to a specific commit, not necessarily the latest commit. The commit the submodule uses is decided by the main repository (ex. Cloudjumper-Ground-Station) and is treated like a tracked file. This means that if the submodule is updated to a more recent commit (`git submodule update`), the main repository treats this like a change which must be added and committed.

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

The submodule should also be set to explicitly track the `main` branch. This configuration goes in the `.gitmodules` file, meaning it must also be added and committed.

```bash
git config -f .gitmodules submodule.Cloudjumper-Sensors.branch main
git add .gitmodules
git commit -m "set Cloudjumper-Sensors to use main branch"
git push
```

After cloning a repository with a submodule, you must run `git submodule init` to initialize the local configuration file and then `git submodule update` to fetch all the data from the submodule's repository and check out the appropriate commit. Alternatively, you can run add the `--recurse-submodules` flag to the `git clone` command to automatically run both the above commands.

```bash
# when someone else clones the main repository
git clone --recurse-submodules https://github.com/UMass-Lowell-Rocketry-Club/Cloudjumper-Ground-Station
```

## Updating Submodules

*Note: See [Editing Submodules](#editing-submodules) for information about updating submodules if you mean to commit changes to a submodule.*

If you're not contributing to a submodule's code and are just pulling changes to the repository as a whole then updating a submodule is easy because **you don't have to touch it**. When you run `git pull` to pull remote changes just add the `--recurse-submodules` flag to automatically **fetch** and **merge** changes to submodules. Note that this updates submodules to whichever commit they're on in the main repository. This is not necessarily the most recent commit in the submodule's source repository, but is the version of the submodule everyone else is using.

```bash
# from the main repository, not the submodule
git pull --recurse-submodules
```

To make this process more convenient, you can configure `git pull` to always recurse submodules so you don't need the `--recurse-submodules` flag. This change applies only to your local copy of the repository.

*Note: Due to issues with merging changes in submodules, this option should **not** be set if you mean to commit changes to a submodule.*

```bash
git config submodule.recurse true
```

If you need to update a submodule to its source repository's most recent commit, you can do this with `git submodule update --remote`. This changes the submodule to use the HEAD commit in the submodule's source repository. Like creating a submodule, **this is considered a change which must be added and committed like any other change**.

```bash
git submodule update --remote  # --remote is required to pull changes
git add Cloudjumper-Sensors
git commit -m "updated Cloudjumper-Sensors submodule"
```

## Editing Submodules

It can be very convenient to work on submodule code at the same time as main repository code. Git allows you to do this, but it requires some additional configuration first. You can go to the [Editing Submodules Setup Script](#editing-submodules-setup-script) section for a quick guide on how to get set up. For more details you can read though the [Setup for Editing Submodules](#setup-for-editing-submodules) section. **After getting set up you must read the [How to Edit Submodules](#how-to-edit-submodules) section**.

### Setup for Editing Submodules

*This section explains the steps for setting up your environment to edit submodules. All the code explained here is run automatically by the script detailed in [Editing Submodules Setup Script](#editing-submodules-setup-script).*

First, you must ensure you have the correct push URLs configured for the main repository and the submodule. In order to commit changes, GitHub requires that you use an SSH URL, which begins with `git@github.com`. You can check this with `git remote -v`, which shows the **fetch** and **push** URLs the repository or submodule uses. You can set this with `git remote`. Note that you will need an [SSH key in your GitHub account](https://docs.github.com/en/authentication/connecting-to-github-with-ssh) for this to work.

```bash
# from the submodule
git remote set-url --push origin git@github.com:UMass-Lowell-Rocketry-Club/Cloudjumper-Sensors.git
```

Next, you need to switch the submodule to the `main` branch. Currently the submodule's local repository is in a **Detached Head** state, pointing at a specific commit rather than a branch.

```bash
# from the submodule
git switch main
```

You can now make changes in your submodule, commit them, and push them from the submodule without issue. Just remember that **every commit in a submodule is a change in the main repository which must be added and committed**. However, pulling changes to a submodule presents an issue. You can, of course, run `git pull` from within a submodule just fine, although you need to remember to commit this change to the submodule from the main repository (`git add Cloudjumper-Sensors` and `git commit -m "pulled changes in Cloudjumper-Sensors"`). The real problem occurs when pulling changes to the main repository.

While in the main repository you may run `git pull --recurse-submodules` to update the main repo and any submodules with any changes from other people. This, unfortunately, resets updated submodules to a detached head state. If this happens you can still go into the submodule and switch to the branch it was on previously, your work will still be there, but now the submodule isn't updated.

A better way of doing this is to first run `git pull` without the `--recurse-submodules` flag. This **fetches** (downloads) changes to submodules but doesn't actually change your local submodules yet. To do this you can run `git submodule update --merge`, which updates all submodules with a merge commit. Crucially, **this keeps submodules attached to their branches**.

```bash
# from the main repository
git pull
git submodule update --merge
```

You can leave out the `--merge` flag if you set it as the default with `git config submodule.Cloudjumper-Sensors.update merge`. You can also combine the two above commands into one using a **Git Alias**. You can change the alias name to whatever you want.

```bash
git config submodule.Cloudjumper-Sensors.update merge
# you can change "spull" to whatever you want. use with "git spull"
git config alias.spull '!git pull && git submodule update --merge'
```

Now there's just one last thing to configure. When you run `git push` from the main repository normally it will only push changes to the main repository, not from any of the submodules. In fact, it might fail if there are un-pushed changes in any submodules. You can fix this by adding the `--recurse-submodules=on-demand` flag, which first pushes any changes to submodules and then pushes changes to the main repository.

```bash
# from the main repository
git push --recurse-submodules=on-demand
```

You can make this the default behavior for `git push` with a Git configuration option.

```bash
git config push.recurseSubmodules on-demand
```

### Editing Submodules Setup Script

The script `submodule-editing-bootstrap.sh` will automatically set up your environment to edit the submodule correctly according to the [Editing Submodules](#editing-submodules) section. To run it, **you must be in a Unix-Like** environment. Linux and macOS are both Unix-Like environments so you don't need to change anything. If you're on Windows you will need to [install WSL](https://learn.microsoft.com/en-us/windows/wsl/install), which is a subsystem that allows you to run Linux from a terminal in your normal Windows installation.

```bash
# from the submodule
./submodule-editing-bootstrap.sh
```

### How to Edit Submodules

*If you haven't already set up your environment to edit submodules, do so before reading this section.*

When editing a submodule, always keep in mind that **the submodule is a separate repository. Changes to files in the submodule must be added and committed in the submodule**.

While in a submodule you can edit, add, and commit files just like you would a normal repository. You can even pull and push changes, just like normal. **Letting the main repository know about changes is where things get a little complex**.

The main repository keeps track of which commit each submodule is using, which makes sure everyone using the repository has the same version of each submodule. To that end, **every commit in a submodule is considered a change to the main repository**. Thus, **whenever you make a commit in a submodule you must add and commit it in the main repository as well**.

```bash
# from the main repository
git add Cloudjumper-Sensors
git commit -m "edited Cloudjumper-Sensors submodule"
git push
```

Also, when pulling changes from the main repository you should use the `git spull` or whatever alias you set during setup instead of the normal `git pull`. This alias makes sure submodules are updated correctly.
