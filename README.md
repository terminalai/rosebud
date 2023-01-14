# Rosebud

Coding our very own AI Trivia-izer.

## Algorithm

We get a "conversation" block of roughly 15 seconds --> ~25 words

E.g.

```js
A: I heard the JWST recently found an exoplanets, that's cool.
B: You're right, it is cool. Very cool :).
A: Imagine if it finds life!
B: I want aliens.
```

This is encoded into a corpus (via the Google's Speech Recognition) as the following:

```js
I heard the JWST recently found an exoplanets, that's cool. You're right, it is cool. Very cool :). Imagine if it finds life! I want aliens.
```

We now utilise **keyword extraction** algorithms (utilising an open-source library known as [KeyBert](https://github.com/MaartenGr/KeyBERT)). The algorithm outputs $n$ keywords, with their respective probabilities, $p_i$. For now, under the pre-testing process, we use $n = 5$, as this is a good standard for our project.

Once we have the 5 keywords, we perform a very simple Google Search, and take the top few results. Scraping these websites, we get a good corpus of data that is useful for our codebase. We then use an algorithm to identify texts relating to the topics (keywords). This text is summarised and outputted in the form of a wav audio with Google's TTS.

This audio is played, and that's it.