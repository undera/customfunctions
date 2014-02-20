import logging

import seglinreg


def seg_lin_reg(request_context, series_list, segment_count=3):
    """
    Graphs the segmented linear regression
      requires python-numpy python-scipy
      segmentCount must be > 2
    """
    for series in series_list:
        series.name = "segLinReg(%s,%s)" % (series.name, segment_count)
        #series.pathExpression = series.name
        s = [(i, value) for i, value in enumerate(series)]
        #logging.info("Source: %s", s)
        regr = seglinreg.SegLinReg(segment_count)
        regr.first_pass_breakpoint_ratio = 10
        res = regr.calculate(s)
        logging.info("Result: %s", res)
        for i, value in enumerate(series):
            series[i] = None

        for k, v in res.get_regression_data():
            series[int(k)] = v
        logging.info("Output: %s", len(series))
    return series_list


def seg_lin_reg_auto(request_context, series_list, segment_count=10, threshold=None):
    """
    Graphs the segmented linear regression up to
      requires python-numpy python-scipy
      segmentCount must be > 2
    """
    for series in series_list:
        series.name = "segLinRegAuto(%s,%s)" % (series.name, segment_count)
        #series.pathExpression = series.name
        s = [(i, value) for i, value in enumerate(series)]
        #logging.info("Source: %s", s)
        regr = seglinreg.SegLinRegAuto(segment_count)
        if threshold:
            regr.r2_threshold = threshold
        res = regr.calculate(s)
        logging.info("Result: %s", res)
        for i, value in enumerate(series):
            series[i] = None

        for k, v in res.get_regression_data():
            series[int(k)] = v
        logging.info("Output: %s", len(series))

    return series_list
