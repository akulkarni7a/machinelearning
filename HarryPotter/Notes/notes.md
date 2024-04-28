I first split by words because I wanted to generate a sentence. But then I struggled with not beint entirely sure how to put stop and end tokens. 

But it was a bit challenging to figure out how to label stop and start - so I'm splitting by paragraph. 

But! it can't be paragraph because every paragraph is a new item in the vocabulary - there's zero overlap

And... turns out, that's expected. I need to use MLP/


MLP
- removed punctuation and lower cased everything this made vocab more manageable
- [](./1.png) --> forgot to turn it into ints!
- wasn't entirely sure how to create stop tokens. maybe i'll do new lines next implementation
- block size of 3 is so hard for it to keep any persistent memory
- but was able to handle so much more than bag of words method