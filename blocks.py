import numpy as np
import numba as nb

from GEModelTools import prev,next

import numpy as np
import numba as nb

from GEModelTools import lag, lead



@nb.njit
def production_firm(par,ini,ss,K,L_Y,rK,w,Y, Gamma_Y):

    K_lag = lag(ini.K,K)


    # a. implied prices 
    rK[:] = par.kappa*Gamma_Y*(K_lag/L_Y)**(par.kappa-1.0)

    w[:] = (1.0-par.kappa)*Gamma_Y*(K_lag/L_Y)**par.kappa

    # b. production and investment

    Y[:] = Gamma_Y*K_lag**(par.kappa)*L_Y**(1-par.kappa)


@nb.njit
def mutual_fund(par,ini,ss,K,rK,A,r):

    # a. total assets
    A[:] = K 

    # b. return
    r[:] = rK-par.delta
    


@nb.njit
def government(par,ini,ss,tau,w,wt, L_G, G,L_Y, Gamma_G,   Y):

    # a. government Production
    L_G[:] = G/Gamma_G
   

    # b. after tax wage
    wt[:] = (1-tau)*w


    


@nb.njit
def market_clearing(par,ini,ss,A,A_hh,L_hh,Y, w, L, tau, C_hh,K, L_G ,I,clearing_A,clearing_L,clearing_Y, clearing_G, G, L_Y):

    L[:] = L_hh

    L_Y[:] = L - L_G


    I[:] = K-(1-par.delta)*lag(ini.K,K)
    clearing_A[:] = A-A_hh
    clearing_L[:] = L_hh - (L_Y + L_G)
    clearing_G[:] = w*L_G  - tau * w * (L_Y + L_G) 
    clearing_Y[:] = Y - C_hh - I 


# @nb.njit
# def additional_var(par,ini,ss, G, L_G, w, L_Y, G_exp, Y, G_share, G_exp_share):
    
#     G_exp[:] = L_G*w

#     G_share[:] = G/Y
#     G_exp_share[:] = G_exp/(G_exp + L_Y*w)