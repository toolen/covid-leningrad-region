import '@picocss/pico/css/pico.min.css';
import './style.css';
import {AgCharts, time} from "ag-charts-community";

const API_ENDPOINT = '/api/v1';
const LS_DISTRICT = 'districtName';
const LS_LOCALITY = 'localityName';

const districtEl = document.querySelector('#district');
const localityEl = document.querySelector('#locality');
const chartContainer = document.querySelector('#chart');
let chart = null;

function makeRequest(url, callback) {
    const httpRequest = new XMLHttpRequest();
    httpRequest.onreadystatechange = function () {
        if (httpRequest.readyState === XMLHttpRequest.DONE) {
            const data = httpRequest.response;
            if (httpRequest.status === 200) {
                callback(data);
            } else {
                // err.innerText = data['description'];
            }
        }
    };
    httpRequest.open('GET', url);
    httpRequest.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    httpRequest.responseType = 'json';
    httpRequest.send();
}

function fillDistrictSelect() {
    makeRequest(`${API_ENDPOINT}/districts`, function (districts) {
        const selectedDistrict = localStorage.getItem(LS_DISTRICT) || "";
        const options = districts.map((value) => {
            return `<option value="${value}" ${selectedDistrict === value ? 'selected' : ''}>${value}</option>`;
        });
        districtEl.innerHTML = options.join("");
        fillLocalitiesSelect(districtEl.value);
    })
}

function fillLocalitiesSelect(districtName) {
    if (districtName) {
        const districtNameEncoded = encodeURIComponent(districtName);
        makeRequest(`${API_ENDPOINT}/districts/${districtNameEncoded}/localities`, function (localities) {
            const selectedLocality = localStorage.getItem(LS_LOCALITY) || "";
            const options = localities.map((value) => {
                return `<option value="${value}" ${selectedLocality === value ? 'selected' : ''}>${value}</option>`
            });
            localityEl.innerHTML = options.join("");
            loadData(districtName, localityEl.value);
        })
    }
}

function formatDate(date) {
    let dd = date.getDate();
    if (dd < 10) dd = '0' + dd;

    let mm = date.getMonth() + 1;
    if (mm < 10) mm = '0' + mm;

    let yy = date.getFullYear();

    return dd + '.' + mm + '.' + yy;
}

function getTooltipContent(date, value) {
    const formattedDate = formatDate(date);
    const formattedValue = value.toFixed(0);
    const valuePostfix = value >= 2 && value <= 4 ? "человека" : "человек";
    return `${formattedDate}: ${formattedValue} ${valuePostfix}`;
}


function loadData(districtName, localityName) {
    if (districtName && localityName) {
        const districtNameEncoded = encodeURIComponent(districtName);
        const localityNameEncoded = encodeURIComponent(localityName);
        makeRequest(`${API_ENDPOINT}/districts/${districtNameEncoded}/localities/${localityNameEncoded}`, function (rawData) {
            let data = rawData.map((item) => {
                return {
                    "date": new Date(item.date),
                    "value": item.localities[0]["locality_number_of_infections"],
                }
            })

            const legendTitle = 'Кол-во заболевших';

            const options = {
                data: data,
                container: chartContainer,
                series: [{
                    xKey: 'date',
                    yKey: 'value',
                    yName: legendTitle,
                    tooltip: {
                        renderer: function ({ datum, xKey, yKey }) {
                            return {
                                title: legendTitle,
                                content: getTooltipContent(datum[xKey], datum[yKey]),
                            };
                        },
                    },
                }],
                axes: [
                    {
                        type: 'number',
                        position: 'left',
                        min: 0
                    },
                    {
                        type: 'time',
                        position: 'bottom',
                        tick: {
                           interval: time.month,
                        },
                        label: {
                            format: '%b %Y',
                            rotation: -45
                        },
                    },
                ],
                legend: {
                    position: 'bottom',
                },
                navigator: {
                    enabled: true
                }
            }

            if (chart) {
                AgCharts.update(chart, options);
            } else {
                chart = AgCharts.create(options);
            }
        });
    }
}

districtEl.addEventListener("change", function (e) {
    const districtName = e.target.value;
    localStorage.setItem(LS_DISTRICT, districtName);
    fillLocalitiesSelect(districtName)
})

localityEl.addEventListener("change", function (e) {
    const districtName = districtEl.value;
    const localityName = e.target.value;
    localStorage.setItem(LS_LOCALITY, localityName);
    loadData(districtName, localityName)
})

fillDistrictSelect();