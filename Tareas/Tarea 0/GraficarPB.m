#Script encargado de graficar la DEP en pasa banda.
#Par�metros:
# A: amplitud del pulso
# Br: tasa de bits
# fp: frecuencia de portadora

function GraficarPB(A,Br,fp)
  #C�lculo del tiempo de bit
  T = 1/Br;
  #Creaci�n del vector de frecuencias con valores l�mite que permitan ver
  #los dos primeros l�bulos de los sincs.
  window = 4*Br + fp;
  f = -window: 0.01:window;
  #Obtenci�n de Syy.
  Sxx = (DEPBB(f-fp,T,A) + DEPBB(f+fp,T,A))/2;
  #Gr�fico Syy.
  xlim([-window, window]);
  plot(f,Sxx);
  xlabel("f")
  ylabel("Syy(f)")
endfunction