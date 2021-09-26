#Función que devuelve el valor de la DEP en banda base para 
#determinados parámetros.
#Parámetros:
# f: frecuencia
# T: Tiempo de bit
# A: amplitud del pulso

function Sxx = DEPBB(f,T,A)
  Sxx=(A^2) * T * (sinc(f.*T/2).^2).* (sin(pi*f.*T/2).^2);
endfunction