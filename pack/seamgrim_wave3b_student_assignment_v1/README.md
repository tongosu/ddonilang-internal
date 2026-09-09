# seamgrim_wave3b_student_assignment_v1

Wave3B G6 product gate for opening Foundation12 classroom bundles as student assignments.

The product browser runner checks all 12 foundation lessons through:

- local `classroom_exchange.v0` bundle import
- prediction entry
- run evidence generation
- one deployment-profile-allowed control change
- explanation entry
- DDN source access
- local "my version" save and reopen restore

The gate does not add DDN syntax, change runtime `state_hash`, or reintroduce runtime student/teacher role toggles.
