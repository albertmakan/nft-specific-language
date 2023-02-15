# package se definise unutar naseg jezika -> jezik to podrzava
# logika/specificne stvari u packageu se definisu pomocu Sol synt
# za pocetak znamo kako hocemo da izgleda krajnji Sol rezultat packagea
# njega cemo hardcodovati za pocetak
# posle cemo praviti podrsku za definisanje novih packagea jer je to manje bitno 

# Prva opcija - definisemo "exporte" paketa
# odnosno, definisemo public deo paketa
package {
  pulbic nesto(): uint256;
}

# Drgua opcija - nasa alatka moze da razume Solidity Interfejse
# tako da svaki sol interfejs jeste zapravo i public deo paketa
# odnosno, definisemo public deo paketa
<Solidity interfejs kod>


S1.sol

# pragma ...
import "ugovor.sol"

contract .... implementacija

S2.sol

# pragma ...
import "nesto2.sol"

contract .... implementacija

# mi uzimamo S1 i S2 i generisemo MIX.sol

# MIX.sol ce izgledati ovako:

import "ugovor.sol"
import "nesto2.sol"

...