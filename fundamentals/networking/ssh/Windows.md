# Use SSH on Windows like a pro

Using SSH and Git together on Windows is not straight forward. The following things are important to understand:

- Windows ships with it´s own version of [OpenSSH](https://docs.microsoft.com/de-de/windows-server/administration/openssh/openssh_install_firstuse)
- Git-Bash may include it´s own SSH executable
- depending on the local configuration any of the two SSH executables may be used
-  terminals instances do not attach to existing SSH agents

I always setup a Windows machine like this:

1. make sure that [OpenSSH](https://docs.microsoft.com/de-de/windows-server/administration/openssh/openssh_install_firstuse) is installed
2. enable & start the service on system startup:
	-  `Get-Service -Name ssh-agent | Set-Service -StartupType Automatic`
3. start the service: `Start-Service ssh-agent`
4. Edit the `C:\Users\username\.ssh` file and add the line `AddKeysToAgent yes` ([[fundamentals/protocols/network/ssh/Fundamentals#Keychain]]])
