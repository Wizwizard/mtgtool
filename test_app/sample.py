import CONSTANT
import re

s = "Mono Red Aggro by laurent delade "

l = []
l.append(s)

for keyword_US_CN in CONSTANT.keywords_US_CN:
    s = re.sub(keyword_US_CN[0] + " ", keyword_US_CN[1], s, flags=re.IGNORECASE)

print(s)

