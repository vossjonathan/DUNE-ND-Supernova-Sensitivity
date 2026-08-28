def calc_Q_value_CC_nue():
    #nue + 56Fe ---> e- + 56Co

    m_56Fe = 55.9349355 # in u
    m_56Co = 55.939839 # in u

    #Q = E_56Co - E_56Fe
    u_MeV = 931.494
    Q_MeV = (m_56Co - m_56Fe)*u_MeV

    return Q_MeV

#print(calc_Q_value_CC_nue())

def calc_Q_value_CC_nue_bar():
    #nue_bar + 56Fe ---> e+ + 56Mn
    
    m_56Fe = 55.9349355 # in u
    m_56Mn = 55.9389028 # in

    u_MeV = 931.494
    Q_MeV = (m_56Mn - m_56Fe)*u_MeV

    return Q_MeV

print(calc_Q_value_CC_nue_bar()) #3.695516