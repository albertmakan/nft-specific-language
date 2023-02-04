# random ideja - nakon compile mozemo izbaciti prompt
# primer: your contract is ERC20 compatible
# primer: your contract is not ERC721 compatible, reason: missing function.......

# za pocetak fokus je na tome da svaki blok bude poseban contract
# ukoliko se korisnik bude bunio, implementiracemo podrsku da sve bude u istom contractu

# token deo

plugins {
  using std.token.numeric.*;
  using custom.equity.sales;
}

numeric token Brojko supports {
  std.token.numeric.minting;
  std.token.numeric.balanceChecking;
  std.token.numeric.burning;
  std.token.numeric.transfering;
}

unique token Skemer supports {
  custom.equity.sales with 10% equity and 1% fee;
}

combined token Tokevestit supports {
  ...
}
