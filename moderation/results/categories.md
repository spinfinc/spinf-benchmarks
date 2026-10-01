## Per category

spinf/moderation 0.1.1: each category score against public category labels. AUROC: positives = texts with the label, negatives = every other text of the dataset (other harm categories included). Recall at default: the share of positives flagged at the category's default threshold (it flags 0.5% of everyday content). 14,504 texts, 24,888,555 billed tokens.

| Category | AUROC (mean) | Dataset (label): positives, AUROC, recall at default |
|---|---|---|
| Gibberish (synthetic test set) | **0.999** | synthetic gibberish (gibberish): 300, 0.999 |
| Self-harm and suicide | **0.958** | OpenAI moderation (SH): 51, 0.991, 100%<br>BeaverTails (self_harm): 19, 0.959, 84%<br>Aegis 2.0 (Suicide and Self Harm): 189, 0.924, 46% |
| Spam and advertising (reported only) | **0.950** | Deysi spam detection (spam): 498, 0.996<br>YouTube comment spam (spam): 1005, 0.936<br>SMS Spam Collection (spam): 747, 0.919 |
| Weapons | **0.942** | Aegis 2.0 (Guns and Illegal Weapons): 155, 0.942, 40% |
| Sexual content | **0.923** | OpenAI moderation (S): 237, 0.987, 96%<br>BeaverTails (sexually_explicit,adult_content): 100, 0.974, 78%<br>Civil Comments (sexual_explicit): 253, 0.866, 38%<br>Aegis 2.0 (Sexual): 251, 0.864, 37% |
| Gore and graphic violence | **0.922** | BeaverTails (animal_abuse): 44, 0.940, 43%<br>OpenAI moderation (V2): 24, 0.903, 62% |
| Child sexual exploitation and grooming | **0.892** | Aegis 2.0 (Sexual (minor)): 123, 0.930, 66%<br>BeaverTails (child_abuse): 27, 0.886, 52%<br>OpenAI moderation (S3): 85, 0.859, 38% |
| Hate against protected groups | **0.873** | OpenAI moderation (H): 162, 0.922, 69%<br>BeaverTails (discrimination,stereotype,injustice): 163, 0.915, 53%<br>Aegis 2.0 (Hate/Identity Hate): 279, 0.896, 32%<br>Civil Comments (identity_attack): 331, 0.848, 52%<br>BeaverTails (hate_speech,offensive_language): 174, 0.783, 33% |
| Violence and threats | **0.860** | Civil Comments (threat): 335, 0.937, 52%<br>OpenAI moderation (V): 94, 0.920, 47%<br>OpenAI moderation (H2): 41, 0.912, 51%<br>Aegis 2.0 (Threat): 62, 0.848, 66%<br>Aegis 2.0 (Violence): 371, 0.806, 47%<br>BeaverTails (violence,aiding_and_abetting,incitement): 368, 0.737, 40% |
| Hacking and malware | **0.858** | Aegis 2.0 (Malware): 88, 0.858, 64% |
| Illegal drugs | **0.857** | Aegis 2.0 (Controlled/Regulated Substances): 186, 0.904, 36%<br>BeaverTails (drug_abuse,weapons,banned_substance): 113, 0.809, 43% |
| Private personal information | **0.841** | BeaverTails (privacy_violation): 103, 0.912, 69%<br>Aegis 2.0 (PII/Privacy): 143, 0.769, 53% |
| Harassment and bullying | **0.824** | OpenAI moderation (HR): 76, 0.949, 46%<br>Aegis 2.0 (Harassment): 236, 0.861, 8%<br>Civil Comments (insult): 1022, 0.662, 10% |
| Extremism and terrorism | **0.820** | BeaverTails (terrorism,organized_crime): 43, 0.820, 7% |
| Profanity | **0.808** | Aegis 2.0 (Profanity): 323, 0.818, 48%<br>Civil Comments (obscene): 211, 0.799, 44% |
| Fraud and scams | **0.808** | Aegis 2.0 (Fraud/Deception): 137, 0.808, 40% |
| Other crime | **0.753** | Aegis 2.0 (Criminal Planning/Confessions): 827, 0.895, 73%<br>BeaverTails (financial_crime,property_crime,theft): 140, 0.842, 81%<br>Aegis 2.0 (Illegal Activity): 174, 0.521, 13% |

Topics (alcohol, tobacco and vaping, gambling, medication) are scored but not calibrated: no public labels yet.
