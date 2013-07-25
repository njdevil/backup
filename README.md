Linux Backup System v3.1
======

A handy little python backup script that will simultaneously manage both your internal files and client files which may reside on the same system.

This script is intended to run automatically via a CRONJOB.  Arguments can be passed for "daily" or "weekly" backups.


Usage
==========
Execute the code via:
python backupmaster.py (daily|weekly)


Directory Include/Exclude
==========
A module was added to allow you to specify which directories you would like to include and also which ones you want to exclude from the inclusion list.  For example, if you wanted to backup "/foo/bar" but not "/foo/bar/bat" you can specify "/foo/bar" in the Include List and "/foo/bar/bat" in the Exclude List.


Daily backups and "Archive Bit" missing
=========
Back in the old DOS days, the FAT filesystem contained an ARCHIVE BIT which would specify if a file was changed.  This is how lots of backup systems used to work.  However, Linux file systems do not include this Archive Bit so a work-around was needed.  In Linux, whenver we write to a file, the date/time of that file changes.  This time is written as an EPOCH time and we can compare it to yesterday's Epoch at midnight to see if that file was changed.  If yes, back it up! If no, ignore it.


Weekly backups
=========
Weekly backups back up all files regardless if they were changed or not.  This can be very helpful if a file mysteriously disappears.


Old backups
=========
All of these backups can take up a lot of space.  Yes you could spend the time trying to prune it down, but this software is also set to only retain 4 iterations of backups and then delete the oldest.  You can change the duration, but the old files are still deleted.


GPL
=========
This code is released as GPL3 and is copyright 2013 by Modular Programming Systems Inc.
