import logging

from graphite.render.datalib import TimeSeries
from graphite.render import functions


def centered_mov_avg(requestContext, seriesList, windowSize):
    windowInterval = None
    if isinstance(windowSize, basestring):
        delta = functions.parseTimeOffset(windowSize)
        windowInterval = abs(delta.seconds + (delta.days * 86400))

    if windowInterval:
        bootstrapSeconds = windowInterval
    else:
        bootstrapSeconds = max([s.step for s in seriesList]) * int(windowSize)

    bootstrapList = functions._fetchWithBootstrap(requestContext, seriesList, seconds=bootstrapSeconds)
    result = []

    for bootstrap, series in zip(bootstrapList, seriesList):
        if windowInterval:
            windowPoints = windowInterval / series.step
        else:
            windowPoints = int(windowSize)

        if isinstance(windowSize, basestring):
            newName = 'centeredMovingAverage(%s,"%s")' % (series.name, windowSize)
        else:
            newName = "centeredMovingAverage(%s,%s)" % (series.name, windowSize)
        newSeries = TimeSeries(newName, series.start, series.end, series.step, [])
        newSeries.pathExpression = newName

        offset = len(bootstrap) - len(series)
        logging.info("Offset: %s", offset)
        logging.info("windowPoints: %s", windowPoints)

        for i in range(len(series)):
            window = bootstrap[i + offset - windowPoints + windowPoints / 2:i + offset + windowPoints / 2]
            logging.info("window: %s", len(window))
            newSeries.append(functions.safeAvg(window))

        result.append(newSeries)

    return result


def percentileOfSeries(requestContext, *args):
    levels = []
    seriesList = []
    for arg in args:
        logging.info("Arg: %s", arg)
        if isinstance(arg, (int, long, float)):
            levels.append(arg)
        elif isinstance(arg, basestring):
            levels += [float(x) for x in arg.split(";")]
        else:
            seriesList += arg

    logging.info("Levels: %s", levels)
    logging.info("Series: %s", seriesList)

    result = []
    for level in levels:
        if levels <= 0:
            raise ValueError('The requested percent is required to be greater than 0')

        name = 'percentilesOfSeries(%s,%g)' % (seriesList[0].pathExpression, level)
        (start, end, step) = functions.normalize([seriesList])[1:]
        values = [functions._getPercentile(row, level, False) for row in functions.izip(*seriesList)]
        resultSeries = TimeSeries(name, start, end, step, values)
        resultSeries.pathExpression = name
        result.append(resultSeries)

    return result
