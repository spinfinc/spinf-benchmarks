#!/usr/bin/env python3
"""One-off patch: lengthen short items and add clearly-neutral mentions.
Appends a paragraph to the item whose headline starts with the given prefix and
adds any new company labels. Applied once to the source files (idempotent check)."""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
U = "U"

PATCHES = [
 # file, headline prefix, appended paragraph, {company: label-const}
 ("regulation.py", "Bluefinch Airlines fined for slow", "Bluefinch carried about 21 million passengers last year, and the authority said most of the delayed claims related to flights cancelled during a strike by air traffic controllers.", {}),
 ("regulation.py", "New EV subsidy rules", "Halvard Motor Group, which does not sell electric cars in the country, is not affected by the change.", {"Halvard Motor Group": U}),
 ("regulation.py", "Dunmore & Pike fined", "The fine is equal to about 1% of the retailer's annual revenue.", {}),
 ("regulation.py", "State approves Harwick Mutual", "The increases apply to about 1.4 million policies.", {}),
 ("regulation.py", "Opaline Software fined", "The penalty is the second-largest the authority has imposed this year. Opaline said the backups, which had been stored on its own servers, had since been encrypted.", {}),
 ("regulation.py", "Regulator orders Maravel Motors", "Halvard Motor Group, which buys its inflators from a different supplier, said none of its vehicles were affected.", {"Halvard Motor Group": U}),
 ("regulation.py", "Parliament passes sugar levy", "Beer is not covered by the levy, and Hollins Creek Brewing, which sells its craft beers in the country through an importer, is not affected.", {"Hollins Creek Brewing": U}),
 ("deals.py", "Lattisfield Software to buy Opaline", "Lattisfield will fund the deal with cash on hand and a new $1 billion term loan arranged by Fenwright Financial. The transaction is expected to close in the first quarter.", {"Fenwright Financial": U}),
 ("deals.py", "Brisco Savings rejects", "Brisco, which has 300 branches in the north of England, is being advised by Tamberlane Advisory.", {"Tamberlane Advisory": U}),
 ("deals.py", "Holtzmann Machinery to acquire Durnham", "The combined company would have annual revenue of about 14 billion euros and 52,000 employees. Brackstone Cement, a large customer of both companies, said it did not expect any change to its existing service contracts.", {"Brackstone Cement": U}),
 ("deals.py", "Ostergaard Biologics buys Pradmoor", "Pradmoor collects royalties on several marketed medicines, including the heart-failure drug Cardevia sold by Mirovia Pharma. Mirovia said the change of ownership would not affect its license agreement. The deal is expected to close in the first half of next year, subject to regulatory approvals.", {"Mirovia Pharma": U}),
 ("deals.py", "Solvik Renewables wins 900 MW", "Construction is due to start in 2028.", {}),
 ("deals.py", "Bluefinch to absorb Vellamo", "The deal requires approval from competition regulators and is expected to close next year.", {}),
 ("deals.py", "Dunmore & Pike sells 30% stake", "The deal requires shareholder approval at a meeting in November. Marchetti Home Goods, which runs furniture concessions in 40 Dunmore & Pike stores, said the arrangement would continue unchanged.", {"Marchetti Home Goods": U}),
 ("deals.py", "Ostmark orders 12 container ships", "The ships, each able to carry 16,000 containers, will be delivered between 2028 and 2030. Ostmark said financing would be arranged by a group of banks led by Pellworth Bank. Selvane Shipping ordered similar vessels from a different yard last year.", {"Pellworth Bank": U, "Selvane Shipping": U}),
 ("deals.py", "Tavora Beverages to buy Hollins Creek", "The deal is expected to close in the first quarter. Tavora already distributes Hollins Creek beers in 12 states under an agreement signed last year.", {}),
 ("deals.py", "Maribel Foods sells snack division", "Fenwright Financial advised Maribel on the sale, which is expected to close by the end of the year.", {"Fenwright Financial": U}),
 ("management.py", "Arvessa Silicon CFO quits", "Arvessa said its operations and customer shipments were not affected. Its largest customer, Oskarsen Drive Systems, said it had no concerns about its supply.", {"Oskarsen Drive Systems": U}),
 ("management.py", "Aldermoor Bank CEO resigns", "The cost program includes the closure of 120 branches and the sale of the bank's credit card business.", {}),
 ("management.py", "Corvex Cloud founder returns", "Varga-Holt left the company in 2021 to start a venture fund. Corvex's revenue growth slowed to 9% last year from 25% in 2022. Its largest reseller, Lattisfield Software, said the leadership change would not affect their partnership.", {"Lattisfield Software": U}),
 ("management.py", "Ironvale shareholders reject", "Harlan Ridge owns about 2% of Ironvale. Chairman Colin Rennard said the board would keep the company's structure under review but saw no case for a split at current valuations.", {}),
 ("management.py", "Lumora cuts 5,000 jobs", "Most of the job cuts will come in France, where the company employs about 38,000 people. Kiroto Mobile, Lumora's fastest-growing rival, said it had no plans for similar cuts.", {"Kiroto Mobile": U}),
 ("management.py", "Selvane Shipping names finance chief", "Kjeldsen joined Selvane in 2015 and has been finance chief since 2021.", {}),
 ("management.py", "Harwick Mutual fires CEO", "The board appointed its chairman, Laura Pettit, as interim chief executive and said the reserving process would be reviewed by outside actuaries.", {}),
 ("management.py", "Pelliton Chips hires Quorvant", "Cho will start in January. Norrhaven Wafer, a major supplier to both companies, said the appointment would not affect its contracts.", {"Norrhaven Wafer": U}),
 ("management.py", "Brisco Savings new CEO", "Brisco, the country's fifth-largest savings lender, reported a 30% drop in first-half profit in August. Onyango said the closures would affect about 600 jobs and that the bank would invest the savings in its mobile app, which is built on software from Nebrin Systems.", {"Nebrin Systems": U}),
 ("management.py", "Grenmark Refining CEO departs", "Chief operating officer Lydia Marsh will run the company on an interim basis. Investigators have not yet determined the cause of the blast, which injured 11 workers.", {}),
 ("management.py", "Nebrin Systems cuts 10%", "The company employs about 9,500 people, and Malhotra said part of the savings would be reinvested in research. Opaline Software, a competitor in workflow automation, said it had no plans for similar cuts.", {"Opaline Software": U}),
 ("management.py", "Tavora hires Hollins Creek CEO", "Carrigan will join Tavora in March and report to chief executive Robert Heale, who has said he plans to retire within two years. Hollins Creek said its finance chief, Ian Moss, would run the brewer until a new chief executive is appointed. A distribution agreement between the two companies runs until 2029 and is unaffected.", {}),
 ("earnings.py", "Quorvant Semiconductor lifts", "Quorvant reports a week before Pelliton Chips, which makes smartphone processors but does not sell data-center accelerators.", {"Pelliton Chips": U}),
 ("earnings.py", "Pellworth Bank profit jumps", "Brisco Savings, a smaller lender, is due to report its half-year results next week.", {"Brisco Savings": U}),
 ("earnings.py", "Lattisfield Software raises", "Lattisfield's platform runs on servers rented from Corvex Cloud under a long-term agreement.", {"Corvex Cloud": U}),
 ("earnings.py", "Cadwell Dairy beats", "Cadwell sells most of its milk through supermarket chains, including Fennimore Grocers.", {"Fennimore Grocers": U}),
 ("supply_chain.py", "Aeralis Airways grounds jets", "Corvane Aircraft, which builds the airframes for the grounded jets, said the parts problem did not involve any of its components.", {"Corvane Aircraft": U}),
 ("supply_chain.py", "Blade factory fire delays Solvik", "Eastmere Power, which will buy electricity from one of the delayed projects, said it had sufficient generating capacity to cover the gap.", {"Eastmere Power": U}),
 ("supply_chain.py", "Bridge collapse halts coal", "Holtzmann Machinery, which is installing a new kiln-handling line at the works, said the project was on schedule.", {"Holtzmann Machinery": U}),
 ("supply_chain.py", "Fire halts output at Arvessa", "Quorvant Semiconductor, which makes its chips at more advanced plants run by other manufacturers, said it was not affected.", {"Quorvant Semiconductor": U}),
 ("supply_chain.py", "Battery recall halts Kelmore", "Brenholt Automotive, which buys its battery cells from other suppliers, said its production was not affected.", {"Brenholt Automotive": U}),
 # shots
 ("shots.py", "Istara Bio wins approval", "The one-time treatment will carry a list price of $2.9 million.", {}),
 ("shots.py", "Norrvald Bank profit beats", "Net interest income rose 9% to 6.1 billion crowns, while costs rose 4%.", {}),
 ("shots.py", "Regulator blocks Tenby Cement", "Tenby said it would not appeal and would instead use the money for a share buyback.", {}),
 ("shots.py", "Sallow Rail wins", "The trains will be built at its plants in Lille and Belfort.", {}),
 ("shots.py", "Ashvane Telecom CEO resigns", "Rafferty had led the company since 2020.", {}),
 ("shots.py", "Ardmore Mobile cuts outlook", "Ardmore said it would cut prices on some plans next month to stem the losses.", {}),
 ("shots.py", "Regulator orders Vandermolen Bikes", "No injuries have been reported.", {}),
 ("shots.py", "Chip shortage forces Ostrander", "The carmaker said it had not been able to find other suppliers at short notice.", {}),
 ("shots.py", "Trevanion Search fined", "It is Trevanion's second antitrust fine in three years.", {}),
 ("shots.py", "Harrowby Bank and Selcombe", "The merger requires approval from Selcombe's members.", {}),
 ("shots.py", "Penhallow Software cuts", "The cuts will affect about 1,100 jobs.", {}),
 ("shots.py", "Cresswell Hotels cuts forecast", "Leisure bookings remained strong over the summer, the company said.", {}),
]


def apply():
    by_file = {}
    for p in PATCHES:
        by_file.setdefault(p[0], []).append(p[1:])
    for fn, patches in by_file.items():
        path = os.path.join(HERE, fn)
        s = open(path, encoding="utf-8").read()
        for prefix, para, comps in patches:
            start = s.find('t="""' + prefix)
            assert start >= 0, (fn, prefix)
            end = s.find('""",\n c={', start)
            assert end > 0, (fn, prefix)
            if para in s[start:end]:
                continue  # already applied
            s = s[:end] + "\n" + para + s[end:]
            cpos = s.find(" c={", end) + len(" c={")
            dict_end = s.find("}", cpos)
            ins = "".join(f', "{k}": {v}' for k, v in comps.items())
            s = s[:dict_end] + ins + s[dict_end:]
        open(path, "w", encoding="utf-8").write(s)


if __name__ == "__main__":
    apply()
