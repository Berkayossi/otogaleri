/**
 * Raporlar Charts Functions
 * Chart.js grafik oluşturma fonksiyonları
 */

// Ortak chart ayarları
var commonChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: { display: true, position: 'top' }
    }
};

// Aylık Satışlar Grafiği
window.initAylikSatislarChart = function (labels, data) {
    var ctx = document.getElementById('aylikSatislarChart');
    if (!ctx || !labels || labels.length === 0) return;

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Satılan Araç Sayısı',
                data: data,
                backgroundColor: 'rgba(59, 130, 246, 0.2)',
                borderColor: 'rgba(59, 130, 246, 1)',
                borderWidth: 3,
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: true, position: 'top' } },
            scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } }
        }
    });
};

// Aylık Satışlar ve Kar Grafiği (Kombine - Çift Y Eksenli)
window.initAylikSatisKarChart = function (labels, satisData, karData) {
    var ctx = document.getElementById('aylikSatisKarChart');
    if (!ctx || !labels || labels.length === 0) return;

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Satış Adedi',
                    data: satisData,
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    borderColor: 'rgba(59, 130, 246, 1)',
                    borderWidth: 3,
                    tension: 0.4,
                    fill: true,
                    yAxisID: 'y-satis'
                },
                {
                    label: 'Kar (₺)',
                    data: karData,
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    borderColor: 'rgba(16, 185, 129, 1)',
                    borderWidth: 3,
                    tension: 0.4,
                    fill: true,
                    yAxisID: 'y-kar'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            var label = context.dataset.label || '';
                            if (label) {
                                label += ': ';
                            }
                            if (context.parsed.y !== null) {
                                if (context.datasetIndex === 0) {
                                    label += context.parsed.y + ' adet';
                                } else {
                                    label += context.parsed.y.toLocaleString('tr-TR') + ' ₺';
                                }
                            }
                            return label;
                        }
                    }
                }
            },
            scales: {
                'y-satis': {
                    type: 'linear',
                    position: 'left',
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Satış Adedi',
                        color: 'rgba(59, 130, 246, 1)',
                        font: {
                            weight: 'bold',
                            size: 12
                        }
                    },
                    ticks: {
                        stepSize: 1,
                        color: 'rgba(59, 130, 246, 1)',
                        callback: function (value) {
                            return value + ' adet';
                        }
                    },
                    grid: {
                        drawOnChartArea: true,
                        color: 'rgba(59, 130, 246, 0.1)'
                    }
                },
                'y-kar': {
                    type: 'linear',
                    position: 'right',
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Kar (₺)',
                        color: 'rgba(16, 185, 129, 1)',
                        font: {
                            weight: 'bold',
                            size: 12
                        }
                    },
                    ticks: {
                        color: 'rgba(16, 185, 129, 1)',
                        callback: function (value) {
                            return value.toLocaleString('tr-TR') + ' ₺';
                        }
                    },
                    grid: {
                        drawOnChartArea: false
                    }
                }
            }
        }
    });
};

// Marka Kar Marjı Grafiği
window.initMarkaKarMarjiChart = function (labels, data) {
    var ctx = document.getElementById('markaKarMarjiChart');
    if (!ctx || !labels || labels.length === 0) return;

    if (data.length === 0) {
        ctx.parentElement.innerHTML = '<div class="text-center py-12 text-gray-500"><p class="text-lg">Kar marjı verisi bulunmamaktadır.</p></div>';
        return;
    }

    var colors = [
        'rgba(16, 185, 129, 0.7)', 'rgba(59, 130, 246, 0.7)',
        'rgba(251, 191, 36, 0.7)', 'rgba(239, 68, 68, 0.7)',
        'rgba(139, 92, 246, 0.7)', 'rgba(236, 72, 153, 0.7)',
        'rgba(34, 197, 94, 0.7)', 'rgba(249, 115, 22, 0.7)'
    ];
    var borderColors = colors.map(function (c) { return c.replace('0.7', '1'); });

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Kar Marjı (%)',
                data: data,
                backgroundColor: colors.slice(0, labels.length),
                borderColor: borderColors.slice(0, labels.length),
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            var label = context.dataset.label || '';
                            if (label) label += ': ';
                            if (context.parsed.y !== null) {
                                label += context.parsed.y.toFixed(2) + '%';
                            }
                            return label;
                        }
                    }
                }
            },
            scales: { y: { beginAtZero: true } }
        }
    });
};

// Marka Satışlar Grafiği (Pie Chart)
window.initMarkaSatislarChart = function (labels, data) {
    var ctx = document.getElementById('markaSatislarChart');
    if (!ctx || !labels || labels.length === 0) return;

    var colors = [
        'rgba(16, 185, 129, 0.8)',
        'rgba(59, 130, 246, 0.8)',
        'rgba(251, 191, 36, 0.8)',
        'rgba(239, 68, 68, 0.8)',
        'rgba(139, 92, 246, 0.8)',
        'rgba(236, 72, 153, 0.8)',
        'rgba(34, 197, 94, 0.8)',
        'rgba(249, 115, 22, 0.8)',
        'rgba(99, 102, 241, 0.8)',
        'rgba(244, 63, 94, 0.8)'
    ];
    var borderColors = colors.map(function (c) { return c.replace('0.8', '1'); });

    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                label: 'Satılan Araç Sayısı',
                data: data,
                backgroundColor: colors.slice(0, labels.length),
                borderColor: borderColors.slice(0, labels.length),
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'right',
                    labels: {
                        padding: 15,
                        font: {
                            size: 12
                        },
                        generateLabels: function (chart) {
                            const data = chart.data;
                            if (data.labels.length && data.datasets.length) {
                                return data.labels.map((label, i) => {
                                    const value = data.datasets[0].data[i];
                                    const total = data.datasets[0].data.reduce((a, b) => a + b, 0);
                                    const percentage = ((value / total) * 100).toFixed(1);
                                    return {
                                        text: `${label}: ${value} (${percentage}%)`,
                                        fillStyle: data.datasets[0].backgroundColor[i],
                                        hidden: false,
                                        index: i
                                    };
                                });
                            }
                            return [];
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            var label = context.label || '';
                            var value = context.parsed;
                            var total = context.dataset.data.reduce((a, b) => a + b, 0);
                            var percentage = ((value / total) * 100).toFixed(1);
                            return label + ': ' + value + ' adet (' + percentage + '%)';
                        }
                    }
                }
            }
        }
    });
};

// Yıl Dağılımı Grafiği
window.initYilDagilimiChart = function (labels, data) {
    var ctx = document.getElementById('yilDagilimiChart');
    if (!ctx || !labels || labels.length === 0) return;

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Satış Sayısı',
                data: data,
                backgroundColor: 'rgba(139, 92, 246, 0.7)',
                borderColor: 'rgba(139, 92, 246, 1)',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: true, position: 'top' } },
            scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } }
        }
    });
};

// Personel Performans Grafiği
window.initPersonelPerformansChart = function (labels, satisAdedi, toplamKar) {
    var ctx = document.getElementById('personelPerformansChart');
    if (!ctx || !labels || labels.length === 0) return;

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Satış Adedi',
                    data: satisAdedi,
                    backgroundColor: 'rgba(59, 130, 246, 0.7)',
                    borderColor: 'rgba(59, 130, 246, 1)',
                    borderWidth: 2,
                    yAxisID: 'y-satis'  // Sol eksen
                },
                {
                    label: 'Toplam Kar (₺)',
                    data: toplamKar,
                    backgroundColor: 'rgba(16, 185, 129, 0.7)',
                    borderColor: 'rgba(16, 185, 129, 1)',
                    borderWidth: 2,
                    yAxisID: 'y-kar'  // Sağ eksen
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            var label = context.dataset.label || '';
                            if (label) {
                                label += ': ';
                            }
                            if (context.parsed.y !== null) {
                                if (context.datasetIndex === 0) {
                                    // Satış adedi
                                    label += context.parsed.y + ' adet';
                                } else {
                                    // Kar
                                    label += context.parsed.y.toLocaleString('tr-TR') + ' ₺';
                                }
                            }
                            return label;
                        }
                    }
                }
            },
            scales: {
                'y-satis': {
                    type: 'linear',
                    position: 'left',
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Satış Adedi',
                        color: 'rgba(59, 130, 246, 1)',
                        font: {
                            weight: 'bold',
                            size: 12
                        }
                    },
                    ticks: {
                        stepSize: 1,
                        color: 'rgba(59, 130, 246, 1)',
                        callback: function (value) {
                            return value + ' adet';
                        }
                    },
                    grid: {
                        drawOnChartArea: true,
                        color: 'rgba(59, 130, 246, 0.1)'
                    }
                },
                'y-kar': {
                    type: 'linear',
                    position: 'right',
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Toplam Kar (₺)',
                        color: 'rgba(16, 185, 129, 1)',
                        font: {
                            weight: 'bold',
                            size: 12
                        }
                    },
                    ticks: {
                        color: 'rgba(16, 185, 129, 1)',
                        callback: function (value) {
                            return value.toLocaleString('tr-TR') + ' ₺';
                        }
                    },
                    grid: {
                        drawOnChartArea: false
                    }
                }
            }
        }
    });
};

// Tüm grafikleri başlat
window.initAllCharts = function (chartData) {
    console.log('📊 initAllCharts çağrıldı, veri:', chartData);

    // Kombine Satış ve Kar Grafiği
    if (chartData.aylikSatislar && chartData.aylikKar) {
        try {
            console.log('📈 Aylık Satış/Kar grafiği başlatılıyor...');
            initAylikSatisKarChart(
                chartData.aylikSatislar.labels,
                chartData.aylikSatislar.data,
                chartData.aylikKar.data
            );
            console.log('✅ Aylık Satış/Kar grafiği başlatıldı');
        } catch (error) {
            console.error('❌ Aylık Satış/Kar grafiği hatası:', error);
        }
    } else {
        console.warn('⚠️ Aylık satış/kar verisi yok');
    }

    if (chartData.markaKarMarji) {
        try {
            console.log('📊 Marka Kar Marjı grafiği başlatılıyor...');
            initMarkaKarMarjiChart(chartData.markaKarMarji.labels, chartData.markaKarMarji.data);
            console.log('✅ Marka Kar Marjı grafiği başlatıldı');
        } catch (error) {
            console.error('❌ Marka Kar Marjı grafiği hatası:', error);
        }
    } else {
        console.warn('⚠️ Marka kar marjı verisi yok');
    }

    if (chartData.markaSatislar) {
        try {
            console.log('🥧 Marka Satışlar grafiği başlatılıyor...');
            initMarkaSatislarChart(chartData.markaSatislar.labels, chartData.markaSatislar.data);
            console.log('✅ Marka Satışlar grafiği başlatıldı');
        } catch (error) {
            console.error('❌ Marka Satışlar grafiği hatası:', error);
        }
    } else {
        console.warn('⚠️ Marka satışlar verisi yok');
    }

    if (chartData.yilDagilimi) {
        try {
            console.log('📅 Yıl Dağılımı grafiği başlatılıyor...');
            initYilDagilimiChart(chartData.yilDagilimi.labels, chartData.yilDagilimi.data);
            console.log('✅ Yıl Dağılımı grafiği başlatıldı');
        } catch (error) {
            console.error('❌ Yıl Dağılımı grafiği hatası:', error);
        }
    } else {
        console.warn('⚠️ Yıl dağılımı verisi yok');
    }

    if (chartData.personelPerformans) {
        try {
            console.log('👥 Personel Performans grafiği başlatılıyor...');
            initPersonelPerformansChart(
                chartData.personelPerformans.labels,
                chartData.personelPerformans.satisAdedi,
                chartData.personelPerformans.toplamKar
            );
            console.log('✅ Personel Performans grafiği başlatıldı');
        } catch (error) {
            console.error('❌ Personel Performans grafiği hatası:', error);
        }
    } else {
        console.warn('⚠️ Personel performans verisi yok');
    }

    console.log('🎉 Tüm grafikler işlendi');
};
