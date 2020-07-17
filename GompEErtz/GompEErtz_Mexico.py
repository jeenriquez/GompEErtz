from GompEErtz import *

nmin = 300
savefig = True

#---------------------------------------------------------------
# Calcular los ajustes dependiendo el porcentaje de sospechosos

#positivos_only
gom = GompEErtz(data_type='N',lugar='Mexico',nmin=nmin)

#positivos + 40% sospeshosos
gom_40sos = GompEErtz(data_type='N',lugar='Mexico',nmin=nmin,factor=0.4)

#positivos + sospeshosos
gom_100sos = GompEErtz(data_type='N',lugar='Mexico',nmin=nmin,factor=1)

#-------
#Plotting

plt.ion()
plt.figure()
plt.bar(range(len(gom.cases_daily)),gom.cases_daily,color='lightcoral',label='Confirmados')

plt.plot(gom.mfit_day,'k-',label='Gompertz Ajuste a Confirmados (G)')
plt.plot(gom.mfit_pronostico_day,'-',color='red',label='Gompertz Pronostico a Confirmados (GP)')
plt.plot(gom.mfit_day,'k-',label='')


plt.plot(gom_40sos.mfit_pronostico_day,'--',color='firebrick',label='GP + 40% de Sospechosos')
plt.plot(gom_100sos.mfit_pronostico_day,'-.',color='peru',label='GP + 100% de Sospechosos')

text(0, gom.cases_daily.max(),gom.dias[0], rotation=90, verticalalignment='top')
text(len(gom.mfit_day)-1, gom.cases_daily.max(),gom.dias[-1], rotation=90, verticalalignment='top')

# plt.hlines(nmin,-1*nmin,500,linestyles='dotted',colors='Gray', label='Limite %i casos'%nmin)
# plt.xlim(-2,300)
#
# plt.vlines(len(gom.dias),-5,np.nanmax(gom_40sos.cases_daily)*1.1,colors='Gray',label=gom.dias[-1])
# plt.ylim(-2,np.nanmax(gom_40sos.cases_daily)*1.05)


plt.hlines(5,-5,len(gom.mfit_pronostico_day)*1.1,linestyles='dotted',colors='Gray', label='Limite 5 casos')
plt.xlim(-2,len(gom.mfit_pronostico_day))

plt.vlines(len(gom.dias),-5,np.nanmax(gom_40sos.mfit_pronostico_day)*1.1,colors='Gray',label=gom.dias[-1])
plt.ylim(-2,np.nanmax(gom_40sos.mfit_pronostico_day)*1.05)


plt.legend()
plt.xlabel('Dias desde %s '%gom.dia_init)
plt.ylabel('Casos Diarios')
plt.title('Casos diarios Mexico')
if savefig:
    plt.savefig('../results/gom_pronostico_Mexico_%s.png'%gom.dated,dpi=300)


#---------------------------------------------------------------
# Calcular el cambio de pronostico devido a actualizacion de datos.


#positivos + 40% sospeshosos
gom_40sos_0606 = GompEErtz(data_type='N',lugar='Mexico',nmin=nmin,factor=0.4,dated='20200606')
gom_40sos_0614 = GompEErtz(data_type='N',lugar='Mexico',nmin=nmin,factor=0.4,dated='20200614')
gom_40sos_0621 = GompEErtz(data_type='N',lugar='Mexico',nmin=nmin,factor=0.4,dated='20200621')
gom_40sos_0626 = GompEErtz(data_type='N',lugar='Mexico',nmin=nmin,factor=0.4,dated='20200626')
gom_40sos_0707 = GompEErtz(data_type='N',lugar='Mexico',nmin=nmin,factor=0.4,dated='20200707')
gom_40sos_0715 = GompEErtz(data_type='N',lugar='Mexico',nmin=nmin,factor=0.4,dated='20200715')

#-------
#Plotting

plt.ion()
plt.figure()

plt.plot(gom_40sos_0606.mfit_pronostico_day,'-.',color='gold',label='GP+40 ; Junio 06')
plt.plot(gom_40sos_0614.mfit_pronostico_day,'-.',color='orange',label='GP+40 ; Junio 14')
plt.plot(gom_40sos_0621.mfit_pronostico_day,'--',color='darkorange',label='GP+40 ; Junio 21')
plt.plot(gom_40sos_0626.mfit_pronostico_day,'--',color='peru',label='GP+40 ; Junio 26')
plt.plot(gom_40sos_0707.mfit_pronostico_day,'--',color='firebrick',label='GP+40 ; Julio 07')
plt.plot(gom_40sos_0715.mfit_pronostico_day,'-.',color='red',label='GP+40 ; Julio 15')


# plt.hlines(nmin,-1*nmin,500,linestyles='dotted',colors='Gray', label='Limite %i casos'%nmin)
# plt.xlim(-2,300)

plt.hlines(5,-5,len(gom.mfit_pronostico_day)*1.1,linestyles='dotted',colors='Gray', label='Limite 5 casos')
plt.xlim(-2,len(gom.mfit_pronostico_day))

plt.vlines(len(gom.dias),-5,np.nanmax(gom_40sos.mfit_pronostico_day)*1.1,colors='Gray',label=gom.dias[-1])
plt.ylim(-2,np.nanmax(gom_40sos.mfit_pronostico_day)*1.05)


plt.legend()
plt.xlabel('Dias desde %s '%gom_40sos_0606.dia_init)
plt.ylabel('Casos Diarios')
plt.title('Casos diarios Mexico')
if savefig:
    plt.savefig('../results/gom_pronostico_Mexico_multi_%s.png'%gom.dated,dpi=300)

#-------
#Plotting

gom_40sos.plot_tot_fit()
if savefig:
    plt.savefig('../results/gom_pronostico_Mexico_fit_%s.png'%gom.dated,dpi=300)

