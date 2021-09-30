#Script encargado de graficar la DEP en banda base.
#Parámetros:
# A: amplitud del pulso
# Br: tasa de bits

function GraficarBB(A,Br)
  #Cálculo del tiempo de bit.
  T = 1/Br;
  #Creación del vector de frecuencias con valores límite que permitan ver
  #los dos primeros lóbulos del sinc.
  window = 4*Br;
  f = -window: 0.01:window;
  #Obtención de Sxx.
  Sxx = DEPBB(f,T,A);
  #Gráfico Sxx.
  xlim([-window, window]);
  plot(f,Sxx,'linewidth',8);
  xlabel("f")
  ylabel("Sxx(f)")
endfunction