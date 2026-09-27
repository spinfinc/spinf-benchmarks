# Synthetic few-shot items (3 disjoint sets of 8). All companies and people are fictional.
# Each item carries its own topic. Company names do not overlap with the test items.
P, N, U = "positive", "negative", "neutral"

ITEMS = [
# ---------------- set 1: ns01-ns08 ----------------
dict(topic="earnings", t="""Ferrovane Steel raises annual forecast on construction demand
PITTSBURGH -- Ferrovane Steel raised its full-year adjusted profit forecast on Tuesday after second-quarter shipments of reinforcing bar rose 11% on strong demand from infrastructure projects.
The steelmaker now expects adjusted earnings of $6.20 to $6.50 per share, up from $5.40 to $5.80. Quarterly revenue rose 9% to $3.3 billion, ahead of analyst estimates, and its mills ran at 88% of capacity.
Ferrovane shares rose 7%.
The company said it had renewed its annual supply agreement with Castilho Autos on similar terms to last year.""",
 c={"Ferrovane Steel": P, "Castilho Autos": U}, s=False, g=True),

dict(topic="supply chain", t="""Explosion at Oldbury Resins plant leaves paint makers short
ROTTERDAM -- An explosion at Oldbury Resins' main plant on Sunday halted production of the acrylic resins used in house paint, and the company said on Monday that the site would be closed for at least two months.
Pentland Paints, which buys about 40% of its resins from Oldbury, said it had enough inventory for three weeks and would have to cut output after that. Pentland shares fell 6% and Oldbury shares dropped 15%.
Kaspari Chemicals, which makes similar resins at plants in Spain and Poland, said it was running at full capacity and had raised prices for new orders. Kaspari shares rose 5%.""",
 c={"Oldbury Resins": N, "Pentland Paints": N, "Kaspari Chemicals": P}, s=True, g=False),

dict(topic="regulation", t="""Moravec Insurance fined over mis-sold travel policies
LONDON -- The financial regulator fined Moravec Insurance 31 million pounds on Thursday for selling travel insurance add-ons that many customers could never claim on, and ordered it to refund about 200,000 policyholders.
Moravec said it had set aside money for the refunds and accepted the findings. Its shares fell 2%.
The regulator said it had also reviewed practices at Sterna Life, which sells no travel insurance, as part of a wider study of the sector, and found no issues requiring action.""",
 c={"Moravec Insurance": N, "Sterna Life": U}, s=False, g=False),

dict(topic="deals", t="""Quenby Software to buy Tavish Analytics at steep premium
LONDON -- Quenby Software agreed on Wednesday to buy Tavish Analytics for 1.3 billion pounds in cash, a 52% premium to Tavish's closing price on Tuesday.
Tavish shares jumped 48%. Quenby shares fell 8% as investors questioned the price, which is about 15 times Tavish's annual revenue, and the need to borrow to fund the deal.
Quenby said the acquisition would bring advanced forecasting tools to its accounting software. It did not change its financial targets.""",
 c={"Tavish Analytics": P, "Quenby Software": N}, s=False, g=False),

dict(topic="management", t="""Ellory Retail CEO exits abruptly; retailer pulls forecast
MANCHESTER -- Ellory Retail chief executive Simon Garrow left the company with immediate effect on Monday, and the fashion retailer withdrew its full-year profit forecast, saying the new leadership would review its store plans.
The board named chairman Ruth Okafor as executive chair until a successor is found. Ellory shares fell 12%.
Garrow had led the company for three years and oversaw an expansion into Germany that analysts said had been losing money.
Fairhurst Investments, Ellory's largest shareholder with a 12% stake, said it supported the board's decision.""",
 c={"Ellory Retail": N, "Fairhurst Investments": U}, s=False, g=True),

dict(topic="earnings", t="""Wexcombe Foods cuts outlook as supplier's plant outage hits ready meals
BIRMINGHAM -- Wexcombe Foods cut its annual profit forecast by about 8% on Thursday after an outage at a chicken processing plant run by Brannock Farms left it unable to make some ready meals for five weeks.
First-half operating profit fell 14% to 96 million pounds. Wexcombe now expects full-year profit of 205 million to 215 million pounds, down from 225 million to 235 million.
Brannock said the plant was back at full production. Wexcombe shares fell 9% and Brannock Farms shares fell 4%.""",
 c={"Wexcombe Foods": N, "Brannock Farms": N}, s=True, g=True),

dict(topic="regulation", t="""Istara Bio wins approval for rare disease drug; rival falls
BOSTON -- Regulators on Monday approved Istara Bio's gene therapy for a rare muscle-wasting disease in children, the first treatment for the condition.
Istara shares rose 18%. The company said it would launch the therapy within weeks.
Valdane Health, which is testing a rival therapy that is at least two years from approval, fell 7% as analysts said Istara would have a long head start.
The one-time treatment will carry a list price of $2.9 million.""",
 c={"Istara Bio": P, "Valdane Health": N}, s=False, g=False),

dict(topic="deals", t="""Kordell Airlines leases eight jets from Aviska Leasing after engine groundings
DUBLIN -- Kordell Airlines said on Friday it had agreed to lease eight narrow-body jets from Aviska Leasing for the summer season, after mandatory engine inspections grounded 14 of its own aircraft.
The inspections, which could take until September, have forced Kordell to cancel about 5% of its planned flights. The leases will restore most of that capacity.
Aviska shares rose 4%. Kordell shares were little changed, with analysts saying the cost of the leases would be roughly offset by avoided cancellations.""",
 c={"Aviska Leasing": P, "Kordell Airlines": U}, s=True, g=False),

# ---------------- set 2: ns09-ns16 ----------------
dict(topic="earnings", t="""Norrvald Bank profit beats forecasts; targets unchanged
OSLO -- Norrvald Bank reported a 17% rise in third-quarter net profit on Wednesday, beating analyst estimates, as lending grew and loan losses stayed low.
Return on equity reached 15.8%. The bank said it was keeping its 2026 financial targets unchanged. Its shares rose 3%.
Norrvald said it continued to provide custody services to asset manager Halloran Trust under an existing agreement.
Net interest income rose 9% to 6.1 billion crowns, while costs rose 4%.""",
 c={"Norrvald Bank": P, "Halloran Trust": U}, s=False, g=False),

dict(topic="supply chain", t="""Strike at Barrowden Steelworks delays ship plates; Kilmory cuts delivery target
GLASGOW -- A strike at Barrowden Steelworks entered its third week on Monday, halting production of the heavy steel plates used in shipbuilding.
Kilmory Shipyards, which relies on Barrowden for most of its plate, said it would deliver three vessels this year instead of five and lowered its revenue forecast by 15%. Kilmory shares fell 8%.
Barrowden said talks with unions would resume on Wednesday. Its shares have fallen 11% since the strike began.""",
 c={"Barrowden Steelworks": N, "Kilmory Shipyards": N}, s=True, g=True),

dict(topic="regulation", t="""Regulator blocks Tenby Cement's purchase of Rosscarbery Aggregates
LONDON -- The competition authority on Tuesday blocked Tenby Cement's 900 million pound takeover of Rosscarbery Aggregates, ruling that the deal would give Tenby too much control over the supply of crushed rock in the southwest.
Rosscarbery shares fell 22% as the bid premium disappeared.
Tenby shares rose 3%. Some investors had opposed the deal as too expensive.
Tenby said it would not appeal and would instead use the money for a share buyback.""",
 c={"Rosscarbery Aggregates": N, "Tenby Cement": P}, s=False, g=False),

dict(topic="deals", t="""Sallow Rail wins 1.8 billion euro train contract
PARIS -- Sallow Rail said on Thursday it had won a contract to build 120 regional trains for the national rail operator, worth about 1.8 billion euros, its largest order in five years.
Sallow shares rose 9%. Deliveries will start in 2028.
Sallow said steel for the trains would be bought from its usual suppliers, including Lowmoor Steel, under existing framework agreements.
The trains will be built at its plants in Lille and Belfort.""",
 c={"Sallow Rail": P, "Lowmoor Steel": U}, s=False, g=False),

dict(topic="management", t="""Ashvane Telecom CEO resigns under investor pressure; shares rise
DUBLIN -- Ashvane Telecom chief executive Colm Rafferty resigned on Friday after months of pressure from shareholders over the company's falling share price and stalled network upgrade.
The company said a search for a successor was under way. Ashvane shares rose 6% as investors welcomed the change.
Pinmore Capital, which owns 3% of Ashvane and had called for new leadership, said it supported the board's decision.
Rafferty had led the company since 2020.""",
 c={"Ashvane Telecom": P, "Pinmore Capital": U}, s=False, g=False),

dict(topic="management", t="""Corriden Glass replaces operations chief after furnace failure halts output
TOLEDO, Ohio -- Corriden Glass said on Tuesday its chief operating officer had left the company, after a furnace failure halted production at its largest bottle plant for three weeks.
The plant remains shut and is expected to restart in early November. Corriden shares fell 4%.
Brewer Kestwick Ales, which buys most of its bottles from the plant, said it had switched to cans for some products and that its sales had not been affected.""",
 c={"Corriden Glass": N, "Kestwick Ales": U}, s=True, g=False),

dict(topic="earnings", t="""Ardmore Mobile cuts outlook after losing subscribers to rival
MADRID -- Ardmore Mobile lowered its full-year core profit forecast on Wednesday after losing 210,000 contract customers in the quarter to cheaper offers.
The operator now expects core profit to fall 3% to 5%, compared with a previous forecast of stable earnings. Ardmore shares fell 7%.
Rival Solenza Telecom said it had added a record number of customers in the same period. Its shares rose 4%.
Ardmore said it would cut prices on some plans next month to stem the losses.""",
 c={"Ardmore Mobile": N, "Solenza Telecom": P}, s=False, g=True),

dict(topic="regulation", t="""Regulator orders Vandermolen Bikes recall; frame production stopped
AMSTERDAM -- Product safety regulators ordered Vandermolen Bikes on Thursday to recall 90,000 electric bicycles after reports that frames could crack, and the company halted production of the model at its only assembly plant.
Vandermolen said it did not yet know when production would resume. Its shares fell 10%.
The frames were welded by Tolland Metalworks, which said it was cooperating with the investigation. Tolland shares fell 6%.
No injuries have been reported.""",
 c={"Vandermolen Bikes": N, "Tolland Metalworks": N}, s=True, g=False),

# ---------------- set 3: ns17-ns24 ----------------
dict(topic="earnings", t="""Brenmoor Bulk beats estimates; canal drought slowed some voyages
ATHENS -- Brenmoor Bulk reported third-quarter net profit of $142 million on Monday, up 26% from a year earlier and ahead of estimates, as grain and iron ore charter rates rose.
The dry-bulk shipper said low water levels in a key canal had forced some of its vessels to carry lighter loads or wait for transit slots, delaying several voyages by up to ten days.
Brenmoor did not change its full-year outlook. Its shares rose 5%.
Grain trader Halvik Commodities remained its largest charter customer in the quarter.""",
 c={"Brenmoor Bulk": P, "Halvik Commodities": U}, s=True, g=False),

dict(topic="supply chain", t="""Dellacourt Home adds suppliers in Morocco and Turkey
MILAN -- Furniture retailer Dellacourt Home said on Tuesday it would source about a quarter of its sofas and textiles from new suppliers in Morocco and Turkey from next year, to shorten delivery times to its European stores.
The company said the change would cut average shipping times from 45 days to 12 and reduce the stock it needs to hold. Its current suppliers are delivering normally.
Dellacourt shares rose 3%. Its logistics partner, Varro Freight, said the new routes would be handled under its existing contract.""",
 c={"Dellacourt Home": P, "Varro Freight": U}, s=False, g=False),

dict(topic="supply chain", t="""Chip shortage forces Ostrander Motors to cut production forecast
TURIN -- Ostrander Motors cut its full-year production forecast by 70,000 vehicles on Wednesday, saying a shortage of power semiconductors had forced it to halt some assembly lines.
Its main chip supplier, Kellagh Semiconductor, has struggled to raise output at a new plant. Ostrander shares fell 5% and Kellagh shares fell 3%.
Ostrander now expects to build 1.05 million vehicles this year, down from 1.12 million.
The carmaker said it had not been able to find other suppliers at short notice.""",
 c={"Ostrander Motors": N, "Kellagh Semiconductor": N}, s=True, g=True),

dict(topic="regulation", t="""Trevanion Search fined for favoring own shopping service
BRUSSELS -- Antitrust regulators fined Trevanion Search 740 million euros on Monday for ranking its own shopping comparison service above rivals' in search results, and ordered it to change its ranking methods within 60 days.
Trevanion said it would appeal. Its shares fell 2%.
Tallyhop Compare, the rival comparison site that brought the original complaint, rose 12% as analysts said the ruling could send it more traffic.
It is Trevanion's second antitrust fine in three years.""",
 c={"Trevanion Search": N, "Tallyhop Compare": P}, s=False, g=False),

dict(topic="deals", t="""Harrowby Bank and Selcombe Building Society agree merger; savings target raised
LEEDS -- Harrowby Bank agreed on Thursday to merge with Selcombe Building Society in a deal that values the combined group at 5.4 billion pounds, and raised its cost savings target to 350 million pounds a year from 200 million.
Harrowby shares rose 5%. Selcombe members will receive a cash payment of 400 pounds each.
Lorrimer Advisory acted as financial adviser to both parties.
The merger requires approval from Selcombe's members.""",
 c={"Harrowby Bank": P, "Selcombe Building Society": P, "Lorrimer Advisory": U}, s=False, g=True),

dict(topic="management", t="""Penhallow Software cuts 12% of staff, raises margin goal
SAN FRANCISCO -- Penhallow Software said on Tuesday it would cut about 12% of its workforce as chief executive Nadia Russo reorganizes the company, and raised its operating margin target for next year to 28% from 24%.
Penhallow shares rose 8%.
The company said it would stop using outsourcing firm Mardle Services for customer support. Mardle shares fell 5%, as Penhallow was one of its largest clients.
The cuts will affect about 1,100 jobs.""",
 c={"Penhallow Software": P, "Mardle Services": N}, s=False, g=True),

dict(topic="earnings", t="""Cresswell Hotels cuts forecast as business travel slows
CHICAGO -- Cresswell Hotels cut its full-year revenue per available room forecast on Thursday, saying corporate bookings had weakened in the third quarter.
The hotel group now expects revenue per room to rise 1% to 2% this year, down from 3% to 5% previously. Quarterly profit fell 6%. Cresswell shares fell 5%.
The company said its loyalty partnership with card issuer Dunmere Payments was unchanged.
Leisure bookings remained strong over the summer, the company said.""",
 c={"Cresswell Hotels": N, "Dunmere Payments": U}, s=False, g=True),

dict(topic="deals", t="""Tolverne Gold bids for Karoo Ridge Mining after pit collapse halts output
JOHANNESBURG -- Tolverne Gold offered on Wednesday to buy Karoo Ridge Mining for 18 billion rand, after a pit wall collapse halted production at Karoo Ridge's main mine and sent its shares to a record low.
The offer is a 35% premium. Karoo Ridge shares rose 30%.
Tolverne shares fell 3%, as some analysts said it was taking on a mine that may need months of repairs before output resumes.""",
 c={"Karoo Ridge Mining": P, "Tolverne Gold": N}, s=True, g=False),
]
