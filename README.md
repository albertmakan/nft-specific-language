# JSD za definisanje Smart Contract-a za rad sa Tokenima

## Uvod

Domen navedenog JSD-a je izrada smart contract-a za definisanje i rad sa tokenima. Pod tokenima se misli na bilo koji vid digitalnih sredstava, odnosno onoga što predstavlja vlasništvo nad fizičkim ili virtuelnim objektom, ne uzimajući u obzir L1 i L2 tokene (nativne kriptovalute), već fokus u potpunosti staviti na L3 rešenja. Dakle, fokusiraćemo se na razvoj JSD-a koji pomaže domenskim ekspertima, u našem slučaju osobama koje se bave razvojem smart contract-a, prilikom implementacije contract-a koji mogu da definišu, dokažu i menjaju vlasništvo nad nekim objektom, odnosno predstavljaju digitalno sredstvo.

## Opis projekta

Za početak, razvićemo JSD za definisanje NFT-a (non-fungible tokens), koji se prevodi na Solidity programski jezik. Standard za definisanje takvih smart contract-a već postoji: `ERC-721`, tako da ćemo podržati rad sa njim, uz moguća proširenja za određene slučajeve korišćenja. Ciljni jezik na koji se naš JSD prevodi jeste Solidity, ali ćemo omogućiti i podršku za direktno prevođenje na Ethereum bytecode (korišćenjem solc - solidity compiler-a). U tom slučaju, JSD bi se preveo na Solidity i odmah nakon toga na Ethereum bytecode.

U zavisnosti od toga koliko je zahtevna implementacija prethodno navedenog, i ukoliko budemo uvideli da ima smisla proširiti domen, bismo takođe podržali i `ERC-20` standard za rad sa tokenima čija vrednost može biti procenjena (fungible), i takođe podržali i najnoviji standard `ERC-1155` koji uzima najbolje od dva prethodno navedena standarda, i podržava rad sa semi-fungible tokenima.

## Članovi tima

- [R2 21/2022 Albert Makan](https://github.com/albertmakan)
- [R2 23/2022 Miloš Panić](https://github.com/panicmilos)
- [R2 24/2022 Dragana Filipović](https://github.com/draganaf)
- [R2 27/2022 Luka Bjelica](https://github.com/bjelicaluka)
