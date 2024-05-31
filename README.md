## What is the main goal of functionality in this project? 

freewrite wes: 1. Produce a schedule given a TABLE of teachers and their rules, students and their rules, a TABLE of classes. 2. When a class is scheduled, it must be scheduled in a recurring format. It must be scheduled with an end time in place. 3. There must be a single class manual override option for same day cancellations. (that makes no alterations to past or future scheduling.) 

* Each student would be schedule assessed in the algorithm 1 class at a time - this will 'thread' their schedule together. This way it is easy to keep track of the soft constraints. (how far apart their classes are every day, hours per week, etc. ) After laying one thread of classes for a student, the next thread would be lain as close to as possible the prior thread.   

Once this is accomplished the work of developing the GUI comes in. Parents, Teachers, Students, Administrators, and Upper Mgmt. all require their own seperate types of profiles. 
