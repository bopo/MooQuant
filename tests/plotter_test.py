# -*- coding: utf-8 -*-
# MooQuant
#
# Copyright 2011-2015 Gabriel Martin Becedillas Ruiz
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""

import os
import sys

from mooquant import plotter
from mooquant.barfeed import yahoofeed

from . import common, sma_crossover

sys.path.append("examples")


class PlotterTestCase(common.TestCase):
    def testDownloadAndParseDaily(self):
        instrument = "orcl"
        barFeed = yahoofeed.Feed()
        barFeed.addBarsFromCSV(instrument, common.get_data_file_path("orcl-2000-yahoofinance.csv"))
        
        strat = sma_crossover.SMACrossOver(barFeed, instrument, 20)
        
        plt = plotter.StrategyPlotter(strat, True, True, True)
        plt.getInstrumentSubplot(instrument).addDataSeries("sma", strat.getSMA())
        
        strat.run()

        with common.TmpDir() as tmpPath:
            fig, subplots = plt.buildFigureAndSubplots()

            self.assertIsNotNone(fig)
            self.assertIsNotNone(subplots)

            # fig = plt.buildFigure()
            fig, _ = plt.buildFigureAndSubplots()
            fig.set_size_inches(10, 8)

            png = os.path.join(tmpPath, "plotter_test.png")
            fig.savefig(png)

            # Check that file size looks ok.
            # 118458 on Mac
            # 116210 on Linux
            # self.assertGreater(os.stat(png).st_size, 110000)
