Podsumowanie projektu
=====================

Sukcesy
-------
* nawiązanie połączenia przy przekierowaniu wejścia
* transmisja z prędkością 200bps 
* stabilność wystarczająca do przesłania artykułu o wadze 4kB

Porażki
-------
* nie udaje się nawiązać połączenia przy użyciu wbudowanego mikrofonu

Wyzwania
--------
Najtrudniejszym elementem zadania było nawiązanie stabilnego połączenia.
Wymagał on dostrojenia odpowiednich częstotliwości i amplitudy sygnału tak,
żeby interpretacja wyników z FFT była możliwie prosta. Najlepsze wyniki
uzyskano przy ustaleniu częstotliwości poszczególnych bitów na częstotliwości
występujące w wynikach FFT, które zależały od ilości próbek w jednym oknie
bitu. Podejrzewam, że zniekształcenia częstotliwości przez słabej jakości
głośnik i mikrofon mogły przyczynić się do niepowodzenia w przypadku próby
nawiązania połączenia przez te media.
Należało również zadbać o możliwie najdokładniejszą synchronizację zegara z
nadawcą wiadomości. Udało się to uzyskać przesuwając ramkę bitu o 1/3 okresu
aż do uzyskania ramki, która jest w 99,9% wypełniona przez jeden bit. Przy
udanej próbie przesłania 4000 znaków najmniejsze wypełnienie dominującego
bitu w ramce wynosiło 83%.
