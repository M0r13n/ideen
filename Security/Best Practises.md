# Best Practises For Enterprise Networks

| Best practise | Implementation                                               |
| ------------- | ------------------------------------------------------------ |
| Immutable     | write only backup (nobody can change backups)                |
| Independent   | separate infrastructure for backups                          |
| Isolated      | separate IAM. **NEVER** use AD                               |
| Versioned     | incremental backups for earlier states                       |
| Verified      | regular end-to-end verification                              |
| Monitored     | Is a backup successful/failed? Is the file system corrupted? |
| Risk-based    | No. 1 Goal: Recovery of operation                            |

> Wer den Backupserver administriert geht mit der Tastatur und dem Monitor in den Serverraum und steckt die da dran. Keine Remoteadministration. Keine Verbindung ins AD.

_Source: Linus Neumann, 37C3 -  Hirne hacken: Hackback Edition_