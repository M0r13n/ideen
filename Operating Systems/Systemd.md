- the dominant init system for Linux distributions
- resources are managed using **units**
	- any resource that the systems operates/manages
	- systemd manages these through **unit files**
	- units abstract services, resources, devices, mounts and resource pools

## Unit Files
- `man systemd.unit` is your friend
- `/usr/lib/systemd/system` holds systemd unit files put there by package managers (e.g. apt)
- `/usr/lib/systemd/system` holds manually placed unit files
- there are different **types of resources**:
	- **.service**: service units describe how to manage a service or application on a machine
	- **.socket**: used for socket based activation of associated `.service` units
	- **.device**: device unit
	- **.mount**: mounts managed by systemd. automatically created by `etc/fstab`
	- ...
- made up of sections and directives
	- sections are wrapped in brackets `[section 1]`
	- directives `Directive=value`
	- sections extend until the next section or the end of the file
- `[Unit]` section
	- defines metadata and relations to other units
	-   **`Description=`**: describes the name and basic functionality of the unit
	-   **`Documentation=`**: provides a location for a list of URIs for documentation
	-   **`Requires=`**: lists any units upon which this unit essentially depends
	-   **`Wants=`**: similar to `Requires=`, but less strict. If these units are not found or fail to start, the current unit will continue to function
	-   **`Before=`**: units listed in this directive will not be started until the current unit is marked as started if they are activated at the same time. 
	-   **`After=`**: units listed in this directive will be started before starting the current unit.
	-   **`Conflicts=`**: list units that cannot be run at the same time as the current unit. 
	-   **`Condition...=`**:  test certain conditions prior to starting the unit. This can be used to provide a generic unit file that will only be run when on appropriate systems. If the condition is not met, the unit is gracefully skipped.
	-   **`Assert...=`**: similar to the directives that start with `Condition`. However, unlike the `Condition` directives, a negative result causes a failure with this directive`**
- `[Install] ` section
	- defines at which moment during boot process the service should be started
	- obligatory if the service is managed by `systemctl enable`
	-   **`WantedBy=`**: a list of units that weakly depend on the unit. When this unit is enabled, the units listed in `WantedBy` gain a `Want` dependency on the unit. `WantedBy=multi-user.target` will inject the service as a dependency for `multi-user.target`. it will start whenever `multi-user` target is started.
	-   **`RequiredBy=`**: a list of units that depend on the unit. When this unit is enabled, the units listed in `RequiredBy` gain a `Require` dependency on the unit.
	-   **`Alias=`**: space-separated list of additional names for the unit
	-   **`Also=`**: specifies a list of units to be installed or uninstalled along with the unit.
- `[Service]` section
	- only applicable for services (well, obviously.. )
		- `Type=`categorizes services by their process and daemonizing behavior
			-   **simple**: default. correct choice for services that run continuously without forking
			-   **forking**: the service forks child processes (e.g. webservers)
			-   **oneshot**: short-lived on-off tasks (e.g. cleanup script). `systemd` should wait for the process to exit before continuing on with other units
			-   [many more](https://www.freedesktop.org/software/systemd/man/systemd.service.html#Options)
	- `ExecStart`: the path and arguments of the command to be executed
	- `ExecStartPre`: additional commands that should be executed before the main process is started (can be used multiple times)
	- `ExecReload=` indicates the command necessary to reload the configuration of the service if available.
	- `ExecStop=` indicates the command needed to stop the service. If this is not given, the process will be killed immediately when the service is stopped.
	- `ExecStartPost`: same exact qualities as `ExecStartPre=` except that it specifies commands that will be run _after_ the main process is started.
	- `WorkingDirectory`: defines the working directory of the process(es). Should be an absolute path
	- `User` defines the user which will run the process (defaults to root)
	- `Group` defines the group as which the process will run
- `[Socket]` enables socket-based activation of units. Each socket unit must have a matching service unit that will be activated when the socket receives activity.
- `[Path]` monitors paths on the filesystem for changes. Another unit must exist that will be be activated when certain activity is detected at the path location.
- `[Timer]` schedule tasks to operate at a specific time or after a certain delay

## Security

- **ProtectHome** which restricts access to /home, /root, and /run/user directories
- **NoNewPrivileges**, which ensures that processes cannot gain new privileges
- **PrivateTmp**: Isolates temporary files of a service.
- **ProtectSystem**: Makes system directories read-only or inaccessible.
- **ProtectKernelTunables**: Prevents alteration of kernel parameters.
- **ProtectControlGroups**: Restricts control group modifications.
- **RestrictAddressFamilies**: Limits socket address families used.
- **CapabilityBoundingSet**: Controls the capabilities granted to the service.
- **MemoryDenyWriteExecute**: Prevents writing and executing memory.
- **RestrictRealtime**: Prevents real-time scheduling.

## Timers as Cronjobs

systemd timers can be used to perform the same kinds of tasks as the cron tool but offer more flexibility in terms of the calendar and monotonic time specifications for triggering events.

**/etc/systemd/system/myMonitor.service**
```txt
# This service unit is for testing timer units

[Unit]
Description=Logs "Hello, World!" to the systemd journal
Wants=myMonitor.timer

[Service]
Type=oneshot
ExecStart=echo "Hello, World!"

[Install]
WantedBy=multi-user.target
```
- the service can be started manually with `systemctl status myMonitor.service`
**cat /etc/systemd/system/myMonitor.timer**

```txt
# This time unit trigger myMonitor.service
[Unit]  
Description=Logs some system statistics to the systemd journal  
Requires=myMonitor.service  
  
[Timer]  
Unit=myMonitor.service  
OnCalendar=*-*-* *:*:00  
  
[Install]  
WantedBy=timers.target
```
- the timer can be started with `systemctl start myMonitor.timer`
- the timer can be enabled with `systemctl enable myMonitor.timer`
- tasks are not triggered exactly at the same time
- this is intentional to prevent multiple services from starting simultaneously (e.g. 00:00)
- override this with `AccuracySec`