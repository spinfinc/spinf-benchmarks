#!/usr/bin/env python3
"""Generator for the synthetic ticket-triage benchmark (MIT).

All texts are original, hand-written for this benchmark. All companies,
products and people are fictional.

Writes:
  data/ticket_triage.jsonl        (test items, ids tt001..)
  data/ticket_triage.shots.jsonl  (few-shot items, ids ts01..ts24 = 3 sets of 8)

Each source item carries a `domain` tag used only for the balance report;
it is not written to the output files.
"""
import json
import random
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"

B, T, A, S, C = "billing", "technical", "account", "shipping", "cancellation"
BOT, HUM = "bot", "human"
U, N = True, False


def it(topic, handling, urgent, domain, text):
    return dict(topic=topic, handling=handling, urgent=urgent, domain=domain,
                text=re.sub(r"\s+", " ", text).strip())


TEST = [
    # ------------------------------------------------------------------ BILLING
    it(B, BOT, N, "saas", """Hi team, could you resend the invoice for August? Our finance department
       needs a PDF copy for their records and I can't find the original email anywhere. Account is under
       Marisol Quintero, Fenwright Logistics, Ledgerwick Team plan. Many thanks, Marisol"""),
    it(B, BOT, U, "streaming", """my card expired and reelhaven keeps saying my account will be paused
       tonight if i dont update payment. where do i actually put the new card?? cant find it in settings
       on the tv app"""),
    it(B, BOT, N, "telecom", """THIS IS THE THIRD TIME I'm asking. I just want a copy of my Tidewire bill
       for July. Not a 'summary', not a link to the app, the actual itemised bill as a PDF. Is that really
       so hard?? Email it to the address on the account."""),
    it(B, BOT, U, "utilities", """Web form - Subject: Bills needed before audit. We need PDF copies of the
       Northmere business water bills for July, August and September before 9am tomorrow, when the external
       auditors arrive. The account holder is Daniel Okafor (Brisk Line Couriers). Please just email them to
       the billing contact on file."""),
    it(B, BOT, N, "fintech", """Quick question - what's the fee for sending money abroad on the free
       Pennyloom plan vs Plus? Thinking of sending about 400 euros to my sister in Lisbon next month."""),
    it(B, BOT, N, "fitness", """Hiya, I've got a new debit card and want my monthly Pulsefield membership
       to come off that one from next month instead of the old card. Can I change it myself in the app or
       do I have to come into the gym?"""),
    it(B, BOT, N, "utilities", """Hello, I would like to change the day of
my direct debit from the 1st to the 15 of each month, because my salary is coming on the 12 and at the moment
the payment is going before I am paid, which is not comfortable for me. Is this possible to do? My account
number is BM-448210 and the account is in my name, Dragana Petrović. If I can do this myself on the website
please explain me where, I did not find it in the menu. Thank you very much and have a nice day."""),
    it(B, BOT, N, "ecommerce", """Where can I download a VAT invoice for order #HC-20931? I bought a monitor
       arm for my home office and need the invoice with VAT shown separately for my expenses claim. The
       order confirmation only shows the total."""),
    it(B, BOT, N, "food", """how do i add my company card to my basketbee account? want the office lunch
       orders to go on the business card and my personal groceries to stay on my own card. is that a
       thing"""),
    it(B, BOT, U, "travel", """Hello, I need a receipt for my Wayfarrow booking WF-77120 (hotel in Utrecht,
       3 nights) for my expense report, which has to be submitted by 5pm today. I accidentally deleted the
       confirmation email. Could you please resend it? Thanks, Priya"""),
    it(B, BOT, N, "electronics", """Is the Orrin Labs Care+ extended warranty charged monthly or as a one-off
       payment? I'm on the checkout page for the Orrin Pace 2 watch and it just says 'from 3.99' which isn't
       very clear."""),
    it(B, BOT, U, "saas", """Chat: hi - our Quorumly workspace just got locked because the company card on
       file expired over the weekend. Whole team can't book any meeting rooms this morning. I have the new
       card right here, just tell me where to enter it so we're back up."""),
    it(B, BOT, N, "streaming", """Which Auralune plan am I on right now and when does it renew? I don't want
       another surprise on my statement like last year. No problem with anything, just want to know the
       date."""),
    it(B, HUM, N, "streaming", """I was charged twice for Cinderbox Premium on the 3rd ($14.99 each). Your
       chat assistant keeps telling me the second one is a 'pending authorisation' that will drop off, but
       it's been three weeks and it has clearly posted on my bank statement. I'd like the duplicate
       refunded, please, and a person to look at this."""),
    it(B, HUM, N, "utilities", """Brightmeadow added £59.99 of 'home emergency cover' to my bill that I
       never signed up for - it was a pre-ticked box when I switched to you and nobody would notice it.
       Refund it or I'm raising a claim with my bank to get the direct debit money back."""),
    it(B, HUM, U, "utilities", """Dear Northmere Water & Power,
For the past four months my bills have been estimated rather than based on actual readings, and the latest
statement (account NM-11872) is roughly three times my usual usage, even though nothing in the household has
changed. I have submitted meter photographs through your website on two occasions, on 4 July and 19 August,
and both times received an automated acknowledgement but no corrected bill. I telephoned once as well and was
told a reading would be arranged, which has not happened. I have now passed our correspondence to my
solicitor, who has advised me to request a formal review of the account in writing, which I am doing with
this message. I would be grateful for a response and for the direct debit to be held at its previous level
while the review takes place.
Kind regards,
Harriet Pomeroy"""),
    it(B, HUM, N, "fitness", """Hi, I've been an IronOak member for six years and just noticed new joiners
       are getting 30% off their first year. Any chance you could offer something similar to long-standing
       members? Totally understand if not, just thought I'd ask."""),
    it(B, HUM, U, "saas", """URGENT - Our Tallowby workspace was suspended this morning for non-payment, but
       invoice INV-5521 was paid by bank transfer on the 2nd (confirmation attached, reference TLW-5521).
       40 analysts are locked out of every dashboard right now. Please match our payment to the invoice and
       lift the suspension, and tell me what went wrong on your end."""),
    it(B, HUM, N, "ecommerce", """I bought the Fernwick Home oak side table on the 2nd for £189 and today
       it's on the site for £139. I know your page says you don't do price adjustments, but I've been
       ordering from you for years - could you refund the £50 difference as a goodwill gesture?"""),
    it(B, HUM, U, "telecom", """Just got a Tidewire bill for €1,240 in roaming data from a four-day trip
to Norway which is completely insane because I had the Travel Pass add-on active the whole time, I checked
before I left and I still have the activation SMS on my phone, and I barely used data anyway, mostly maps. The
direct debit goes out tomorrow morning and it will empty my account, so I need this charge removed before
then, not in 5-7 working days."""),
    it(B, HUM, N, "streaming", """Love how you 'forgot' to remind me my free trial was ending and then
       charged me for a full YEAR of Auralune Premium. Really classy. I haven't opened the app once since
       the trial. I want that annual charge refunded."""),
    it(B, HUM, N, "food", """Crumbfleet order #CF-88213 was marked as delivered but it never arrived. Your
       support gave me Crumbfleet credit instead of a refund. I don't want credit, I paid by card and I want
       the £32.40 back on my card. Please sort this."""),
    it(B, HUM, N, "travel", """Hello, Wayfarrow charged us a €180 cancellation fee for booking WF-60218,
       but it was the hotel that cancelled on us, not we. I forward you the hotel email where they confirm
       it was overbooking. Please remove this fee and refund it to my card. Best regards, Luca Ferrandi"""),
    it(B, HUM, U, "saas", """Our fiscal year closes tomorrow and we need Ledgerwick to reissue invoice
       INV-3302 addressed to our new legal entity (Harrowgate Analytics GmbH instead of Harrowgate Ltd),
       with PO number 4410-A added and the amount split across two cost centres. I know the billing portal
       can't do this, so please pass it to someone who can."""),
    it(B, HUM, N, "electronics", """Ordered Lumacoil Pro earbuds from the Canadian store, checkout showed
       $229 CAD (I have a screenshot) but my card was charged in USD and my bank added a foreign
       transaction fee on top. Could you refund the difference and the fee? Not a huge amount but it's the
       principle."""),
    it(B, HUM, U, "fitness", """IronOak has continued to take £45 a month for five months after I cancelled
       my membership in writing (letter dated 3 February, I hold proof of postage). If the £225 is not
       refunded in full within 14 days I will be filing a claim in the small claims court."""),

    # ---------------------------------------------------------------- TECHNICAL
    it(T, BOT, N, "fintech", """How do I export my Pennyloom transaction list as a CSV for my budgeting
       spreadsheet? The export menu in the app only gives me PDF. Is CSV only on certain plans or am I just
       missing a setting somewhere?"""),
    it(T, BOT, N, "electronics", """how do I factory reset the vantorra thermostat? we're moving house next
       month and I want to wipe our schedules and wifi details off it before the new owners move in"""),
    it(T, BOT, N, "telecom", """Your STUPID Glintwave router from Tidewire has a blinking orange light AGAIN
       and the little booklet it came with is useless!!! What does blinking orange even mean?? Internet
       still works but I want to know what it's telling me. Honestly the worst designed box I've ever
       owned."""),
    it(T, BOT, N, "streaming", """Can I download Reelhaven shows to watch offline on a long flight? If so
       how, and do downloads expire? Using an Android tablet."""),
    it(T, BOT, U, "saas", """I'm presenting to our board at 8am tomorrow and need to share a Tallowby
       dashboard with two directors who don't have Tallowby accounts. Is there a view-only public link
       option, and where do I turn it on?"""),
    it(T, BOT, N, "fintech", """How do I turn on push notifications for card payments in the Pennyloom app?
       My partner gets a ping every time she pays for something and I get nothing. iPhone, latest app
       version."""),
    it(T, BOT, N, "travel", """The Staylark app keeps saying 'location services are off' when I search for
       hotels near me, but location is definitely on in my phone settings. Android 14. Is there some other
       setting I'm missing?"""),
    it(T, BOT, N, "fitness", """how do I pair my chest heart rate strap with the Stridehaus app? It shows up
       in my phone's bluetooth list but not in the app's device screen. Strap is a generic one, not your
       brand, if that matters"""),
    it(T, BOT, N, "utilities", """Hi, the in-home display for my Northmere smart meter is showing 'E-14' in
       the corner. Everything else seems normal and the readings are updating. What does that code mean and
       do I need to do anything?"""),
    it(T, BOT, U, "saas", """We rotated our Plinthdesk webhook signing secret this morning and since then
       every delivery to our endpoint is failing, so no tickets are syncing into our system and the support
       team is effectively blocked. Where in the admin settings do I paste the new secret on your side?"""),
    it(T, BOT, N, "travel", """Is there a way to add my Jetmarsh boarding pass to my phone's wallet app? I
       checked in through the Jetmarsh app but I can't see an 'add to wallet' button anywhere."""),
    it(T, BOT, N, "electronics", """Hello, I have buy the Lumacoil Air earbuds last week. How I can change
       the touch controls so double tap is skipping the song and not pause? In the app I not find this
       option. Thank you"""),
    it(T, BOT, U, "electronics", """Playing a gig tonight at 8 and my Brightcoil wireless mic receiver won't
       pair with the transmitter anymore - it just flashes blue. How do I reset the pairing? Manual's at
       home and I'm already at the venue."""),
    it(T, HUM, U, "saas", """Ledgerwick has been returning 502 errors for our whole finance team since 07:40
       UTC. We can't create or send a single invoice and it's month-end close. Your status page says all
       systems operational. Please escalate this to engineering now."""),
    it(T, HUM, U, "saas", """After yesterday's mobile sync, three months of call notes have disappeared from
       Stackmere CRM for two of our sales reps. The version history shows nothing before Tuesday. These
       notes are the only record of several deals in progress. We need them restored."""),
    it(T, HUM, N, "electronics", """This is my third replacement Vantorra T3 thermostat.
Each one works for about a week and then stops calling for heat - the display still shows the schedule, the
app still connects, but the boiler just never fires. I've done every reset in the help centre, including the
full factory reset and re-running the wiring wizard, and my heating engineer has checked the boiler and the
wiring and says it's fine. We have a backup heater so it's not an emergency, but I'd like to speak to someone
technical about whether this model is even compatible with my system, rather than being sent a fourth one
that does the same thing."""),
    it(T, HUM, U, "telecom", """Voicemail transcript: Hi, this is Dr Amara Nwosu from Riverside Family
       Clinic, account TW-B-20417. Our Tidewire business fibre has been down since six this morning, we
       can't reach our patient booking system and the phones are on the same line. We need an engineer out
       today, please call me back on my mobile."""),
    it(T, HUM, N, "streaming", """Hi there, small thing and no rush at all. Since the last update the
       Auralune app skips to the next track after about 30 seconds whenever it's connected to my car's
       display. I've reinstalled, cleared the cache and tried two different phones, same result. Looks like
       a genuine bug so maybe worth passing to your developers."""),
    it(T, HUM, U, "fitness", """The Stridehaus app update last night wiped my entire workout history. Four
       years of runs, PBs, everything - the app now says 'no activities yet'. Please tell me this is backed
       up somewhere on your servers and you can restore it."""),
    it(T, HUM, N, "food", """App store review (1 star), forwarded to support:
Crashes EVERY single time I get to checkout and pick one of my saved cards. Been like this over a week. Updated,
reinstalled, removed and re-added the card, restarted the phone - everything your help page says. Still
crashes. Pixel, Android 14. Fix your app."""),
    it(T, HUM, U, "electronics", """Something is very wrong with the Vantorra app. When I open my Front Door
       camera feed, I'm seeing video of someone else's hallway - a house I've never been in. If I can see
       theirs, can someone see inside mine? I've unplugged my cameras for now."""),
    it(T, HUM, N, "streaming", """Since the last update the Reelhaven app on my living room smart TV crashes
       back to the home screen the moment I press Sign In. My password is fine - I can sign in on my phone
       and laptop without any problem. I've already uninstalled and reinstalled the TV app and unplugged the
       TV. Same thing every time."""),
    it(T, HUM, U, "electronics", """My Brightcoil 20000 power bank swelled up overnight while charging and
       scorched the desk it was on. Luckily nobody was hurt, but it could easily have started a fire. My
       home insurer has asked for a formal response from you, and I have been advised to seek legal advice.
       Please treat this as a formal complaint."""),
    it(T, HUM, N, "fintech", """The Coinwell Business export to our accounting software is creating duplicate
       payees whenever a name contains an accented character (Zoë, José, Björn...). It's not urgent - we're
       merging them by hand for now - but we'd appreciate a fix or a workaround. Happy to share examples
       with whoever looks into it."""),
    it(T, HUM, U, "fintech", """The Coinwell Business web app won't load the payroll screen - just a spinning
       wheel since 8 this morning, on three different computers and two browsers. We have to submit payroll
       for 23 staff by 3pm today or they won't be paid on Friday. Please help."""),
    it(T, HUM, N, "utilities", """Since Northmere replaced my meter three weeks ago, my online account shows
       zero solar export every day, even though the display on the meter itself shows export readings. I
       assume the new meter isn't configured correctly for export. Could someone check the setup? Happy to
       send photos."""),

    # ------------------------------------------------------------------ ACCOUNT
    it(A, BOT, N, "streaming", """forgot my reelhaven password again lol. can you send me a reset link to the
       email on the account? tried the forgot password thing but I think I typed the wrong email"""),
    it(A, BOT, N, "travel", """How do I change the email address I use to log in to Staylark? I'm moving
       from my old work address to a personal one and want to keep all my bookings and saved hotels. Is it
       under profile or account settings?"""),
    it(A, BOT, N, "ecommerce", """Every. Single. Time. I try to log into Harborcart it tells me my password
       is wrong. I KNOW my password. Whatever. Just send me a reset link so I can finally place my order
       before I lose my mind."""),
    it(A, BOT, U, "travel", """Flying at 6am tomorrow and I'm locked out of my Jetmarsh account after too
       many wrong password attempts. I need to get in tonight to check in online. How do I unlock it?
       Booking ref JM4K7Q."""),
    it(A, BOT, N, "fitness", """Hi! I got married last month and need to update my surname on my Pulsefield
       membership profile (from Carver to Okonkwo). Is that something I can do in the app myself?"""),
    it(A, BOT, N, "fintech", """Got a new phone. How do I move my Pennyloom login and the two-factor codes
       over to it? The old phone still works fine and I can still log in on it, I just want to switch before
       I trade it in."""),
    it(A, BOT, N, "saas", """How do I invite a new team member to our Plinthdesk account? We have two unused
       seats on our plan. I'm the account admin but I can't find where to send an invite."""),
    it(A, BOT, N, "utilities", """Please can you update the phone number on my Brightmeadow Energy account?
       The old landline has been disconnected. Or tell me where to do it online, I'm happy to do it myself.
       Account BM-771043."""),
    it(A, BOT, N, "food", """Hello, I can not receive the verification code by SMS for create my account in
       Plumtray. I try 3 times already, nothing come. Can you send again or is there other way to verify,
       for example by email? Thank you"""),
    it(A, BOT, U, "saas", """I'm the Stackmere admin for our company. One of our contractors finishes today
       and I need to remove her access before she leaves at 5pm. Where's the option to deactivate a user? I
       don't want to delete her records, just block her login."""),
    it(A, BOT, N, "streaming", """how do I change the display name on my Auralune account? it still shows the
       embarrassing gamer tag I picked when I was 15 and it's visible on my shared playlists now lol"""),
    it(A, BOT, U, "telecom", """Voicemail transcript: hi, um, I need to get into
my Tidewire account tonight to download a proof-of-address letter for my visa appointment at nine tomorrow
morning, but the password reset email just isn't arriving, I've checked spam. Can you resend it or send it by
text instead? Thanks."""),
    it(A, BOT, N, "fitness", """I lost my IronOak membership card and I need my membership number to book
       classes on the website. Where can I find it? Also can I order a new card? Name is Rafael Duarte."""),
    it(A, HUM, U, "streaming", """Someone got into my Reelhaven account last night. I got an email saying my
       email address had been changed, and now my password doesn't work either. There's a profile on there
       I didn't create. I've paid for this account for years - please lock it and get it back to me."""),
    it(A, HUM, U, "fintech", """Hello. I received a text this afternoon asking me to confirm a new device
       signing in to my Coinwell account. It wasn't me and I did not approve it. I'm not sure whether my
       password has been compromised. Could someone please check my account and advise? Thank you, Mei
       Lin"""),
    it(A, HUM, N, "fintech", """Under data protection law I'd like to request a copy of all the personal
       data Coinwell holds about me, including any profiling or credit-scoring data and call recordings. I
       understand you have a month to respond, so no rush beyond that. My account email is the one I'm
       writing from."""),
    it(A, HUM, N, "telecom", """My mother passed away in August. Her Tidewire family plan has three
lines on it - hers, mine and my brother's - and my brother and I still use our two lines every day. We'd like
to take the account over in my name and keep both our numbers, and close her line. I have the death
certificate, the will naming me as executor and my own ID. I've tried the online chat twice but it just
offers me a link to cancel the whole account, which is the opposite of what we want. What do you need from
us, and is there a way to do this without the numbers being cut off in the meantime?"""),
    it(A, HUM, U, "saas", """Our only Ledgerwick admin left the company last week and nobody else has admin
       rights. We can't approve invoices, add users or change anything, and she isn't responding to
       messages. How do we prove we own the account and get admin rights transferred? The whole finance
       team is stuck."""),
    it(A, HUM, N, "food", """I accidentally ended up with two Basketbee accounts - one on my work email and
       one on my personal email. Both have order history and loyalty points (about 2,300 on one and 900 on
       the other). Could you merge them into the personal one so I don't lose the points?"""),
    it(A, HUM, U, "saas", """Our Tallowby audit log shows one of our user accounts (j.whitlock) signing in
       from two countries we don't operate in, starting at 02:14 UTC. We've disabled the user on our side.
       We need your security team to confirm whether any data or reports were exported during those
       sessions."""),
    it(A, HUM, N, "fitness", """My Stridehaus account was suspended yesterday for 'violating community
       guidelines' and I genuinely have no idea why. I mostly just log runs and occasionally comment on
       friends' posts. I'd like to know what I'm supposed to have done and how to appeal."""),
    it(A, HUM, U, "ecommerce", """This is the third time I've asked Fernwick Home to erase my account and
       personal data. I'm still receiving marketing emails. This is a breach of data protection law. If I
       don't get written confirmation of erasure, I will be filing a complaint with the data protection
       regulator."""),
    it(A, HUM, N, "fintech", """I've legally changed my name (deed poll attached) and have a new passport. The
       Pennyloom app won't let me edit my name and tells me to contact support. Could you let me know what
       documents you need to update my account? No huge rush."""),
    it(A, HUM, U, "telecom", """My phone lost all signal about an hour ago and I've just had two emails saying
       my bank password was reset. I think someone has moved my Tidewire number to another SIM. Please lock
       my account and number right now, I'm calling from my partner's phone."""),
    it(A, HUM, N, "saas", """I lost my phone on holiday, and it had both my authenticator app and my backup
       codes for Quorumly on it, so I can't sign in. I'm on leave until the 14th, so no urgency, but I'd
       like to get it sorted before I'm back. What identity verification do you need from me?"""),
    it(A, HUM, U, "utilities", """My ex-partner still has the login for our old joint Brightmeadow account,
       which is now in my name only. He keeps changing the contact email and phone to lock me out and has
       been messaging me about it. I am the account holder. Please remove his access today."""),

    # ----------------------------------------------------------------- SHIPPING
    it(S, BOT, N, "ecommerce", """Hi, just wondering where my Harborcart order #HC-44102 is? Ordered on
       Monday with standard delivery. Could you send me the tracking link? Nothing wrong, just keen to know
       when to expect it."""),
    it(S, BOT, N, "food", """Which delivery slot did I book for my Basketbee shop this Saturday? I forgot to
       write it down and want to make sure I'm home. Can't see it on the home screen of the app."""),
    it(S, BOT, N, "ecommerce", """Your 'tracking page' has said LABEL CREATED for two days now. Is my parcel
       even moving?? I don't want a lecture about busy periods, just tell me where it actually is. Order
       CB-5120. Unbelievable."""),
    it(S, BOT, N, "electronics", """Can I still change the delivery address for my Orrin Labs Pace 2 order?
       The app says it hasn't shipped yet. I'd rather send it to my office where someone can sign for
       it."""),
    it(S, BOT, U, "ecommerce", """I'm moving out tomorrow at noon and order #FW-8812 still says 'not yet
       dispatched'. Please change the delivery address to my new flat: 14 Larkspur Row, Flat 3, Brindle
       Hill. Or tell me where I can change it myself tonight."""),
    it(S, BOT, N, "telecom", """When will my new Tidewire SIM card arrive? I ordered it on the website last
       Wednesday and haven't had any email about delivery yet. Just want to know if it's been posted."""),
    it(S, BOT, N, "ecommerce", """Hi, my packet say is delivered to the parcel locker at the train station,
       but I don't receive the code to open the locker. Order CB-2231. Please can you send the code again to
       my phone? Thanks, Oksana"""),
    it(S, BOT, N, "food", """Do you deliver to Hollin Moor? We've just moved out of the city and I'm not sure
       if we're in your area. If you do, which days does the Basketbee van come out our way?"""),
    it(S, BOT, U, "food", """Hosting a dinner party for six at 7 tonight and my Plumtray box is arriving
       today. Can I still add a delivery note? The buzzer's broken, so the courier needs to ring my mobile
       when they arrive rather than buzz."""),
    it(S, BOT, U, "ecommerce", """Can I switch my Copperbell order from home delivery to collecting it at the
       Eastgate store today? It hasn't shipped yet and I need the hiking boots for a trip first thing
       tomorrow."""),
    it(S, BOT, N, "utilities", """Brightmeadow emailed to say my free energy monitor had been sent out last
       week. Is there a tracking number for it? The email didn't include one."""),
    it(S, BOT, U, "electronics", """I need a Brightcoil 65W laptop charger by tomorrow afternoon for an exam -
       mine just died. Do you offer next-day delivery to Leeds, and what's the order cutoff time today to get
       it tomorrow?"""),
    it(S, BOT, N, "travel", """Wayfarrow said they'd post the printed rail passes for our Europe trip. Have
       they been dispatched yet? The trip isn't until next month, I just want to know roughly when to expect
       them."""),
    it(S, HUM, N, "ecommerce", """Tracking says my parcel was delivered five days ago but nothing arrived.
       I've asked every neighbour and checked the bins and the shed. Order HC-51290, it's a €340 espresso
       machine. Please open an investigation with the courier and send a replacement."""),
    it(S, HUM, N, "ecommerce", """The four Fernwick dining chairs arrived yesterday and two of them have legs
       snapped clean off - the box was crushed at one corner so it clearly happened in transit. Photos
       attached. I'd like the two chairs replaced rather than refunded, as they're part of a set."""),
    it(S, HUM, U, "food", """Our weekly Basketbee Business order didn't arrive this morning. We're a café,
       we open in two hours and have no milk, eggs or butter. The app says 'delivery attempted' but nobody
       came - we've been here since 6. Please get it to us or tell me what's happening."""),
    it(S, HUM, N, "food", """The Crumbfleet courier who brought my order last night swore at me because I
       took a minute to come down the stairs, then threw the bag on the ground. Food was fine, I don't want
       a refund. I just want this reported and I'd rather he didn't deliver to me again."""),
    it(S, HUM, U, "ecommerce", """The courier is holding my Copperbell order and demanding £86 in import duty,
       but your checkout said 'duties and taxes included' (screenshot attached). They say they'll send it
       back to you tomorrow if nobody pays. Please sort this out with them so the parcel is released."""),
    it(S, HUM, N, "electronics", """Ordered Lumacoil Air earbuds in white. Got a black pair instead that are
       clearly used - scuffed case and somebody else's ear tips still on them. Second time this has happened
       with an order from you. Please send a correct, new pair and tell me what to do with these."""),
    it(S, HUM, U, "ecommerce", """Dear Fernwick Home,
I am writing about my sofa, order FW-40077, which was due to be delivered six weeks ago. Since then I have
been given four different delivery dates by your customer service team and by the courier, none of which were
kept, and on two of those days I took unpaid leave to be at home. I paid the full amount of £1,480 at the time
of order. I have asked my lawyer to prepare a letter regarding my consumer rights, although I would still
prefer to resolve this directly with you if possible. Please confirm a firm delivery date, in writing, that
you are able to keep.
Regards,
Hannelore Birk"""),
    it(S, HUM, N, "electronics", """The courier left my Vantorra Cam 2 parcel on the doorstep in the pouring
       rain and the box was soaked right through when I got home. The camera turns on, but I'm not
       comfortable mounting an electrical device that sat in a puddle. Could you send a replacement?"""),
    it(S, HUM, U, "food", """I ordered a birthday cake from Plumtray for my daughter's party at 3pm today. The
       delivery window was 10-12, it's now 1:15 and the tracking hasn't moved since 9am. The chat just keeps
       sending me the same tracking link. I need someone to actually find out where it is."""),
    it(S, HUM, N, "ecommerce", """ok so order HC-60017 was supposed to come in two boxes but only one
box actually arrived and the one that did had the wrong size trainers in it (ordered 9, got 7) and then when I
looked at my bank I think I was charged delivery twice?? and the tracking for the second box just says
'exception' with no explanation. Honestly don't know where to start, your chat keeps asking me to pick one
issue. The missing box is what I care about most, it had my nephew's birthday present in it."""),
    it(S, HUM, U, "saas", """Plinthdesk shipped the six check-in kiosks for our new branch to our old office
       address, even though we updated it in the admin console two weeks ago. The branch opens tomorrow at
       9. Tracking shows them out for delivery at the old address. Can you get the courier to redirect
       them?"""),
    it(S, HUM, N, "telecom", """Wow, great job Tidewire. My new phone was 'delivered' to number 47 - my
       street only goes up to 40. The courier's photo shows a front door I've never seen in my life.
       Fantastic service. I'd like my actual phone, please. Order TW-O-55318."""),
    it(S, HUM, N, "fitness", """The delivery team for my Stridehaus treadmill refused to carry it upstairs,
       even though I paid extra for 'room of choice' delivery. It's now sitting in my hallway. I need
       someone to come back and put it where I paid for it to go."""),

    # ------------------------------------------------------------- CANCELLATION
    it(C, BOT, N, "streaming", """How do I cancel my Reelhaven subscription? I don't want it to renew next
       month. I'm happy to keep watching until the end of this billing period, I just can't find the
       option."""),
    it(C, BOT, N, "fitness", """I want to cancel my Pulsefield membership as I'm moving to another city at the
       end of next month. What is the notice period and can I do it through the app?"""),
    it(C, BOT, N, "food", """pls cancel my plumtray weekly meal plan. not unhappy, just cooking more myself
       these days. thx"""),
    it(C, BOT, U, "streaming", """My Cinderbox free trial ends tonight at midnight and I don't want to be
       charged for the first month. How do I cancel before then? I signed up through the website, not the
       app."""),
    it(C, BOT, N, "utilities", """I'd like to cancel the boiler cover add-on on my Brightmeadow Energy
       account from its next renewal date. The electricity and gas supply stay as they are. Where do I do
       that in the online account?"""),
    it(C, BOT, U, "ecommerce", """Can I cancel order FW-9034? I placed it about ten minutes ago and picked
       the wrong colour. The confirmation email says it'll be dispatched at 6pm today, so I'd like to cancel
       before then."""),
    it(C, BOT, N, "telecom", """Good morning, I want to terminate my mobile contract with Tidewire. The
       contract is finish last month so I think there is no penalty. What is the procedure please? I will
       keep my number and go to other operator. Regards, Tomasz Wierzbicki"""),
    it(C, BOT, U, "travel", """I need to cancel my Staylark hotel booking SL-4471. Confirmation says free
       cancellation until 6pm today. How do I do it in the app? Don't want to miss the window."""),
    it(C, BOT, N, "fintech", """Please tell me how to cancel my Pennyloom Plus subscription. I'd like to go
       back to the free account at the end of this month - the extra features just aren't worth it for
       me."""),
    it(C, BOT, N, "food", """App store review (1 star), forwarded to support:
Been trying to cancel Crumbfleet Pass for TWENTY minutes and the app keeps sending me round in circles to
'special offers'. I DON'T WANT OFFERS. Where is the actual cancel button???"""),
    it(C, BOT, N, "utilities", """We're moving out of 22 Alder Close on the 30th. How do I close our
       Northmere account for this address and submit the final meter reading? We don't need service at the
       new place, the landlord handles it."""),
    it(C, BOT, U, "travel", """My Wayfarrow Plus membership auto-renews tomorrow and I've decided not to
       continue with it. Please tell me how to turn off auto-renewal today so I'm not charged. I don't need
       anything else - just want to stop the renewal."""),
    it(C, BOT, N, "electronics", """How do I cancel the Vantorra Cloud video storage plan? I'm keeping the
       camera, I just don't need cloud recordings anymore since I've set up local storage on a memory
       card."""),
    it(C, HUM, N, "utilities", """Hello, my father, Gerald Ashworth, passed away
last month and I'm the executor of his estate. I need to close his Brightmeadow Energy account at his flat
(12 Quarry View, account BM-209955) and arrange the final bill. The flat will be empty from the end of this
month and will eventually be sold, so nobody will be living there. His bank account has been frozen by the
bank, so I expect the next direct debits to fail - I don't want that to cause any late fees or letters
addressed to him, which my mother finds very upsetting. What documents do you need from me, and is there a
particular team or person I should speak to? Thank you for your help."""),
    it(C, HUM, N, "fitness", """I need to cancel my IronOak contract, which still has eight months left,
       because I've been diagnosed with a spinal condition and my physio has told me to stop weight
       training. I have a letter from her. Is it possible to waive the early termination fee?"""),
    it(C, HUM, U, "telecom", """I have tried to cancel my Tidewire broadband four times since moving abroad in
       June. Each time I'm told only the account holder can cancel. I am the account holder. I have now
       instructed a solicitor, but I'd rather you simply cancel the contract effective immediately and
       confirm in writing."""),
    it(C, HUM, N, "streaming", """Honestly about to cancel Reelhaven after seven years. The price has gone
       up again and half the shows I actually watch have disappeared. Before I hit cancel, give me a good
       reason to stay - otherwise I'm out at the end of the month."""),
    it(C, HUM, N, "saas", """After the three outages this month that took our invoicing offline, we'd like to
       terminate our Ledgerwick contract early and discuss a refund of the prepaid months. Please route this
       to our account manager or someone with the authority to agree terms. We'd like to talk before the end
       of the month."""),
    it(C, HUM, N, "travel", """I have to cancel our Staylark booking for next month because my husband has
       been admitted to hospital and won't be able to travel. The booking is marked non-refundable, but I'm
       hoping you might make an exception given the circumstances. I can provide a letter from the
       hospital."""),
    it(C, HUM, U, "fitness", """Please cancel my IronOak membership before tomorrow's direct debit. I know the
       policy is 30 days' notice, but I only found out this week that I'm being deployed overseas with the
       army for nine months. I can send my orders if needed."""),
    it(C, HUM, N, "food", """Congratulations Basketbee, that's five late deliveries in a row. I'm cancelling
       my annual Delivery Saver, and I expect the unused months refunded - I've paid for a whole year of a
       service you clearly can't provide."""),
    it(C, HUM, N, "streaming", """My 16-year-old signed up for Auralune Family using my saved card without
       asking me. I'd like the subscription cancelled and, if at all possible, the two months refunded, as I
       never authorised it. Happy to verify I'm the card holder."""),
    it(C, HUM, U, "electronics", """Please cancel our order of 40 Brightcoil docking stations (PO 7781) - our
       client has pulled the project. The portal says it's being packed and will leave your warehouse
       tomorrow morning, so it won't let me cancel it myself. We'd also like to avoid the restocking fee if
       at all possible."""),
    it(C, HUM, U, "fitness", """I have tried to cancel my Stridehaus Premium subscription online five times,
       and each time the final 'confirm' step shows an error. Your terms say cancellation must be done
       online. I've kept screenshots of every attempt and I've spoken to a lawyer about it, but I'd rather
       you just cancel it for me and confirm by email."""),
    it(C, HUM, N, "telecom", """I want to cancel the TV part of my Tidewire bundle but keep broadband. Also
       there's a charge on my last bill for a TV box I returned in May, and the contract end date in the app
       looks wrong to me. Could someone go through it all with me on the phone?"""),
    it(C, HUM, U, "travel", """Our flight tomorrow morning has been cancelled by the airline, so we won't make
       the trip. We need to cancel the Wayfarrow airport transfer and the first night at the hotel, but both
       show as non-refundable in the app. Can someone help us today? Booking WF-83390."""),
]

SHOTS = [
    # ---- set 1: ts01-ts08
    it(B, BOT, N, "travel", """Hi, could you send me a copy of the receipt for my Staylark stay in Porto last
       weekend? My accountant needs it and I can't find the original email. Reservation SL-2089."""),
    it(T, HUM, U, "saas", """Stackmere's API has been timing out on every request since about 10:15. Our
       order system depends on it and we've had to stop taking phone orders. Nothing on your status page.
       Please get an engineer on this."""),
    it(A, BOT, N, "food", """I can't remember my Plumtray password. Can you send me a link to reset it? Using
       the same email as always."""),
    it(S, HUM, N, "electronics", """My Lumacoil Home speaker pair arrived with the box ripped open and one of
       the two speakers missing. The seal was already broken when the courier handed it over. Please send
       the missing speaker - I don't want to return the whole set."""),
    it(C, BOT, U, "saas", """How do I cancel our Stackmere team trial before it converts to a paid plan at
       midnight tonight? We've decided to go with a different tool."""),
    it(A, HUM, U, "fintech", """I think my Pennyloom account has been hacked. I got an email saying my phone
       number was changed and I didn't do that, and now I can't log in. Please freeze it."""),
    it(B, HUM, N, "fitness", """I'm a student now and money is tight. Is there any chance of a discount on my
       Pulsefield membership? I've been a member for three years and I'd really rather not leave."""),
    it(S, BOT, N, "ecommerce", """hey where's my order? HC-30551, ordered last thursday, just want the
       tracking link. thanks in advance, no rush"""),
    # ---- set 2: ts09-ts16
    it(B, BOT, U, "utilities", """I need a copy of my latest Northmere bill as a PDF by 10am tomorrow for a
       mortgage application. Can you email it to me tonight? Account NM-30982."""),
    it(T, BOT, N, "fitness", """How do I set the Stridehaus app to show distance in kilometres instead of
       miles? Can't find it anywhere in the settings."""),
    it(A, HUM, N, "travel", """My late husband had about 60,000 miles on his Jetmarsh account. Is it possible
       to transfer them to my account? I have the death certificate and can send whatever else you need."""),
    it(S, HUM, U, "food", """My Crumbfleet order was supposed to be at our office for a client lunch at 12:30.
       It's 12:50, the driver's map has been stuck two streets away for 20 minutes and he isn't answering.
       Clients are sitting here waiting. Please help now."""),
    it(C, HUM, N, "telecom", """Tidewire wants a £180 early exit fee to cancel my contract, but I'm only
       leaving because your signal at my new address is basically zero indoors. That doesn't seem fair. Can
       the fee be waived?"""),
    it(B, HUM, U, "saas", """Plinthdesk charged our card $4,800 for 40 seats on renewal; we have 12 users.
       Our finance director has asked me to tell you we're prepared to involve our lawyers if this isn't
       reversed."""),
    it(T, HUM, N, "electronics", """My Orrin Labs Pace 2 watch battery now lasts about six hours instead of
       three days. I've reset it and turned off the always-on display. It's 14 months old, so just outside
       the warranty, but this looks like a defect to me. What are my options?"""),
    it(A, BOT, N, "streaming", """How do I turn on two-step verification for my Cinderbox account? Just want
       to make it a bit more secure."""),
    # ---- set 3: ts17-ts24
    it(S, BOT, N, "telecom", """Hi, has the replacement router Tidewire promised me been posted yet? Is there
       a tracking number I can follow?"""),
    it(C, BOT, N, "fitness", """How do I cancel my Stridehaus Premium subscription? I'll just stick with the
       free version from now on."""),
    it(T, BOT, U, "travel", """My Jetmarsh flight is at 7am tomorrow. How do I make the app show my boarding
       pass offline? The airport wifi is always terrible."""),
    it(A, HUM, U, "ecommerce", """Someone placed two orders on my Harborcart account overnight using my saved
       card and sent them to an address in another city. I didn't do this. I've already called my bank.
       Please secure my account and tell me how they got in."""),
    it(B, BOT, N, "food", """Where do I find receipts for my Crumbfleet orders? I need last month's for my
       expense report, no rush."""),
    it(S, HUM, N, "food", """Tracking for my Basketbee order says it was handed to 'a neighbour' but doesn't
       say which one, and no-one on my street has it. It was £90 of groceries. Can someone look into
       this?"""),
    it(C, HUM, U, "fitness", """My mother is in a care home now with dementia and still has a Pulsefield
       membership. I have power of attorney. Please cancel it - the next payment comes out tomorrow and she
       can't afford it."""),
    it(B, HUM, N, "fintech", """Coinwell charged me a £15 overdraft fee because a payment went out a day
       early - it was your system that moved the date, not me. Please refund the fee."""),
]


def strip(item):
    return {k: item[k] for k in ("id", "text", "topic", "handling", "urgent")}


def main():
    rng = random.Random(20260926)
    test = TEST[:]
    rng.shuffle(test)
    for i, x in enumerate(test, 1):
        x["id"] = f"tt{i:03d}"
    for i, x in enumerate(SHOTS, 1):
        x["id"] = f"ts{i:02d}"
    DATA.mkdir(parents=True, exist_ok=True)
    with open(DATA / "ticket_triage.jsonl", "w", encoding="utf-8") as f:
        for x in test:
            f.write(json.dumps(strip(x), ensure_ascii=False) + "\n")
    with open(DATA / "ticket_triage.shots.jsonl", "w", encoding="utf-8") as f:
        for x in SHOTS:
            f.write(json.dumps(strip(x), ensure_ascii=False) + "\n")
    print("test", len(test), "shots", len(SHOTS))
    print("domains", sorted(Counter(x["domain"] for x in test).items(), key=lambda kv: -kv[1]))


if __name__ == "__main__":
    main()
