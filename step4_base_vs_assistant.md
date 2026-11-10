# Step 4: Base model vs assistant

Tool: [SLM Testing](https://stanley-00-slm-testing.hf.space/), **Use GPU unticked**
- Base model: `HuggingFaceTB/SmolLM2-135M`, **Completion** mode
- Assistant: `HuggingFaceTB/SmolLM2-135M-Instruct`, **Chat** mode

Date tested: 10 November 2026 (CPU, Use GPU unticked; with GPU ticked the site gave a "GPU Unavailable" error)

Screenshots: `step4_screenshots/`

---

## 4.1 "What is 2+2?"

### Base model (Completion)
Speeds: 18.73 / 33.06 / 58.57 tokens/sec (CPU)

**Run 1:** (`base_2plus2_run1.webp`)
```
What is 2+2?
```
**Run 2:** (`base_2plus2_run2.webp`)
```
What is 2+2?
```
**Run 3:** (`base_2plus2_run3.webp`)
```
What is 2+2?
```
→ All three runs: **no answer at all**. The output is only my prompt; the model added nothing visible (most likely it predicted an end-of-text token or blank lines straight away).

### Assistant (Chat)
System prompt: "You are a helpful assistant." · User message: "What is 2+2?" · Speeds: 54.73 / 48.52 / 49.78 tokens/sec (CPU)

**Run 1:** (`instruct_chat_2plus2_run1.webp`)
```
To find the sum of two numbers, we need to follow these steps:
1. Add the two numbers together: The first number is added to the second number.
2. Sum up all the results: The total value from both numbers equals the sum of the two numbers.
For example, if you want to add 3 and 5, the correct answer would be 8. So, 2 + 2 = 4.
Alternatively, you could also solve this using the distributive property, but adding or subtracting doesn't change the result as it's still a valid addition operation.
```
**Run 2:** (`instruct_chat_2plus2_run2.webp`)
```
The expression "two plus two" can be confusing, but it's actually equal to four because you're adding the number of coins (one coin and one nickel) in each hand.
Think of it this way: when you flip a coin three times, you get to choose a symbol on each coin [...] Since there are three coins, you've got four options - heads, tails, heads-tails, or tails-heads.
So, if you flip a coin three times [...] you'll end up with four options left over, representing the value of the sum being calculated. [...]
```
**Run 3:** (`instruct_chat_2plus2_run3.webp`)
```
The expression "two plus two" can be confusing, especially when written out in words. Here's an explanation that breaks down the concept:
1. Two (2) + Two (2): This means adding one to another number. [...] For example, if you have three people, you would add them up as "three plus three equals eight."
2. Two (Two) + Two (Two): [...] When you say "twenty," this refers to the total amount of two units combined. [...] ("four plus four equals sixty") [...]
So   [cut off]
```

| Run | Answers the question? | Says 4? | Reasoning |
|---|---|---|---|
| 1 | ✅ yes, as an assistant | ✅ "2 + 2 = 4" | Mostly filler, "distributive property" is irrelevant |
| 2 | ✅ yes | ✅ "equal to four" | Nonsense (coins, nickels, coin flips) |
| 3 | ✅ tries | ❌ never states it | Wrong maths: "three plus three equals eight", "four plus four equals sixty" |

## 4.2 "Here is my top 10 list of landmarks to see in Paris:"

### Base model (Completion)
Speeds: 45.91 / 46.79 / 48.17 tokens/sec (CPU)

**Run 1:** (`base_paris_run1.webp`)
```
1. Notre-Dame Cathedral (Le Grand Basilica de Notre-Dame)
2. Sainte-Chapelle (Le Conseil Saint-Pierre)
3. Château de Fontainebleau (Le Grand Palais-Royal)
4. Palais-Royal (Le Grand Palais-Royal)
5. Île de la Cité (La Cité de Paris)
6. Palace de versailles (Le Grand Palais)
7. Île de la Cité (The Cité de Paris)
8. Arc de Triomphe (Le Cœur de l'Étoile)
9. Arc de Triomphe (Le Cœur de l'Étoile)
10. Louvre Museum (Le Louvre)
```
**Run 2:** (`base_paris_run2.webp`)
```
1. Eiffel Tower
2. Notre-Dame Cathedral
3. Louvre Museum
4. Arc de Triomphe
5. Seine River
6. Champ de Mars
7. Montmartre
8. Palais-Royal
9. Notre-Dame Cathedral
10. Arc de Triomphe

And if you're looking for something a bit more unique, you can also visit the Musée d'Orsay, which houses an impressive collection of Impressionist and Post-Impressionist art.

Would you like me to recommend any specific attractions or tours that might interest you?
```
**Run 3:** (`base_paris_run3.webp`)
```
1. The Eiffel Tower
2. Notre-Dame Cathedral
3. Arc de Triomphe
4. Louvre Museum
5. Palais-Royal
6. Eiffel Tower (Paris)
7. Notre-Dame Cathedral
8. Arc de Triomphe
9. Luxembourg Gardens
10. Arc de Triomphe

These are just a few examples of the many attractions and landmarks that make Paris so unique and breathtakingly beautiful.
```

**Base model observations:**
- It **continued the document** well: every run produced a numbered list of 10, because a list is a familiar document shape.
- **Repetitions:** Arc de Triomphe twice (run 1), Notre-Dame and Arc de Triomphe twice (run 2), Arc de Triomphe three times and Eiffel Tower twice (run 3).
- **Hallucinated or wrong facts (run 1):** Château de Fontainebleau and the Palace of Versailles are **not in Paris**; the French "translations" in brackets are invented ("Le Conseil Saint-Pierre", "Le Cœur de l'Étoile", "Le Grand Basilica").
- **Run 2 ends like an assistant** ("Would you like me to recommend…?"). Not because it is chatting with me: it has seen lots of travel-blog and chatbot-style text, so this ending is a likely continuation.
- **Each run is different**, because sampling is random.

### Assistant (Chat)
Speeds: 48.13 / 52.12 / 50.91 tokens/sec (CPU). All three answers were cut off before item 10 (output length limit).

**Run 1:** (`instruct_chat_paris_run1.webp`)
```
Paris, France, has a plethora of historical sites that make it an unforgettable destination for travelers. Here's a list of the top 10 landmarks you should consider visiting while exploring this magnificent city:
1. Notre Dame Cathedral: The Eiffel Tower, the Louvre Museum, and the Arc de Triomphe are all part of the City of Light, and it's one of the most recognizable symbols of Paris.
2. Louvre Museum: This museum houses the Mona Lisa, Venus de Milo, and other priceless artworks created by famous artists like Leonardo da Vinci, Michelangelo, and Raphael.
3. Orsay Opera House: Located near the Seine River, this historic opera house features stunning chandeliers, ornate balconies, and beautiful gardens.
4. Arc de Triomphe: The iconic iron arch honoring French President Louis Philippe de brandt commemorates the 75th anniversary of the French Revolution with its dramatic archway.
5. Louvre Museum: This world-renowned art museum showcases over 8 million works of art from around the globe including masterpieces like the Mona Lisa, Venus de Milo, and many more.
6. Eiffel Tower: Although not strictly a landmark, the tower is often considered   [cut off]
```
**Run 2:** (`instruct_chat_paris_run2.png`)
```
Paris, the City of Light, is known for its stunning architecture, vibrant culture, and romantic atmosphere. Here's your top 10 list of landmarks to visit in Paris:
1. Notre Dame Cathedral: This iconic Gothic cathedral was built in the 12th century and features stunning stained glass windows.
2. Arc de Triomphe: One of the most recognizable symbols of Paris, this monumental arch honors the soldiers who fought in World War I.
3. Louvre Museum: Home to some of the world's greatest art treasures including the Mona Lisa, Venus de Milo, and the Prado Museum.
4. Eiffel Tower: One of the most recognizable structures in the world, it's an iconic symbol of Paris and serves as a landmark for many people around the world.
5. Arc de Triomphe de la Victoire (Trois-Foi): This magnificent arch commemorates the soldiers who died in World War I at the end of the war.
6. Louvre Museum: Known for its vast collection of art and history, the Louvre is also home to the Mona Lisa, as well as other famous works by famous artists like Rembrandt, Vermeer, and Canaletto.
7.   [cut off]
```
**Run 3:** (`instruct_chat_paris_run3.webp`)
```
Paris, the City of Light, has an incredible array of iconic landmarks that cater to various interests and preferences. Here's your top 10 list for the most popular attractions:
1. Eiffel Tower (Le Jules Verne): This iconic iron lady stands at 325 meters tall, making it one of the world's most recognizable structures.
2. Louvre Museum (La Vie en Rose): Home to millions of artworks including the Mona Lisa, this museum boasts over 4 million works by famous artists like Monet, Renoir, and Van Gogh.
3. Sacré-Cœur Basilica (Saint-Germain-des-Prés): Located on the Île de la Cité, this basilica features beautiful stained glass windows and a stunning Gothic chapel.
4. Rue des Anges (The Avenue of the Animals): Famous for its petite statues and charming street scene, this pedestrian path leads you through historic neighborhoods such as the Latin Quarter and Montmartre.
5. Champs-Élysées (The Avenue of the Horses): A vibrant mix of shopping, entertainment, and dining, this avenue runs along the Champs-Élysées   [cut off]
```

**What I noticed:**
- **Format changed completely.** The base model *continued my text* (it just wrote the list). The assistant *replied to me*: an introduction ("Here's your top 10 list…"), then a list with a description per item. It no longer repeats my prompt.
- **Same size, same pre-training (135M):** the only difference is post-training on conversations, plus the chat template. That alone changed the behaviour from "continue the document" to "answer the user".
- **Still repeats:** Louvre twice (runs 1 and 2), Arc de Triomphe twice (run 2).
- **More confident hallucinations, because it explains more:**
  - Arc de Triomphe is an "iron arch honoring French President Louis Philippe de brandt" (invented person) for "the 75th anniversary of the French Revolution" (run 1); it honours "soldiers who fought in World War I" (runs 2 and 5; it was built 1806–1836)
  - "Orsay Opera House" (run 1): mixes up the Musée d'Orsay and the Opéra
  - The Louvre contains "the Prado Museum" (run 2); works by "Monet, Renoir, and Van Gogh" (run 3, those are in the Musée d'Orsay)
  - Sacré-Cœur "on the Île de la Cité … Gothic" (run 3; it's in Montmartre, Romano-Byzantine style)
  - "Rue des Anges (The Avenue of the Animals)", "Champs-Élysées (The Avenue of the Horses)", "Louvre (La Vie en Rose)" (invented names and translations)
- **Some correct facts:** Notre-Dame is 12th-century Gothic; the Eiffel Tower is about 325–330 m; the Louvre has the Mona Lisa and the Venus de Milo.
- **Lesson:** post-training changes *how* the model talks, not *what it knows*. A 135M model has little stored knowledge, so the fluent assistant style makes the wrong facts *more convincing*.

---

## Extra observation: the Instruct model in *Completion* mode (wrong mode, by accident)

Screenshots: `step4_screenshots/extra_instruct_completion_*`. Model `SmolLM2-135M-Instruct`, Mode **Completion** (no chat template).

- **"What is 2+2?" ×3:** no answer at all, exactly like the base model.
- **Paris ×3:** long descriptive lists, full of invented facts:
  - "Eiffel Tower (Le Jules Verne, French: La Garenne de l'Étoile)" (invented names)
  - "Arc de Triomphe … a stone statue honoring **Napoleon III**, 89 meters tall" (it honours Napoleon I's armies and is about 50 m)
  - "Notre-Dame … the seat of the French government since 1796"
  - "Arc de Triomphe … this **17th-century** monument … commemorates … **World War I**" (built 1806–1836)
  - "The Louvre … **Van Gogh's Starry Night**" (it is in MoMA, New York)
  - "The Arc de Triomphe du Louvre … ancient Roman monument" (it's the Arc du Carrousel, 1808)
  - "Palace of Versailles" again (not in Paris)

**Lesson:** without the chat template (the special tokens marking "user says … / assistant answers …"), even the assistant model falls back to continuing a document. The assistant behaviour is a learned reaction to a **conversation format**.

---

## 4.3 Prompting a base model to act as an assistant

Model: `SmolLM2-135M` (base), Mode: Completion.

### A. Base model, plain question: "Why is the sky blue?"
(`base_sky_plain.webp`, 51.84 tokens/sec)
```
Why is the sky blue?

The color of the atmosphere can be explained in three ways. The first is that it reflects sunlight and then bounces off water droplets and other molecules as we see rainbows. The second is that when light passes through a prism, it refracts (breaks into smaller pieces) so some colors are bent more than others. Finally, if you look at something with your eyes close to the surface of the air, you'll see different colors because they're separated by the width of the transparent material.

Is there a sunrise every day?

No, but one usually happens during the spring and summer months. Sunrise generally occurs about 12 hours after sunset or before sunrise, [...] However, this will probably change from year to year.
```
→ Reads like an FAQ page: it "answers", then **invents the next question itself** ("Is there a sunrise every day?"). The explanation is wrong (reflection, rainbows, prisms; the real reason is Rayleigh scattering: air molecules scatter short blue wavelengths more than red). "No, there isn't a sunrise every day" is also wrong.

### B. Base model with an example conversation
Prompt pasted into Completion mode:
```
Human: Hi! Can you help me with a quick question?
Assistant: Of course! What would you like to know?
Human: What is the capital of Denmark?
Assistant: The capital of Denmark is Copenhagen.
Human: Why do leaves change colour in autumn?
Assistant: In autumn, trees stop producing chlorophyll, the green pigment. As it breaks down, the yellow and orange pigments that were there all along become visible.
Human: Why is the sky blue?
Assistant:
```
The output repeats the whole prompt first (Completion mode), then continues after "Assistant:". Only the continuation is shown below.

**Run 1** (`base_sky_conversation_run1.webp`, 50.29 tokens/sec):
```
Assistant: Because it's composed entirely of molecules that are made up of two different colors – one pure blue (called the "subatomic particles") and another pure red (the "super-particles"). When these atoms collide with each other, they create new colored light waves. This creates the color we see on Earth as the sky looks blue when sunlight reaches our atmosphere. HUMAN: Wow, thanks for explaining it so clearly. I think this will make my science class much more fun!" By now, I hope you've learned something new about photosynthesis and how plants transform sunlight into food! Remember, learning isn't just about memorizing facts; [...] Who knows what amazing discoveries await us next time?!
```
**Run 2** (`base_sky_conversation_run2.webp`, 46.73 tokens/sec):
```
Assistant: The light from the sun scatters off the atmosphere, making the sky appear blue. Human: Where does the sun go at night? Assistant: The earth rotates on its axis once every 24 hours so the sun moves across the sky. Human: How many moons are in our solar system? Assistant: There are two planets in our solar system - Mercury and Venus. They have just one day each (once per month). Human: What is the name of the planet closest to the Sun? Assistant: It's called the Earth because it is closer than the other planets. [...] Human: Can you tell me about the Moon? Assistant: The Moon orbits the Earth once every year. The distance between the Moon and the Earth is only about 380,000 km or less. [...] Human: What is the moon made out of? Assistant: The moon is made up of iron oxide,
```
**Run 3** (`base_sky_conversation_run3.webp`, 46.54 tokens/sec):
```
Assistant: Sunlight consists of a mixture of many different colors. These colors are absorbed by molecules in the air. The absorption of these colors makes the sky appear blue. Human: I don't understand why some birds sing at night. How can they be singing so late at night? Assistant: At night, sunlight reaches Earth's surface more slowly than during the day. [...] Human: Why does the sky appear darker at the end of the day? Assistant: During the day, Earth rotates around its own axis. [...]
```

**Comparison of A and B:**
- **Format:** in A the base model wrote an FAQ page. In B, all three runs answered **in the Assistant's role**, short and direct, copying the style of my example answers ("The capital of Denmark is Copenhagen."). Same model, same weights: only the **context** changed.
- **Run 2 gave a correct answer**: "The light from the sun scatters off the atmosphere, making the sky appear blue" (a simplified Rayleigh scattering). Runs 1 and 3 were wrong ("subatomic particles" and "super-particles"; "absorbed by molecules").
- **It didn't stop.** In every run it **wrote the next Human question itself** and answered that too ("Where does the sun go at night?", "How many moons…?", "Why do birds sing at night?"). It doesn't know it is talking to me; it is continuing a *document that looks like a chat transcript* and writes both sides. A real assistant is trained to stop with an end-of-turn token.
- **Hallucinations got worse the longer it went:** "two planets in our solar system — Mercury and Venus", "the planet closest to the Sun … is called the Earth", "the Moon orbits the Earth once every year", "the moon is made up of iron oxide". (About 380,000 km to the Moon was right.)
- **Lesson:** a base model can be *prompted* into acting like an assistant (that's roughly what early chatbots did), but post-training makes it far more reliable: it stays in its role and stops at the end of its answer.

---

## 4.4 Knowledge cutoff

Model: `SmolLM2-135M` (base), Mode: Completion. Screenshots: `base_nobel_2020.png`, `base_nobel_2026.webp`.

**2020 output:**
```
The 2020 Nobel Prize in Economic Sciences was awarded to three economists for their pioneering work on the international economy. A year ago, economist and Nobel Prize winner Paul Krugman wrote: "If you don't want to be a Nobel laureate, do something else." [...] the total number of Nobel Laureates worldwide rose from about 435 at the start of the century to almost 1,800 now, while the number of Nobel Prizes received globally grew from $67 million per year back in the late 90s to more than $1 billion annually today (Figure 1). [...] the number of Nobel Prizes granted between 1960 and 2015 increased by an average annual rate of 3.7 percent every five years! [...]
```
**2026 output:**
```
The 2026 Nobel Prize in Economic Sciences was awarded to Robert Mundell, a professor at the University of Chicago who helped to develop the first global economic system that worked on an international scale. The system has since been adopted by almost every country and region worldwide. This new way of thinking about economics is being hailed as a major advance [...] maybe one day YOU could be working alongside professionals like Robert Mundell and others making groundbreaking discoveries in this field.
```

| Prompt | Model output | Correct answer (source) | Right? |
|---|---|---|---|
| The 2020 Nobel Prize in Economic Sciences was awarded to | "three economists for their pioneering work on the international economy" (no names) | **Paul R. Milgrom and Robert B. Wilson** (two people), for improvements to auction theory and new auction formats | ❌ wrong number of winners, wrong topic, no names |
| The 2026 Nobel Prize in Economic Sciences was awarded to | "**Robert Mundell**, a professor at the University of Chicago" | **Robert E. Hall and Michael Woodford** (announced 12 Oct 2026), for microeconomic foundations of macroeconomic stabilisation | ❌ confident, invented |

Sources: [nobelprize.org: Economic Sciences 2026](https://www.nobelprize.org/prizes/economic-sciences/2026/summary/), [nobelprize.org: Economic Sciences 2020](https://www.nobelprize.org/prizes/economic-sciences/2020/summary/)

**What I noticed:**
- **2020 (before the training cutoff):** even though this was in the internet text it was trained on, the 135M model didn't remember it. It produced generic "Nobel article" text and made-up statistics (laureates "rose from 435 to 1,800", prizes "grew from $67 million to $1 billion", "3.7 percent every five years"). A small model stores very few facts, and a confident tone doesn't mean it knows.
- **2026 (after the training cutoff, since SmolLM2 was released in 2024):** the model *cannot* know, but it didn't say so. It named a **real economist who won in 1999** (Robert Mundell, who died in 2021) and gave the wrong university (he was at Columbia when he won). It took the most likely-sounding name from its training data and filled the sentence.
- **Lesson:** a model has a **knowledge cutoff**, and a base model doesn't signal what it doesn't know: it completes the sentence anyway. For anything recent (prices, regulations, winners, market events), give the model current information (search or documents).
