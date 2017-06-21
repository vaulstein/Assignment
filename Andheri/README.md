# Andheri Based company

Had 5 simple programs and one additional program.

The problem statement for the 5 simple programs is present in problem_set.pdf

The additional program code is as follows:

Once you are done with these 5 problems, implement the following connection history parsing problem. Data-set for this problem is attached in a zip file.

The csv files indicate connection log for meters deployed in the field.
The relevant fields are Meter-ID, Date, and Connection status.
The sequence id orders the events received.

When the meter connects to the server, it sends status = connected
When it disconnects, the status is registered as disconnected.

A meter can remain connected for multiple days at a stretch.

We need to get a list of days per meter when it was disconnected (i.e days after the last status registered was disconnected and no connect event was received in the entire day)

If any connect event is received for a day, we consider the meter to be connected on that day. 

**The required output was different from what the problem statement said.**
**The required output was the dates that were not present in the file**

Example:

00100467

It should show disconnected at following dates..

* 13
* 15
* 21
* 22
* 24
* 25
* 26
* 27
* 28
* 29
* 1
* 2
* 3
* 4
* 5
* 6
