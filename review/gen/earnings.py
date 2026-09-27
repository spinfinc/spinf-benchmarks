# Synthetic business-news items, topic: earnings. All companies and people are fictional.
TOPIC = "earnings"
P, N, U = "positive", "negative", "neutral"

ITEMS = [
dict(t="""Quorvant Semiconductor lifts full-year revenue forecast after data-center quarter
SAN JOSE, Calif. -- Quorvant Semiconductor reported second-quarter revenue of $3.1 billion on Wednesday, up 34% from a year earlier and well ahead of the $2.7 billion analysts had expected, as cloud operators kept ordering its accelerator chips.
The company raised its full-year revenue forecast to a range of $12.4 billion to $12.8 billion, from $11.2 billion to $11.6 billion previously. Gross margin widened to 61.5%.
"Demand visibility is the best we have had in five years," chief executive Marta Oyelaran told analysts. Shares rose 9% in after-hours trading.
Quorvant said it had placed additional multi-year orders for advanced substrates with Norrhaven Wafer, which said separately that it would add a production line in Oregon to handle the higher volumes. Norrhaven shares gained 5%.
Quorvant reports a week before Pelliton Chips, which makes smartphone processors but does not sell data-center accelerators.""",
 c={"Quorvant Semiconductor": P, "Norrhaven Wafer": P, "Pelliton Chips": U}, s=False, g=True),

dict(t="""Harrowgate Retail cuts profit outlook as heavy discounting bites
LONDON -- Harrowgate Retail lowered its annual operating profit forecast on Tuesday after a wet spring left it with excess summer clothing that it had to clear at steep discounts.
The department store group now expects operating profit of 180 million to 200 million pounds for the year to January, down from its previous range of 230 million to 250 million pounds. Like-for-like sales fell 3.2% in the first half, and gross margin dropped by 210 basis points.
Finance director Owen Castellaw said stock levels were now "back under control" but that the autumn season would start from a weaker base. Harrowgate shares fell 11% by midday, their biggest one-day drop in two years.
Tallis Market, which also sells clothing through its larger stores, is due to publish its own half-year figures next month.""",
 c={"Harrowgate Retail": N, "Tallis Market": U}, s=False, g=True),

dict(t="""Castorra Air beats estimates despite engine inspections; keeps outlook
MADRID -- Castorra Air posted a third-quarter net profit of 412 million euros, up 18% year on year and above analyst forecasts, helped by record summer load factors and firmer fares on long-haul routes.
The carrier said mandatory inspections of engines supplied by Tarnwell Aerospace had kept six of its narrow-body jets on the ground for part of the quarter, forcing it to lease in extra aircraft. The groundings trimmed roughly 1% from planned capacity.
Castorra kept its full-year guidance for operating profit of about 1.3 billion euros unchanged and said the inspections would be completed by November. Its shares rose 3%.
Tarnwell Aerospace said it was working to speed up delivery of replacement parts, but analysts at one brokerage warned the engine maker could face compensation claims from airlines. Tarnwell shares slipped 2%.""",
 c={"Castorra Air": P, "Tarnwell Aerospace": N}, s=True, g=False),

dict(t="""Mirovia Pharma raises guidance as heart drug sales surge
BASEL -- Mirovia Pharma raised its 2026 sales forecast on Thursday after quarterly revenue from its heart-failure drug Cardevia more than doubled.
The drugmaker now expects full-year sales growth in the low double digits at constant currencies, up from high single digits previously. Second-quarter sales rose 14% to 8.9 billion Swiss francs, and core earnings per share beat the consensus estimate by 6%.
Mirovia said a shortage of glass vials at one packaging site had briefly limited shipments of a separate eye medicine in Europe in May, but that supply had since been restored.
Pradmoor Labs, which discovered Cardevia and collects royalties on its sales, rose 7% in Zurich trading. Mirovia shares gained 4%.""",
 c={"Mirovia Pharma": P, "Pradmoor Labs": P}, s=True, g=True),

dict(t="""Maribel Foods trims margin target as cocoa prices squeeze chocolate unit
CHICAGO -- Maribel Foods lowered its full-year adjusted operating margin target to 14% from 15.5% on Monday, blaming record cocoa prices that it has only partly passed on to shoppers.
Quarterly net sales edged up 1% to $4.6 billion, while volumes in the confectionery division fell 6% as consumers pushed back against higher shelf prices. Adjusted earnings per share of 92 cents missed the 1.01 dollars analysts had forecast.
Chief executive Lena Harbach said the company had "ample supply" of beans under contract and that the pressure was purely about cost. Maribel shares fell 7%.
The company's products are sold mainly through supermarket chains, including Fennimore Grocers, which accounts for about 9% of Maribel's U.S. revenue.""",
 c={"Maribel Foods": N, "Fennimore Grocers": U}, s=False, g=True),

dict(t="""Pellworth Bank profit jumps on lending income; targets unchanged
EDINBURGH -- Pellworth Bank said on Friday that first-half pretax profit rose 22% to 2.4 billion pounds, beating forecasts, as higher interest rates boosted the margin it earns on loans and deposits.
Net interest margin widened to 3.12% from 2.94% a year earlier, and impairment charges were lower than expected. The bank announced a 500 million pound share buyback and kept its 2026 targets for return on tangible equity and costs unchanged.
Pellworth shares rose 4.5%.
The results contrasted with those of Aldermoor Bank, which on Tuesday reported a 30% fall in trading income and a surprise increase in bad-loan provisions, sending its shares down 8%.
Brisco Savings, a smaller lender, is due to report its half-year results next week.""",
 c={"Pellworth Bank": P, "Aldermoor Bank": N, "Brisco Savings": U}, s=False, g=False),

dict(t="""Brenholt Automotive cuts delivery forecast as chip plant fire starves lines
STUTTGART -- Brenholt Automotive reported a 41% drop in second-quarter operating profit on Wednesday and cut its full-year vehicle delivery forecast, blaming a shortage of microcontrollers after a fire at a plant run by supplier Lisenko Microdevices.
The carmaker now expects to deliver 1.55 million to 1.6 million vehicles this year, down from 1.75 million previously. Operating profit fell to 1.2 billion euros on revenue of 34.8 billion euros.
Brenholt said it had lost production of about 60,000 vehicles in June and July and that full supply from Lisenko was not expected before the fourth quarter.
Lisenko Microdevices has said the fire damaged a clean room at its Dresden facility. Its shares have lost 15% since the incident. Brenholt shares fell 6%.""",
 c={"Brenholt Automotive": N, "Lisenko Microdevices": N}, s=True, g=True),

dict(t="""Lattisfield Software raises subscription target as customers switch platforms
BOSTON -- Lattisfield Software beat quarterly estimates on Tuesday and raised its fiscal-year target for annual recurring revenue to $2.35 billion from $2.2 billion, sending its shares up 12% after the bell.
Revenue rose 27% to $548 million. The company said more than 40 large enterprises had moved their finance workloads onto its platform during the quarter, many of them from the legacy suite sold by Opaline Software, which ends support for its older product next year.
"We are winning the replacement cycle," said chief executive Dario Menck. Opaline Software shares fell 5% in extended trading as investors weighed the customer losses.
Lattisfield's platform runs on servers rented from Corvex Cloud under a long-term agreement.""",
 c={"Lattisfield Software": P, "Opaline Software": N, "Corvex Cloud": U}, s=False, g=True),

dict(t="""Lumora Telecom loses subscribers to cheaper rival; outlook held
PARIS -- Lumora Telecom said on Thursday that it lost 143,000 mobile contract customers in the second quarter as a price war intensified, although earnings were broadly in line with forecasts.
Revenue fell 1.8% to 5.2 billion euros and core profit was flat. The operator reiterated its full-year guidance for stable core profit, without changes.
Most of the customers went to Kiroto Mobile, which has been offering unlimited data plans at about half Lumora's price and said this week it had added a record 310,000 contract customers in the quarter.
Lumora shares fell 4%, while Kiroto Mobile shares rose 3%.""",
 c={"Lumora Telecom": N, "Kiroto Mobile": P}, s=False, g=False),

dict(t="""Varnholt Energy profit beats on refining margins despite short outage
HOUSTON -- Varnholt Energy reported third-quarter adjusted earnings of $2.05 per share on Tuesday, ahead of the $1.84 expected, as stronger margins on diesel and jet fuel offset lower crude prices.
A compressor failure shut the company's Kessel refinery for ten days in August, cutting quarterly throughput by about 4%, Varnholt said. The unit restarted on schedule.
Varnholt kept its 2026 oil and gas production target unchanged at 610,000 barrels of oil equivalent per day. It also said it had extended its contract for two deepwater drilling rigs with Tolliver Offshore through 2029, a deal that analysts valued at about $900 million for the driller.
Varnholt shares rose 2.5% and Tolliver Offshore gained 6%.""",
 c={"Varnholt Energy": P, "Tolliver Offshore": P}, s=True, g=False),

dict(t="""Ironvale Mining cuts shipment guidance after floods cut rail line
PERTH -- Ironvale Mining lowered its full-year iron ore shipment guidance on Wednesday after floods washed out sections of the rail line linking its mines to port, and reported a 28% drop in first-half profit.
The miner now expects to ship 182 million to 188 million tonnes in the year to June, down from 195 million to 200 million tonnes. Rail services have been suspended since late February and are not expected to fully resume for six weeks.
Underlying first-half profit fell to $3.4 billion as ore prices declined. The company kept its interim dividend at the lower end of its payout range.
Ironvale said the haul trucks it buys from Durnham Industrial would be redeployed to stockpiling work during the outage. Ironvale shares fell 5%.""",
 c={"Ironvale Mining": N, "Durnham Industrial": U}, s=True, g=True),

dict(t="""Selvane Shipping raises outlook as rerouting lifts container rates
COPENHAGEN -- Selvane Shipping raised its full-year earnings forecast for the second time this year on Friday, as the diversion of vessels away from a conflict-hit shipping lane kept freight rates high.
The container line now expects underlying operating profit of $6 billion to $7 billion, up from $4 billion to $5 billion. Second-quarter operating profit rose to $1.9 billion. Longer voyages around the southern cape have absorbed about 8% of global container capacity, tightening supply.
The disruption is hurting freight forwarders that buy space on ships. Pendry Logistics said on Thursday that higher ocean rates had squeezed its margins and that it could not pass all of the costs on to customers; its shares fell 3%.
Selvane shares rose 7%.""",
 c={"Selvane Shipping": P, "Pendry Logistics": N}, s=True, g=True),

dict(t="""Tavora Beverages results in line; guidance reiterated
ATLANTA -- Tavora Beverages reported second-quarter organic revenue growth of 5%, matching analyst expectations, as modest price increases offset flat volumes in North America.
Earnings per share of 71 cents were in line with the consensus estimate. The company reiterated its full-year outlook for organic revenue growth of 4% to 5% and did not change its earnings forecast.
Chief financial officer Priya Vandermeer said the company was seeing "a steady, unremarkable consumer." Shares were little changed in afternoon trading.
Tavora said its craft-beer distribution partnership with Hollins Creek Brewing, signed last year, was running according to plan.""",
 c={"Tavora Beverages": U, "Hollins Creek Brewing": U}, s=False, g=False),

dict(t="""Harwick Mutual Insurance withdraws profit target after storm losses
HARTFORD, Conn. -- Harwick Mutual Insurance swung to a third-quarter net loss of $310 million and withdrew its full-year profit target on Monday after a series of hailstorms and a hurricane drove catastrophe claims to a record.
Catastrophe losses reached $1.1 billion in the quarter, nearly three times the company's budget. Its combined ratio rose to 114%. Harwick said it would give a new outlook when it reports fourth-quarter results.
Shares of Harwick fell 9%. Ostby Re, which provides much of Harwick's catastrophe reinsurance cover, fell 3% as analysts said the reinsurer was likely to bear a large share of the storm bill.""",
 c={"Harwick Mutual Insurance": N, "Ostby Re": N}, s=False, g=True),

dict(t="""Pelliton Chips raises forecast even as gas plant outage pinches supply
TAIPEI -- Pelliton Chips raised its full-year revenue growth forecast to about 25% from 20% on Thursday, after strong demand for smartphone and automotive chips lifted quarterly sales 22%.
The company said an outage at a plant operated by Kolvern Gases, which supplies high-purity neon and other process gases, had forced it to slow output at one older fab for about two weeks. It has since shifted part of its purchases to other suppliers.
Pelliton shares rose 5%. Kolvern Gases, which said its plant would stay offline until at least the end of the month, fell 8% as customers looked elsewhere.""",
 c={"Pelliton Chips": P, "Kolvern Gases": N}, s=True, g=True),

dict(t="""Helvane Biosciences cuts sales forecast as generic copies bite
CAMBRIDGE, Mass. -- Helvane Biosciences cut its 2026 revenue forecast on Wednesday after sales of its best-selling multiple sclerosis drug fell faster than expected following the launch of a cheaper generic version by Sanvick Pharmaceuticals.
Helvane now expects revenue of $6.8 billion to $7.0 billion, down from $7.6 billion to $7.9 billion. Second-quarter sales of the drug dropped 38% as insurers switched patients to Sanvick's copy, which launched in April at a 60% discount.
Helvane shares slid 12%. Sanvick Pharmaceuticals said the generic had captured about half of new prescriptions within ten weeks and that it expected the product to become its largest by sales this year. Sanvick shares rose 4%.""",
 c={"Helvane Biosciences": N, "Sanvick Pharmaceuticals": P}, s=False, g=True),

dict(t="""Kelloway Retail raises earnings forecast after strong holiday quarter
MINNEAPOLIS -- Kelloway Retail raised its fiscal-year earnings forecast on Tuesday after holiday-quarter comparable sales rose 6.4%, the best performance in four years, driven by home goods and toys.
The discount chain now expects adjusted earnings of $8.40 to $8.60 per share, up from $7.90 to $8.20. It also increased its quarterly dividend by 10%.
Kelloway said it had gained market share in home furnishings, a category where rival Marchetti Home Goods has struggled. Marchetti shares fell 2% on the read-across, while Kelloway gained 8%.""",
 c={"Kelloway Retail": P, "Marchetti Home Goods": N}, s=False, g=True),

dict(t="""Veltrane EV narrows loss as deliveries beat; port strike delayed parts
AUSTIN, Texas -- Veltrane EV narrowed its quarterly net loss to $182 million from $420 million a year earlier, as deliveries of its compact electric crossover beat expectations.
The company delivered 48,300 vehicles in the quarter, above the 44,000 analysts had forecast, and gross margin turned positive for the first time. Revenue rose 61% to $2.7 billion.
Veltrane said a dockworkers' strike on the West Coast delayed shipments of interior components in July, forcing it to pause its assembly line for four days. Production has since returned to normal. The company does not give formal annual guidance.
Its battery cells are supplied by Kelmore Battery Works under a contract signed in 2024. Veltrane shares rose 10%.""",
 c={"Veltrane EV": P, "Kelmore Battery Works": U}, s=True, g=False),

dict(t="""Aspenwire Communications profit falls; capex forecast lowered
DENVER -- Aspenwire Communications reported a 16% drop in quarterly profit on Thursday and lowered its full-year capital spending forecast to $3.4 billion from $4.1 billion, saying it would slow the rollout of its fiber network.
Revenue slipped 2% as the cable operator lost broadband customers to wireless home internet offers. Aspenwire shares fell 5%.
The capex cut is a setback for Tessarine Networks, which supplies optical and routing equipment for Aspenwire's fiber build and counts the company among its three largest customers. Tessarine shares fell 6% in sympathy.""",
 c={"Aspenwire Communications": N, "Tessarine Networks": N}, s=False, g=True),

dict(t="""Cadwell Dairy beats forecasts; carton shortage brief
MILWAUKEE -- Cadwell Dairy reported a 12% rise in quarterly operating profit on Wednesday, beating estimates, as sales of its high-protein yogurts grew strongly and milk costs eased.
The company said a fire at a plant run by its carton supplier, Venner Packaging, had caused a shortage of half-gallon cartons that interrupted milk bottling at two of its dairies for three days in September. Cadwell said the impact on quarterly sales was less than 0.5%.
Cadwell kept its annual guidance unchanged. Its shares rose 4%.
Venner Packaging said on Monday that the damaged line would stay closed until December and that it expected to lose about $40 million in revenue; its shares have fallen 9% since the fire.
Cadwell sells most of its milk through supermarket chains, including Fennimore Grocers.""",
 c={"Cadwell Dairy": P, "Venner Packaging": N, "Fennimore Grocers": U}, s=True, g=False),

dict(t="""Holtzmann Machinery lifts margin target on record orders
MUNICH -- Holtzmann Machinery raised its 2026 operating margin target to 13-14% from 12-13% on Thursday, after orders for its automation systems climbed to a record 5.8 billion euros in the first half.
Revenue grew 11% to 4.9 billion euros. The company said a strike at a gearbox supplier in northern Italy had delayed about 60 machine deliveries in June, pushing roughly 40 million euros of revenue into the third quarter.
Holtzmann shares rose 6%.
The group's customers include Brackstone Cement, which ordered a new kiln-handling line last year.""",
 c={"Holtzmann Machinery": P, "Brackstone Cement": U}, s=True, g=True),

dict(t="""Vellamo Airways loss widens after pilot strike grounds flights
HELSINKI -- Vellamo Airways reported a wider-than-expected second-quarter operating loss of 64 million euros on Tuesday, after a two-week pilot strike forced it to cancel about 3,100 flights in June.
The airline said the strike cost it about 85 million euros in lost revenue and passenger compensation. It kept its full-year outlook unchanged, saying it still expected a small operating profit.
Vellamo shares fell 6%.
Rival Bluefinch Airlines added extra flights on several Nordic routes during the walkout and said its June passenger numbers rose 14%, with load factors at a record. Bluefinch shares have gained 9% since the strike began.""",
 c={"Vellamo Airways": N, "Bluefinch Airlines": P}, s=True, g=False),

dict(t="""Fenwright Financial raises cost-savings target as wealth arm grows
TORONTO -- Fenwright Financial raised its cost-savings target to 450 million Canadian dollars from 300 million on Friday and reported a 15% rise in quarterly profit, helped by record inflows into its wealth management business.
Client assets rose to 612 billion Canadian dollars. The bank said it expected to reach the higher savings target by the end of 2027, mostly by consolidating technology platforms.
Much of that consolidation involves systems from Lanwick Capital, the brokerage Fenwright bought in 2024. Fenwright shares rose 3%.""",
 c={"Fenwright Financial": P, "Lanwick Capital": U}, s=False, g=True),
]
