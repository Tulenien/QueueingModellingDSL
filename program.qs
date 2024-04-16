begin
 SetTimeConstraint 1000
 Generator normal 1 10 "A"
 Generator uniform 2 5 "B"
 Processor normal 3 7 0 "A" "B"
 Statistics generator 0
end