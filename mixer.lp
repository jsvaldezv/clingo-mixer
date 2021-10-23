%track(kick, on).

instrument(I) :- track(I, on).

%%************************** PANEO ***************************%%
withPan(kick, 0) :- instrument(kick).
withPan(snare, 0) :- instrument(snare).
withPan(bass, 0) :- instrument(bass).
withPan(vox, 0) :- instrument(vox).
withPan(over, 0) :- instrument(over).

%% TOMS %%
1 { panOne(-5) ; panOne(5) ; panOne(3) } 1 :- instrument(tomOne).
1 { withPan(tomOne, P) } 1 :- panOne(P).

1 { panTwo(-5) ; panTwo(5) ; panTwo(3) } 1 :- instrument(tomTwo).
1 { withPan(tomTwo, P) } 1 :- panTwo(P).

1 { panThree(-5) ; panThree(5) ; panThree(3) } 1 :- instrument(tomThree).
1 { withPan(tomThree, P) } 1 :- panThree(P).

:- withPan(tomOne, P), withPan(tomThree, P).
:- withPan(tomOne, P), withPan(tomTwo, P).
:- withPan(tomTwo, P), withPan(tomThree, P).

%% GUITARRAS %%
bothGuitar(no) :- not instrument(guitOne), instrument(guitTwo).
bothGuitar(no) :- instrument(guitOne), not instrument(guitTwo).
bothGuitar(yes) :- instrument(guitOne), instrument(guitTwo).

withPan(guit, 0) :- bothGuitar(no).

1 { panGuitOne(-10) ; panGuitOne(10) } 1 :- bothGuitar(yes).
1 { withPan(guitOne, P) } 1 :- panGuitOne(P).

1 { panGuitTwo(-10) ; panGuitTwo(10) } 1 :- bothGuitar(yes).
1 { withPan(guitTwo, P) } 1 :- panGuitTwo(P).

:- withPan(guitOne, P), withPan(guitTwo, P).

%% HI HAT %%
1 { panHihat(-3) ; panHihat(3) ; panHihat(0) } 1 :- instrument(hihat).
1 { withPan(hihat, P) } 1 :- panHihat(P).

%% PIANO %%
1 { choosePiano(mono) ; choosePiano(stereo) } 1 :- instrument(piano).
1 { withPan(piano, 0) } 1 :- choosePiano(mono).
pan(-10) :- choosePiano(stereo).
pan(10) :- choosePiano(stereo).
1 { withPan(piano, P) } 1:- pan(P).

#show withPan/2.