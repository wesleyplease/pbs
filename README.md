## What is the main goal of functionality in this project? 

freewrite wes: 
1. Produce a schedule given a TABLE of teachers and their rules, TABLE of students and their rules, a TABLE of classes. 
2. When a class is scheduled, it must be scheduled in a recurring format. It must be scheduled with an end time in place.
3. There must be a single day manual override option for same day cancellations. (that makes no alterations to past or future scheduling.) 
4. The schedule must adhere to the priority rules for student, then priority rules teacher.

Each student would be schedule assessed in the algorithm 1 class at a time - this will 'thread' their schedule together. This way it is easy to keep track of the soft constraints. (how far apart their classes are every day, hours per week, etc. ) After laying one thread of classes for a student, the next thread would be lain as close to as possible the prior thread.   



... if the algorithm works
Once this is accomplished the work of developing the GUI comes in. Parents, Teachers, Students, Administrators, and Upper Mgmt. all require their own seperate types of profiles. 
A vizualization of the schedule that everyone can see. Plus other vizualisation options for individulas to see their own personal schedules. 
UNLESS OF COURSE we just want to make them plug it into teachworks after the algorithm runs its course but thats just lazzzzy. 
It also may be nice to include other functionality that we can gather from teachers to make it special. 
