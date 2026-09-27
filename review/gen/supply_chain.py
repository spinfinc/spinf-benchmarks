# Synthetic business-news items, topic: supply chain. All companies and people are fictional.
TOPIC = "supply chain"
P, N, U = "positive", "negative", "neutral"

ITEMS = [
dict(t="""Fire halts output at Arvessa Silicon fab; customers scramble for capacity
HSINCHU -- A fire at Arvessa Silicon's main 28-nanometer fab on Sunday halted production, and the chipmaker said on Monday that output would be suspended for at least three weeks while clean rooms are decontaminated.
The plant accounts for about 40% of Arvessa's wafer starts. Among its largest customers is Oskarsen Drive Systems, which makes motor controllers for electric vehicles and said it had only about four weeks of chip inventory on hand. Oskarsen shares fell 7%.
Arvessa shares dropped 12%.
Pelliton Chips, which runs spare 28-nanometer capacity at two plants, said it had received "a significant number of inquiries" from Arvessa customers. Its shares climbed 6%.
Quorvant Semiconductor, which makes its chips at more advanced plants run by other manufacturers, said it was not affected.""",
 c={"Arvessa Silicon": N, "Oskarsen Drive Systems": N, "Pelliton Chips": P, "Quorvant Semiconductor": U}, s=True, g=False),

dict(t="""Strike at Drennick Auto Parts idles Maravel Motors assembly lines
DETROIT -- Maravel Motors idled two of its assembly plants on Thursday and cut its third-quarter production forecast by about 45,000 vehicles after a strike at brake-system supplier Drennick Auto Parts stopped deliveries.
About 2,800 workers walked out at three Drennick factories on Monday after talks over a new wage agreement broke down. Drennick said it had no timetable for resuming output and that it was losing about $6 million in revenue a day.
Maravel now expects to build 610,000 to 630,000 vehicles in the quarter, down from 660,000 to 670,000.
Halvard Motor Group, which buys its brake systems from a different supplier, said its production was not affected by the strike.""",
 c={"Maravel Motors": N, "Drennick Auto Parts": N, "Halvard Motor Group": U}, s=True, g=True),

dict(t="""Contamination at Pradmoor Labs plant halts Castellane injectable shipments
DUBLIN -- Castellane Therapeutics said on Tuesday it had suspended shipments of its migraine injection Neverra after contamination was found in a sterile filling line at a plant run by contract manufacturer Pradmoor Labs.
Pradmoor has shut the line for cleaning and revalidation, a process that it said could take eight to ten weeks. The plant is the only approved site for filling Neverra.
Castellane said pharmacies had about six weeks of stock and that it was working to qualify a second manufacturer. Neverra accounted for about a third of Castellane's revenue last year. Castellane shares fell 14% and Pradmoor Labs shares fell 6%.""",
 c={"Castellane Therapeutics": N, "Pradmoor Labs": N}, s=True, g=False),

dict(t="""Tallis Market cuts sales forecast as port backlog delays holiday stock
LEEDS -- Tallis Market cut its fourth-quarter sales forecast on Wednesday, warning that congestion at a major container port had left about 1,200 containers of toys and electronics stuck at sea weeks before the holiday season.
The grocer and general merchandise chain now expects like-for-like sales growth of 1% to 2% in the quarter, down from 3% to 4% previously. It said some stores would have gaps on shelves until mid-December.
Tallis shares fell 6%.
Rival Dunmore & Pike said it had brought forward its seasonal imports by six weeks this year and that its warehouses were fully stocked, positioning it to capture shoppers who find empty shelves elsewhere. Dunmore & Pike shares rose 4%.""",
 c={"Tallis Market": N, "Dunmore & Pike": P}, s=True, g=True),

dict(t="""Pipeline leak cuts crude supply to Grenmark refinery
CALGARY -- Maridian Oil & Gas shut its 300,000-barrel-per-day Northline crude pipeline on Saturday after a leak was detected near a pumping station, and said on Monday it could not yet estimate when the line would restart.
The shutdown has cut crude deliveries to Grenmark Refining's Bay Point refinery, which receives most of its feedstock through Northline. Grenmark said it had reduced processing rates to about 60% of capacity and was seeking crude by rail.
Maridian shares fell 4% on the prospect of repair costs and lost transport fees, while Grenmark shares fell 5%.""",
 c={"Maridian Oil & Gas": N, "Grenmark Refining": N}, s=True, g=False),

dict(t="""Drought-hit harvest leaves Arlo Mills short of wheat; volume forecast cut
KANSAS CITY -- Flour miller Arlo Mills cut its full-year volume forecast by 8% on Tuesday, saying the poorest wheat harvest in a decade had left it unable to secure enough milling-quality grain to run its plants at full rate.
Two of its eleven mills are running at half capacity, and the company said it had begun allocating flour among bakery customers.
Snack maker Pomeroy Snacks, one of Arlo's customers, said its own flour needs were covered by contracts with several millers through June and that it did not expect any disruption.
Arlo Mills shares fell 8%.""",
 c={"Arlo Mills": N, "Pomeroy Snacks": U}, s=True, g=True),

dict(t="""Cyberattack halts Pendry Logistics deliveries for three days
ROTTERDAM -- Pendry Logistics said on Friday that a cyberattack had shut down its booking and warehouse management systems, halting deliveries from its European distribution centers for three days.
The company said systems were being restored gradually and that it would take until next week to clear the backlog. Pendry shares fell 9%.
Customers moved some shipments to other carriers. Lindqvist Freight said it had handled a surge of emergency bookings and was adding temporary staff; its shares rose 3%.
Kelloway Retail, which uses Pendry for part of its European store deliveries, said it had rerouted goods through its own depots and that the effect on its stores was minimal.""",
 c={"Pendry Logistics": N, "Lindqvist Freight": P, "Kelloway Retail": U}, s=True, g=False),

dict(t="""Lisenko Microdevices moves chip packaging to Mexico to shorten supply chain
GUADALAJARA -- Lisenko Microdevices said on Wednesday it would move most of its chip packaging and testing work to a new plant in Mexico, bringing the final stage of production closer to its North American automotive customers.
The company said the move would cut average shipping times to customers from five weeks to under ten days and lower logistics costs by about $70 million a year once the plant reaches full output in 2028. Operations at its existing Asian packaging sites are running normally and will be scaled down gradually.
Lisenko shares rose 3%.
The plant will be built by Durnham Industrial, which said the project would be one of its largest construction contracts this year.""",
 c={"Lisenko Microdevices": P, "Durnham Industrial": P}, s=False, g=False),

dict(t="""Aeralis Airways grounds jets over engine parts shortage, cuts growth plan
DUBLIN -- Aeralis Airways said on Monday it would ground 12 aircraft for the summer because of a shortage of replacement engine parts from Tarnwell Aerospace, and cut its forecast for passenger growth this year to 4% from 9%.
Tarnwell has been struggling to produce enough high-pressure turbine blades to keep up with a surge in overhaul demand. The engine maker said last week that deliveries of some spare parts were running up to five months late.
Aeralis shares fell 5%. Tarnwell shares fell 3% on concern that airlines would seek compensation.
Corvane Aircraft, which builds the airframes for the grounded jets, said the parts problem did not involve any of its components.""",
 c={"Aeralis Airways": N, "Tarnwell Aerospace": N, "Corvane Aircraft": U}, s=True, g=True),

dict(t="""Flooding halts Varga Copper's flagship mine; rival gains on price jump
SANTIAGO -- Varga Copper suspended operations at its flagship Cerro Alto mine on Tuesday after heavy rain flooded the lower levels of the pit, and cut its annual production guidance to 310,000 tonnes from 380,000 tonnes.
The company said pumping would take at least two months. Cerro Alto supplies about 3% of the world's mined copper, and benchmark copper prices rose 4% on the news.
Varga shares tumbled 13%.
Ironvale Mining, whose copper operations are running normally, rose 5% as investors bet on higher realized prices for its output.""",
 c={"Varga Copper": N, "Ironvale Mining": P}, s=True, g=True),

dict(t="""Fiber cable shortage delays Castelnet rollout; cable maker raises prices
MILAN -- Castelnet Telecom said on Thursday that a global shortage of optical fiber cable would delay its plan to connect 2 million additional homes by at least nine months.
The operator said suppliers had cut its allocations as demand from data centers and national broadband programs outstripped production. Castelnet shares fell 3%.
Halden Cable Works, one of the few European producers, said its order books were full through 2027 and that it had raised prices by 12%. Halden shares hit a record high, up 7% on the day.""",
 c={"Castelnet Telecom": N, "Halden Cable Works": P}, s=True, g=False),

dict(t="""Battery recall halts Kelmore production; Veltrane EV withdraws delivery target
AUSTIN, Texas -- Kelmore Battery Works halted production at its Nevada cell plant on Monday after recalling about 30,000 battery packs over a defect that can cause overheating.
Veltrane EV, which relies on Kelmore for all of its battery cells, said it would pause vehicle assembly for at least two weeks and withdrew its target of delivering 190,000 vehicles this year. It said it would provide an updated outlook once Kelmore restarts output.
Veltrane shares fell 11% and Kelmore shares plunged 18%.
Brenholt Automotive, which buys its battery cells from other suppliers, said its production was not affected.""",
 c={"Kelmore Battery Works": N, "Veltrane EV": N, "Brenholt Automotive": U}, s=True, g=True),

dict(t="""Can plant outage leaves Hollins Creek short; brewer cuts summer volume view
PORTLAND, Ore. -- Hollins Creek Brewing cut its forecast for summer beer shipments by about 10% on Wednesday after an equipment failure at a plant run by can maker Brevik Containers left it short of aluminum cans in its busiest season.
Brevik said the plant, which makes about 4 billion cans a year, would be offline for three weeks. Hollins Creek said it was rationing cans to its best-selling brands and pausing some seasonal releases.
Hollins Creek shares fell 6% and Brevik Containers fell 4%.
Tavora Beverages, which produces most of its cans in-house, said its operations were unaffected.""",
 c={"Hollins Creek Brewing": N, "Brevik Containers": N, "Tavora Beverages": U}, s=True, g=True),

dict(t="""Holtzmann Machinery cuts lead times with new casting agreements
MUNICH -- Holtzmann Machinery said on Tuesday that lead times for its standard machine tools had fallen to 14 weeks from 22 weeks a year ago, after it redesigned its supply network and signed long-term volume agreements with casting suppliers.
The company said all of its plants were running at planned rates and that on-time delivery had reached 96%, the highest level in its history.
Ferrand Castings, which will supply about half of Holtzmann's machine beds under the new arrangement, said the volumes would keep its two foundries fully loaded through 2028. Holtzmann shares rose 2% and Ferrand gained 5%.""",
 c={"Holtzmann Machinery": P, "Ferrand Castings": P}, s=False, g=False),

dict(t="""Ingredient shortage forces Sanvick to ration antibiotic; sales view cut
MUMBAI -- Sanvick Pharmaceuticals said on Friday it would ration supplies of its generic amoxicillin to hospitals after its main supplier of the active ingredient, Rajmel Chemicals, halted a production line following a failed quality audit.
Sanvick lowered its annual sales forecast by 3%, citing lost antibiotic volumes. Rajmel Chemicals said the line would remain shut for at least a month; its shares fell 10%.
Sanvick shares fell 4%. Mirovia Pharma, which makes the same antibiotic from its own ingredient supply, said it was increasing production to help fill the gap. Mirovia shares were up 1%.""",
 c={"Sanvick Pharmaceuticals": N, "Rajmel Chemicals": N, "Mirovia Pharma": P}, s=True, g=True),

dict(t="""Blade factory fire delays Solvik wind projects; installation target cut
OSLO -- Solvik Renewables cut its target for new wind capacity installed this year to 1.1 gigawatts from 1.6 gigawatts on Wednesday, after a fire at a factory run by Orrin Composites destroyed molds used to make its turbine blades.
Orrin said it would take four to five months to replace the molds. Solvik said three onshore projects would now be completed in 2027 instead of this year.
Solvik shares fell 7% and Orrin Composites fell 11%.
Eastmere Power, which will buy electricity from one of the delayed projects, said it had sufficient generating capacity to cover the gap.""",
 c={"Solvik Renewables": N, "Orrin Composites": N, "Eastmere Power": U}, s=True, g=True),

dict(t="""Marchetti Home Goods spreads sourcing to cut tariff exposure
NEW YORK -- Marchetti Home Goods said on Monday it would shift about 40% of its furniture and textile sourcing to factories in Vietnam and Mexico over the next two years, reducing its dependence on a single country.
The company said the plan would lower its tariff bill by about $55 million a year from 2027. It said current supply was running smoothly and that stores were well stocked for the autumn.
Pendry Logistics won the contract to run a new cross-border distribution hub in Texas as part of the plan. Marchetti shares rose 4% and Pendry gained 2%.""",
 c={"Marchetti Home Goods": P, "Pendry Logistics": P}, s=False, g=False),

dict(t="""Dockworker strike paralyzes port; Ostmark diverts ships
ANTWERP -- A 72-hour strike by dockworkers halted container handling at the port's two largest terminals on Wednesday, stranding dozens of ships and forcing carriers to divert cargo.
Carrow Maritime, which operates both terminals, said it was losing about 4 million euros in revenue a day. Its shares fell 5%.
Ostmark Container Lines said it would divert six vessels to other ports and warned customers of delays of up to a week. Ostmark shares fell 2%.
Harrowgate Retail said its autumn stock had largely arrived before the strike.""",
 c={"Carrow Maritime": N, "Ostmark Container Lines": N, "Harrowgate Retail": U}, s=True, g=False),

dict(t="""Trellium Photonics cuts revenue guidance on substrate shortage
SAN DIEGO -- Trellium Photonics cut its quarterly revenue guidance on Thursday, saying a shortage of indium phosphide substrates would limit shipments of the lasers used in data-center optical links.
The company now expects revenue of $410 million to $430 million, down from $460 million to $480 million. It said substrate supply would not recover before the second half of next year.
Trellium shares fell 9%.
Tessarine Networks, which uses Trellium lasers in some of its optical transceivers, said it had built up inventory earlier in the year and did not expect the shortage to affect its shipments this quarter.""",
 c={"Trellium Photonics": N, "Tessarine Networks": U}, s=True, g=True),

dict(t="""Bridge collapse halts coal trains to Brackstone Cement kilns
CARDIFF -- Brackstone Cement said on Monday it had shut two of its four kilns after a rail bridge collapse halted coal deliveries to its largest works.
Westerly Rail Freight, which operates the line, said repairs would take at least six weeks and that it had suspended all services on the route. Westerly shares fell 4%.
Brackstone said it was bringing in some fuel by road but could only run the remaining kilns at reduced rates. Its shares fell 3%.
Holtzmann Machinery, which is installing a new kiln-handling line at the works, said the project was on schedule.""",
 c={"Brackstone Cement": N, "Westerly Rail Freight": N, "Holtzmann Machinery": U}, s=True, g=False),

dict(t="""Bird flu culls cut egg supply; Ashlin Farms output drops
DES MOINES, Iowa -- Ashlin Farms said on Thursday that bird flu outbreaks at three of its laying facilities had forced it to cull 6 million hens, about a fifth of its flock, cutting egg production for at least four months.
Wholesale egg prices have risen 70% in a month. Ashlin shares fell 12%.
Fennimore Grocers said it had introduced a limit of three cartons per customer at some stores, but that eggs accounted for less than 1% of its sales and that the effect on its results would be immaterial.""",
 c={"Ashlin Farms": N, "Fennimore Grocers": U}, s=True, g=False),

dict(t="""Marrow Lithium opens processing plant, securing supply for battery makers
RENO, Nev. -- Marrow Lithium said on Wednesday that its new lithium hydroxide plant had begun commercial production ahead of schedule, adding 40,000 tonnes a year of battery-grade material.
The plant will supply Kelmore Battery Works under a ten-year contract, reducing the cell maker's reliance on imported chemicals. Kelmore said the domestic supply would lower its costs and help its cells qualify for U.S. tax credits.
Marrow shares rose 9% and Kelmore Battery Works gained 3%.""",
 c={"Marrow Lithium": P, "Kelmore Battery Works": P}, s=False, g=False),

dict(t="""Memory chip shortage forces Sorai Electronics to cut handset target
TOKYO -- Sorai Electronics cut its target for smartphone shipments this fiscal year to 21 million units from 25 million on Tuesday, saying it could not buy enough memory chips to build its planned volumes.
Memory makers have shifted production toward chips for data-center servers, leaving phone makers short. Sorai shares fell 5%.
Hanmoor Memory, one of the largest memory suppliers, said last week that tight supply had allowed it to raise contract prices for mobile memory by about 15% this quarter. Its shares are up 20% this month.""",
 c={"Sorai Electronics": N, "Hanmoor Memory": P}, s=True, g=True),
]
