import React, { useEffect, useState, useRef } from "react";
import { Row, Col } from "react-bootstrap";
import { Chart } from "react-google-charts";
import './Chart.css';
import './Chart.css';
import axios from "axios";
import { createChart, AreaSeries, LineSeries } from 'lightweight-charts';

const ChartComponent = ({ data, c_symbol }) => {
    const chartContainerRef = useRef(null);
    const toolTipRef = useRef(null);

    // const defaultData = data?.data || [];
    const defaultData = data || [];

    console.log(defaultData);
    console.log(c_symbol);

    useEffect(() => {
        const chart = createChart(chartContainerRef.current, {
            width: chartContainerRef.current.clientWidth,
            height: 630,
            layout: {
                background: { color: '#000000' },
                textColor: '#ffffff',
            },
            grid: {
                vertLines: { color: '#444' },
                horzLines: { color: '#444' },
            },
            crosshair: {
                mode: 0,
            },
            timeScale: {
                timeVisible: true,
                secondsVisible: false,
            },
        });

        const closeSeries = chart.addSeries(AreaSeries, { color: 'blue', lineWidth: 2 });
        const ema100Series = chart.addSeries(LineSeries, { color: 'orange', lineWidth: 1 });
        const ema200Series = chart.addSeries(LineSeries, { color: 'red', lineWidth: 1 });

        const closeData = defaultData.map(item => ({ time: item.Date, value: item.Close }));
        const ema100Data = defaultData.map(item => ({ time: item.Date, value: item.ema100 }));
        const ema200Data = defaultData.map(item => ({ time: item.Date, value: item.ema200 }));

        closeSeries.setData(closeData);
        ema100Series.setData(ema100Data);
        ema200Series.setData(ema200Data);

        // Tooltip
        const toolTip = document.createElement('div');
        toolTipRef.current = toolTip;
        const toolTipWidth = 110;

        toolTip.style = `
        width: ${toolTipWidth}px;
        position: absolute;
        display: none;
        padding: 8px;
        box-sizing: border-box;
        font-size: 12px;
        text-align: left;
        z-index: 1000;
        pointer-events: none;
        border-radius: 4px 4px 0px 0px;
        box-shadow: 0 2px 5px 0 rgba(117, 134, 150, 0.45);
        font-family: -apple-system, BlinkMacSystemFont, 'Trebuchet MS', Roboto, Ubuntu, sans-serif;
        background: rgba(0, 0, 0, 0.25);
        color: white;
        border: 1px solid rgb(0, 255, 98);
      `;
        chartContainerRef.current.appendChild(toolTip);

        chart.subscribeCrosshairMove(param => {
            if (
                !param.time ||
                param.point.x < 0 ||
                param.point.x > chartContainerRef.current.clientWidth ||
                param.point.y < 0 ||
                param.point.y > chartContainerRef.current.clientHeight
            ) {
                toolTip.style.display = 'none';
                return;
            }

            const dateStr = param.time;
            const data = param.seriesData.get(closeSeries);
            const price = data?.value !== undefined ? data.value : data?.close;

            if (price === undefined) return;

            toolTip.innerHTML = `
                <div style="color: rgb(9, 255, 0)">${c_symbol}</div>
                <div style="font-size: 24px; margin: 4px 0; color: white;">${price.toFixed(2)}</div>
                <div style="color: white;">${dateStr}</div>
            `;
            toolTip.style.display = 'block';

            let left = param.point.x - toolTipWidth / 2;
            left = Math.max(0, Math.min(left, chartContainerRef.current.clientWidth - toolTipWidth));
            toolTip.style.left = `${left}px`;
            toolTip.style.top = `95rem`;
        });

        return () => {
            chart.remove();
        };
    }, []);

    return (
        <div>
            <div
                ref={chartContainerRef}
                id="container"
            />
        </div>
    );
};

function RevenueChart({ c_symbol, years, revenue }) {
    const data = [["Year", "Revenue"]];
    if (years && revenue && revenue.length === years.length) {
        for (let i = 0; i < years.length; i++) {
            data.push([String(years[i]), revenue[i]]);
        }
        const options = {
            title: `${c_symbol} Revenue Growth`,
            titleTextStyle: {
                color: 'white',  // Change the axis title color (red here)
                fontSize: 15
            },
            vAxis: {
                gridlines: { color: 'none' },
                format: 'short',
                textStyle: {
                    color: 'white'
                }
            },
            hAxis: {
                gridlines: { color: 'white' },
                textStyle: {
                    color: 'white'
                }
            },
            colors: ['rgb(62, 178, 36)', 'rgb(255, 255, 51)'],
            curveType: 'function',
            legend: {
                position: 'bottom',
                textStyle: {
                    color: 'white'
                }
            },
            backgroundColor: 'transparent',
            chartArea: {
                left: 50,         // Reduces space on the left (adjust value as needed)
                right: 10,        // Reduces space on the right (adjust value as needed)
                top: 50,          // Adjust the top margin (for title)
                bottom: 50,       // Adjust space at the bottom
                width: '80%',     // Adjust the chart width within the container
                height: '50%'     // Adjust the chart height within the container
            },
            tooltip: {
                isHtml: true,  // Enable HTML tooltips for more customization
                trigger: 'focus'  // Show the tooltip for all companies when hovering over a single year
            },

            // Focus on column data, no crosshair lines
            focusTarget: 'category', // This shows all data for a year when hovering over that year

            // Column width increase
            pointSize: 7, // Make points slightly larger
            interpolateNulls: true

        }
        return (
            <Chart
                chartType='LineChart'
                width="100%"
                height="30rem"
                data={data}
                options={options}
            />
        );
    }
    return <p>No Revenue data available.</p>;
}

function IncomeChart({ c_symbol, years, income }) {
    const data = [["Year", "Income"]];
    if (years && income && income.length === years.length) {
        for (let i = 0; i < years.length; i++) {
            data.push([String(years[i]), income[i]]);
        }
        const options = {
            title: `${c_symbol} Income Growth`,
            titleTextStyle: {
                color: 'white',  // Change the axis title color (red here)
                fontSize: 15
            },
            vAxis: {
                gridlines: { color: 'none' },
                format: 'short',
                textStyle: {
                    color: 'white'
                }
            },
            hAxis: {
                gridlines: { color: 'white' },
                textStyle: {
                    color: 'white'
                }
            },
            colors: ['rgb(62, 178, 36)'],
            curveType: 'function',
            legend: {
                position: 'bottom',
                textStyle: {
                    color: 'white'
                }
            },
            backgroundColor: 'transparent',
            chartArea: {
                left: 50,         // Reduces space on the left (adjust value as needed)
                right: 10,        // Reduces space on the right (adjust value as needed)
                top: 50,          // Adjust the top margin (for title)
                bottom: 50,       // Adjust space at the bottom
                width: '80%',     // Adjust the chart width within the container
                height: '50%'     // Adjust the chart height within the container
            },
            tooltip: {
                isHtml: true,  // Enable HTML tooltips for more customization
                trigger: 'focus'  // Show the tooltip for all companies when hovering over a single year
            },

            // Focus on column data, no crosshair lines
            focusTarget: 'category', // This shows all data for a year when hovering over that year

            // Column width increase
            pointSize: 7, // Make points slightly larger
            interpolateNulls: true

        }
        return (
            <Chart
                chartType='LineChart'
                width="100%"
                height="30rem"
                data={data}
                options={options}
            />
        );
    }
    return <p>No Income data available.</p>;
}

function EPSChart({ c_symbol, years, eps }) {
    const data = [["Year", "EPS"]];
    if (years && eps && eps.length === years.length) {
        for (let i = 0; i < years.length; i++) {
            data.push([String(years[i]), eps[i]]);
        }
        const options = {
            title: `${c_symbol} EPS Growth`,
            titleTextStyle: {
                color: 'white',  // Change the axis title color (red here)
                fontSize: 15
            },
            vAxis: {
                gridlines: { color: 'none' },
                format: 'short',
                textStyle: {
                    color: 'white'
                }
            },
            hAxis: {
                gridlines: { color: 'white' },
                textStyle: {
                    color: 'white'
                }
            },
            colors: ['rgb(62, 178, 36)'],
            curveType: 'function',
            legend: {
                position: 'bottom',
                textStyle: {
                    color: 'white'
                }
            },
            backgroundColor: 'transparent',
            chartArea: {
                left: 50,         // Reduces space on the left (adjust value as needed)
                right: 10,        // Reduces space on the right (adjust value as needed)
                top: 50,          // Adjust the top margin (for title)
                bottom: 50,       // Adjust space at the bottom
                width: '80%',     // Adjust the chart width within the container
                height: '50%'     // Adjust the chart height within the container
            },
            tooltip: {
                isHtml: true,  // Enable HTML tooltips for more customization
                trigger: 'focus'  // Show the tooltip for all companies when hovering over a single year
            },

            // Focus on column data, no crosshair lines
            focusTarget: 'category', // This shows all data for a year when hovering over that year

            // Column width increase
            pointSize: 7, // Make points slightly larger
            interpolateNulls: true

        }
        return (
            <Chart
                chartType='LineChart'
                width="100%"
                height="30rem"
                data={data}
                options={options}
            />
        );
    }
    return <p>No EPS data available.</p>;
}

function ROEChart({ c_symbol, years, roe }) {
    const data = [["Year", "ROE"]];
    if (years && roe && roe.length === years.length) {
        for (let i = 0; i < years.length; i++) {
            data.push([String(years[i]), roe[i]]);
        }
        const options = {
            title: `${c_symbol} ROE Growth`,
            titleTextStyle: {
                color: 'white',  // Change the axis title color (red here)
                fontSize: 15
            },
            vAxis: {
                gridlines: { color: 'none' },
                format: 'short',
                textStyle: {
                    color: 'white'
                }
            },
            hAxis: {
                gridlines: { color: 'white' },
                textStyle: {
                    color: 'white'
                }
            },
            colors: ['rgb(62, 178, 36)', 'rgb(255, 255, 51)'],
            curveType: 'function',
            legend: {
                position: 'bottom',
                textStyle: {
                    color: 'white'
                }
            },
            backgroundColor: 'transparent',
            chartArea: {
                left: 50,         // Reduces space on the left (adjust value as needed)
                right: 10,        // Reduces space on the right (adjust value as needed)
                top: 50,          // Adjust the top margin (for title)
                bottom: 50,       // Adjust space at the bottom
                width: '80%',     // Adjust the chart width within the container
                height: '50%'     // Adjust the chart height within the container
            },
            tooltip: {
                isHtml: true,  // Enable HTML tooltips for more customization
                trigger: 'focus'  // Show the tooltip for all companies when hovering over a single year
            },

            // Focus on column data, no crosshair lines
            focusTarget: 'category', // This shows all data for a year when hovering over that year

            // Column width increase
            pointSize: 7, // Make points slightly larger
            interpolateNulls: true

        }
        return (
            <Chart
                chartType='LineChart'
                width="100%"
                height="30rem"
                data={data}
                options={options}
            />
        );
    }
    return <p>No ROE data available.</p>;
}

export function ChartSection({ companySymbol }) {
    if (companySymbol === undefined) {
        return
    }
    const [fundamentalData, setFundamentalData] = useState(null);
    const [sharePriceData, setSharePriceData] = useState(null);
    const [isSharePriceLoading, setIsSharePriceLoading] = useState(false);
    const [sharePriceError, setSharePriceError] = useState(null);

    useEffect(() => {
        const fetchFundamentals = async () => {
            try {
                const resFundamentals = await axios.get(`/api/${companySymbol}/getFundamentals`);
                setFundamentalData(resFundamentals.data);
            } catch (error) {
                console.error('Error fetching fundamentals:', error);
                setFundamentalData(null);
            }
        };

        fetchFundamentals();
    }, [companySymbol]);

    useEffect(() => {
        const fetchSharePrice = async () => {
            setIsSharePriceLoading(true);
            setSharePriceError(null); // Reset error on new fetch
            const range = 4;
            try {
                const sharePriceUrl = `/api/${companySymbol}/getSharePrice/${range}`;
                const respSharePrice = await axios.get(sharePriceUrl);
                // Format the data to match what Lightweight Charts expects
                // const formattedData = respSharePrice.data.map(item => ({
                //     time: item.Date,
                //     value: item.Close,
                // }));
                setSharePriceData(respSharePrice.data);
            } catch (error) {
                console.error('Error fetching Share price data:', error);
                setSharePriceError(error.message || 'Failed to fetch share price data');
                setSharePriceData(null);
            } finally {
                setIsSharePriceLoading(false);
            }
        };
        fetchSharePrice();
    }, [companySymbol]);

    return (
        <>
            <Row className="ChartRow">
                <Col className="ChartCol">
                    <div>
                        {fundamentalData && fundamentalData.years && fundamentalData.revenue ? (
                            <RevenueChart
                                c_symbol={companySymbol}
                                years={fundamentalData.years}
                                revenue={fundamentalData.revenue}
                            />
                        ) : (
                            <p>Loading Revenue data...</p>
                        )}
                    </div>
                </Col>
                <Col className="ChartCol">
                    <div>
                        {fundamentalData && fundamentalData.years && fundamentalData.income ? (
                            <IncomeChart
                                c_symbol={companySymbol}
                                years={fundamentalData.years}
                                income={fundamentalData.income}
                            />
                        ) : (
                            <p>Loading Income data...</p>
                        )}
                    </div>
                </Col>
            </Row>
            <Row className="ChartRow">
                <Col className="ChartCol">
                    <div>
                        {fundamentalData && fundamentalData.years && fundamentalData.eps ? (
                            <EPSChart
                                c_symbol={companySymbol}
                                years={fundamentalData.years}
                                eps={fundamentalData.eps}
                            />
                        ) : (
                            <p>Loading EPS data...</p>
                        )}
                    </div>
                </Col>
                <Col className="ChartCol">
                    <div>
                        {fundamentalData && fundamentalData.years && fundamentalData.roe ? (
                            <ROEChart
                                c_symbol={companySymbol}
                                years={fundamentalData.years}
                                roe={fundamentalData.roe}
                            />
                        ) : (
                            <p>Loading ROE data...</p>
                        )}
                    </div>
                </Col>
            </Row>

            <Row className="ChartRow">
                <Col className="SharePriceChart">
                    {isSharePriceLoading ? (
                        <p>Loading Share Price data...</p>
                    ) : sharePriceError ? (
                        <p>Error loading Share Price data: {sharePriceError}</p>
                    ) : sharePriceData ? (
                        <ChartComponent
                            data={sharePriceData}
                            c_symbol={companySymbol}
                        />
                    ) : (
                        <p>No Share Price data available.</p>
                    )}
                </Col>
            </Row>
        </>
    );
}