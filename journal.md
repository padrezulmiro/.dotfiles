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
