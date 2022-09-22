# ease_fall_school_2022
This repository contains the files for the hands-on of the EASE Fall School 2022

## Additional hints for the exercises



| Query |  Explanation / Example |
| -------- | -------- |
| triple(Subject, Predicate, Object)     |  Retrieves all the matching Subject, Object and Predicate. triple(pr2:'PR2Arm', rdf:type, ArmType).   ArmType is assigned to soma:'Arm'.  (Please load the PR2 owl file for the query to work)|
|tf:tf_get_pose(Object, [Parent, Position, Orientation]) | Fetches the pose of the object with respect to the parent frame. Use this instead of is_at/2 as mentioned in the exercise. |
|event_interval(Action, Start, End)| Gives the start and end timestamp of an event|

## Prolog built-in predicates
Refer to https://www.swi-prolog.org/


|  Query | Explanation / Example |
| -------- | -------- |
| findall     | Use findall when you need to retrieve more than one result. For ex: To get all the grasping tasks in the NEEM. findall(GraspTask, (triple(GraspTask, rdf:type, Grasping)), GraspTasks). There are other ways to get the results, for example, using recursion.     |
|sort(List, Sorted)| Sorts the list in ascending order|
|min_member(MinValue, List)| MinValue is the least value in the provided List|
|number(A)| Checks if A is a number|
|var(A)| Checks if the value is not ground|


## Good to know
- You can define a predicate as below,

        get_member(ListVal, Member) :-
            member(Member, ListVal).
            
and use it as get_member([2,3,7], Member).

- Another way to do this, is to follow the instructions in the exercise. Add a .pl file to the prolog folder and use cloud_consult('/prolog/myfile.pl').




