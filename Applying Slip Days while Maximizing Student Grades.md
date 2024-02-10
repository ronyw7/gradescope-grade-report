`101_final_grades.ipynb
![[Screenshot 2024-02-10 at 01.19.29.png]]
- First step is to check how many total "late" days a student has accumulated
	- `9` is the total number of slip days available to each student
	- Some students had previous extensions/extenuating circumstances so they've used some of their slip days. This is accounted for by `slip`

![[Pasted image 20240210012309.png]]
- `to_be_updated` contains a list of student emails who have more late days than remaining slip days. **We need to figure out how to maximize grades for these students.**

![[Screenshot 2024-02-10 at 01.27.29.png]]
- This cell prints out the late assignment items for each student in the `to_be_updated` list. Useful for debugging/verifying if slip days are correctly applied.
- `to_process` is a dictionary with key `email: string` and value `student_late_items: List`
- Note that `student_late_items` is sorted by score from highest to lowest. This makes applying slip days easier - we just need to try applying slip days to assignments where students scored the highest points. 
	- e.g. If a student scored 0/25 in their multivitamin (late = 1), then we won't bother applying slip days to this assignment, because they'll be better off if we applied this slip day to their late project instead.

![[Pasted image 20240210012951.png]]
- This is the cell for actually applying slip days while maximizing student grades. The logic is as follows:
	- If the student has enough slip days to cover one of their late assignments, then apply the slip days. Eventually we remove the assignment from the list so no late penalty is applied.
	- Otherwise, the student has fewer slip days than the number of late days on the given assignment. So here we are just on a "best-effort basis" -  apply the remaining slip days to that assignment.