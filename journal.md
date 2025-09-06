# Dotfiles journal

## 30 Jan 25
Started to test the install script on a clean OS.

Note on pexpect's exit status:
> If you wish to get the exit status of the child you must call the close() method. The exit or signal status of the child will be stored in self.exitstatus or self.signalstatus. 
> If the child exited normally then exitstatus will store the exit return code and signalstatus will be None. If the child was terminated abnormally with a signal then signalstatus will store the signal value and exitstatus will be None
```python
child = pexpect.spawn('some_command')
child.close()
print(child.exitstatus, child.signalstatus)
```

## 6 Feb 25
I've been concerned over the last few days about packages that go through a separate configuration window. I've then learned that is probably related to an utility named `debconf`; and its behaviour might be configured using `DEBIAN_FRONTEND`.

## 17 Feb 25
I've decided to emulate a new installation of all the packages I'm looking for and keep detailed notes.
- zsh asks for a config when starting for the first time. It's kind of irrelevant since we're going to copy a .zshrc file from the repo
- oh-my-zsh not only needs a special command to install (as in, it doesn't use apt) but it might ask to change the default shell with `Do you want to change your default shell to zsh? [Y/n]`.
 
## 18 Feb 25
- I'm now going to try to install emacs from apt-get. It asked for a config via `debconf`. Using the `DEBIAN_FRONTEND` envvar didn't prevent the config window to show up, because apparently `sudo` doesn't usually preserve envvars by default. Setting the envvar directly in sudo fixed it!
- Installing fd-find and ripgrep with apt-get worked fine.

## 22 Feb 25
Spent last week trying to find out how to sync this code base with virtualbox so I don't need to constantly commit and pull the repo. I worked out I could use a shared folder between WSL and the VM via Windows. 
But to avoid IOing in Win through WSL (which is likely slow) I used `rsync`. Using `rsync -av --exclude='.git' --exclude='.gitignore' --exclude='.venv' SRC DEST` in WSL and `rsync -rv SRC DEST` in the VM did the trick; but I should probably look into setting up an auto sync mechanism.

## 14 Jul 25
Finally got back to tinker with a devenv installer. Learned about Ansible recently and it looked like it could fit my needs. It would replace my apt installing code. I'm now looking at how it'd work.

## 16 Jul 25
You can run `sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" -- unattended` to merely install oh-my-zsh without the installer doing anything else. I could run this in ansible.

## 17 Jul 25
Got to look into the copy script. Actually there's nothing to see, it's already implemented...
Added an ansible task to download the oh-my-zsh installer script, so I can run it in a separate task.

## 18 Jul 25
My ansible play can save the omz installer in path starting from the user's HOME dir.
`ansible-playbook -K <playbook-path>` to ask for BECOME (sudo) pwd.

## 21 Jul 25
Added plenty of more packages to the playbook so I'm getting to the point where I'm only missing the most difficult ones, `doom-emacs` and a neovim distro.
**Memo**: `starship` can be installed using a `-y` flag!

## 31 Jul 25
I'm testing a manual install of doom-emacs. It asked a y/n question to generate an env file.
The y/n prompt can be forced by running `doom install --force`

## 4 Aug 25
Not that happy that Ansible doesn't have a clean way to print a script's stdout in realtime as the script is running. `doom install` takes several minutes to run and I wanted a way for the user to know what's happening in the meantime.

A way to avoid this is to run the installer with `pexpect`.

## 25 Aug 25
Adding a point to the TODO checklist:
- [ ] Force an update to the cursor's color when SPC h t. If the theme is already "loaded" it doesn't update the cursor

## 26 Aug 25
Regarding the fact that Ansible doesn't [write](#4-Aug-25) to stdout whatever the underlying program outputs, I maybe have found a good enough solution: write everything to a log file which can be tailed - simple enough IG.

## 30 Aug 25 
#emacs-config
Just recalled again that I wanted to work on some functions that would allow to set up the window layout of workspaces. Something like, press `SPC TAB w` and then `j` for the setup I use more: 1 vertical big window on the left and two split up horizontal windows on the right.
