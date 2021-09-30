function graficarPebBP();
   EbN0 = 0:0.0001:50;
   Peb = qfunc(sqrt(EbN0*2));
   plot(EbN0,Peb);
end