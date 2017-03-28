from nltk.tag import pos_tag

sentence = "forever angry that gh ruined molly and morgan's bond/friendship"
tagged_sent = pos_tag(sentence.split())
# [('Michael', 'NNP'), ('Jackson', 'NNP'), ('likes', 'VBZ'), ('to', 'TO'), ('eat', 'VB'), ('at', 'IN'), ('McDonalds', 'NNP')]
print tagged_sent
propernouns = [word for word,pos in tagged_sent if pos == 'NNP']

print propernouns