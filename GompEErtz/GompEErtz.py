#! /usr/bin/env python3
'''
Clase GompEErtz, que utiliza el modelo Gompertz para analizar casos confirmados, estimados o fallecidos de municipios, y estados de Mexico, asi como a nivel nacional.
'''

try:
    from  .get_data import *
except:
    from  get_data import *

import matplotlib.pylab as plt
from scipy.stats import gompertz
from scipy.optimize import *
from scipy.ndimage.interpolation import shift
from matplotlib.pyplot import text


class GompEErtz:
    '''
    '''

    def __init__(self,data_type='E',fit_deaths=False,factor=0,dated='20200715',lag=-7,nmin=5,lugar='CHIHUAHUA'):

        #-------
        #The global wild west
        self.nmin = nmin
        self.lag = lag
        self.dated = dated
        self.data_type = data_type
        self.factor = factor
        self.lugar = lugar
        self.fit_deaths = fit_deaths

        if self.data_type == 'E':
            self.entidad = 'Edo'
        elif self.data_type == 'M':
            self.entidad = 'Mpio'
        else:
            self.entidad = ''

        if self.fit_deaths:
            self.tipo_datos= 'Fallecidos'
        elif self.factor > 0:
            self.tipo_datos = 'Estimados'
        else:
            self.tipo_datos = 'Confirmados'

        #Formating the place name
        self.lugar_name = self.lugar[0].upper()+self.lugar[1:].lower()

        #Format place name for data access.
        if self.data_type == 'E':
            self.lugar = self.lugar.upper()
        elif self.data_type == 'M':
            self.lugar = self.lugar_name
        else:
            self.lugar = 'Nacional'

        #-------
        #Get data, excluding the last few days

        if self.fit_deaths:
            cases_full = get_stdout_data(nmin=self.nmin,data_type=self.data_type,format='D',dated=self.dated,lugar=self.lugar)

            self.cases = np.array(cases_full['Numero personas totales'][:self.lag].tolist())
            self.cases_daily =  np.array(cases_full['Numero personas diarias'][:self.lag].tolist())
        else:
            cases_full, cases_S = get_stdout_data(nmin=self.nmin,data_type=self.data_type,format='IS',dated=self.dated,lugar=self.lugar)

            self.cases = np.array(cases_full['Numero personas totales'][:self.lag].tolist()) +np.array(cases_S['Numero personas totales'][:self.lag].tolist())*self.factor
            self.cases_daily =  np.array(cases_full['Numero personas diarias'][:self.lag].tolist())

        self.dia_init = cases_full['Dias'].iloc[0]
        self.dias = cases_full['Dias'].tolist()[:self.lag]

        #-------
        #Fitting
        self.N = max(self.cases)
        self.t = self.cases.shape[0]

        self.mfit, self.mfit_pronostico, self.mfit_min_sol =  self.fit_gompertz()

        #-------
        #Calc dailies

        self.mfit_day = self.mfit - shift(self.mfit,1)
        self.mfit_day[0] = np.NaN   # For plotting

        self.mfit_pronostico_day = self.mfit_pronostico - shift(self.mfit_pronostico,1)
        self.mfit_pronostico_day[0] = np.NaN   # For plotting


    def inv_gom(self,x0,x1,c,t,N):
        '''Returns inverse of gompertz PDF
        '''

        x = np.linspace(gompertz.ppf(x0, c),gompertz.ppf(x1, c), t)

        return N*(1-1*gompertz.pdf(x,c))


    def sumsq(self,values):
        '''
        '''
        #Calc inv Gompertz
        x0,x1,c = values

        model_gom = self.inv_gom(x0,x1,c,self.t,1)
        model_norm = model_gom*self.N/max(model_gom)#+ nmin

        return(sum((model_norm-self.cases)**2))

    def fit_gompertz(self,normalized=True,verbose=True):

        x0 = 1e-4
        x1 = 0.95
        c = 1
        bounds=((1e-7,0.3),(0.3,0.9999),(0.9,1.5))

        self.method = 'TNC'

        min_sol = minimize(self.sumsq,(x0,x1,c),bounds=bounds,method=self.method,options={'maxiter':1000})

        if verbose:
            print(min_sol)

        if 'failed' in min_sol.message:
            if verbose:
                print('NOTE: TNC:  %s  \n Attempting L-BFGS-B method.'%min_sol.message)

            self.method = 'L-BFGS-B'
            min_sol = minimize(self.sumsq,(x0,x1,c),bounds=bounds,method=self.method,options={'maxiter':1000})

            if verbose:
                print(min_sol)

            min_sol.message = min_sol.message.decode("utf-8")[:11]

        #Modelo del fit
        model_gom = self.inv_gom(min_sol.x[0],min_sol.x[1],min_sol.x[2],self.t,1)
        mfit = model_gom*self.N/max(model_gom)#+nmin

        #Modelo para pronostico
        x3 = 1.-1e-5

        t_pronostico = int(self.t * (gompertz.ppf(x3,c)-gompertz.ppf(min_sol.x[0],c)) / (gompertz.ppf(min_sol.x[1],c)-gompertz.ppf(min_sol.x[0],c)))#+10

        model_pronostico = self.inv_gom(min_sol.x[0],x3,min_sol.x[2],t_pronostico,1)
        mfit_pronostico = model_pronostico*self.N/max(model_gom)

        if normalized:
            return mfit,mfit_pronostico,min_sol
        else:
            return model_gom,model_pronostico,min_sol

    def plot_tot_fit(self,subplot=False,extra=''):

        if not subplot:
            plt.ion()
            plt.figure()

        plt.plot(self.cases,'o',label='Casos %s'%self.tipo_datos)
        plt.plot(self.mfit,'k-',label='Gompertz\nMetodo: %s\nResultado: %s'%(self.method,self.mfit_min_sol.message))

        plt.legend()
        plt.xlabel('Dias desde %s '%self.dia_init)
        plt.ylabel('%s Totales'%self.tipo_datos)
        plt.title('%s%s Acumulados %s. %s'%(extra,self.tipo_datos,self.entidad,self.lugar_name) )







