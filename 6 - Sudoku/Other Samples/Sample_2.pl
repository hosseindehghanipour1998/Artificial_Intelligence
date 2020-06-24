:- use_module(library(clpfd)).

/*metodo que comprueba si un tablero esta correctamente armado*/
comprobar(Salid):-

	/*Establezco formato*/
	Salid =[ [A1,A2,A3,  A4,A5,A6,  A7,A8,A9],
	    	 [B1,B2,B3,  B4,B5,B6,  B7,B8,B9],
        	 [C1,C2,C3,  C4,C5,C6,  C7,C8,C9],

             [D1,D2,D3,  D4,D5,D6,  D7,D8,D9],
             [E1,E2,E3,  E4,E5,E6,  E7,E8,E9],
             [F1,F2,F3,  F4,F5,F6,  F7,F8,F9],

             [G1,G2,G3,  G4,G5,G6,  G7,G8,G9],
             [H1,H2,H3,  H4,H5,H6,  H7,H8,H9],
             [I1,I2,I3,  I4,I5,I6,  I7,I8,I9]
			],

	/*comprobrar las filas*/
	validar([A1,A2,A3,A4,A5,A6,A7,A8,A9]),
	validar([B1,B2,B3,B4,B5,B6,B7,B8,B9]),
	validar([C1,C2,C3,C4,C5,C6,C7,C8,C9]),
	validar([D1,D2,D3,D4,D5,D6,D7,D8,D9]),
	validar([E1,E2,E3,E4,E5,E6,E7,E8,E9]),
	validar([F1,F2,F3,F4,F5,F6,F7,F8,F9]),
	validar([G1,G2,G3,G4,G5,G6,G7,G8,G9]),
	validar([H1,H2,H3,H4,H5,H6,H7,H8,H9]),
	validar([I1,I2,I3,I4,I5,I6,I7,I8,I9]),
 
	/*comprobar las columnas*/
	validar([A1,B1,C1,D1,E1,F1,G1,H1,I1]),
	validar([A2,B2,C2,D2,E2,F2,G2,H2,I2]),
	validar([A3,B3,C3,D3,E3,F3,G3,H3,I3]),
	validar([A4,B4,C4,D4,E4,F4,G4,H4,I4]),
	validar([A5,B5,C5,D5,E5,F5,G5,H5,I5]),
	validar([A6,B6,C6,D6,E6,F6,G6,H6,I6]),
	validar([A7,B7,C7,D7,E7,F7,G7,H7,I7]),
	validar([A8,B8,C8,D8,E8,F8,G8,H8,I8]),
	validar([A9,B9,C9,D9,E9,F9,G9,H9,I9]),

	/*comprobar las cuadriculas*/
	validar([A1,A2,A3,B1,B2,B3,C1,C2,C3]),
	validar([A4,A5,A6,B4,B5,B6,C4,C5,C6]),
	validar([A7,A8,A9,B7,B8,B9,C7,C8,C9]),
	validar([D1,D2,D3,E1,E2,E3,F1,F2,F3]),
	validar([D4,D5,D6,E4,E5,E6,F4,F5,F6]),
	validar([D7,D8,D9,E7,E8,E9,F7,F8,F9]),
	validar([G1,G2,G3,H1,H2,H3,I1,I2,I3]),
	validar([G4,G5,G6,H4,H5,H6,I4,I5,I6]),
	validar([G7,G8,G9,H7,H8,H9,I7,I8,I9])
	.

/*predicado que resuelve un tablero de sudoku a partir de una par de cifras */
resolver( Salida):-
	
	format("Test 1 "),
	/*Establezco formato*/
	Salida =[A1,A2,A3,  A4,A5,A6,  A7,A8,A9,
		 B1,B2,B3,  B4,B5,B6,  B7,B8,B9,
        	 C1,C2,C3,  C4,C5,C6,  C7,C8,C9,

        	 D1,D2,D3,  D4,D5,D6,  D7,D8,D9,
             	 E1,E2,E3,  E4,E5,E6,  E7,E8,E9,
     	         F1,F2,F3,  F4,F5,F6,  F7,F8,F9,

     	         G1,G2,G3,  G4,G5,G6,  G7,G8,G9,
     	         H1,H2,H3,  H4,H5,H6,  H7,H8,H9,
     	         I1,I2,I3,  I4,I5,I6,  I7,I8,I9],

format("Test 2 "),
	/*comprobrar las filas*/
	validar([A1,A2,A3,A4,A5,A6,A7,A8,A9]),
	validar([B1,B2,B3,B4,B5,B6,B7,B8,B9]),
	validar([C1,C2,C3,C4,C5,C6,C7,C8,C9]),
	validar([D1,D2,D3,D4,D5,D6,D7,D8,D9]),
	validar([E1,E2,E3,E4,E5,E6,E7,E8,E9]),
	validar([F1,F2,F3,F4,F5,F6,F7,F8,F9]),
	validar([G1,G2,G3,G4,G5,G6,G7,G8,G9]),
	validar([H1,H2,H3,H4,H5,H6,H7,H8,H9]),
	validar([I1,I2,I3,I4,I5,I6,I7,I8,I9]),
 format("Test 3 "),
	/*comprobar las columnas*/
	validar([A1,B1,C1,D1,E1,F1,G1,H1,I1]),
	validar([A2,B2,C2,D2,E2,F2,G2,H2,I2]),
	validar([A3,B3,C3,D3,E3,F3,G3,H3,I3]),
	validar([A4,B4,C4,D4,E4,F4,G4,H4,I4]),
	validar([A5,B5,C5,D5,E5,F5,G5,H5,I5]),
	validar([A6,B6,C6,D6,E6,F6,G6,H6,I6]),
	validar([A7,B7,C7,D7,E7,F7,G7,H7,I7]),
	validar([A8,B8,C8,D8,E8,F8,G8,H8,I8]),
	validar([A9,B9,C9,D9,E9,F9,G9,H9,I9]),
format("Test 4 "),
	/*comprobar las cuadriculas*/
	validar([A1,A2,A3,B1,B2,B3,C1,C2,C3]),
	validar([A4,A5,A6,B4,B5,B6,C4,C5,C6]),
	validar([A7,A8,A9,B7,B8,B9,C7,C8,C9]),
	validar([D1,D2,D3,E1,E2,E3,F1,F2,F3]),
	validar([D4,D5,D6,E4,E5,E6,F4,F5,F6]),
	validar([D7,D8,D9,E7,E8,E9,F7,F8,F9]),
	validar([G1,G2,G3,H1,H2,H3,I1,I2,I3]),
	validar([G4,G5,G6,H4,H5,H6,I4,I5,I6]),
	validar([G7,G8,G9,H7,H8,H9,I7,I8,I9]),

	format("Test 5 "),
	label(Salida).

validar(L) :-
	length(L,9),
	L ins 1..9,
	all_distinct(L).

problem(1, P) :-
        P = [[1,_,_,8,_,4,_,_,_],
             [_,2,_,_,_,_,4,5,6],
             [_,_,3,2,_,5,_,_,_],
             [_,_,_,4,_,_,8,_,5],
             [7,8,9,_,5,_,_,_,_],
             [_,_,_,_,_,6,2,_,3],
             [8,_,1,_,_,_,7,_,_],
             [_,_,_,1,2,3,_,8,_],
             [2,_,5,_,_,_,_,_,9]].