%utils.pl

% Utilities

% modified for SWI-Prolog
% Walter Nauber
% 26.01.01

:- dynamic (randomlast/1).

% startvalue for generator of random numbers
randomlast(0.123456789).

%sets a new startvalue for random numbers randomly
init_random(0):-init_random(random),!.
init_random(random):-
              R is (random(1000000000) + 1)/1000000000,
              retract(randomlast(_)),
              assert(randomlast(R)),!.

%sets a new startvalue R for random numbers
init_random(R)     :-
              retract(randomlast(_)), assert(randomlast(R)).

%gives randomly a value Value with 0 <= Value < Max using randomlast
random2(Max, Value):-
              randomlast(Q),!, P is 1234.56789 * Q, R is float_fractional_part(P),
              retract(randomlast(_)), assert(randomlast(R)), 
              % AM integer
              Value is integer(truncate(R * Max)).


%generates randomly a integer number Value with Min<= Value <= Max
random3(Min, Max, Value):-
             D is Max - Min + 1, random2(D,R), Value is Min + R.

%predicate maybe is true with propability P whereby 0<= P <=1
maybe(1):-true,!.
maybe(0):-fail,!.
maybe(P):-
    random2(1000000000,P1), P1<1000000000*P.


% gets randomly an element E of list L
random_member(E,L):- 
             length(L,N), random2(N,K), nth0(K,L,E).
