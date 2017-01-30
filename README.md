# TeamSnap
Generates a list of currently online Teamspeak instances, and creates a virtualserver snapshot.

I created this to enable simpler backup of teamspeak virtual servers across platforms.
Simply add the server query details you wish to use at the bottom of the file, or multiple for multiple phyiscal servers, And call the script.
A folder will be created in the execution directory, named with the current date, which will contain .txt files with the server snapshots.
These snapshot files are named with the Server name (Most of it), and the port, along with the date and time for sorting purposes.
These can either be restored using a Telnet client, or used with YaTqA, if you aren't a masochist.

Many thanks to Sam for his invaluable assistance, and to the developer of YaTqA for the inspiration.
For more information regarding YaTqa, you can visit http://yat.qa/ :- It is an excellent tool for any Teamspeak administration.
