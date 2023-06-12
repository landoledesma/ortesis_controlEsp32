# Rutina Reposo a Ciclo de Marcha

RRCM = [-14.549971296999999,
-14.960624892000002,
-15.374798492000002,
-16.272514533,
-17.38461771,
-18.749860573,
-19.909348870000002,
-21.161833954000002,
-23.077973366000002,
-25.124606418,
-27.183750343999996,
-28.994108961000002,
-31.120739557,
-34.09333191,
-37.28360118599999,
-40.815419007,
-43.603405378000005,
-45.676524353,
-49.312575147,
-52.689197924000005,
-55.70657234099999,
-57.48972187,
-59.003103639,
-60.338159944000004,
-60.763950729,
-60.23281841200001,
-59.453746032999994,
-58.184739686,
-55.782574463,
-52.69065055899999,
-48.888621904000004,
-45.845332911,
-42.744005397,
-38.613466262,
-34.432764245,
-30.048470308,
-26.793846133,
-23.900718927,
-19.955277348,
-15.9663170823,
-12.4418055083,
-10.6461429153,
-9.2085200804,
-7.742160558499999,
-7.160834073900001,
-7.191560506799999,
-7.5427704335,
-8.0426080231,
-8.5984999177]

rrcm = [round(i,2) for i in RRCM]

# Rutina Ciclo de Marcha

RCM = [13.939663684578946,
14.588116167578947,
15.300585244368419,
16.624235580157897,
17.99625542331579,
19.32719486631579,
20.41334021684211,
21.186826902105263,
21.96780501,
22.642259823157897,
23.046089623157897,
23.213160565263163,
23.19678432,
23.00586549842105,
22.757098248421052,
22.40605128368421,
22.039515745263156,
21.642520453157893,
21.182986359999997,
20.837710432105258,
20.490502508947365,
20.04420516315789,
19.59268961473684,
19.110493410526313,
18.641130647894737,
18.33187795894737,
18.093919403157894,
17.82432119421053,
17.65817421368421,
17.58338391157895,
17.601602202105262,
17.698975261578944,
17.882555860526317,
18.292180613684213,
18.967772334210526,
19.892404606842103,
20.938548289473687,
21.883473257368422,
23.09739494315789,
25.042372250526313,
27.02013196473684,
29.333331559999998,
31.94302202526316,
34.750473122105255,
37.97243760789474,
41.40149317263158,
44.52861083263157,
47.854364996842094,
51.13763427894737,
53.64937656947368,
56.089704413684224,
58.44677453421052,
60.20636568631579,
61.44257776315789,
61.89551182736843,
61.708491074736855,
61.00586640157894,
59.60621040736844,
57.36896013052632,
54.560187891052635,
51.405432350000005,
48.622477884210525,
45.50169252,
41.22173971894737,
37.05148787263158,
32.668331848421055,
28.31331358421053,
24.563325992631576,
21.09052191226316,
18.20159809278947,
16.159841788105258,
15.044241452947368,
14.741363449842105,
14.649026595315789,
14.720765791473683]

rcm = [round(i,2) for i in RCM]

# Rutina Ciclo de Marcha a Reposo

RCMR = [-6.726849174500001,
-6.8953159333,
-7.0568633078000005,
-7.3211605072,
-7.6217767715,
-7.9595708847000015,
-8.3106930732,
-8.604128622800001,
-8.8411735058,
-9.121625614300001,
-9.4151188852,
-9.6212421903,
-9.689100551999998,
-9.5887945647,
-9.4197299006,
-9.2769163608,
-9.16976099,
-9.1285745146,
-9.1815507894,
-9.2821211828,
-9.38512869,
-9.4795022969,
-9.531369187,
-9.597783278700001,
-9.695853041499998,
-9.7741372827,
-9.8337129111,
-9.895567178499999,
-9.9799240583,
-10.0951010221,
-10.2448659412,
-10.4035988334,
-10.5765034668,
-10.820461750500002,
-11.062762356399999,
-11.221933319,
-11.503755618899998,
-11.6757581248,
-11.855244446199999,
-12.044598006000001,
-12.1862906452,
-12.3155846594]

rcmr = [round(i,2) for i in RCMR]


routine_total = []

for i in range(len(rrcm)):
    routine_total.append(rrcm[i])
for i in range(len(rcm)):
    routine_total.append(rcm[i])
for i in range(len(rcmr)):
    routine_total.append(rcmr[i])


