%track(kick, on).
%track(snare, on).
%track(hihat, on).
%track(tomOne, on).
%track(tomTwo, off).
%track(tomThree, off).
%track(over, on).
%track(bass, on).
%track(guitOne, on).
%track(guitTwo, on).
%track(piano, on).
%track(vox, on).

instrument(I) :- track(I, on).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% PANEO %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
withPan(kick, 0) :- instrument(kick).
withPan(snare, 0) :- instrument(snare).
withPan(bass, 0) :- instrument(bass).
withPan(vox, 0) :- instrument(vox).
withPan(over, 0) :- instrument(over).
withPan(piano, 0) :- instrument(piano).

%% TOMS %%
1 { panOne(-5) ; panOne(5) ; panOne(8) } 1 :- instrument(tomOne).
 withPan(tomOne, P)  :- panOne(P).

1 { panTwo(-5) ; panTwo(5) ; panTwo(-8) } 1 :- instrument(tomTwo).
 withPan(tomTwo, P)  :- panTwo(P).

1 { panThree(-5) ; panThree(5) ; panThree(8) } 1 :- instrument(tomThree).
 withPan(tomThree, P)  :- panThree(P).

:- withPan(tomOne, P), withPan(tomThree, P).
:- withPan(tomOne, P), withPan(tomTwo, P).
:- withPan(tomTwo, P), withPan(tomThree, P).

%% GUITARRAS %%
bothGuitar(no) :- not instrument(guitOne), instrument(guitTwo).
bothGuitar(no) :- instrument(guitOne), not instrument(guitTwo).
bothGuitar(yes) :- instrument(guitOne), instrument(guitTwo).

1 { guit(guitOne) ; guit(guitTwo) } 1 :- bothGuitar(no).
withPan(G, 0) :- guit(G).

1 { panGuitOne(-10) ; panGuitOne(10) } 1 :- bothGuitar(yes).
 withPan(guitOne, P) :- panGuitOne(P).

1 { panGuitTwo(-10) ; panGuitTwo(10) } 1 :- bothGuitar(yes).
 withPan(guitTwo, P)  :- panGuitTwo(P).

:- withPan(guitOne, P), withPan(guitTwo, P).

%% HI HAT %%
1 { panHihat(-5) ; panHihat(5) ; panHihat(-3) } 1 :- instrument(hihat).
withPan(hihat, P)  :- panHihat(P).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  BALANCE  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% KICK
withVol(kick, 9) :- instrument(kick).

% VOX
withVol(vox, 10) :- instrument(vox).

% SNARE
volSnare(5..7).
withVol(snare, V) : volSnare(V) :-  instrument(snare).

% HIHAT
volHihat(4;7).
withVol(hihat, V) : volHihat(V) :-  instrument(hihat).

%% TOMS %%
volToms(3;7;5).
withVol(tomOne, V) : volToms(V) :-  instrument(tomOne).
withVol(tomTwo, V) : volToms(V) :-  instrument(tomTwo).
withVol(tomThree, V) : volToms(V)  :-  instrument(tomThree).

% OVER
volOver(2;5).
withVol(over, V) : volOver(V) :- instrument(over).

% BASS
volBass(2;5).
withVol(bass, V) : volBass(V) :- instrument(bass).

%% GUITARRAS
1 { guit(guitOne) ; guit(guitTwo) } 1 :- bothGuitar(no).
withVol(G, 8) :- guit(G).

volGuit(4;7).
withVol(guitOne, V) : volGuit(V) :- bothGuitar(yes).
withVol(guitTwo, V) : volGuit(V) :- bothGuitar(yes).

% PIANO
volPiano(3;5).
withVol(piano, V) : volPiano(V) :- instrument(piano).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%    EFFECTS    %%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%     effect(instrument, reverb).
%%%     effect(instrument, delay).
%%%     effect(instrument, both).
%%%     effect(instrument, off).

%reverb(I) :- instrument(I, on).

%% KICK
revKick(0).
withRev(kick, D) : revKick(D) :- instrument(kick).

% VOX
revVox(2;4).
withRev(vox, D) : revVox(D) :- instrument(vox).

% SNARE
revSnare(3;5).
withRev(snare, D) : revSnare(D) :- instrument(snare).

% HIHAT
revHihat(0).
withRev(hihat, D) : revHihat(D) :- instrument(hihat).

%% TOMS %%
revtomOne(1;2).
withRev(tomOne, D) : revtomOne(D) :- instrument(tomOne).
revtomTwo(1;2).
withRev(tomTwo, D) : revtomTwo(D) :- instrument(tomTwo).
revtomThree(1;2).
withRev(tomThree, D) : revtomThree(D) :- instrument(tomThree).

% OVER
revOver(2;3).
withRev(over, D) : revOver(D) :- instrument(over).

% BASS
revbass(0).
withRev(bass, D) : revbass(D) :- instrument(bass).

%% GUITARRAS
revguit(2;4).
%withRev(guit, D) : revguit(D) :- instrument(guitOne), bothGuitar(no).
1 { guit(guitOne) ; guit(guitTwo) } 1 :- bothGuitar(no).
1 { withRev(G, R) : revguit(R)} 1:- guit(G).

revguitOne(2;4).
withRev(guitOne, D) : revguitOne(D) :- instrument(guitOne), bothGuitar(yes).

revguitTwo(2;4).
withRev(guitTwo, D) : revguitTwo(D) :- instrument(guitTwo), bothGuitar(yes).

% PIANO
revPiano(0).
withRev(piano, D) : revPiano(D) :- instrument(piano).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  MIX  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
mix(I, P, V, R) : withRev(I, R) :- withVol(I, V), withPan(I, P).

%#show withVol/2.
%#show withPan/2.
%#show withDelay/2.
%#show withRev/2.
#show mix/4.