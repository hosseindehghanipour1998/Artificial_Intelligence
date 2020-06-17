soduku(Rows) :-
    sudoku_length(Len),
    length(Rows, Len),
    maplist(Len, Rows),
    Elements ins 1..9,
    append(Rows,Elements),
    deepSearchSoduku(Rows)

    Rows = [R1,R2,R3,
            R4,R5,R6,
            R7,R8,R9],
    checkCubes(R1,R2,R3),
    checkCubes(R4,R5,R6),
    checkCubes(R7,R8,R)
.

sudoku_length(9).


deepSearchSoduku([]).
deepSearchSoduku([H|T]) :-
    all_distinct(H),
    deepSearchSoduku(T)
.

checkCubes([],[],[]).
checkCubes([EL1,EL2,EL3|RestRow1],
            [EL4,EL5,EL6|RestRow2],
            [EL7,EL8,EL9|RestRow3]) :-
        all_distinct([EL1,EL2,EL3,EL4,EL5,EL6,EL7,EL8,EL9]),
        checkCubes(RestRow1,RestRow2,RestRow3).


example(Table) :-
    Table = [
      [1,_,6,_,9,_,-,_,7],
      [_,_,_,_,3,_,4,_,_],
      [4,_,_,2,_,_,9,_,8],
      [_,6,2,_,1,_,_,9,_],
      [7,_,9,_,5,_,6,_,1],
      [_,_,4,_,_,_,2,_,3],
      [8,_,1,_,4,_,_,_,_],
      [_,9,_,_,_,3,_,_,_],
      [_,_,_,6,_,_,_,_,9]
    ].

%           Solution
%       [1,5,6,8,9,4,3,2,7],
%       [9,2,8,7,3,1,4,5,6],
%       [4,7,3,2,6,5,9,1,8],
%       [3,6,2,4,1,7,8,9,5],
%       [7,8,9,3,5,2,6,4,1],
%       [5,1,4,9,8,6,2,7,3],
%       [8,3,1,5,4,9,7,6,2],
%       [6,9,7,1,2,3,5,8,4],
%       [2,4,5,6,7,8,1,3,9]