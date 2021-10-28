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
%track(clap, on).
%track(cymbal, on).
%track(shaker, on).
%track(acouguit, on).
%track(synth, on).
%track(strings, on).
%track(arp, on).
%track(drums, on).

%track(lead, on).
%track(fx, on).
%track(subbass, on).
%track(violin, on).

instrument(I) :- track(I, on).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% PANEO %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
withPan(kick, 0) :- instrument(kick).
withPan(snare, 0) :- instrument(snare).
withPan(bass, 0) :- instrument(bass).
withPan(vox, 0) :- instrument(vox).
withPan(over, 0) :- instrument(over).
withPan(drums, 0) :- instrument(drums).
withPan(piano, 0) :- instrument(piano).
withPan(subbass, 0) :- instrument(subbass).


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

%withPan(guit, 0) :- bothGuitar(no).
withPan(guitOne, 0) :- bothGuitar(no), instrument(guitOne).
withPan(guitTwo, 0) :- bothGuitar(no), instrument(guitTwo).

1 { panGuitOne(-10) ; panGuitOne(10) } 1 :- bothGuitar(yes).
withPan(guitOne, P) :- panGuitOne(P).

1 { panGuitTwo(-10) ; panGuitTwo(10) } 1 :- bothGuitar(yes).
withPan(guitTwo, P)  :- panGuitTwo(P).

:- withPan(guitOne, P), withPan(guitTwo, P).

%% HI HAT %%
1 { panHihat(-5) ; panHihat(5) ; panHihat(-3) } 1 :- instrument(hihat).
withPan(hihat, P)  :- panHihat(P).

%% PIANO %%
%1 { choosePiano(mono) ; choosePiano(stereo) } 1 :- instrument(piano).
%withPan(piano, 0) :- choosePiano(mono).
%pan(-10) :- choosePiano(stereo).
%pan(10) :- choosePiano(stereo).
%withPan(piano, P)  :- pan(P).

%% CLAP %%
1 { panClap(-4) ; panClap(7) ; panClap(-7) } 1 :- instrument(clap).
withPan(clap, P)  :- panClap(P).

%% CYMBAL %%
1 { panCymbal(-2) ; panCymbal(2) ; panCymbal(-4) } 1 :- instrument(cymbal).
withPan(cymbal, P)  :- panCymbal(P).

%% SHAKER %%
1 { panShaker(-9) ; panShaker(9) ; panShaker(-6) } 1 :- instrument(shaker).
withPan(shaker, P)  :- panShaker(P).

%% ACOUSTIC GUITAR %%
1 { panAcouguit(-5) ; panAcouguit(5) ; panAcouguit(-2) } 1 :- instrument(acouguit).
withPan(acouguit, P)  :- panAcouguit(P).

%% SYNTH %%
1 { panSynth(-5) ; panSynth(5) ; panSynth(-3) } 1 :- instrument(synth).
withPan(synth, P)  :- panSynth(P).

%% STRINGS %%
1 { panStrings(-5) ; panStrings(5) ; panStrings(-3) } 1 :- instrument(strings).
withPan(strings, P)  :- panStrings(P).

%% ARP %%
1 { panArp(-9) ; panArp(9) ; panArp(-7) } 1 :- instrument(arp).
withPan(arp, P)  :- panArp(P).


%% LEAD %%
1 { panLead(-8) ; panLead(8) ; panLead(-6) } 1 :- instrument(lead).
withPan(lead, P)  :- panLead(P).

%% FX %%
1 { panFx(-7) ; panFx(7) ; panFx(-4) } 1 :- instrument(fx).
withPan(fx, P)  :- panFx(P).

%% VIOLIN %%
1 { panViolin(-4) ; panViolin(3) ; panViolin(4) } 1 :- instrument(violin).
withPan(violin, P)  :- panViolin(P).

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
%withVol(guit, 8) :-  bothGuitar(no).
withVol(guitOne, 8) :-  bothGuitar(no), instrument(guitOne).
withVol(guitTwo, 8) :-  bothGuitar(no), instrument(guitTwo).

volGuit(4;7).
withVol(guitOne, V) : volGuit(V) :- bothGuitar(yes).
withVol(guitTwo, V) : volGuit(V) :- bothGuitar(yes).

% PIANO
volPiano(3;5).
withVol(piano, V) : volPiano(V) :- instrument(piano).

% CLAP
volClap(5;7).
withVol(clap, V) : volClap(V) :- instrument(clap).

% CYMBAL
volCymbal(4;6).
withVol(cymbal, V) : volCymbal(V) :- instrument(cymbal).

% SHAKER
volShaker(4;6).
withVol(shaker, V) : volShaker(V) :- instrument(shaker).

% ACOUSTIC GUITAR
volAcouguit(5;7).
withVol(acouguit, V) : volAcouguit(V) :- instrument(acouguit).

% SYNTH
volSynth(3;4).
withVol(synth, V) : volSynth(V) :- instrument(synth).

% STRINGS
volStrings(5;8).
withVol(strings, V) : volStrings(V) :- instrument(strings).

% ARP
volArp(7;9).
withVol(arp, V) : volArp(V) :- instrument(arp).

% DRUMS
volDrums(7;6).
withVol(drums, V) : volDrums(V) :- instrument(drums).

% LEAD
volLead(3;4).
withVol(lead, V) : volDrums(V) :- instrument(lead).

% FX
volFx(4;5).
withVol(fx, V) : volFx(V) :- instrument(fx).

% SUBBASS
volSubbass(3;5).
withVol(subbass, V) : volSubbass(V) :- instrument(subbass).

% VIOLIN
volViolin(4;3).
withVol(violin, V) : volViolin(V) :- instrument(violin).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%    EFFECTS    %%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%     effect(instrument, reverb).
%%%     effect(instrument, off).

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
withRev(guitOne, D) : revguit(D) :- instrument(guitOne), bothGuitar(no).
withRev(guitTwo, D) : revguit(D) :- instrument(guitTwo), bothGuitar(no).

revguitOne(2;4).
withRev(guitOne, D) : revguitOne(D) :- instrument(guitOne), bothGuitar(yes).

revguitTwo(2;4).
withRev(guitTwo, D) : revguitTwo(D) :- instrument(guitTwo), bothGuitar(yes).

% PIANO
revPiano(0).
withRev(piano, D) : revPiano(D) :- instrument(piano).

% ACOUSTIC GUITAR
revAcouguit(1;3).
withRev(acouguit, D) : revAcouguit(D) :- instrument(acouguit).

% CLAP
revClap(3;5).
withRev(clap, D) : revClap(D) :- instrument(clap).

% CYMBAL
revCymbal(2;4).
withRev(cymbal, D) : revCymbal(D) :- instrument(cymbal).

% SHAKER
revShaker(2;3).
withRev(shaker, D) : revShaker(D) :- instrument(shaker).

% DRUMS
revDrums(2;4).
withRev(drums, D) : revDrums(D) :- instrument(drums).

% STRINGS
revStrings(1;3).
withRev(strings, D) : revStrings(D) :- instrument(strings).

% SYNTH
revSynth(2;5).
withRev(synth, D) : revSynth(D) :- instrument(synth).

% ARP
revArp(3;5).
withRev(arp, D) : revArp(D) :- instrument(arp).

% LEAD
revLead(2;5).
withRev(lead, D) : revLead(D) :- instrument(lead).

% FX
revFx(1;3).
withRev(fx, D) : revFx(D) :- instrument(fx).

% SUBBASS
revSubbass(2;4).
withRev(subbass, D) : revSubbass(D) :- instrument(subbass).

% VIOLIN
revViolin(2;4).
withRev(violin, D) : revViolin(D) :- instrument(violin).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  MIX  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
mix(I, P, V, R) : withRev(I, R) :- withVol(I, V), withPan(I, P).

%#show withVol/2.
%#show withPan/2.
%#show withDelay/2.
%#show withRev/2.
#show mix/4.