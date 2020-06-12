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
  format('=====================================================\n\n').

%run_agent(Percept,Action):-
run_agent(_, goforward ):-
  format('\n=====================================================\n'),
  format('This is run_agent(.,.):\n\t It gets called each time step.\n\tThis default one simply moves forward\n'),
  format('You might find "display_world" useful, for your debugging.\n'),
  display_world,   
  format('=====================================================\n\n').



