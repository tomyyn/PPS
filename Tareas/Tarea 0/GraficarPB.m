#Script encargado de graficar la DEP en pasa banda.
#Parámetros:
# A: amplitud del pulso
# Br: tasa de bits
# fp: frecuencia de portadora

function GraficarPB(A,Br,fp)
  #Cálculo del tiempo de bit
  T = 1/Br;
  #Creación del vector de frecuencias con valores límite que permitan ver
  #los dos primeros lóbulos de los sincs.
  window = 4*Br + fp;
  f = -window: 0.01:window;
  #Obtención de Syy.
  Sxx = (DEPBB(f-fp,T,A) + DEPBB(f+fp,T,A))/2;
  #Gráfico Syy.
  xlim([-window, window]);
  plot(f,Sxx);
  xlabel("f")
  ylabel("Syy(f)")
endfunction