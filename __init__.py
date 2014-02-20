from graphite.render.functions import SeriesFunctions
import functions

SeriesFunctions['segLinReg'] = functions.seg_lin_reg
SeriesFunctions['segLinRegAuto'] = functions.seg_lin_reg_auto

