
% Dynamic Relations :
%
:- load_files([utils]).  % Basic utilities
:- dynamic(breeze/1).
:- dynamic(hasGold/0).
:- dynamic(updateOrientation/1).
:- dynamic(adjacent_squares/2).
:- dynamic(updateCoordinate/1).
:- dynamic(safe/1).
:- dynamic(pit/2).
:- dynamic(yMax/1).
:- dynamic(currentPos/1).
:- dynamic(prevPos/1).
:- dynamic(orientation/1).
:- dynamic(fact/1).
:- dynamic(updateBump/0).
:- dynamic(checkFront/0).
:- dynamic(checkFront/1).
:- dynamic(xMax/1).
:- dynamic(wumpusAlive/0).
:- dynamic(hasArrow/0).
%===============================================

init_agent:-
  format('\n=====================================================\n'),
  format('This is init_agent:\n\tIt gets called once, use it for your initialization\n\n'),
  format('=====================================================\n\n'),
  resetAgent(),
  assert(pit(_,_)),
  retract(pit(1,1)),
  assert(safe([1,1])),
  assert(xMax(10000)),
  assert(yMax(10000)),
  assert(wumpusAlive),
  assert(safe([1,2])),
  assert(safe([2,1])),
  assert(hasArrow),
  assert(currentPos([1,1])),
  assert(visited([1,1])),
  assert(prevPos([1,1])),
  assert(orientation(0)),
  assert(path([turnleft,goforward,turnright])).
%===============================================
resetAgent() :-
  retractall(hasGold),
  retractall(currentPos([X,Y])),
  retractall(prevPos(A,B)),
  retractall(orientation(C)).

%------------------------------------------------------------------------


% ==========================================================
%
updateOrientation(NextAction) :-
  orientation(Orient),
  format("orientation is ~d \n", [Orient]),
  (NextAction = turnright -> NewOrientation is (Orient - 90) mod 360;
    (NextAction = turnleft -> NewOrientation is (Orient + 90) mod 360;
   NewOrientation is Orient)),
  format("NextAction is ~w \n", [NextAction]),
  format("New orientation is ~d \n", [NewOrientation]),
  retractall(orientation(Orient)),
  assert(orientation(NewOrientation)).
%===============================================

updateCoordinate(NextAction) :-
  orientation(Orient),
  currentPos([X,Y]),
  postion_calculator(X,Y,NewX,NewY,NextAction),
  retractall(currentPos(P)),
  retractall(prevPos(P)),
  assert(prevPos([X,Y])),
  assert(currentPos([NewX,NewY])),
  format("UpdatedCoordinate is [~d,~d]\n",[NewX,NewY]).


%===============================================

% take a turn with 50% possibility for each.
random_turn(A) :-
  random2(100,Value),
  (
    (A = turnleft , Value>50);
    (A = turnright , Value<50)
  ),!.
%===============================================
% move forward or left with 50% possibility for each.
random_walk(A) :-
  random2(100,Value),
  (
    (A = goforward , Value>50);
    (A = turnleft , Value<50)
  ),!.
%===============================================


next_action([H|T], H):-
  retract(path([H|T])),
  assert(path(T)).

% ===============================================
%% **************** Agent's Movements ************

% run_Agent(Percept,Action) : according to the percept chooses what
% should the action be.
%

%$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

%%     climb:     if in square 1,1, leaves the cave and adds 1000 points
%                for each piece of gold

run_agent([no,no,no,no,no], climb):-
  currentPos([1,1]),
  hasGold,
  format("Get out of here \n"),
  format("We have escaped the Cave Successfully \n"),
  format(" ***************Finished !!!!! ***************\n"),
  ignore((safety_update,false)),
  display_world,!.

% $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
%     grab:      pickup gold if in square

run_agent([_,_,yes,_,_], grab):-
  format("Found the gold and grabbed it \n"),
  %% updateOrientation(Action),
  updateCoordinate(grab),
  assert(hasGold),
  display_world,!.
% $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
% goforward: move one square along current orientation if possible

run_agent([_,no,_,_,yes], goforward):-
  format("Killed Wumpus \n"),
  retract(wumpusAlive),
  ignore((safety_update,false)),
  updateOrientation(goforward),
  updateCoordinate(goforward),
  display_world,
  !.
% $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

% if you sense a stench and the wumpus is also alive , kill it then ->
% shot the wumpus
% shoot: shoot an arrow along orientation, killing wumpus if
%                in that direction

run_agent([yes,_,_,_,_], shoot):-
  wumpusAlive,
  hasArrow,
  format("kill wumpus if alive \n"),
  updateOrientation(shoot),
  updateCoordinate(shoot),
  retract(hasArrow),
  display_world,!.

% $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
% if the spot has a stench and wumpus is dead:
  % if there is no breeze: set it as a safe spot =>safety_update
  % random move or random turn depending on which one is safe.
run_agent([yes,no,_,no,_], Action):-
  checkFront,
  \+wumpusAlive,
  \+hasArrow,
  ignore((safety_update,false)),
  random_walk(Action),
  updateOrientation(Action),
  updateCoordinate(Action),
  display_world,!.
% $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

run_agent([yes,no,_,no,_], Action):-
  \+checkFront,
  \+wumpusAlive,
  \+hasArrow,
  ignore((safety_update,false)),
  random_turn(Action),
  updateOrientation(Action),
  updateCoordinate(Action),
  display_world,!.
% $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

% if the spot has a stench and wumpus is dead:
  % if there is a breeze:Don't mark the spot as safe.
  % random move or random turn depending on which one is safe.
run_agent([yes,yes,_,no,_], Action):-
  checkFront,
  \+wumpusAlive,
  \+hasArrow,
  random_walk(Action),
  updateOrientation(Action),
  updateCoordinate(Action),
  display_world,!.
% $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

run_agent([yes,yes,_,no,_], Action):-
  \+checkFront,
  \+wumpusAlive,
  \+hasArrow,
  random_turn(Action),
  updateOrientation(Action),
  updateCoordinate(Action),
  display_world,!.
% $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

run_agent([no,no,no,no,no], Action):-
  checkFront,
  ignore((safety_update,false)),
  random_walk(Action),
  updateOrientation(Action),
  updateCoordinate(Action),
  display_world,!.
% $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

run_agent([no,no,no,no,no], Action):-
  \+checkFront,
  ignore((safety_update,false)),
  random_turn(Action),
  updateOrientation(Action),
  updateCoordinate(Action),
  display_world,!.
% $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

run_agent([_,_,_,yes,_], Action):-
  format("bumped into wall \n"),
  updateBump,
  random_turn(Action),
  updateOrientation(Action),
  updateCoordinate(Action),
  display_world,!.
%===============================================
% if you feel a breeze and it's safe to move forward,take it then :D
run_agent([no,yes,no,no,no], goforward):-
  checkFront,
  format("Breeze + forward is safe => going forward \n"),
  currentPos([X,Y]),
  updateCoordinate(goforward),
  display_world,!.
%===============================================
% if you sense a breeze and it's possible to die if you move forward,
% turn away and go somewhere else
run_agent([no,yes,no,no,no], Action):-
  format("Breeze + forward is not safe => Turning Randomly \n"),
  currentPos([X,Y]),
  \+checkFront,
  random_turn(Action),
  updateOrientation(Action),
  updateCoordinate(Action),
  display_world,!.
%===============================================

%================================================
updateBump:-
  orientation(O),
  retractall(currentPos(_)),
  prevPos([X,Y]),
  (O = 90 -> format("O is 90 \n"), YMAX is Y+1, retractall(ymax(WYES)), asserta(ymax(YMAX)); format("O is not 90 \n")),
  (O = 0 -> format("O is 0 \n"), XMAX is X+1, retractall(xmax(EXES)), asserta(xmax(XMAX)); format("O is not 0 \n")),
  assert(currentPos([X,Y])).



%===============================================

postion_calculator(X,Y,NewX,NewY,NextAction) :-
  NextAction \= goforward,
  NewX is X,
  NewY is Y,!.
%===============================================

postion_calculator(X,Y,NewX,NewY,NextAction) :-
  orientation(O),
  O =:= 0,
  NextAction = goforward,
  NewX is X + 1,
  NewY is Y,!.
%===============================================

postion_calculator(X,Y,NewX,NewY,NextAction) :-
  orientation(O),
  O =:= 90,
  NextAction = goforward,
  NewX is X,
  NewY is Y + 1,!.
%===============================================

postion_calculator(X,Y,NewX,NewY,NextAction) :-
  orientation(O),
  O =:= 180,
  NextAction = goforward,
  NewX is X - 1,!,
  NewY is Y.
%===============================================

postion_calculator(X,Y,NewX,NewY,NextAction) :-
  orientation(O),
  O =:= 270,
  NextAction = goforward,
  NewX is X,
  NewY is Y - 1,!.

%===============================================

adjacent_squares([X,Y],[X1,Y]) :-
  X1 is X-1.
adjacent_squares([X,Y],[X1,Y]) :-
  X1 is X+1.
adjacent_squares([X,Y],[X,Y1]) :-
  Y1 is Y-1.
adjacent_squares([X,Y],[X,Y1]) :-
  Y1 is Y+1.
%===============================================
assertOnce(Fact):-
    \+( Fact ),!,
    assert(Fact).
assertOnce(_).
%===============================================

safety_update :-
  currentPos([X,Y]),
  adjacent_squares([X,Y],[X1,Y1]),
  assertOnce(safe([X1,Y1])),
  format("Safe status has been updated \n"),
  format("Asserting [~d,~d] \n",[X1,Y1]).
%===============================================
%===============================================

checkFront:-
  orientation(O),
  xMax(XMAX),
  yMax(YMAX),
  O =:= 0,
  currentPos([X,Y]),
  X1 is X+1,
  X+1 > 0,
  X+1 < XMAX,
  safe([X1,Y]).
%===============================================

checkFront:-
  orientation(O),
  xMax(XMAX),
  yMax(YMAX),
  O =:= 90 ,
  currentPos([X,Y]),
  Y1 is Y+1,
  Y+1 < YMAX,
  safe([X,Y1]).
%===============================================

checkFront:-
  orientation(O),
  xMax(XMAX),
  yMax(YMAX),
  O =:= 180,
  currentPos([X,Y]),
  X1 is X-1,
  X-1 > 0,
  X-1 < XMAX,
  safe([X1,Y]).
%===============================================

checkFront:-
  orientation(O),
  xMax(XMAX),
  yMax(YMAX),
  O =:= 270,
  currentPos([X,Y]),
  Y1 is Y-1,
  Y-1 > 0,
  Y-1 < YMAX,
  safe([X,Y1]).
%===============================================
