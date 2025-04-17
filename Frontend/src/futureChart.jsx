import React, { useEffect, useState, useRef } from "react";
import { Row, Col, Alert } from "react-bootstrap";
import { Chart } from "react-google-charts";
import './Chart.css';
import axios from "axios";
import { createChart, AreaSeries, LineSeries } from 'lightweight-charts';


function FutureRevenueChart({ revenueValues }) {
    if (!revenueValues) {
        return <div>Data not available</div>;
    }

    console.log({ 'futureRevenueChart': revenueValues });
    const { c_symbol, previous_years, previous_revenue, future_years, future_revenue } = revenueValues;

    const data = [['Years', 'Previous Revenue', 'Future Revenue']];

    const combinedYears = [...previous_years, ...future_years];
    const combinedPreviousRevenue = [...previous_revenue, ...Array(future_years.length).fill(null)];
    const combinedFutureRevenue = [...Array(previous_years.length).fill(null), ...future_revenue];

    for (let i = 0; i < combinedYears.length; i++) {
        data.push([String(combinedYears[i]), combinedPreviousRevenue[i], combinedFutureRevenue[i]]);
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
        colors: ['rgb(62, 178, 36)', 'orange'], // Define colors for the lines
        curveType: 'function',
        legend: {
            position: 'bottom',
            textStyle: {
                color: 'white',
            },
        },
        backgroundColor: 'transparent',
        chartArea: {
            left: 50,
            right: 10,
            top: 50,
            bottom: 50,
            width: '80%',
            height: '50%',
        },
        tooltip: {
            isHtml: true,
            trigger: 'focus',
        },
        focusTarget: 'category',
        pointSize: 7,
        interpolateNulls: true,
    };

    return (
        <Chart
            chartType="LineChart"
            width="100%"
            height="30rem"
            data={data}
            options={options}
        />
    );
}

function FutureIncomeChart({ incomeValues }) {
    if (!incomeValues) {
        return <div>Data not available</div>;
    }

    console.log(incomeValues);
    const { c_symbol, previous_years, previous_income, future_years, future_income } = incomeValues;
    const data = [['Years', 'Previous Income', 'Future Income']];

    const combinedYears = [...previous_years, ...future_years];
    const combinedPreviousIncome = [...previous_income, ...Array(future_years.length).fill(null)];
    const combinedFutureIncome = [...Array(previous_years.length).fill(null), ...future_income];

    for (let i = 0; i < combinedYears.length; i++) {
        data.push([String(combinedYears[i]), combinedPreviousIncome[i], combinedFutureIncome[i]]);
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
        colors: ['rgb(62, 178, 36)', 'orange'], // Define colors for the lines
        curveType: 'function',
        legend: {
            position: 'bottom',
            textStyle: {
                color: 'white',
            },
        },
        backgroundColor: 'transparent',
        chartArea: {
            left: 50,
            right: 10,
            top: 50,
            bottom: 50,
            width: '80%',
            height: '50%',
        },
        tooltip: {
            isHtml: true,
            trigger: 'focus',
        },
        focusTarget: 'category',
        pointSize: 7,
        interpolateNulls: true,
    };

    return (
        <Chart
            chartType="LineChart"
            width="100%"
            height="30rem"
            data={data}
            options={options}
        />
    );
}

function FutureEPSChart({ epsValues }) {
    if (!epsValues) {
        return <div>Data not available</div>;
    }

    console.log(epsValues);
    const { c_symbol, previous_years, previous_eps, future_years, future_eps } = epsValues;

    const data = [['Years', 'Previous EPS', 'Future EPS']];

    // Combine previous and future data into the chart data
    const combinedYears = [...previous_years, ...future_years];
    const combinedPreviousEPS = [...previous_eps, ...Array(future_years.length).fill(null)];
    const combinedFutureEPS = [...Array(previous_years.length).fill(null), ...future_eps];


    for (let i = 0; i < combinedYears.length; i++) {
        data.push([String(combinedYears[i]), combinedPreviousEPS[i], combinedFutureEPS[i]]);
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
        colors: ['rgb(62, 178, 36)', 'orange'], // Define colors for the lines
        curveType: 'function',
        legend: {
            position: 'bottom',
            textStyle: {
                color: 'white',
            },
        },
        backgroundColor: 'transparent',
        chartArea: {
            left: 50,
            right: 10,
            top: 50,
            bottom: 50,
            width: '80%',
            height: '50%',
        },
        tooltip: {
            isHtml: true,
            trigger: 'focus',
        },
        focusTarget: 'category',
        pointSize: 7,
        interpolateNulls: true,
    };

    return (
        <Chart
            chartType="LineChart"
            width="100%"
            height="30rem"
            data={data}
            options={options}
        />
    );
}

function FutureROEChart({ roeValues }) {
    if (!roeValues) {
        return <div>Data not available</div>;
    }

    console.log(roeValues);
    const { c_symbol, previous_years, previous_roe, future_years, future_roe } = roeValues;

    const data = [['Years', 'Previous ROE', 'Future ROE']];

    // Combine previous and future data into the chart data
    const combinedYears = [...previous_years, ...future_years];
    const combinedPreviousROE = [...previous_roe, ...Array(future_years.length).fill(null)];
    const combinedFutureROE = [...Array(previous_years.length).fill(null), ...future_roe];

    for (let i = 0; i < combinedYears.length; i++) {
        data.push([String(combinedYears[i]), combinedPreviousROE[i], combinedFutureROE[i]]);
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
        colors: ['rgb(62, 178, 36)', 'orange'], // Define colors for the lines
        curveType: 'function',
        legend: {
            position: 'bottom',
            textStyle: {
                color: 'white',
            },
        },
        backgroundColor: 'transparent',
        chartArea: {
            left: 50,
            right: 10,
            top: 50,
            bottom: 50,
            width: '80%',
            height: '50%',
        },
        tooltip: {
            isHtml: true,
            trigger: 'focus',
        },
        focusTarget: 'category',
        pointSize: 7,
        interpolateNulls: true,
    };

    return (
        <Chart
            chartType="LineChart"
            width="100%"
            height="30rem"
            data={data}
            options={options}
        />
    );
}


function FutureChartComponent({ sharePriceValue }) {
    const chartContainerRef = useRef(null);
    const toolTipRef = useRef(null);

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

        const pastCloseSeries = chart.addSeries(AreaSeries, { color: 'blue', lineWidth: 2 });
        const futureCloseSeries = chart.addSeries(LineSeries, { color: 'orange', lineWidth: 2 });
        const ema200Series = chart.addSeries(LineSeries, { color: 'red', lineWidth: 1 });

        const pastCloseData = sharePriceValue.previous_share_price.map(item => ({
            time: item.Date.split('T')[0],
            value: item.Close,
        }));

        const futureCloseData = sharePriceValue.future_share_price.map(item => ({
            time: item.Date.split('T')[0],
            value: item.Close,
        }));

        const ema200Data = sharePriceValue.previous_share_price.map(item => ({
            time: item.Date.split('T')[0],
            value: item.ema200,
        }));

        pastCloseSeries.setData(pastCloseData);
        futureCloseSeries.setData(futureCloseData);
        ema200Series.setData(ema200Data);

        const toolTip = document.createElement('div');
        toolTipRef.current = toolTip;
        toolTip.style = `
            width: 110px;
            position: absolute;
            display: none;
            padding: 8px;
            box-sizing: border-box;
            font-size: 12px;
            text-align: left;
            z-index: 1000;
            pointer-events: none;
            border-radius: 4px;
            box-shadow: 0 2px 5px 0 rgba(117, 134, 150, 0.45);
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

            const timeStr = param.time;
            const pointData =
                param.seriesData.get(pastCloseSeries) ||
                param.seriesData.get(futureCloseSeries);

            if (!pointData || pointData.value === undefined) return;

            toolTip.innerHTML = `
                <div style="color: rgb(9, 255, 0)">${sharePriceValue.c_symbol}</div>
                <div style="font-size: 24px; margin: 4px 0; color: white;">${pointData.value.toFixed(2)}</div>
                <div style="color: white;">${timeStr}</div>
            `;
            toolTip.style.display = 'block';

            let left = param.point.x - 55;
            left = Math.max(0, Math.min(left, chartContainerRef.current.clientWidth - 110));
            toolTip.style.left = `${left}px`;
            toolTip.style.top = `95rem`;
        });

        return () => chart.remove();
    }, [
        sharePriceValue.previous_share_price,
        sharePriceValue.future_share_price,
        sharePriceValue.c_symbol
    ]);

    return <div ref={chartContainerRef} id="container" />;
}

export function FutureChartSection({ c_symbol, futureValues }) {
    if (futureValues === undefined) {
        return
    }
    const [loading, setLoading] = useState(false);

    console.log({ 'FutureChartSection': futureValues })

    const futureFundamentalsVal = futureValues.futureFundamentals;
    const futureSharePriceVal = futureValues.futureSharePrice;

    console.log({ 'futureFundamentals': futureFundamentalsVal })
    console.log({ 'futureSharePrice': futureSharePriceVal })
    const revenueValues = {
        'c_symbol': c_symbol,
        'previous_years': futureFundamentalsVal.years,
        'previous_revenue': futureFundamentalsVal.revenue,
        'future_years': futureFundamentalsVal.future_years,
        'future_revenue': futureFundamentalsVal.future_revenue
    };

    const incomeValues = {
        'c_symbol': c_symbol,
        'previous_years': futureFundamentalsVal.years,
        'previous_income': futureFundamentalsVal.income,
        'future_years': futureFundamentalsVal.future_years,
        'future_income': futureFundamentalsVal.future_income
    };

    const EPSValues = {
        'c_symbol': c_symbol,
        'previous_years': futureFundamentalsVal.years,
        'previous_eps': futureFundamentalsVal.eps,
        'future_years': futureFundamentalsVal.future_years,
        'future_eps': futureFundamentalsVal.future_eps
    };

    const ROEValues = {
        'c_symbol': c_symbol,
        'previous_years': futureFundamentalsVal.years,
        'previous_roe': futureFundamentalsVal.roe,
        'future_years': futureFundamentalsVal.future_years,
        'future_roe': futureFundamentalsVal.future_roe
    };

    const sharePriceValue = {
        'c_symbol': c_symbol,
        'previous_share_price': futureSharePriceVal.previous_share_price,
        'future_share_price': futureSharePriceVal.future_share_price
    };

    console.log({
        'revenueValues': revenueValues,
        'incomeValues': incomeValues,
        'EPSValues': EPSValues,
        'ROEValues': ROEValues
    });

    console.log({
        'sharePriceValue': sharePriceValue
    });

    return (
        <>
            <Row className="ChartRow">
                <Col className="ChartCol">
                    <div>
                        {loading ? (
                            <p>Predicting Future Values...</p> // Show this while loading
                        ) : revenueValues ? (
                            <FutureRevenueChart revenueValues={revenueValues} /> // Show chart if data is available
                        ) : (
                            <p>No revenue data available.</p> // Fallback when no data is provided
                        )}
                    </div>
                </Col>
                <Col className="ChartCol">
                    <div>
                        {loading ? (
                            <p>Predicting Future Values...</p> // Show this while loading
                        ) : incomeValues ? (
                            <FutureIncomeChart incomeValues={incomeValues} /> // Show chart if data is available
                        ) : (
                            <p>No revenue data available.</p> // Fallback when no data is provided
                        )}
                    </div>
                </Col>
            </Row>
            <Row className="ChartRow">
                <Col className="ChartCol">
                    <div>
                        {loading ? (
                            <p>Predicting Future Values...</p> // Show this while loading
                        ) : EPSValues ? (
                            <FutureEPSChart epsValues={EPSValues} /> // Show chart if data is available
                        ) : (
                            <p>No revenue data available.</p> // Fallback when no data is provided
                        )}
                    </div>
                </Col>
                <Col className="ChartCol">
                    <div>
                        {loading ? (
                            <p>Predicting Future Values...</p> // Show this while loading
                        ) : ROEValues ? (
                            <FutureROEChart roeValues={ROEValues} /> // Show chart if data is available
                        ) : (
                            <p>No revenue data available.</p> // Fallback when no data is provided
                        )}
                    </div>
                </Col>
            </Row>
            <Row className="ChartRow">
                <Col className="SharePriceChart">
                    <FutureChartComponent
                        sharePriceValue={sharePriceValue}
                    />
                </Col>
            </Row>
        </>
    )
}