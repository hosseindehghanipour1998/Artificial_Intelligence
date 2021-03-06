
%   this procedure requires the external definition of two procedures:
%
%     init_agent: called after new world is initialized.  should perform
%                 any needed agent initialization.
%
%     run_agent(percept,action): given the current percept, this procedure
%                 should return an appropriate action, which is then
%                 executed.
%

:- dynamic (gold/1).
:- dynamic(arrow/1).
:- dynamic(currentLocation/2).
:- dynamic(previous_location/2).
:- dynamic(orientation/1).
:- dynamic(is_wumpus_dead/1).
:- dynamic(pit_free_cord/2).
:- dynamic(wumpus_free_cord/2).
:- dynamic(safeHouse/2).
:- dynamic(breeze/2).
:- dynamic(stench/2).
:- dynamic(samep/1).
:- dynamic(sameO/1).


init_agent:-
	format("Hello Welcome To Wumpus World ! "),
	retractall(gold(_)),								%if has gold
	retractall(arrow(_)),								%if has any arrows left
	retractall(currentLocation(_,_)),					%current location of agent
	retractall(previous_location(_,_)),
	retractall(orientation(_)),
	retractall(is_wumpus_dead(_)),
	retractall(pit_free_cord(_,_)),						% There is no pit in that location
	retractall(wumpus_free_cord(_,_)),
	retractall(safeHouse(_,_)),
	retractall(breeze(_,_)),
	retractall(stench(_,_)),
	retractall(samep(_)),
	retractall(sameO(_)),

	retractall(visited(_,_)),
	assert(gold(0)),					 %record the number of golds obtained
	assert(arrow(1)),					 %record the amount of the arrow
	assert(currentLocation(1,1)),			 %record the current position of the agent
	assert(previous_location(1,1)),							 %record the previous position of the agent
	assert(orientation(0)),
	assert(is_wumpus_dead(0)),
	assert(pit_free_cord(1,1)),
	assert(wumpus_free_cord(1,1)),
	assert(safeHouse(1,1)),
	assert(breeze(-8,-8)),					% ?
	assert(stench(-8,-8)),					% ?
    assert(samep(0)),
	assert(sameO(0)),
    assert(visited(1,1)),
	initialize_file("a.txt","B").			 % Delete the file and create it again.


run_agent(Percept,Action):-
	% Write to File
	currentLocation(X,Y),
	arrow(G),
    is_wumpus_dead(W),
	orientation(FFF),
	sameO(MM),
	samep(VV),
	assert(safeHouse(X,Y)),
	display_world,
	action(Percept,Action),

	%% Taking a log
	adding("("),
	adding(X),
	adding(","),
	adding(Y),
	adding(") | "),
	adding(FFF),
	adding(" | "),
	adding("Arrow : "),
	adding(G),
	adding("|SameO: "),
	adding(MM),
	adding("|SameP: "),
	adding(VV),
	adding("|Action:"),
	adding(Action),
	adding(" | "),
	adding(Percept),
	adding("\n"),
	%% End of Taking a log

	changelocation(Action),
	previous_location(XP,YP),
	((X=XP,Y=YP,samep(Counter),Counter1 is Counter+1,retractall(samep(_)),assert(samep(Counter1)),assert(sameO(FFF)));
	((X=\=XP;Y=\=YP),retractall(sameO(_)),assert(sameO(FFF)),retractall(samep(_)),assert(samep(0)))).




changelocation(Action):-
	currentLocation(X,Y), Left_X is X-1,Right_X is X+1,Up_Y is Y+1,Down_Y is Y-1,
    orientation(Angle),
	(
		(Action = turnright,retractall(orientation(_)),Angle = 0,Angle1 is 270,assert(orientation(Angle1)));
		(Action = turnright,retractall(orientation(_)),Angle = 90,Angle1 is 0,assert(orientation(Angle1)));
		(Action = turnright,retractall(orientation(_)),Angle = 180,Angle1 is 90,assert(orientation(Angle1)));
		(Action = turnright,retractall(orientation(_)),Angle = 270,Angle1 is 180,assert(orientation(Angle1)));
		(Action = turnleft,retractall(orientation(_)),Angle = 0,Angle1 is 90,assert(orientation(Angle1)));
		(Action = turnleft,retractall(orientation(_)),Angle = 90,Angle1 is 180,assert(orientation(Angle1)));
		(Action = turnleft,retractall(orientation(_)),Angle = 180,Angle1 is 270,assert(orientation(Angle1)));
		(Action = turnleft,retractall(orientation(_)),Angle = 270,Angle1 is 0,assert(orientation(Angle1)));
		(Action = goforward,retractall(currentLocation(_,_)),retractall(previous_location(_,_)),Angle = 0,assert(currentLocation(Right_X,Y)),assert(previous_location(X,Y)));
		(Action = goforward,retractall(currentLocation(_,_)),retractall(previous_location(_,_)),Angle = 90,assert(currentLocation(X,Up_Y)),assert(previous_location(X,Y)));
		(Action = goforward,retractall(currentLocation(_,_)),retractall(previous_location(_,_)),Angle = 180,assert(currentLocation(Left_X,Y)),assert(previous_location(X,Y)));
		(Action = goforward,retractall(currentLocation(_,_)),retractall(previous_location(_,_)),Angle = 270,assert(currentLocation(X,Down_Y)),assert(previous_location(X,Y)));
		(Action = grab);
		(Action = climb);
		(Action = shoot,retractall(arrow(_)),assert(arrow(0)))
	).
% ================================================= Spin for orientation

spin(X,O):-
	adj(X,Y),
	\+ sameO(Y),
	O = Y .

adj(0,90).
adj(90,0).

adj(180,90).
adj(90,180).

adj(180,270).
adj(270,180).

adj(0,270).
adj(270,0).

minus(X,Y,Z) :-
	X is Y-Z.

% ============================================== Coordinates Status

is_wumpus(X, Y) :-
	Left_X is X-1,Right_X is X+1,Up_Y is Y+1,Down_Y is Y-1,
	(
		( (stench(Left_X,Y)),(stench(Right_X, Y)) );
		( (stench(Left_X, Y)),(stench(X, Up_Y)) );
		( (stench(Left_X, Y)),(stench(X, Down_Y)) );
		( (stench(Right_X, Y)),(stench(X, Up_Y)) );
		( (stench(Right_X, Y)),(stench(X, Down_Y)) );
		( (stench(X, Up_Y)),(stench(X, Down_Y)) ),
		(\+wumpus_free_cord(X,Y))  % check this again
	).


possible_pit(X,Y):-
	Left_X is X-1,Right_X is X+1,Up_Y is Y+1,Down_Y is Y-1,
	(breeze(Left_X, Y); Left_X < 1),
	(breeze(Right_X, Y); Right_X > 4),
	(breeze(X, Up_Y); Up_Y > 4),
	(breeze(X, Down_Y); Down_Y < 1).



safe(X,Y):-
	(safeHouse(X,Y);
	(is_wumpus_dead(0),pit_free_cord(X,Y),wumpus_free_cord(X,Y));
	(is_wumpus_dead(1),pit_free_cord(X,Y))).

% ================================================= Taking Actions according to situations
action([no,no,_,_,_],_):-

	% Left_X -> Left X
	% Right_X -> Right X
	% Up_Y -> Upper Y
	% Down_Y -> Down Y
	currentLocation(X,Y),Left_X is X-1,Right_X is X+1,Up_Y is Y+1,Down_Y is Y-1,
	((Right_X < 5,assert(safeHouse(Right_X,Y)));
	(Up_Y < 5,assert(safeHouse(X,Up_Y)));
	(Left_X > 0,assert(safeHouse(Left_X,Y)));
	(Down_Y>0,assert(safeHouse(X,Down_Y)))),
    assert(safeHouse(X,Y)),
	fail.% for trackbacking


action([yes,_,_,_,_],_):-
	currentLocation(X,Y),assert(stench(X,Y)),fail.

action([_,yes,_,_,_],_):-
	currentLocation(X,Y),assert(breeze(X,Y)),fail.


action([_,_,_,_,yes],_):-
	retractall(is_wumpus_dead(_)),
	assert(is_wumpus_dead(1)),
	currentLocation(X,Y),
	assert(safeHouse(X,Y)),
	fail. % for trackbacking

action([_,no,_,_,_],_):-
    currentLocation(X,Y),
	Left_X is X-1,Right_X is X+1,Up_Y is Y+1,Down_Y is Y-1,
	((Left_X>0,assert(pit_free_cord(Left_X,Y)));
	(Right_X<5,assert(pit_free_cord(Right_X,Y)));
	(Down_Y>0,assert(pit_free_cord(X,Down_Y)));
	(Up_Y<5,assert(pit_free_cord(X,Up_Y)))),
	fail.% for trackbacking


action([no,_,_,_,_],_):-
    currentLocation(X,Y),
	Left_X is X-1,Right_X is X+1,Up_Y is Y+1,Down_Y is Y-1,
	((Left_X>0,assert(wumpus_free_cord(Left_X,Y)));
	(Right_X<5,assert(wumpus_free_cord(Right_X,Y)));
	(Down_Y>0,assert(wumpus_free_cord(X,Down_Y)));
	(Up_Y<5,assert(wumpus_free_cord(X,Up_Y)))),
	fail.% for trackbacking


action([_,_,yes,_,_],grab):-   %grab gold
	gold(X),
	retractall(gold(_)),
	X1 is X+1,
	assert(gold(X1)).


action([yes,_,_,_,no],shoot):-
    is_wumpus_dead(0),
        arrow(1),
    currentLocation(X,Y),
    Left_X is X-1,Right_X is X+1,Up_Y is Y+1,Down_Y is Y-1,
    orientation(Angle),
    ((Angle=0,is_wumpus(Right_X,Y));
    (Angle=90,is_wumpus(X,Up_Y));
    (Angle=180,is_wumpus(Left_X,Y));
    (Angle=270,is_wumpus(X,Down_Y))).

action([_,_,_,_,_],climb):-
	currentLocation(1,1),
    samep(Repeatense),
	Repeatense > 5.

action([_,_,_,_,_],climb):-
	gold(NumberOfGold),
	NumberOfGold > 0,
	currentLocation(1,1).

action([_,_,no,_,_],goforward):-
	currentLocation(X,Y),Left_X is X-1,Right_X is X+1,Up_Y is Y+1,Down_Y is Y-1,
	orientation(Angle),
	((Angle=0,X <4,safe(Right_X,Y));
	(Angle=90,Y <4,safe(X,Up_Y));
	(Angle=180,X>1,safe(Left_X,Y));
	(Angle=270,Y>1,safe(X,Down_Y))).

action([_,_,_,_,_],Action):-

	%orientation(FFF),
	%spin(FFF,NewO),
	random_between(0,1,R),
	((R=0,Action = turnright);
	(R=1,Action = turnleft)).
	%minus(Diff,FFF,NewO),
	%((Diff > 0 , Action = turnright );
	%(Diff < 0 , Action = turnleft)).

action([_,_,_,yes,_],Action):-
	random_between(0,1,R),
	previous_location(X,Y),
	((R=0,Action = turnright);
	(R=1,Action = turnleft)),
	retractall(currentLocation(_,_)),assert(currentLocation(X,Y)).
% ================================================= Log Management
initialize_file(File, Text) :-
  open(File, write, Stream),
  write(Stream, Text), nl,
  close(Stream).

adding(Text) :-
	open('a.txt', append, Handle),
	write(Handle, Text),
	close(Handle).


