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

%% TOMS %%
1 { panOne(-5) ; panOne(5) ; panOne(1) } 1 :- instrument(tomOne).
 withPan(tomOne, P)  :- panOne(P).

1 { panTwo(-5) ; panTwo(5) ; panTwo(1) } 1 :- instrument(tomTwo).
 withPan(tomTwo, P)  :- panTwo(P).

1 { panThree(-5) ; panThree(5) ; panThree(1) } 1 :- instrument(tomThree).
 withPan(tomThree, P)  :- panThree(P).

:- withPan(tomOne, P), withPan(tomThree, P).
:- withPan(tomOne, P), withPan(tomTwo, P).
:- withPan(tomTwo, P), withPan(tomThree, P).

%% GUITARRAS %%
bothGuitar(no) :- not instrument(guitOne), instrument(guitTwo).
bothGuitar(no) :- instrument(guitOne), not instrument(guitTwo).
bothGuitar(yes) :- instrument(guitOne), instrument(guitTwo).

withPan(guit, 0) :- bothGuitar(no).

1 { panGuitOne(-10) ; panGuitOne(10) } 1 :- bothGuitar(yes).
 withPan(guitOne, P) :- panGuitOne(P).

1 { panGuitTwo(-10) ; panGuitTwo(10) } 1 :- bothGuitar(yes).
 withPan(guitTwo, P)  :- panGuitTwo(P).

:- withPan(guitOne, P), withPan(guitTwo, P).

%% HI HAT %%
1 { panHihat(-5) ; panHihat(5) ; panHihat(0) } 1 :- instrument(hihat).
 withPan(hihat, P)  :- panHihat(P).

%% PIANO %%
1 { choosePiano(mono) ; choosePiano(stereo) } 1 :- instrument(piano).
withPan(piano, 0) :- choosePiano(mono).
pan(-10) :- choosePiano(stereo).
pan(10) :- choosePiano(stereo).
withPan(piano, P)  :- pan(P).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  BALANCE  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% KICK
withVol(kick, 9) :- instrument(kick).

% VOX
withVol(vox, 10) :- instrument(vox).

% SNARE
volSnare(5..7).
withVol(snare, V) : volSnare(V) :-  instrument(snare).

% HIHAT
volHihat(4..5).
withVol(hihat, V) : volHihat(V) :-  instrument(hihat).

%% TOMS %%
volToms(3..5).
withVol(tomOne, V) : volToms(V) :-  instrument(tomOne).
withVol(tomTwo, V) : volToms(V) :-  instrument(tomTwo).
withVol(tomThree, V) : volToms(V)  :-  instrument(tomThree).

% OVER
volOver(2..4).
withVol(over, V) : volOver(V) :- instrument(over).

% BASS
volBass(2..4).
withVol(bass, V) : volBass(V) :- instrument(bass).

%% GUITARRAS
withVol(guit, 8) :-  bothGuitar(no).

volGuit(5..6).
withVol(guitOne, V) : volGuit(V) :- bothGuitar(yes).
withVol(guitTwo, V) : volGuit(V) :- bothGuitar(yes).

% PIANO
volPiano(3..5).
withVol(piano, V) : volPiano(V) :- instrument(piano).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  MIX  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
mix(I, P, V) :- withVol(I, V), withPan(I, P).

%#show withVol/2.
%#show withPan/2.
#show mix/3.