import re
CONS=set("കഖഗഘങചഛജഝഞടഠഡഢണതഥദധനപഫബഭമയരറലളഴവശഷസഹ")
INDV=set("അആഇഈഉഊഋഎഏഐഒഓഔ")
CHILLU=set("ൺൻർൽൾ")
def eng_syl(w):
    w=w.lower(); g=re.findall(r"[aeiouy]+",w)
    n=max(1,len(g))
    if w.endswith("e") and n>1 and not w.endswith(("le","ee")): n-=1
    return n
NUM={"1916":5,"1970":5,"737":5,"777":5,"380":4,"251":4,"2021":5,"100":2,"4":1,"2":1}
def syl(text):
    n=0
    for tok in re.findall(r"\d+|[A-Za-z]+|[ഀ-ൿ]+",text):
        if tok.isdigit(): n+=NUM.get(tok,max(1,len(tok)))
        elif re.match(r"[A-Za-z]",tok): n+=eng_syl(tok)
        else:
            c=sum(1 for ch in tok if ch in CONS)-tok.count("്")+sum(1 for ch in tok if ch in INDV)+sum(1 for ch in tok if ch in CHILLU)
            # word-final virama (ആണ്, ന്റെ) already removed above; each remaining consonant carries a vowel
            n+=max(c,1)
    return n
