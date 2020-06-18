:- use_module(library(clpfd)).

sudoku(Rows) :-
    sudoku_length(Len),
    format("Len : ~d",Len),
    length(Rows, Len),
    maplist(same_length(Rows), Rows),
    
    append(Rows,X),
    X ins 1..9,

    
    % Check Rows
    format("\n Checking Rows \n"),
    checkRows(Rows),

    
    %Check Columns
    format("\n Checking Columns\n "),
    Rows = [
            [A1,A2,A3,  A4,A5,A6,  A7,A8,A9],
		    [B1,B2,B3,  B4,B5,B6,  B7,B8,B9],
		    [C1,C2,C3,  C4,C5,C6,  C7,C8,C9],

            [D1,D2,D3,  D4,D5,D6,  D7,D8,D9],
            [E1,E2,E3,  E4,E5,E6,  E7,E8,E9],
            [F1,F2,F3,  F4,F5,F6,  F7,F8,F9],

            [G1,G2,G3,  G4,G5,G6,  G7,G8,G9],
            [H1,H2,H3,  H4,H5,H6,  H7,H8,H9],
            [I1,I2,I3,  I4,I5,I6,  I7,I8,I9]
        ],

    Col1 = [A1,B1,C1,D1,E1,F1,G1,H1,I1],
    Col2 = [A2,B2,C2,D2,E2,F2,G2,H2,I2],
    Col3 = [A3,B3,C3,D3,E3,F3,G3,H3,I3],
    Col4 = [A4,B4,C4,D4,E4,F4,G4,H4,I4],
    Col5 = [A5,B5,C5,D5,E5,F5,G5,H5,I5],
    Col6 = [A6,B6,C6,D6,E6,F6,G6,H6,I6],
    Col7 = [A7,B7,C7,D7,E7,F7,G7,H7,I7],
    Col8 = [A8,B8,C8,D8,E8,F8,G8,H8,I8],
    Col9 = [A9,B9,C9,D9,E9,F9,G9,H9,I9],

    checkAllColumns(Col1,Col2,Col3,Col4,Col5,Col6,Col7,Col8,Col9),
    

    % Check Cubic Form
    format("\n Checking Cubes\n "),
    Rows = [R1,R2,R3,
            R4,R5,R6,
            R7,R8,R9],
    checkCubes(R1,R2,R3),
    checkCubes(R4,R5,R6),
    checkCubes(R7,R8,R9)
.

checkRows([]).
checkRows([H|T]) :-
    all_distinct(H),
    checkRows(T)
.

checkAColumn(Column) :-
	length(Column,9),
	all_distinct(Column).


checkAllColumns(Col1,Col2,Col3,Col4,Col5,Col6,Col7,Col8,Col9):-
    checkAColumn(Col1),
    checkAColumn(Col2),
    checkAColumn(Col3),

    checkAColumn(Col4),
    checkAColumn(Col5),
    checkAColumn(Col6),

    checkAColumn(Col7),
    checkAColumn(Col8),
    checkAColumn(Col9)
.



checkCubes([],[],[]).
checkCubes([EL1,EL2,EL3|RestRow1],
            [EL4,EL5,EL6|RestRow2],
            [EL7,EL8,EL9|RestRow3]) :-
        all_distinct([EL1,EL2,EL3,EL4,EL5,EL6,EL7,EL8,EL9]),
        checkCubes(RestRow1,RestRow2,RestRow3).


puzzle(X) :-
    format("\n Entered The Puzzle \n"),
    example(X,Table),
    format("\n Obtained the Table \n"),
    sudoku(Table),
    format("\n Solved The Table \n"),
    maplist(label,Table),
    maplist(portray_clause,Table)
.

sudoku_length(9).
example(1,Table) :-
    Table = [
      [1,_,6,_,9,_,_,_,7],
      [_,_,_,_,3,_,4,_,_],
      [4,_,_,2,_,_,9,_,8],
      [_,6,2,_,1,_,_,9,_],
      [7,_,9,_,5,_,6,_,1],
      [_,_,4,_,_,_,2,_,3],
      [8,_,1,_,4,_,_,_,_],
      [_,9,_,_,_,3,_,_,_],
      [_,_,_,6,_,_,_,_,9]
    ].

example(2,Table) :-
    % This is a well-formed sudoku which means it has only one unique solution
    Table = [
        [_,_,_,_,_,_,2,_,_],
        [_,8,_,_,_,7,_,9,_],
        [6,_,2,_,_,_,5,_,_],
        [_,7,_,_,6,_,_,_,_],
        [_,_,_,9,_,1,_,_,_],
        [_,_,_,_,2,_,_,4,_],
        [_,_,5,_,_,_,6,_,3],
        [_,9,_,4,_,_,_,7,_],
        [_,_,6,_,_,_,_,_,_]
    ].

example(3,Table) :-
    Table = [
      [5,3,_,_,7,_,_,_,_],
      [6,_,_,1,9,5,_,_,_],
      [_,9,8,_,_,_,_,6,_],
      [8,_,_,_,6,_,_,_,3],
      [4,_,_,8,_,3,_,_,1],
      [7,_,_,_,2,_,_,_,6],
      [_,6,_,_,_,_,2,8,_],
      [_,_,_,4,1,9,_,_,5],
      [_,_,_,_,8,_,_,7,9]
    ].    

%           Solution (Example 1)
%       [1,5,6,8,9,4,3,2,7],
%       [9,2,8,7,3,1,4,5,6],
%       [4,7,3,2,6,5,9,1,8],
%       [3,6,2,4,1,7,8,9,5],
%       [7,8,9,3,5,2,6,4,1],
%       [5,1,4,9,8,6,2,7,3],
%       [8,3,1,5,4,9,7,6,2],
%       [6,9,7,1,2,3,5,8,4],
%       [2,4,5,6,7,8,1,3,9]


