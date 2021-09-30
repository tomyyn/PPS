#Script encargado de graficar la DEP en banda base.
#Par�metros:
# A: amplitud del pulso
# Br: tasa de bits

function GraficarBB(A,Br)
  #C�lculo del tiempo de bit.
  T = 1/Br;
  #Creaci�n del vector de frecuencias con valores l�mite que permitan ver
  #los dos primeros l�bulos del sinc.
  window = 4*Br;
  f = -window: 0.01:window;
  #Obtenci�n de Sxx.
  Sxx = DEPBB(f,T,A);
  #Gr�fico Sxx.
  xlim([-window, window]);
  plot(f,Sxx,'linewidth',8);
  xlabel("f")
  ylabel("Sxx(f)")
endfunction