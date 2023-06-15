this repo holds modules with code to be run on a machine that is stationed on board a test-ship.

The machine must be connected to a 'Pepwave Max HD4 modem', by Peplink.

Work is needed on the code:
1. add a 'main' module, that will act as point of entry for the program.
2. the other code modules must be made more robust by a python programmer (see code review comments for a first start).
3. The code need a way to be initiated at a set interval. Presumably by cron-job.
4. code commenting is needed, as well as program documentation. No information about the database is given.
5. code must be added to sync the local database with an on-shore database, if connection is confirmed, but only once in a while 
		(one hour?).
