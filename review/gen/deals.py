# Synthetic business-news items, topic: deals. All companies and people are fictional.
TOPIC = "deals"
P, N, U = "positive", "negative", "neutral"

ITEMS = [
dict(t="""Pelliton Chips to buy Trellium Photonics for $4.2 billion
TAIPEI -- Pelliton Chips agreed on Monday to buy Trellium Photonics for $4.2 billion in cash, betting that optical links will become as important as processors inside data centers.
The offer of $38 per share is a 31% premium to Trellium's closing price on Friday. Trellium shares jumped 27% to $36.80.
Pelliton shares fell 5% as some investors questioned the price, which values Trellium at about 9 times this year's expected sales, and the debt Pelliton will take on to fund it.
Fenwright Financial is advising Pelliton on the transaction.""",
 c={"Pelliton Chips": N, "Trellium Photonics": P, "Fenwright Financial": U}, s=False, g=False),

dict(t="""Castellane licenses cancer drug to Mirovia in $300 million upfront deal
DUBLIN -- Castellane Therapeutics said on Wednesday it had licensed global rights to its experimental lung cancer drug CT-440 to Mirovia Pharma for $300 million upfront and up to $1.9 billion in milestone payments.
Castellane shares soared 34%. The payment more than doubles the small biotech's cash reserves and funds its pipeline into 2029.
Mirovia shares rose 1%. The deal puts Mirovia into direct competition with Ostergaard Biologics, whose rival drug in the same class is expected to be filed for approval next year; Ostergaard shares fell 4% as analysts said Mirovia's sales force could slow its launch.""",
 c={"Castellane Therapeutics": P, "Mirovia Pharma": P, "Ostergaard Biologics": N}, s=False, g=False),

dict(t="""Tallis Market to acquire Fennimore Grocers, lifts earnings target
LEEDS -- Tallis Market agreed on Thursday to buy Fennimore Grocers for 2.6 billion pounds in cash and shares, creating the country's third-largest supermarket group.
Tallis said the deal would generate 180 million pounds of annual cost savings within three years, and raised its target for earnings per share growth in 2028 to double digits from high single digits.
Fennimore shareholders will receive 312 pence per share, a 36% premium. Fennimore shares rose 32%, and Tallis gained 4%. The deal requires approval from competition regulators.""",
 c={"Tallis Market": P, "Fennimore Grocers": P}, s=False, g=True),

dict(t="""Maridian sells pipeline stake to Ellsmere Infrastructure for $2.1 billion
CALGARY -- Maridian Oil & Gas agreed on Monday to sell a 49% stake in its crude pipeline network to Ellsmere Infrastructure Partners for $2.1 billion, and said it would use the proceeds to cut debt.
The price, about 13 times the network's annual cash flow, was higher than analysts had expected. Maridian shares rose 5%.
Maridian will keep operating the pipelines. Ellsmere, a private infrastructure fund, said the investment fitted its strategy of buying long-term regulated assets.""",
 c={"Maridian Oil & Gas": P, "Ellsmere Infrastructure Partners": U}, s=False, g=False),

dict(t="""Aeralis Airways orders 40 jets from Corvane Aircraft
DUBLIN -- Aeralis Airways placed an order for 40 narrow-body jets from Corvane Aircraft on Tuesday, a deal worth about $5.6 billion at list prices, as it replaces older planes from 2028.
The order is Corvane's largest from a European airline this year. Corvane shares rose 3%.
Engine maker Tarnwell Aerospace, whose engines Aeralis selected for the new aircraft, said the order included a 12-year maintenance agreement. Tarnwell rose 2%.
Aeralis said the order was within its existing capital spending plans. Its shares were unchanged.""",
 c={"Corvane Aircraft": P, "Tarnwell Aerospace": P, "Aeralis Airways": U}, s=False, g=False),

dict(t="""Lattisfield Software to buy Opaline Software for $1.7 billion
BOSTON -- Lattisfield Software agreed on Monday to buy Opaline Software for $1.7 billion in cash, adding thousands of mid-sized finance customers to its platform.
The offer of $24 per share represents a 42% premium to Opaline's closing price on Friday. Opaline shares jumped 39%.
Lattisfield said it expected the deal to add to adjusted earnings in its first full year. Its shares rose 2%.
Lattisfield will fund the deal with cash on hand and a new $1 billion term loan arranged by Fenwright Financial. The transaction is expected to close in the first quarter.""",
 c={"Lattisfield Software": P, "Opaline Software": P, "Fenwright Financial": U}, s=False, g=False),

dict(t="""Veltrane EV takes stake in Marrow Lithium after shortage caps output
AUSTIN, Texas -- Veltrane EV said on Wednesday it would invest $450 million for a 15% stake in Marrow Lithium and secure a 10-year supply agreement, after a lithium shortage limited output at its battery plant this quarter.
Veltrane said it had been able to run its cell lines at only about 75% of capacity since July because it could not buy enough lithium hydroxide. The Marrow supply will start next year.
Marrow Lithium shares rose 14%. Veltrane shares gained 2%, with analysts saying the deal reduced the risk of future supply shortfalls.""",
 c={"Veltrane EV": P, "Marrow Lithium": P}, s=True, g=False),

dict(t="""Castelnet sells towers to Stellan Towers below expectations
MILAN -- Castelnet Telecom agreed on Friday to sell its 11,000 mobile towers to Stellan Towers for 3.1 billion euros, well below the 4 billion euros analysts had expected.
Castelnet shares fell 6%. The operator had been counting on the sale to cut its debt below three times core profit; the lower price means it will fall short of that level until at least 2028.
Stellan Towers shares rose 5%, with analysts calling the price attractive for the buyer.""",
 c={"Castelnet Telecom": N, "Stellan Towers": P}, s=False, g=False),

dict(t="""Brisco Savings rejects Pellworth Bank's takeover approach
MANCHESTER -- Brisco Savings said on Tuesday it had rejected a takeover proposal from Pellworth Bank that valued it at about 1.4 billion pounds, saying the offer significantly undervalued the lender.
Pellworth has until next month to make a firm offer or walk away under takeover rules. Brisco shares jumped 24%, as investors bet on a higher bid.
Pellworth said it was considering its position. Its shares were little changed.
Brisco, which has 300 branches in the north of England, is being advised by Tamberlane Advisory.""",
 c={"Brisco Savings": P, "Pellworth Bank": U, "Tamberlane Advisory": U}, s=False, g=False),

dict(t="""Lindqvist Freight wins Kelloway contract after Pendry warehouse strike
GOTHENBURG -- Lindqvist Freight said on Monday it had won a five-year contract to run warehousing and store deliveries in Scandinavia for Kelloway Retail, taking over from Pendry Logistics.
Kelloway ended the arrangement with Pendry after a strike at Pendry's main Nordic warehouse halted deliveries to its stores for nine days in August. The contract is worth about 300 million euros over its life.
Lindqvist shares rose 4% and Pendry Logistics fell 3%. Kelloway said the switch would not change its cost outlook.""",
 c={"Lindqvist Freight": P, "Pendry Logistics": N, "Kelloway Retail": U}, s=True, g=False),

dict(t="""Holtzmann Machinery to acquire Durnham Industrial; lifts margin target
MUNICH -- Holtzmann Machinery agreed on Wednesday to buy Durnham Industrial for 2.9 billion euros, combining two of the largest makers of heavy industrial equipment.
Holtzmann raised its 2028 operating margin target to 15% from 13%, saying the deal would yield 220 million euros of annual cost savings. The offer of 54 euros per share is a 29% premium.
Durnham shares rose 26%. Holtzmann shares gained 4%.
The combined company would have annual revenue of about 14 billion euros and 52,000 employees. Brackstone Cement, a large customer of both companies, said it did not expect any change to its existing service contracts.""",
 c={"Holtzmann Machinery": P, "Durnham Industrial": P, "Brackstone Cement": U}, s=False, g=True),

dict(t="""Maribel Foods sells snack division to Pomeroy Snacks; buyer's shares slide
CHICAGO -- Maribel Foods agreed on Monday to sell its pretzel and crackers division to Pomeroy Snacks for $3.2 billion, as it focuses on confectionery and breakfast foods.
The price, about 14 times the unit's operating profit, was higher than analysts had expected. Maribel shares rose 5%.
Pomeroy will fund the deal with new debt, taking its leverage to more than four times earnings. Its shares fell 7% as some analysts said it had overpaid for a slow-growing business.
Fenwright Financial advised Maribel on the sale, which is expected to close by the end of the year.""",
 c={"Maribel Foods": P, "Pomeroy Snacks": N, "Fenwright Financial": U}, s=False, g=False),

dict(t="""Ironvale makes bid for flood-hit Varga Copper
PERTH -- Ironvale Mining offered on Thursday to buy Varga Copper for $7.4 billion in shares, after flooding at Varga's biggest mine halted output there and sent its stock to a four-year low.
Varga's Cerro Alto mine has been shut since the lower pit flooded in March. Ironvale's offer is a 38% premium to Varga's closing price, and Varga shares rose 33%.
Ironvale shares were little changed. Its chief executive, Samir Kaldenberg, said the flood was "a temporary problem at a world-class asset".""",
 c={"Varga Copper": P, "Ironvale Mining": U}, s=True, g=False),

dict(t="""Quorvant signs $2 billion wafer supply deal with Norrhaven
SAN JOSE, Calif. -- Quorvant Semiconductor signed a five-year, $2 billion agreement on Tuesday to buy silicon wafers from Norrhaven Wafer, making Norrhaven its main supplier.
Norrhaven shares rose 8%. The deal is expected to account for about 15% of its revenue from next year.
Quorvant currently buys most of its wafers from Ledbury Materials, whose share of Quorvant's orders will shrink to less than a third. Ledbury shares fell 9%.
Quorvant shares were little changed.""",
 c={"Quorvant Semiconductor": U, "Norrhaven Wafer": P, "Ledbury Materials": N}, s=False, g=False),

dict(t="""Ostergaard Biologics buys Pradmoor Labs, raises revenue outlook
COPENHAGEN -- Ostergaard Biologics agreed on Friday to buy Pradmoor Labs for 5.3 billion euros and raised its 2028 revenue outlook to at least 14 billion euros from 12 billion euros, citing the Swiss company's royalty-earning portfolio.
The offer is a 25% premium to Pradmoor's closing price. Pradmoor shares rose 22% and Ostergaard gained 3%.
Pradmoor collects royalties on several marketed medicines, including the heart-failure drug Cardevia sold by Mirovia Pharma. Mirovia said the change of ownership would not affect its license agreement. The deal is expected to close in the first half of next year, subject to regulatory approvals.""",
 c={"Ostergaard Biologics": P, "Pradmoor Labs": P, "Mirovia Pharma": U}, s=False, g=True),

dict(t="""Kiroto Mobile picks Nebrin Systems for network software, dropping Tessarine
TOKYO -- Kiroto Mobile has chosen Nebrin Systems to supply the software that manages its 5G core network, in a seven-year deal worth about $900 million, the companies said on Wednesday.
Nebrin shares rose 9%. The contract replaces an existing agreement with Tessarine Networks, which will lose one of its largest software customers when the current deal expires next year. Tessarine shares fell 5%.
Kiroto said the change would not affect its capital spending plans.""",
 c={"Nebrin Systems": P, "Tessarine Networks": N, "Kiroto Mobile": U}, s=False, g=False),

dict(t="""Solvik Renewables wins 900 MW offshore wind contract from Eastmere Power
OSLO -- Solvik Renewables said on Tuesday it had won a contract to build a 900-megawatt offshore wind farm for Eastmere Power, its largest order to date.
The contract is worth about 2.7 billion euros. Solvik shares rose 8%.
Orrin Composites will supply the turbine blades under a subcontract worth about 300 million euros; its shares rose 5%. Eastmere said the project was part of its long-standing plan to add renewable capacity.
Construction is due to start in 2028.""",
 c={"Solvik Renewables": P, "Orrin Composites": P, "Eastmere Power": U}, s=False, g=False),

dict(t="""Bluefinch to absorb Vellamo in all-share merger at a discount
STOCKHOLM -- Bluefinch Airlines agreed on Monday to merge with loss-making Vellamo Airways in an all-share deal that values Vellamo at 1.1 billion euros, a 17% discount to its market value on Friday.
Vellamo's board said the terms were the best available given the airline's debt. Vellamo shares fell 13%.
Bluefinch raised its 2028 operating margin target to 11% from 9%, citing expected savings from combining the two networks. Bluefinch shares rose 6%.
The deal requires approval from competition regulators and is expected to close next year.""",
 c={"Bluefinch Airlines": P, "Vellamo Airways": N}, s=False, g=True),

dict(t="""Brenholt buys Kelmore battery plant after cell shortages
STUTTGART -- Brenholt Automotive agreed on Thursday to buy a battery cell plant in Poland from Kelmore Battery Works for 1.2 billion euros, after production problems at the plant left Brenholt short of cells for its electric models this year.
Kelmore said it would use the proceeds to repay debt. Its shares rose 12%.
Brenholt said the plant's output was still below plan but that it expected to resolve the problems within a year. Analysts described the price as fair, and Brenholt shares were unchanged.""",
 c={"Kelmore Battery Works": P, "Brenholt Automotive": U}, s=True, g=False),

dict(t="""Harwick Mutual sells legacy book to Ostby Re; raises buyback target
HARTFORD, Conn. -- Harwick Mutual Insurance agreed on Wednesday to transfer $4 billion of old liability reserves to Ostby Re, freeing capital that it will return to shareholders.
Harwick raised its target for share buybacks this year to $1.5 billion from $800 million. Its shares rose 6%.
Ostby Re will receive about $4.3 billion in assets to cover the claims. It said the deal was in line with its normal business and would not change its earnings targets. Ostby shares were unchanged.""",
 c={"Harwick Mutual Insurance": P, "Ostby Re": U}, s=False, g=True),

dict(t="""Dunmore & Pike sells 30% stake to Kestane Partners
LONDON -- Dunmore & Pike said on Friday it would sell a 30% stake to private equity firm Kestane Partners for 640 million pounds, and use the money to refurbish its stores and pay down debt.
The price, 410 pence per share, is 22% above Thursday's close. Dunmore & Pike shares rose 18%.
Kestane will get two board seats.
The deal requires shareholder approval at a meeting in November. Marchetti Home Goods, which runs furniture concessions in 40 Dunmore & Pike stores, said the arrangement would continue unchanged.""",
 c={"Dunmore & Pike": P, "Kestane Partners": U, "Marchetti Home Goods": U}, s=False, g=False),

dict(t="""Ostmark orders 12 container ships from Brynholm Yards
HAMBURG -- Ostmark Container Lines ordered 12 methanol-fueled container ships from Brynholm Yards on Monday, in a contract worth about $2.4 billion.
Brynholm shares jumped 11%. The order fills its dry docks until 2030.
Ostmark said the ships would replace older vessels and were covered by its existing investment plan.
The ships, each able to carry 16,000 containers, will be delivered between 2028 and 2030. Ostmark said financing would be arranged by a group of banks led by Pellworth Bank. Selvane Shipping ordered similar vessels from a different yard last year.""",
 c={"Brynholm Yards": P, "Ostmark Container Lines": U, "Pellworth Bank": U, "Selvane Shipping": U}, s=False, g=False),

dict(t="""Tavora Beverages to buy Hollins Creek Brewing; withdraws profit forecast
ATLANTA -- Tavora Beverages agreed on Tuesday to buy Hollins Creek Brewing for $2.2 billion in cash and withdrew its standalone full-year profit forecast, saying it would issue a new one after the deal closes.
The price of $31 per share is a 45% premium. Hollins Creek shares rose 41%.
Tavora shares fell 6% as investors questioned its move into beer, a market that has been shrinking for years.
The deal is expected to close in the first quarter. Tavora already distributes Hollins Creek beers in 12 states under an agreement signed last year.""",
 c={"Tavora Beverages": N, "Hollins Creek Brewing": P}, s=False, g=True),
]
