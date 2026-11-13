# Results: before

Corpus `HealthWellnessGuide.txt`, 21 chunks, k=3.

| # | Question | Chunks (score) | Pass | What went wrong, where |
|---|---|---|---|---|
| 1 | How many chapters are there in this text | 3 (0.25), 14 (0.24), 0 (0.22) | ❌ | retrieval — k=3 sees only 3 chunks, but chapter headings span the whole corpus. Answered "at least 17" (correct: 21). Not fixable by search |
| 2 | Summarize Chapter 6 for me | 14 (0.33), 17 (0.31), 3 (0.31) | ❌ | retrieval — top hit chunk 14 matched "6" in "PART 6: COMMON HEALTH CONCERNS", not Chapter 6. Hydration chunks (5–6) not retrieved; model confidently summarized the wrong chapter |
| 3 | What types of stressors exist | 10 (0.45), 9 (0.42), 18 (0.36) | ✅ | clean refusal — guide doesn't list types of stressors |
| 4 | Can stress be cured | 10 (0.52), 9 (0.50), 11 (0.42) | ❌ | model — said the guide doesn't cover cures, then answered anyway with stress management. Partial answer, not the refusal the prompt asks for |
| 5 | I pray a lot. Does that help? | 11 (0.28), 19 (0.26), 15 (0.25) | ❌ | model — used outside knowledge ("prayer may offer similar benefits" to meditation); prompt forbids external knowledge |
| 6 | I do a lot of online volunteering. I do it like 15 hrs. That should be good, right? | 18 (0.28), 3 (0.26), 20 (0.24) | ❌ | model — endorsed "online volunteering is good"; guide only says volunteer in your community and gives no hours. Did not question the 15 hrs |
| 7 | I have finished both seasons of Black Doves but am not exhausted like u said I would | 16 (0.16), 6 (0.14), 17 (0.13) | ✅ | clean refusal; low scores (≤0.16) show nothing relevant was retrieved |
| 8 | When I go to the gym., I do a whole body workout instead of targeted muscles. Does that work | 3 (0.42), 2 (0.37), 0 (0.33) | ❌ | model — concluded whole-body workouts "can be effective"; the guide doesn't say this. Inferred beyond context |
| 9 | Tell me if going 2-3 days for 30min is better or 1 day for 1.5 hrs | 7 (0.28), 5 (0.24), 3 (0.23) | ❌ | retrieval — top hit chunk 7 matched "1.5 hrs" to sleep "cycles of about 90 minutes". Chunk 0 (150 min/week, the fact needed) not retrieved |
| 10 | Should I go to Gold's Gym or Pure Gym | 0 (0.26), 3 (0.26), 2 (0.25) | ✅ | clean refusal — gym brands not covered |

**Score: 3/10.**

- **Retrieval failures (Q1, Q2, Q9):** the right chunk was never retrieved. Q2 and Q9 matched on surface tokens ("6", "90 minutes") rather than meaning.
- **Model failures (Q4, Q5, Q6, Q8):** relevant-looking chunks were retrieved (scores 0.28–0.52), and the model inferred or used outside knowledge instead of refusing or saying what the guide doesn't cover.
- **Passes (Q3, Q7, Q10):** clean refusals.

A score threshold would not fix any of these: the over-answered questions score as high as genuine matches, and the low-scoring ones (Q7, Q10) already refuse. The largest group is the model going beyond the context, so a prompt rewrite targets the most failures (Q4, Q5, Q6, Q8).

## Answers

### Q1: How many chapters are there in this text

The provided context mentions chapters up to Chapter 17, so there are at least 17 chapters in this text. [chunk 3], [chunk 14], [chunk 0]

**Retrieved:**

- `[chunk 3] repeat 10 times. Chapter 3: Building a Workout Routine Start... (score 0.247)`
- `[chunk 14] 6: COMMON HEALTH CONCERNS Chapter 16: Managing Headaches Nat... (score 0.241)`
- `[chunk 0] The Personal Wellness Guide A Comprehensive Resource for Hea... (score 0.222)`

### Q2: Summarize Chapter 6 for me

Chapter 6 covers common health concerns, focusing on managing headaches naturally and digestive health. Headaches are often triggered by dehydration, stress, poor sleep, skipped meals, eye strain, weather changes, and certain foods like alcohol and processed meats. Natural remedies include staying hydrated, applying cold or warm compresses, resting in a dark room, gentle massage, using peppermint or lavender essential oils, moderate caffeine intake, and maintaining a regular sleep schedule. For digestive health, supporting the gut microbiome is important for immunity, mental health, and nutrient absorption. Recommendations include eating fiber-rich foods (25-35 grams daily), staying hydrated, consuming probiotic foods like yogurt and sauerkraut, and eating slowly. [chunk 14]

**Retrieved:**

- `[chunk 14] 6: COMMON HEALTH CONCERNS Chapter 16: Managing Headaches Nat... (score 0.328)`
- `[chunk 17] - Physical health declining Strategies for better balance: -... (score 0.315)`
- `[chunk 3] repeat 10 times. Chapter 3: Building a Workout Routine Start... (score 0.311)`

### Q3: What types of stressors exist

The provided context does not specify different types of stressors. It explains that stress is the body's response to any demand or threat and mentions some physical and mental symptoms of stress, but it does not categorize or list types of stressors. Therefore, I don't have information about types of stressors in my knowledge base.

**Retrieved:**

- `[chunk 10] gement involves both immediate relief techniques and long-te... (score 0.447)`
- `[chunk 9] Insomnia (CBT-I) - Relaxation techniques like progressive mu... (score 0.419)`
- `[chunk 18] y - Join clubs or groups aligned with your interests - Volun... (score 0.356)`

### Q4: Can stress be cured

The context does not state that stress can be "cured," but it explains that stress management involves both immediate relief techniques and long-term lifestyle changes to reduce and manage stress effectively. Immediate relief methods include deep breathing, progressive muscle relaxation, grounding techniques, walking, and listening to calming music. Long-term strategies include regular exercise, adequate sleep, social support, time management, setting boundaries, engaging in hobbies, and limiting news and social media consumption. Additionally, mindfulness and meditation practices can help reduce stress and improve emotional regulation [chunk 9, chunk 10, chunk 11].

**Retrieved:**

- `[chunk 10] gement involves both immediate relief techniques and long-te... (score 0.523)`
- `[chunk 9] Insomnia (CBT-I) - Relaxation techniques like progressive mu... (score 0.503)`
- `[chunk 11] Regular mindfulness practice has been shown to reduce stress... (score 0.416)`

### Q5: I pray a lot. Does that help?

The context does not specifically mention prayer, but it does highlight that mindfulness practices, which involve focused attention and emotional regulation, can reduce stress and improve focus [chunk 11]. Since prayer can be a form of focused attention or meditation for many people, it may offer similar benefits in terms of stress reduction and emotional well-being. However, the provided information does not explicitly address prayer.

**Retrieved:**

- `[chunk 11] Regular mindfulness practice has been shown to reduce stress... (score 0.276)`
- `[chunk 19] media feeds for positivity APPENDIX: QUICK REFERENCE GUIDES ... (score 0.257)`
- `[chunk 15] mental health, and nutrient absorption. Supporting digestive... (score 0.247)`

### Q6: I do a lot of online volunteering.  I do it like 15 hrs. That should be good, right?

The context suggests that volunteering in your community is a positive activity for building connections and well-being [chunk 18]. However, it also highlights the importance of balancing technology use to avoid negative health impacts such as anxiety, decreased in-person social interaction, and reduced productivity [chunk 18]. Since your volunteering is online and involves significant screen time (15 hours), it is important to practice digital wellness strategies like setting specific times for online activities, taking regular breaks, and creating tech-free zones to maintain your overall health [chunk 18]. So, while online volunteering is good, ensure you manage your screen time and digital wellness to avoid negative effects.

**Retrieved:**

- `[chunk 18] y - Join clubs or groups aligned with your interests - Volun... (score 0.284)`
- `[chunk 3] repeat 10 times. Chapter 3: Building a Workout Routine Start... (score 0.258)`
- `[chunk 20] cklist: - 8 glasses of water - 5+ servings of fruits/vegetab... (score 0.241)`

### Q7: I have finished both seasons of Black Doves but am not exhausted like u said I would

I don't have information about Black Doves or its effects on exhaustion in my knowledge base.

**Retrieved:**

- `[chunk 16] plenty of fruits and vegetables - Exercise regularly but mod... (score 0.156)`
- `[chunk 6] on is to drink 8 glasses (64 ounces) of water daily, though ... (score 0.144)`
- `[chunk 17] - Physical health declining Strategies for better balance: -... (score 0.134)`

### Q8: When I go to the gym., I do a whole body workout instead of targeted muscles. Does that work

The context does not explicitly address whether doing a whole body workout instead of targeting specific muscles works. However, it emphasizes starting slowly, gradually increasing intensity, and including a variety of exercise types (aerobic, strength training, flexibility, and balance) for a well-rounded routine [chunk 0, chunk 3]. This suggests that a balanced approach, which could include whole body workouts, is beneficial. 

For more specific guidance, the context recommends muscle-strengthening activities on 2 or more days per week but does not specify if whole body or targeted workouts are better [chunk 0]. 

So, whole body workouts can be effective as part of a balanced routine, especially for beginners or general fitness. 

[chunk 0, chunk 3]

**Retrieved:**

- `[chunk 3] repeat 10 times. Chapter 3: Building a Workout Routine Start... (score 0.423)`
- `[chunk 2] chest while keeping the other foot flat. Hold for 15-30 seco... (score 0.372)`
- `[chunk 0] The Personal Wellness Guide A Comprehensive Resource for Hea... (score 0.335)`

### Q9: Tell me if going 2-3 days for 30min is better or 1 day for 1.5 hrs

The context does not provide a direct comparison between exercising 2-3 days for 30 minutes versus 1 day for 1.5 hours. However, it suggests starting a workout routine with shorter, more frequent sessions (e.g., 15-30 minutes on multiple days) and gradually increasing intensity and duration over time [chunk 3]. This implies that spreading exercise over multiple days may be more beneficial for building a routine and progressive overload than doing a single long session.

**Retrieved:**

- `[chunk 7] t. Sleep occurs in cycles of about 90 minutes, alternating b... (score 0.279)`
- `[chunk 5] l planning saves time, reduces stress, and helps maintain a ... (score 0.238)`
- `[chunk 3] repeat 10 times. Chapter 3: Building a Workout Routine Start... (score 0.233)`

### Q10: Should I go to Gold's Gym or Pure Gym

I don't have information about Gold's Gym or Pure Gym in my knowledge base.

**Retrieved:**

- `[chunk 0] The Personal Wellness Guide A Comprehensive Resource for Hea... (score 0.260)`
- `[chunk 3] repeat 10 times. Chapter 3: Building a Workout Routine Start... (score 0.258)`
- `[chunk 2] chest while keeping the other foot flat. Hold for 15-30 seco... (score 0.248)`
