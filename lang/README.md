# Solidity DSL for ERC-20, ERC-721 and ERC-1155

## Getting started

```bash
cd src
```

```bash
python main.py 'echo "123asdasdas";'
```

## Discussion Notes

Da li podrzavamo vise contracta? _i dalje otvoreno pitanje_

- okej je da on napravi vise, tako sto ce imati razlicite nase skripte
- da li mu je bitno da moze da reuse?

Sta zelimo da uradimo?

- pomazemo ljudima koji hoce da kreiraju contracte (tokene)
- njegova odgovornost je da distribuira contract
- nas cilj je da kreiramo "laicki" jezik koji se lako moze citati i razumeti
- cilj je pokriti razlicite usecaseove koje smo naveli
- cilj je implementirati grupe tipova funkcionalnosti (module) i podrzati njihovo proizvoljno kombinovanje

#### Primeri use-cases:

- Los primer: zato sto mu ne treba contract
- ja sam kolekcionar online umetnickih dela - hocu da kupim fejk sliku monalize - nasao sam je na marketu za 120 dolara

Korisnici:

- umetnici

  - ja sam digitalni fotograf - hocu radove da convert u NFT - ne znam nista znam samo da slikam
  - ja sam narkoman - povremeno napravim depresivna umetnicka dela - hocu da ih unovcim
  - ja sam 3D umetnik - povremeno napravim neke freestyle projekte - hocu da unovcim doticne

- <_rec za nemoralne ljude bez morala_>

  - ja sam online influenser i celav sam - cuo sam za BITCONNECT - hocu da napravim podjednako dobar scam
  - ja sam coinmaster - imam ideju kako da reklamiram i napravim community oko novog coina - $$$ hocu da to uradim brzo i jednostavno $$$
  - ja sam vlasnik jakog brenda - brend je premium i dosta ljudi ga prati - zelim da ojacam svoj brend i zaradim jos $$$

- biznismeni

  - ja sam kreator igrice - igrica ima razlicite stvari - zelim da omogucim ljudima da ih uzmu i "_poseduju_"
  - ja sam kreator/vlasnik odredjenih NFT-a - imam problem sa odredjivanjem cene za iste - zelim da napravim contract za aukciju doticnih tokena
  - ja sam ENTERPRENEUR - treba mi para za fejk ideju za novi biznis - zelim da uzmem pare od ljudi a ne od bogatih <_rec za <b>uspesne</b> ljude koji imaju puno para_>, pardon andjela
  - ja sam investitor - prepoznao sam potencijal u odredjenom NFTu - zelim da imam udeo u njemu KAKO BIH NAPRAVIO OPTIMALNU STRATEGIJU RISK MANAGEMENTA
  - ja sam NFT agencija - ja preprodajem NFT-ove, tako sto se dogovorim sa vlasnikom da ga prodam u njegovo ime - zelim da imam jednokratni udeo _u prodaji_
