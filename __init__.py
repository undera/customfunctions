import logging

from graphite.render.functions import SeriesFunctions
import calculatefn
import seglinr


SeriesFunctions['segLinReg'] = seglinr.seg_lin_reg
SeriesFunctions['segLinRegAuto'] = seglinr.seg_lin_reg_auto

SeriesFunctions['centeredMovingAverage'] = calculatefn.centered_mov_avg

logging.basicConfig(format='%(asctime)s\t%(message)s', level=logging.INFO)
