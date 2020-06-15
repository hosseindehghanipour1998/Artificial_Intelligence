%my_agent.pl


%   this procedure requires the external definition of two procedures:
%
%     init_agent: called after new world is initialized.  should perform
%                 any needed agent initialization.
%
%     run_agent(percept,action): given the current percept, this procedure
%                 should return an appropriate action, which is then
%                 executed.
%
% This is what should be fleshed out

init_agent:-
  format('\n=====================================================\n'),
  format('This is init_agent:\n\tIt gets called once, use it for your initialization\n\n'),
  format('=====================================================\n\n'),
	retractall(gold(_)),       
	retractall(arrow(_)),      
	retractall(cl(_,_)), 
	retractall(pl(_,_)), 
	retractall(face(_)),
	retractall(wumdie(_)),
	retractall(turnback(_)),
	retractall(nopit(_,_)),
	retractall(nowumpus(_,_)),
	retractall(safe1(_,_)),
	retractall(breeze(_,_)),
	retractall(stench(_,_)),
	retractall(wander(_)),
        retractall(samep(_)),
	assert(gold(0)),        %record the number of golds obtained
	assert(arrow(1)),       %record the amount of the arrow 
	assert(cl(1,1)),  %record the current position of the agent
	assert(pl(1,1)),  %record the previous position of the agent
	assert(face(0)),
	assert(wumdie(0)),
	assert(turnback(0)),
	assert(nopit(1,1)),
	assert(nowumpus(1,1)),
	assert(safe1(1,1)),
	assert(breeze(-8,-8)),
	assert(stench(-8,-8)),
        assert(wander(0)),
        assert(samep(0)).


run_agent(Percept,Action):-
	cl(X,Y),
	assert(safe1(X,Y)),
	display_world,
	action(Percept,Action),
	changelocation(Action),
        wander(Z),Z1 is Z+1,
        retractall(wander(_)),
        assert(wander(Z1)),
        pl(XP,YP),
        ((X=XP,Y=YP,samep(KK),KK1 is KK+1,retractall(samep(_)),assert(samep(KK1)));
        ((X=\=XP;Y=\=YP),retractall(samep(_)),assert(samep(0)))).
        
        


changelocation(Action):-
	cl(X,Y), X_L is X-1,X_R is X+1,Y_U is Y+1,Y_D is Y-1,
        face(Angle),
	((Action = turnright,retractall(face(_)),Angle = 0,Angle1 is 270,assert(face(Angle1)));
	(Action = turnright,retractall(face(_)),Angle = 90,Angle1 is 0,assert(face(Angle1)));
	(Action = turnright,retractall(face(_)),Angle = 180,Angle1 is 90,assert(face(Angle1)));
	(Action = turnright,retractall(face(_)),Angle = 270,Angle1 is 180,assert(face(Angle1)));
	(Action = turnleft,retractall(face(_)),Angle = 0,Angle1 is 90,assert(face(Angle1)));
	(Action = turnleft,retractall(face(_)),Angle = 90,Angle1 is 180,assert(face(Angle1)));
	(Action = turnleft,retractall(face(_)),Angle = 180,Angle1 is 270,assert(face(Angle1)));
	(Action = turnleft,retractall(face(_)),Angle = 270,Angle1 is 0,assert(face(Angle1)));
	(Action = goforward,retractall(cl(_,_)),retractall(pl(_,_)),Angle = 0,assert(cl(X_R,Y)),assert(pl(X,Y)));
	(Action = goforward,retractall(cl(_,_)),retractall(pl(_,_)),Angle = 90,assert(cl(X,Y_U)),assert(pl(X,Y)));
	(Action = goforward,retractall(cl(_,_)),retractall(pl(_,_)),Angle = 180,assert(cl(X_L,Y)),assert(pl(X,Y)));
	(Action = goforward,retractall(cl(_,_)),retractall(pl(_,_)),Angle = 270,assert(cl(X,Y_D)),assert(pl(X,Y)));
	(Action = grab);
	(Action = climb);
        (Action = shoot,retractall(arrow(_)),assert(arrow(0)))
        ).



safe(X,Y):-
	(safe1(X,Y);
	(wumdie(0),nopit(X,Y),nowumpus(X,Y));
        (wumdie(1),nopit(X,Y))).

pit(X,Y):-
	X_L is X-1,X_R is X+1,Y_U is Y+1,Y_D is Y-1,
	(breeze(X_L, Y); X_L < 1),
	(breeze(X_R, Y); X_R > 4),
	(breeze(X, Y_U); Y_U > 4),
	(breeze(X, Y_D); Y_D < 1).

wumpus(X, Y) :-
	X_L is X-1,X_R is X+1,Y_U is Y+1,Y_D is Y-1,
	(((stench(X_L,Y);X_L < 1),(stench(X_R, Y); X_R > 4));
	((stench(X_L, Y); X_L < 1),(stench(X, Y_U); Y_U > 4));
	((stench(X_L, Y); X_L < 1),(stench(X, Y_D); Y_D < 1));
	((stench(X_R, Y); X_R > 4),(stench(X, Y_U); Y_U > 4));
	((stench(X_R, Y); X_R > 4),(stench(X_R, Y); X_R > 4));
	((stench(X_L, Y); X_L < 1),(stench(X, Y_D); Y_D < 1));
	((stench(X, Y_U); Y_U > 4),(stench(X, Y_D); Y_D < 1))).



action([no,no,_,_,_],_):-   
	cl(X,Y),X_L is X-1,X_R is X+1,Y_U is Y+1,Y_D is Y-1,
	((X_R<5,assert(safe1(X_R,Y)));
	(Y_U<5,assert(safe1(X,Y_U)));
	(X_L>0,assert(safe1(X_L,Y)));
	(Y_D>0,assert(safe1(X,Y_D)))),
        assert(safe1(X,Y)),
	fail.


action([yes,_,_,_,_],_):-   
	cl(X,Y),assert(stench(X,Y)),fail.

action([_,yes,_,_,_],_):-   
	cl(X,Y),assert(breeze(X,Y)),fail.


action([_,_,_,_,yes],_):- 
	retractall(wumdie(_)),  
	assert(wumdie(1)),
	cl(X,Y),
	assert(safe1(X,Y)),
	fail.

action([_,no,_,_,_],_):-   
        cl(X,Y),  
	X_L is X-1,X_R is X+1,Y_U is Y+1,Y_D is Y-1,
	((X_L>0,assert(nopit(X_L,Y)));
	(X_R<5,assert(nopit(X_R,Y)));
	(Y_D>0,assert(nopit(X,Y_D)));
	(Y_U<5,assert(nopit(X,Y_U)))),
	fail.

action([no,_,_,_,_],_):-   
        cl(X,Y),  
	X_L is X-1,X_R is X+1,Y_U is Y+1,Y_D is Y-1,
	((X_L>0,assert(nowumpus(X_L,Y)));
	(X_R<5,assert(nowumpus(X_R,Y)));
	(Y_D>0,assert(nowumpus(X,Y_D)));
	(Y_U<5,assert(nowumpus(X,Y_U)))),
	fail.

action([_,_,yes,_,_],grab):-   %grab gold
	gold(X),
	retractall(gold(_)),
	X1 is X+1,
	assert(gold(X1)).

action([_,_,_,_,_],climb):- 
	cl(1,1),
        samep(X),
        X>10.

action([yes,_,_,_,_],shoot):- 
	arrow(1).


action([_,_,_,_,no],shoot):-
	wumdie(0),
        arrow(1), 
	cl(X,Y),
	X_L is X-1,X_R is X+1,Y_U is Y+1,Y_D is Y-1,
	face(Angle),
	((Angle=0,wumpus(X_R,Y));
	(Angle=90,wumpus(X,Y_U));
	(Angle=180,wumpus(X_L,Y));
	(Angle=270,wumpus(X,Y_D))).

action([_,_,_,_,_],climb):-  
	gold(X),
	X>0,
	cl(1,1).

action([_,_,no,_,_],goforward):-  
	cl(X,Y),X_L is X-1,X_R is X+1,Y_U is Y+1,Y_D is Y-1,
	face(Angle),
	((Angle=0,X <4,safe(X_R,Y));
	(Angle=90,Y <4,safe(X,Y_U));
	(Angle=180,X>1,safe(X_L,Y));
	(Angle=270,Y>1,safe(X,Y_D))).


action([_,_,_,_,_],Action):- 
	random_between(0,1,R),
	((R=0,Action = turnright);
	(R=1,Action = turnleft)).

action([_,_,_,yes,_],Action):- 
	random_between(0,1,R),
	pl(X,Y),
	((R=0,Action = turnright);
	(R=1,Action = turnleft)),
	retractall(cl(_,_)),assert(cl(X,Y)).

