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
