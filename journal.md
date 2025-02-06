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
