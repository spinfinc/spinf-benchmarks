# Synthetic business-news items, topic: management. All companies and people are fictional.
TOPIC = "management"
P, N, U = "positive", "negative", "neutral"

ITEMS = [
dict(t="""Maravel Motors ousts CEO after year of plant stoppages
DETROIT -- Maravel Motors said on Monday its board had removed chief executive Thomas Ardleigh with immediate effect, after repeated breakdowns in its paint shops halted production at its largest plant four times this year.
The company named Karin Soelberg, previously head of manufacturing at Halvard Motor Group, as its new chief executive. Maravel said the Kentucky plant remained idle after the latest breakdown last week and would restart on Thursday.
Investors welcomed the change. Maravel shares rose 5%, their best day in six months.""",
 c={"Maravel Motors": P, "Halvard Motor Group": U}, s=True, g=False),

dict(t="""Arvessa Silicon CFO quits; chipmaker withdraws guidance
HSINCHU -- Arvessa Silicon said on Thursday that its chief financial officer, Wen-Li Hsaio, had resigned, and withdrew its full-year revenue and margin guidance pending a review of how it records long-term customer contracts.
The company said the review was being led by the audit committee and could lead to revisions of previously reported revenue. Arvessa shares fell 14%.
Hsaio will join Quorvant Semiconductor as head of treasury next month, Quorvant said.
Arvessa said its operations and customer shipments were not affected. Its largest customer, Oskarsen Drive Systems, said it had no concerns about its supply.""",
 c={"Arvessa Silicon": N, "Quorvant Semiconductor": U, "Oskarsen Drive Systems": U}, s=False, g=True),

dict(t="""Harrowgate Retail to cut 2,000 jobs, close 18 stores under new CEO
LONDON -- Harrowgate Retail said on Wednesday it would close 18 of its 60 department stores and cut about 2,000 jobs, the first major move by chief executive Sofia Brandt since she took over in June.
Brandt said the closures would remove loss-making space and let the group invest in its online business. The shares rose 7% as investors welcomed the restructuring.
Pennick Property Trust, which owns seven of the stores being closed, fell 4%. The landlord said it would need to find new tenants for about 900,000 square feet of space.""",
 c={"Harrowgate Retail": P, "Pennick Property Trust": N}, s=False, g=False),

dict(t="""Activist Wendlow wins board seats at Ostergaard Biologics
COPENHAGEN -- Ostergaard Biologics agreed on Monday to give two board seats to activist investor Wendlow Value Partners and to set up a committee to review its research spending, ending a four-month campaign.
Wendlow, which owns about 4% of the company, had argued that Ostergaard was spending too much on early-stage projects with little chance of success. Ostergaard shares rose 6% as investors bet on tighter cost control.
Wendlow said it had no plans to push for a sale of the company.""",
 c={"Ostergaard Biologics": P, "Wendlow Value Partners": U}, s=False, g=False),

dict(t="""Aldermoor Bank CEO resigns after money-laundering fine
LONDON -- Aldermoor Bank's chief executive, Graham Pellow, resigned on Friday, two days after regulators fined the bank 190 million pounds for failing to monitor suspicious transactions.
The board appointed finance chief Anita Morrow as interim chief executive while it searches for a permanent replacement. Aldermoor shares fell 4%, with analysts warning that the leadership vacuum could delay the bank's cost-cutting program.
Pellow joined Aldermoor in 2019 from Pellworth Bank.
The cost program includes the closure of 120 branches and the sale of the bank's credit card business.""",
 c={"Aldermoor Bank": N, "Pellworth Bank": U}, s=False, g=False),

dict(t="""New Varnholt CEO scales back renewables, raises oil output target
HOUSTON -- Varnholt Energy's new chief executive, Ray Castaneda, on Tuesday scrapped plans to spend $3 billion a year on renewable power and raised the company's 2028 oil and gas production target to 700,000 barrels per day from 640,000.
Castaneda, who took over in August, said the company would return more cash to shareholders. Varnholt shares rose 5%.
The shift is a blow to Solvik Renewables, which had a joint venture with Varnholt to build wind farms in Texas. Varnholt said it would exit the venture; Solvik shares fell 7%.""",
 c={"Varnholt Energy": P, "Solvik Renewables": N}, s=False, g=True),

dict(t="""Bluefinch Airlines CEO steps down after summer of cancellations
STOCKHOLM -- Bluefinch Airlines chief executive Mats Lindgren will step down at the end of the month after a summer in which a shortage of cabin crew and ground staff forced the airline to cancel about 4,000 flights, the company said on Wednesday.
The board named chief operating officer Hanna Rydell as his successor. Bluefinch shares rose 3%.
Bluefinch said it would review its contract with Averly Ground Services, whose staffing problems at two airports contributed to the disruption. Averly shares fell 8%.""",
 c={"Bluefinch Airlines": P, "Averly Ground Services": N}, s=True, g=False),

dict(t="""Corvex Cloud founder returns as chief executive
SEATTLE -- Corvex Cloud said on Monday that co-founder Elena Varga-Holt would return as chief executive, replacing Paul Denning, who led the company for four years as growth slowed.
Investors cheered the return of Varga-Holt, who built Corvex's storage business. The shares rose 8%.
Denning will become chairman of Tallowin Data, a smaller software company, Tallowin said.
Varga-Holt left the company in 2021 to start a venture fund. Corvex's revenue growth slowed to 9% last year from 25% in 2022. Its largest reseller, Lattisfield Software, said the leadership change would not affect their partnership.""",
 c={"Corvex Cloud": P, "Tallowin Data": U, "Lattisfield Software": U}, s=False, g=False),

dict(t="""Ironvale shareholders reject activist's board nominees
PERTH -- Ironvale Mining shareholders voted on Thursday against all four board candidates put forward by activist investor Harlan Ridge Capital, which wanted the miner to split its copper and iron ore businesses.
The result means the break-up plan is off the table for now. Ironvale shares fell 5% as hopes for a split faded.
Harlan Ridge said it would remain a shareholder.
Harlan Ridge owns about 2% of Ironvale. Chairman Colin Rennard said the board would keep the company's structure under review but saw no case for a split at current valuations.""",
 c={"Ironvale Mining": N, "Harlan Ridge Capital": U}, s=False, g=False),

dict(t="""Lumora cuts 5,000 jobs, raises savings target under new chief
PARIS -- Lumora Telecom said on Tuesday it would cut 5,000 jobs over two years and raised its annual cost savings target to 1.2 billion euros from 700 million euros, in the first plan presented by chief executive Claire Duvalier.
Lumora will also outsource network maintenance to Tessarine Networks under a seven-year contract. Tessarine shares rose 4%.
Lumora shares rose 6%.
Most of the job cuts will come in France, where the company employs about 38,000 people. Kiroto Mobile, Lumora's fastest-growing rival, said it had no plans for similar cuts.""",
 c={"Lumora Telecom": P, "Tessarine Networks": P, "Kiroto Mobile": U}, s=False, g=True),

dict(t="""Maribel Foods CEO resigns after recall shuts two plants; outlook cut
CHICAGO -- Maribel Foods chief executive Lena Harbach resigned on Thursday, a month after a listeria recall forced the company to shut two of its breakfast-food plants, which remain closed.
Maribel cut its full-year earnings per share forecast to $3.10-$3.30 from $3.80-$4.00, citing lost production and recall costs. Its shares fell 6%.
The board named director Walter Ng as interim chief executive. Arlo Mills, which supplies flour to the plants, said the closures would not materially affect its business.""",
 c={"Maribel Foods": N, "Arlo Mills": U}, s=True, g=True),

dict(t="""Selvane Shipping names finance chief as next CEO
COPENHAGEN -- Selvane Shipping said on Wednesday that chief financial officer Astrid Kjeldsen would become chief executive in January, succeeding Henrik Mols, who is retiring after nine years in the role.
The appointment had been widely expected, and the company said its strategy and financial targets were unchanged. Selvane shares were flat.
Mols will remain on the board of Carrow Maritime, where he has been a director since 2020.
Kjeldsen joined Selvane in 2015 and has been finance chief since 2021.""",
 c={"Selvane Shipping": U, "Carrow Maritime": U}, s=False, g=False),

dict(t="""Harwick Mutual fires CEO over accounting problems, pulls forecast
HARTFORD, Conn. -- Harwick Mutual Insurance fired its chief executive, Dean Colquhoun, on Monday after an internal investigation found that reserves for commercial liability claims had been understated, and withdrew its 2026 earnings forecast.
The insurer said it expected to add $600 million to $800 million to reserves. Its shares fell 13%.
Reinsurer Ostby Re said its exposure to the affected Harwick policies was limited.
The board appointed its chairman, Laura Pettit, as interim chief executive and said the reserving process would be reviewed by outside actuaries.""",
 c={"Harwick Mutual Insurance": N, "Ostby Re": U}, s=False, g=True),

dict(t="""Veltrane EV founder quits as chairman amid clash over plant delays
AUSTIN, Texas -- Veltrane EV founder Marcus Oyelowo resigned as chairman on Tuesday after a dispute with the board over repeated equipment failures that have halted production at the company's new Arizona plant.
The plant was meant to start building cars in June but has produced fewer than 2,000 because of breakdowns on the stamping and battery lines. Oyelowo had called for the plant's management to be replaced.
Veltrane shares fell 8%. Its battery supplier, Kelmore Battery Works, said the dispute had no bearing on its contract.""",
 c={"Veltrane EV": N, "Kelmore Battery Works": U}, s=True, g=False),

dict(t="""Durnham Industrial to cut 1,200 jobs; lowers revenue outlook
SHEFFIELD -- Durnham Industrial said on Thursday it would cut 1,200 jobs and close its Rotherham factory as chief executive Neil Ashworth restructures the business, and lowered its full-year revenue outlook to a decline of 5% from flat.
Unions said they would ballot members on strike action, though production is continuing normally. Durnham shares fell 9%.
Durnham has been losing orders to Holtzmann Machinery, which on Wednesday reported record order intake. Holtzmann shares rose 2%.""",
 c={"Durnham Industrial": N, "Holtzmann Machinery": P}, s=False, g=True),

dict(t="""Pelliton Chips hires Quorvant executive as CEO
TAIPEI -- Pelliton Chips named Daniel Cho, head of Quorvant Semiconductor's data-center business, as its new chief executive on Monday.
Analysts said Cho was one of the most respected executives in the industry. Pelliton shares rose 7%.
Quorvant shares slipped 2%. Cho had been widely seen as a candidate to succeed Quorvant's chief executive, and his departure leaves the company without an obvious successor.
Cho will start in January. Norrhaven Wafer, a major supplier to both companies, said the appointment would not affect its contracts.""",
 c={"Pelliton Chips": P, "Quorvant Semiconductor": N, "Norrhaven Wafer": U}, s=False, g=False),

dict(t="""Mirovia Pharma CEO to step down for health reasons
BASEL -- Mirovia Pharma chief executive Jonas Ebnother will step down in December for health reasons, the company said on Thursday. The board has started a search for a successor and will appoint chief operating officer Lea Maurer as interim chief if needed.
Mirovia reaffirmed its full-year guidance, with no change. Its shares were unchanged.
The company's collaboration with Castellane Therapeutics on a lung cancer drug will continue as planned, both companies said.""",
 c={"Mirovia Pharma": U, "Castellane Therapeutics": U}, s=False, g=False),

dict(t="""Tallis Market logistics chief leaves after warehouse automation failure
LEEDS -- Tallis Market said on Friday its chief operating officer, Gareth Symes, had left the company, weeks after a failed switch to a new automated warehouse system left hundreds of stores short of stock.
The company said the problems at its Doncaster distribution center were still causing gaps on shelves. Tallis shares fell 3%.
Tallis said it had suspended its contract with Qirra Robotics, which supplied the automation system. Qirra shares fell 10%.""",
 c={"Tallis Market": N, "Qirra Robotics": N}, s=True, g=False),

dict(t="""Brisco Savings new CEO withdraws profit target, cuts branches
MANCHESTER -- Brisco Savings' new chief executive, Rachel Onyango, said on Wednesday she would close 45 of the lender's 300 branches and withdrew the 2026 profit target set by her predecessor, calling it "unrealistic."
Brisco shares fell 8%.
Onyango previously ran the mortgage business at Pellworth Bank.
Brisco, the country's fifth-largest savings lender, reported a 30% drop in first-half profit in August. Onyango said the closures would affect about 600 jobs and that the bank would invest the savings in its mobile app, which is built on software from Nebrin Systems.""",
 c={"Brisco Savings": N, "Pellworth Bank": U, "Nebrin Systems": U}, s=False, g=True),

dict(t="""Grenmark Refining CEO departs after refinery explosion
HOUSTON -- Grenmark Refining said on Monday its chief executive, Carl Brewington, would leave the company, three weeks after an explosion shut its Bay Point refinery.
The refinery, Grenmark's largest, remains closed and is not expected to restart until the first quarter. Grenmark shares fell 4%.
Maridian Oil & Gas, which supplied crude to Bay Point, said it was selling the barrels to other buyers without disruption.
Chief operating officer Lydia Marsh will run the company on an interim basis. Investigators have not yet determined the cause of the blast, which injured 11 workers.""",
 c={"Grenmark Refining": N, "Maridian Oil & Gas": U}, s=True, g=False),

dict(t="""Nebrin Systems cuts 10% of staff, raises margin target
SAN FRANCISCO -- Nebrin Systems said on Tuesday it would cut about 10% of its workforce and raised its long-term operating margin target to 30% from 25%, as chief executive Priya Malhotra reorganizes the company around its automation software.
Nebrin shares rose 9%.
Lattisfield Software, which resells some Nebrin products, said the partnership would continue.
The company employs about 9,500 people, and Malhotra said part of the savings would be reinvested in research. Opaline Software, a competitor in workflow automation, said it had no plans for similar cuts.""",
 c={"Nebrin Systems": P, "Lattisfield Software": U, "Opaline Software": U}, s=False, g=True),

dict(t="""Castorra Air chairman ousted in boardroom fight
MADRID -- Castorra Air shareholders voted on Friday to remove chairman Ignacio Beltran after a dispute over the airline's fleet strategy, leaving the company without a chairman and chief executive at the same time.
The chief executive resigned last month. Castorra shares fell 6%, with analysts warning that the leadership vacuum could delay decisions on a large aircraft order.
Several board members come from Aeralis Airways, which owns a 9% stake in Castorra and voted in favor of removing Beltran.""",
 c={"Castorra Air": N, "Aeralis Airways": U}, s=False, g=False),

dict(t="""Tavora hires Hollins Creek CEO
ATLANTA -- Tavora Beverages named Beth Carrigan, chief executive of Hollins Creek Brewing, as its new president on Thursday, putting her in line to become chief executive.
Carrigan led Hollins Creek for eight years, tripling its sales. Tavora shares rose 3%.
Hollins Creek shares fell 7%. The company has named no successor.
Carrigan will join Tavora in March and report to chief executive Robert Heale, who has said he plans to retire within two years. Hollins Creek said its finance chief, Ian Moss, would run the brewer until a new chief executive is appointed. A distribution agreement between the two companies runs until 2029 and is unaffected.""",
 c={"Tavora Beverages": P, "Hollins Creek Brewing": N}, s=False, g=False),
]
