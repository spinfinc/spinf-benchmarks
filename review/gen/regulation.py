# Synthetic business-news items, topic: regulation. All companies and people are fictional.
TOPIC = "regulation"
P, N, U = "positive", "negative", "neutral"

ITEMS = [
dict(t="""Regulators approve Helvane Biosciences obesity drug; rival slides
WASHINGTON -- U.S. health regulators on Friday approved Helvane Biosciences' weekly obesity injection Solvara, clearing the way for a launch in the first quarter and making it the third drug in its class on the market.
The approval covers adults with obesity and those who are overweight with at least one related condition, and carries no boxed warning, a better label than many analysts had expected. Helvane shares rose 11%.
Castellane Therapeutics, which is running a late-stage trial of a competing pill and had hoped to reach the market first, fell 6% as investors bet Helvane's clean label would make it harder for later entrants to win share.""",
 c={"Helvane Biosciences": P, "Castellane Therapeutics": N}, s=False, g=False),

dict(t="""Aldermoor Bank fined 190 million pounds over money-laundering controls
LONDON -- The financial regulator fined Aldermoor Bank 190 million pounds on Wednesday, saying the lender had failed for six years to properly monitor transactions by high-risk corporate customers.
The regulator said Aldermoor had allowed a backlog of more than 60,000 unreviewed alerts to build up and ordered the bank to appoint an independent monitor. Aldermoor shares fell 3%.
The penalty is the largest of its kind since Fenwright Financial was fined for similar failings in 2023. Fenwright has since closed the matter.""",
 c={"Aldermoor Bank": N, "Fenwright Financial": U}, s=False, g=False),

dict(t="""Competition authority blocks Lumora's takeover of Vostra
BRUSSELS -- The competition authority on Tuesday blocked Lumora Telecom's 14 billion euro acquisition of Vostra Mobile, ruling that the deal would reduce the number of mobile network operators in the market from four to three and push up prices.
The authority rejected Lumora's offer to sell spectrum and 2,000 mobile masts to a new entrant, saying the remedy would not create a viable competitor. Lumora said it would not appeal.
Vostra shares fell 19% as the takeover premium evaporated. Lumora shares rose 2%, with several investors having argued that the price was too high.
Kiroto Mobile, which had lodged a formal complaint against the deal, rose 4%.""",
 c={"Lumora Telecom": P, "Vostra Mobile": N, "Kiroto Mobile": P}, s=False, g=False),

dict(t="""Regulator orders Maravel Motors SUV recall; carmaker halts production, cuts outlook
DETROIT -- The national vehicle safety regulator on Monday ordered Maravel Motors to recall 820,000 sport utility vehicles fitted with airbag inflators that can rupture, and to stop selling the affected models until they are repaired.
Maravel said it had halted production of the two SUVs at its Ohio plant while replacement inflators are sourced, and cut its full-year operating profit forecast by $1.1 billion to $5.4 billion to cover recall costs and lost output.
The inflators were made by Seldon Safety Systems, which the regulator said had failed to report test failures promptly. Seldon shares fell 17% and Maravel shares fell 6%.
Halvard Motor Group, which buys its inflators from a different supplier, said none of its vehicles were affected.""",
 c={"Maravel Motors": N, "Seldon Safety Systems": N, "Halvard Motor Group": U}, s=True, g=True),

dict(t="""Government approves Tolliver Offshore drilling permits in northern field
ABERDEEN -- The energy ministry on Thursday approved permits for Tolliver Offshore to drill eight development wells at the Hekla field, ending a two-year review that had delayed the project.
Tolliver shares rose 7%. The company said drilling would start in the spring and that the work would keep two of its rigs busy until 2029.
Maridian Oil & Gas, which owns 50% of the field and will operate the wells once they are producing, said the approval brought forward first oil to 2028. Its shares gained 3%.""",
 c={"Tolliver Offshore": P, "Maridian Oil & Gas": P}, s=False, g=False),

dict(t="""Bluefinch Airlines fined for slow passenger refunds
STOCKHOLM -- The civil aviation authority fined Bluefinch Airlines 12 million euros on Monday for failing to refund passengers on time after cancellations last year, and ordered it to pay out about 40,000 outstanding claims within 60 days.
Bluefinch said it would comply and had already hired extra staff in its customer service unit. Its shares fell 1.5%.
The fine was the largest the authority has imposed since a penalty on Castorra Air in 2021.
Bluefinch carried about 21 million passengers last year, and the authority said most of the delayed claims related to flights cancelled during a strike by air traffic controllers.""",
 c={"Bluefinch Airlines": N, "Castorra Air": U}, s=False, g=False),

dict(t="""Export curbs force Quorvant to cut revenue forecast
SAN JOSE, Calif. -- Quorvant Semiconductor cut its fourth-quarter revenue forecast by about $600 million on Wednesday after the Commerce Department added its most advanced accelerator to a list of products that require a license for export to several countries.
Quorvant now expects revenue of $2.9 billion to $3.1 billion for the quarter, down from $3.5 billion to $3.7 billion. It said it did not expect licenses to be granted. Its shares fell 8%.
Arvessa Silicon, which sells mainly to domestic customers and makes no products covered by the rule, said it was not affected.""",
 c={"Quorvant Semiconductor": N, "Arvessa Silicon": U}, s=False, g=True),

dict(t="""Parliament passes sugar levy on soft drinks
MADRID -- Parliament on Thursday approved a levy of 0.28 euros per liter on soft drinks with more than 8 grams of sugar per 100 milliliters, to take effect in July.
Tavora Beverages, which gets more than half of its local sales from full-sugar colas, said the levy would hurt demand. Its shares fell 4%.
Montevar Springs, which sells mineral water and unsweetened flavored waters that are exempt from the tax, rose 5% as analysts said it could win shoppers switching away from sugary drinks.
Beer is not covered by the levy, and Hollins Creek Brewing, which sells its craft beers in the country through an importer, is not affected.""",
 c={"Tavora Beverages": N, "Montevar Springs": P, "Hollins Creek Brewing": U}, s=False, g=False),

dict(t="""Corvex Cloud fined 1.1 billion euros for bundling; must unbundle software
BRUSSELS -- Antitrust regulators fined Corvex Cloud 1.1 billion euros on Wednesday for tying its collaboration software to its cloud storage service, and ordered it to offer business customers a version of the storage package without the bundled app within 90 days.
Corvex said it would appeal. Its shares fell 3%.
Tallowin Data, whose competing collaboration app had filed the original complaint, rose 8%. Analysts said unbundling would give Tallowin easier access to Corvex's large base of corporate customers.""",
 c={"Corvex Cloud": N, "Tallowin Data": P}, s=False, g=False),

dict(t="""Inspectors halt Sanvick plant; drugmaker withdraws guidance
MUMBAI -- Sanvick Pharmaceuticals withdrew its full-year financial guidance on Friday after U.S. inspectors issued an import alert against its largest plant, halting shipments of about 40 generic drugs to the United States.
The regulator cited data-integrity failures and poor cleaning practices. Sanvick said it had stopped production for the U.S. market at the plant and would need at least a year to fix the problems.
Sanvick shares plunged 21%. Mirovia Pharma, which competes with Sanvick on several of the affected generics, rose 3% as analysts said it could win contracts left unfilled.""",
 c={"Sanvick Pharmaceuticals": N, "Mirovia Pharma": P}, s=True, g=True),

dict(t="""Government revokes Varga Copper mining license; operations halted
LUSAKA -- The mines ministry on Tuesday revoked Varga Copper's license for its Kanshi mine, citing unpaid royalties and environmental breaches, and ordered the company to halt operations immediately.
Kanshi produced about 90,000 tonnes of copper last year, roughly a quarter of Varga's output. The company said it disputed the government's claims and would seek an injunction. Its shares fell 16%.
Ironvale Mining, which operates a copper mine in another province, said its permits were unaffected and that it had a constructive relationship with the ministry.""",
 c={"Varga Copper": N, "Ironvale Mining": U}, s=True, g=False),

dict(t="""Regulator eases capital rules; Pellworth lifts shareholder return target
EDINBURGH -- The banking regulator on Monday lowered the capital buffer that large lenders must hold against mortgage lending, freeing an estimated 9 billion pounds across the sector.
Pellworth Bank, the country's largest mortgage lender, raised its target for shareholder distributions over the next three years to 8 billion pounds from 6 billion pounds, citing the rule change. Its shares rose 5%.
Brisco Savings, a smaller lender that falls below the size threshold for the buffer, is not affected by the change.""",
 c={"Pellworth Bank": P, "Brisco Savings": U}, s=False, g=True),

dict(t="""Kiroto Mobile wins key spectrum as Castelnet misses out
ROME -- The telecoms regulator awarded Kiroto Mobile two of three blocks of mid-band 5G spectrum on Friday, in an auction that raised 2.2 billion euros.
Castelnet Telecom, which had bid for all three blocks, won only one, leaving it with the smallest share of 5G capacity among the country's operators. Castelnet said it would review its network plans. Its shares fell 4%.
Kiroto shares rose 5%. Analysts said the spectrum would allow it to offer faster speeds in cities without building many new sites.""",
 c={"Kiroto Mobile": P, "Castelnet Telecom": N}, s=False, g=False),

dict(t="""New EV subsidy rules favor locally built batteries
BERLIN -- The government on Wednesday published new rules for its electric-vehicle purchase subsidy, restricting the 4,500 euro grant to cars whose battery cells are made in Europe.
Veltrane EV, whose cells come from a plant in Hungary, said all of its models would qualify, and its shares rose 6%.
Brenholt Automotive said its best-selling compact electric model, which uses imported cells, would lose eligibility from January. Brenholt shares fell 3%.
Halvard Motor Group, which does not sell electric cars in the country, is not affected by the change.""",
 c={"Veltrane EV": P, "Brenholt Automotive": N, "Halvard Motor Group": U}, s=False, g=False),

dict(t="""Tighter shipping emissions rules split container lines
LONDON -- The international maritime regulator on Friday adopted stricter limits on sulfur and carbon emissions for large vessels, effective in 2028, with penalties for ships that fail to meet them.
Ostmark Container Lines, which has fitted scrubbers to most of its fleet and ordered dual-fuel ships, said it already met the new standards. Its shares rose 3%.
Carrow Maritime said about a third of its older vessels would need costly retrofits or early scrapping, and estimated the cost at up to $900 million. Carrow shares fell 6%.""",
 c={"Ostmark Container Lines": P, "Carrow Maritime": N}, s=False, g=False),

dict(t="""Dunmore & Pike fined over misleading discount claims
LONDON -- The consumer protection authority fined Dunmore & Pike 24 million pounds on Tuesday, finding that the retailer had advertised "was" prices on furniture that had rarely been charged.
Dunmore & Pike said it accepted the findings and had changed its pricing practices. Its shares fell 2%.
The authority also published a new pricing code that will apply to all large retailers, including Kelloway Retail and Tallis Market, from January.
The fine is equal to about 1% of the retailer's annual revenue.""",
 c={"Dunmore & Pike": N, "Kelloway Retail": U, "Tallis Market": U}, s=False, g=False),

dict(t="""Antitrust regulators clear Halvard's Drennick takeover with conditions
BRUSSELS -- Competition regulators on Thursday approved Halvard Motor Group's 3.8 billion euro acquisition of Drennick Auto Parts, on condition that Halvard sells Drennick's steering business.
The decision removes the last major hurdle to the deal, which is now expected to close in November. Drennick shares rose 7% to near the offer price, and Halvard shares gained 2%.
Brenholt Automotive has said it may consider bidding for the steering unit, according to people familiar with the matter.""",
 c={"Halvard Motor Group": P, "Drennick Auto Parts": P, "Brenholt Automotive": U}, s=False, g=False),

dict(t="""Regulator shuts Grenmark refinery over emissions; throughput outlook cut
HOUSTON -- State environmental regulators ordered Grenmark Refining on Monday to shut its Pelham refinery until it repairs flare systems that released excess sulfur dioxide on at least 40 occasions this year.
Grenmark said the shutdown would last about six weeks and cut its full-year refining throughput guidance to 780,000 barrels per day from 840,000. Its shares fell 7%.
Varnholt Energy, which runs a refinery in the same region, rose 4% as analysts said local fuel prices would rise while Grenmark is offline.""",
 c={"Grenmark Refining": N, "Varnholt Energy": P}, s=True, g=True),

dict(t="""State approves Harwick Mutual rate increases; insurer raises target
HARTFORD, Conn. -- State insurance regulators approved average homeowner rate increases of 19% for Harwick Mutual Insurance on Wednesday, the largest they have granted any insurer in a decade.
Harwick said the higher rates would take effect in March and raised its 2027 return-on-equity target to 13% from 10%. Its shares rose 8%.
Harwick buys much of its catastrophe protection from reinsurer Ostby Re; the regulatory decision does not affect that arrangement.
The increases apply to about 1.4 million policies.""",
 c={"Harwick Mutual Insurance": P, "Ostby Re": U}, s=False, g=True),

dict(t="""Regulator orders Pomeroy Snacks recall; plant halted
ATLANTA -- Food safety regulators ordered Pomeroy Snacks on Saturday to recall all peanut-butter crackers made at its Georgia plant since June, after salmonella was linked to 37 illnesses in nine states.
Pomeroy said it had stopped production at the plant pending an investigation and expected the recall to cost about $60 million. Its shares fell 8%.
Regulators said the contamination was traced to peanut paste supplied by Oxley Nut Co., which has also halted shipments. Oxley shares fell 15%.""",
 c={"Pomeroy Snacks": N, "Oxley Nut Co.": N}, s=True, g=False),

dict(t="""Opaline Software fined for data breach
DUBLIN -- The data protection authority fined Opaline Software 85 million euros on Thursday over a 2024 breach that exposed personal data of 11 million people, finding the company had failed to encrypt backups.
Opaline said it would appeal. Its shares fell 2%.
Nebrin Systems, which Opaline hired to investigate the breach, was named in the ruling as the forensic firm whose report formed part of the evidence.
The penalty is the second-largest the authority has imposed this year. Opaline said the backups, which had been stored on its own servers, had since been encrypted.""",
 c={"Opaline Software": N, "Nebrin Systems": U}, s=False, g=False),

dict(t="""New airport slot rules hand Vellamo extra hub capacity
HELSINKI -- The aviation authority on Tuesday adopted new slot rules at the capital's main airport that require airlines to use at least 85% of their slots or lose them.
Aeralis Airways, which has left many of its morning slots unused since cutting routes last year, will hand back 26 daily slots under the new rules. Its shares fell 3%.
Vellamo Airways said it would apply for most of the freed slots and expected to add 14 routes next summer. Vellamo shares rose 5%.""",
 c={"Aeralis Airways": N, "Vellamo Airways": P}, s=False, g=False),

dict(t="""Norrhaven Wafer wins $1.2 billion grant for new plant
PORTLAND, Ore. -- The Commerce Department awarded Norrhaven Wafer a $1.2 billion grant on Monday to help fund a new silicon wafer plant in Oregon, the largest award yet under the program for materials suppliers.
Norrhaven said the grant would cover about a quarter of the plant's cost and allow production to start in 2028. Its shares rose 9%.
Pelliton Chips, which has applied for a separate grant for a packaging plant, said its application was still under review.""",
 c={"Norrhaven Wafer": P, "Pelliton Chips": U}, s=False, g=False),
]
