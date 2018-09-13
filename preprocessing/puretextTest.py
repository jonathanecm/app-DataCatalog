from lxml import etree

with open('../data/some.txt', 'r', encoding='utf-8') as f:
    text = f.read()

def unique(list_in): 
    #Initialize an empty list
    list_out = [] 
    
    #Traverse all elements, check if exists
    for i in list_in: 
        if i not in list_out: list_out.append(x)
            
    return list_out

#'pixnet.net'
doc = etree.HTML(text)
finder = etree.XPath('//*[@class="article-content-inner"]/descendant::p/descendant::text()')
result = unique(finder(doc))

for i in result:
    if i.strip() != '': print(i.strip())
    print(etree.tostring(i, pretty_print=True, method="html", encoding='unicode'))