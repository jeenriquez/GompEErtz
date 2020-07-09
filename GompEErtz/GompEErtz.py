from  get_data import *
import matplotlib.pylab as plt
from scipy.stats import gompertz
#from scipy.optimize import minimize
from scipy.optimize import *
from scipy.ndimage.interpolation import shift
from matplotlib.pyplot import text


class GompEErtz:
    '''
    '''

    def __init__(self,data_type='E',fit_deaths=False,factor=0,dated='20200707',lag=-7,nmin=5,lugar='CHIHUAHUA'):

        #-------
        #The global wild west
        self.nmin = nmin
        self.lag = lag
        self.dated = dated
        self.data_type = data_type
        self.factor = factor
        self.lugar = lugar
        self.fit_deaths = fit_deaths

        #-------
        #Get data, excluding the last few days

        cases_I, cases_D, cases_S = get_stdout_data(nmin=self.nmin,data_type=self.data_type,format='all',dated=self.dated,lugar=self.lugar)

        if self.fit_deaths:
            self.cases = np.array(cases_D['Numero personas totales'][:self.lag].tolist())
            self.cases_daily =  np.array(cases_D['Numero personas diarias'][:self.lag].tolist())
        else:
            self.cases = np.array(cases_I['Numero personas totales'][:self.lag].tolist()) +np.array(cases_S['Numero personas totales'][:self.lag].tolist())*self.factor
            self.cases_daily =  np.array(cases_I['Numero personas diarias'][:self.lag].tolist())

        self.dia_init = cases_I['Dias'].iloc[0]
        self.dias = cases_I['Dias'].tolist()[:self.lag]

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

        min_sol = minimize(self.sumsq,(x0,x1,c),bounds=bounds,method='TNC',options={'maxiter':1000})

        if verbose:
            print(min_sol)

        #Modelo del fit
        model_gom = self.inv_gom(min_sol.x[0],min_sol.x[1],min_sol.x[2],self.t,1)
        mfit = model_gom*self.N/max(model_gom)#+nmin

        #Modelo para pronostico
        x3 = 1.-1e-5
        t_pronostico = int(self.t * gompertz.ppf(x3,c) / gompertz.ppf(min_sol.x[1],c))
        model_pronostico = self.inv_gom(min_sol.x[0],x3,min_sol.x[2],t_pronostico,1)
        mfit_pronostico = model_pronostico*self.N/max(model_gom)#+nmin

        if normalized:
            return mfit,mfit_pronostico,min_sol
        else:
            return model_gom,model_pronostico,min_sol

    def plot_tot_fit(self):

        if self.fit_deaths:
            label = 'Fallecidos'
        else:
            label = 'Confirmados'

        plt.ion()
        plt.figure()

        plt.plot(self.cases,'o',label='Casos ; %s'%self.lugar)
        plt.plot(self.mfit,'k-',label='Gompertz\n Status: %s'%self.mfit_min_sol.message)

        plt.legend()
        plt.xlabel('Dias desde %s '%self.dia_init)
        plt.ylabel('%s Totales'%label)
        plt.title('%s Acumulados en %s'%(label,self.lugar) )







